# app/crud.py

import uuid
from datetime import datetime

from sqlalchemy.orm import Session
from . import models, schemas, auth

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    # <--- CORRECCIÓN CLAVE: Ahora 'user.role' viene del schema y funcionará
    db_user = models.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=user.role.value  # Usamos .value para obtener el string del Enum
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_activity(db: Session, user_id: int, is_active: bool):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.is_active = is_active
        db.commit()
        db.refresh(db_user)
    return db_user

def activate_all_users(db: Session):
    """Activa todos los usuarios inactivos en el sistema."""
    users = db.query(models.User).filter(models.User.is_active == False).all()
    count = 0
    for user in users:
        user.is_active = True
        count += 1
    db.commit()
    return count

def get_patient(db: Session, patient_id: int):
    """Obtiene un paciente activo por ID. Los pacientes con soft-delete
    (is_active=False) no son visibles, igual que en get_all_patients /
    get_patients_by_owner, para evitar que GET/PUT/DELETE por ID expongan
    o modifiquen registros ya eliminados."""
    return db.query(models.Patient).filter(
        models.Patient.id == patient_id,
        models.Patient.is_active == True,
    ).first()

def get_all_patients(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(models.Patient).filter(models.Patient.is_active == True)
    if search:
        term = f"%{search}%"
        query = query.filter(
            models.Patient.nombre_apellidos.ilike(term) |
            models.Patient.numero_documento.ilike(term)
        )
    return query.offset(skip).limit(limit).all()

def get_patients_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(models.Patient).filter(
        models.Patient.owner_id == owner_id,
        models.Patient.is_active == True
    )
    if search:
        term = f"%{search}%"
        query = query.filter(
            models.Patient.nombre_apellidos.ilike(term) |
            models.Patient.numero_documento.ilike(term)
        )
    return query.offset(skip).limit(limit).all()

def create_user_patient(db: Session, patient: schemas.PatientCreate, user_id: int):
    """
    Crea un nuevo paciente en la base de datos.
    Maneja errores de integridad (duplicados, etc.)
    """
    try:
        db_patient = models.Patient(**patient.model_dump(), owner_id=user_id)
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        return db_patient
    except Exception as e:
        db.rollback()
        print(f"❌ Error en create_user_patient: {type(e).__name__}: {str(e)}")
        raise

def update_patient(db: Session, db_patient: models.Patient, patient_update: schemas.PatientUpdate):
    update_data = patient_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_patient, key, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: int):
    db_patient = get_patient(db, patient_id)
    if db_patient:
        db_patient.is_active = False
        db.commit()
        db.refresh(db_patient)
    return db_patient

def update_patient_prediction(db: Session, patient_id: int, profile: int, description: str):
    db_patient = get_patient(db, patient_id)
    if db_patient:
        db_patient.prediction_profile = profile
        db_patient.prediction_description = description
        db.commit()
        db.refresh(db_patient)
    return db_patient


# ----------------------------------------------------------------------
# HU-07c: sugerencias de codigos CIF-IA
# ----------------------------------------------------------------------
_ICF_GROUPS = (("functions", "b"), ("structures", "s"), ("activities", "d"))


def create_icf_batch(db: Session, patient_id: int, result: dict, diag_cie, clinical_notes):
    """Guarda como un lote nuevo (estado `sugerido`) los codigos que devolvio el servicio ICF.
    Descarta con tolerancia los elementos mal formados; los lotes anteriores se conservan."""
    batch_id = str(uuid.uuid4())
    model_name = str(result.get("model") or "")[:80] or None
    rows = []
    for key, component in _ICF_GROUPS:
        items = result.get(key) or []
        if not isinstance(items, list):
            continue
        for position, item in enumerate(items[:3]):  # maximo 3 por componente (Anexo 1239)
            if not isinstance(item, dict) or not item.get("code") or not item.get("title"):
                continue
            rows.append(models.IcfSuggestion(
                patient_id=patient_id,
                batch_id=batch_id,
                position=position,
                component=component,
                code=str(item["code"])[:10],
                title=str(item["title"])[:300],
                qualifier=item.get("qualifier"),
                qualifier_cn=item.get("qualifier_cn"),
                qualifier_cl=item.get("qualifier_cl"),
                justification=(str(item.get("justification") or "")[:400] or None),
                origin=str(item.get("origin") or "rules")[:20],
                status="sugerido",
                model=model_name,
                diag_cie=diag_cie,
                clinical_notes=clinical_notes,
            ))
    db.add_all(rows)
    db.commit()
    for row in rows:
        db.refresh(row)
    return rows


def get_latest_icf_batch(db: Session, patient_id: int):
    """Codigos de la generacion mas reciente del paciente, ordenados por componente y relevancia."""
    last = (
        db.query(models.IcfSuggestion)
        .filter(models.IcfSuggestion.patient_id == patient_id)
        .order_by(models.IcfSuggestion.created_at.desc(), models.IcfSuggestion.id.desc())
        .first()
    )
    if last is None:
        return []
    return (
        db.query(models.IcfSuggestion)
        .filter(models.IcfSuggestion.batch_id == last.batch_id)
        .order_by(models.IcfSuggestion.component, models.IcfSuggestion.position, models.IcfSuggestion.id)
        .all()
    )


def get_icf_suggestion(db: Session, suggestion_id: int):
    return db.query(models.IcfSuggestion).filter(models.IcfSuggestion.id == suggestion_id).first()


def decide_icf_suggestion(db: Session, row: models.IcfSuggestion, decision: schemas.IcfDecision, user_id: int):
    """Aplica la decision del medico. En `editado` cambia calificadores y/o el codigo (con su titulo),
    conservando en `original_code` el codigo que sugirio la maquina."""
    if decision.status == schemas.IcfStatus.editado:
        if decision.code:
            if decision.code != row.code:
                row.original_code = row.original_code or row.code
            row.code, row.title = decision.code, decision.title
        if decision.qualifier is not None:
            row.qualifier = decision.qualifier
        if decision.qualifier_cn is not None:
            row.qualifier_cn = decision.qualifier_cn
        if decision.qualifier_cl is not None:
            row.qualifier_cl = decision.qualifier_cl
    row.status = decision.status.value
    row.decided_at = datetime.utcnow()
    row.decided_by_id = user_id
    db.commit()
    db.refresh(row)
    return row