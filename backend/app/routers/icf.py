# app/routers/icf.py
"""
HU-07: sugerencia de codigos CIF-IA.

- `router` (prefijo /icf): diagnostico de conexion (admin) y decision del medico sobre cada codigo.
- `patient_router` (prefijo /patients): generar y consultar las sugerencias de un paciente.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, dependencies, models, schemas
from ..services import icf_client

router = APIRouter(
    tags=["ICF"]
)
patient_router = APIRouter(
    tags=["ICF"]
)

MIN_AGE_FOR_SUGGESTION = 6  # el Anexo 1239 no calcula niveles por dominio para 0-5 anios

_GROUP_OF = {"b": "functions", "s": "structures", "d": "activities"}


def _build_set(patient_id: int, rows: List[models.IcfSuggestion], **extra) -> schemas.IcfSuggestionSet:
    grouped = {"functions": [], "structures": [], "activities": []}
    for row in rows:
        grouped[_GROUP_OF[row.component]].append(schemas.IcfSuggestionItem.model_validate(row))
    first = rows[0] if rows else None
    fields = {
        "patient_id": patient_id,
        "batch_id": first.batch_id if first else None,
        "model": first.model if first else None,
        "llm_used": any(r.origin == "llm" for r in rows),  # al releer; al generar manda lo que informo el servicio
        "created_at": first.created_at if first else None,
        **grouped,
    }
    fields.update(extra)
    return schemas.IcfSuggestionSet(**fields)


@router.get("/health")
def icf_health(
    current_user: models.User = Depends(dependencies.get_current_active_admin),
):
    """
    Diagnostico de la conexion con el servidor local de IA (HU-07).
    Solo administradores. No expone la URL ni el token del servidor.
    """
    return icf_client.check_health()


@patient_router.post("/{patient_id}/icf-suggestions", response_model=schemas.IcfSuggestionSet)
def generate_icf_suggestions(
    patient_id: int,
    body: schemas.IcfGenerateRequest = schemas.IcfGenerateRequest(),
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_active_user),
):
    """
    Genera una sugerencia de codigos CIF-IA (maximo 3 por componente: funciones, estructuras y actividades)
    para el paciente y la guarda como un lote nuevo en estado `sugerido`. Al servicio ICF solo viajan edad,
    genero, causa, categorias, niveles D1-D6, la prediccion y los campos clinicos opcionales; nunca el
    nombre, el documento ni la orientacion sexual.
    """
    patient = dependencies.get_accessible_patient(db, patient_id, current_user)
    if patient.edad is None or patient.edad < MIN_AGE_FOR_SUGGESTION:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Para pacientes menores de 6 años no aplica la sugerencia basada en los niveles D1–D6.",
        )

    payload = icf_client.build_patient_context(patient, body.diag_cie, body.clinical_notes)
    try:
        result = icf_client.request_suggestion(payload)
    except icf_client.IcfServiceError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc))

    if not result.get("applicable", True):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=result.get("message") or "No aplica la sugerencia para este paciente.",
        )

    rows = crud.create_icf_batch(db, patient.id, result, payload.get("diag_cie"), payload.get("clinical_notes"))
    warnings = [str(w) for w in (result.get("warnings") or [])][:10]
    if result.get("llm_error"):
        warnings.append("El modelo no respondió; se muestra la sugerencia por similitud.")
    latency = result.get("latency_ms")
    return _build_set(
        patient.id, rows,
        warnings=warnings,
        latency_ms=latency if isinstance(latency, int) else None,
        llm_used=bool(result.get("llm_used")),
    )


@patient_router.get("/{patient_id}/icf-suggestions", response_model=schemas.IcfSuggestionSet)
def read_icf_suggestions(
    patient_id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_active_user),
):
    """Ultima sugerencia generada para el paciente, con la decision del medico sobre cada codigo."""
    patient = dependencies.get_accessible_patient(db, patient_id, current_user)
    return _build_set(patient.id, crud.get_latest_icf_batch(db, patient.id))


@router.patch("/suggestions/{suggestion_id}", response_model=schemas.IcfSuggestionItem)
def decide_icf_suggestion(
    suggestion_id: int,
    decision: schemas.IcfDecision,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_active_user),
):
    """
    El medico acepta, edita o rechaza un codigo sugerido. Al editar puede ajustar los calificadores y,
    enviando `code` y `title` juntos, cambiar el codigo (queda guardado el codigo original).
    """
    row = crud.get_icf_suggestion(db, suggestion_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Sugerencia no encontrada")
    dependencies.get_accessible_patient(db, row.patient_id, current_user)

    if decision.status == schemas.IcfStatus.sugerido:
        raise HTTPException(status_code=422, detail="La decisión debe ser aceptado, editado o rechazado.")
    content = (decision.qualifier, decision.qualifier_cn, decision.qualifier_cl, decision.code, decision.title)
    if decision.status == schemas.IcfStatus.editado:
        if all(value is None for value in content):
            raise HTTPException(status_code=422, detail="Para editar, indica al menos un calificador o un código.")
        if (decision.code is None) != (decision.title is None):
            raise HTTPException(status_code=422, detail="Para cambiar el código, envía el código y su título juntos.")
        if decision.code and decision.code[0] != row.component:
            raise HTTPException(status_code=422, detail="El código nuevo debe ser del mismo componente.")
        if row.component != "s" and (decision.qualifier_cn is not None or decision.qualifier_cl is not None):
            raise HTTPException(status_code=422, detail="Naturaleza y localización solo aplican a estructuras (s).")
    elif any(value is not None for value in content):
        raise HTTPException(status_code=422, detail="Solo la decisión «editado» permite cambiar el contenido.")

    return crud.decide_icf_suggestion(db, row, decision, current_user.id)
