"""Memoria de casos confirmados por el medico (HU-07j).

Cuando el medico acepta o edita un codigo, el backend envia la decision (POST /cases). Aqui se guarda el texto clinico
del caso (diagnostico y notas, sin identificadores) con su vector, y el codigo confirmado con su gravedad y su
justificacion. Si el medico rechaza despues un codigo ya guardado, se retira. /suggest consulta los casos parecidos
(repository.similar_cases) para usarlos como ejemplos.
"""
from typing import Callable, Sequence

from . import rules
from .repository import PgRepo
from .schemas import CaseRecord
from .suggest import case_context

EmbedFn = Callable[[str], Sequence[float]]


def store_case(record: CaseRecord, repo: PgRepo, embed_fn: EmbedFn) -> str:
    """Devuelve 'stored', 'removed' o 'skipped' (sin diagnostico ni notas no hay nada que comparar)."""
    if record.status == "rechazado":
        repo.delete_case_code(record.case_key, record.item_ref)
        return "removed"
    patient = record.patient
    context = case_context(patient)
    if context is None:
        return "skipped"
    embedding = None if repo.case_context(record.case_key) == context else embed_fn(context)
    repo.upsert_case(
        record.case_key, context, rules.clean_diagnosis(patient.diag_cie)[:200] or None, rules.age_group(patient.age), embedding
    )
    repo.upsert_case_code(
        record.case_key,
        record.item_ref,
        {
            "component": record.component,
            "code": record.code,
            "status": record.status,
            "qualifier": record.qualifier,
            "qualifier_cn": record.qualifier_cn,
            "qualifier_cl": record.qualifier_cl,
            "qualifier_suggested": record.qualifier_suggested,
            "justification": (record.justification or "").strip() or None,
        },
    )
    return "stored"
