"""HU-08 — Agregados para el dashboard de analisis y la exportacion.

Solo devuelve conteos y promedios: nunca nombre, documento, orientacion sexual ni fecha de nacimiento de un paciente.
El administrador ve todos los pacientes activos; el medico, solo los suyos. Los filtros se aplican antes de agregar.
"""
from collections import Counter
from datetime import datetime
from typing import Dict, Iterable, List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models

# Dominios de HAB (D1-D6) y su capitulo CIF, para rotular los promedios.
DOMAINS = [
    ("D1", "nivel_d1", "Aprendizaje y aplicación del conocimiento"),
    ("D2", "nivel_d2", "Tareas y demandas generales"),
    ("D3", "nivel_d3", "Comunicación"),
    ("D4", "nivel_d4", "Movilidad"),
    ("D5", "nivel_d5", "Autocuidado"),
    ("D6", "nivel_d6", "Vida doméstica"),
]
AGE_GROUPS = [("0-17", 0, 17), ("18-29", 18, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60+", 60, 200)]
SEVERITY_ORDER = ["Ninguna", "Leve", "Moderada", "Grave", "Severa", "Completa"]
COMPONENTS = ("b", "s", "d")
DECIDED = ("aceptado", "editado", "rechazado")
TOP_CODES = 10
TOP_CAUSES = 8


def _counts(values: Iterable[Optional[str]], order: Optional[List[str]] = None) -> List[Dict]:
    counter = Counter((v if v not in (None, "") else "Sin dato") for v in values)
    keys = list(counter)
    if order:
        keys.sort(key=lambda k: (order.index(k) if k in order else len(order), k))
    else:
        keys.sort(key=lambda k: (-counter[k], k))
    return [{"key": k, "count": counter[k]} for k in keys]


def _label(value: Optional[str]) -> Optional[str]:
    """El género se escribe de varias formas en los datos ('femenino', 'Femenino'): se unifica para no duplicar categorías."""
    return value.strip().capitalize() if value and value.strip() else value


def _rate(num: int, den: int) -> Optional[float]:
    return round(num / den, 4) if den else None


def _age_group(age: Optional[int]) -> str:
    if age is None:
        return "Sin dato"
    for label, low, high in AGE_GROUPS:
        if low <= age <= high:
            return label
    return "Sin dato"


def _scope_query(db: Session, user: models.User, owner_id: Optional[int]):
    query = db.query(models.Patient).filter(models.Patient.is_active == True)  # noqa: E712
    if user.role == "admin":
        if owner_id is not None:
            query = query.filter(models.Patient.owner_id == owner_id)
    else:
        query = query.filter(models.Patient.owner_id == user.id)
    return query


def filter_patients(
    db: Session,
    user: models.User,
    genero: Optional[str] = None,
    edad_min: Optional[int] = None,
    edad_max: Optional[int] = None,
    causa: Optional[str] = None,
    perfil: Optional[int] = None,
    owner_id: Optional[int] = None,
) -> List[models.Patient]:
    query = _scope_query(db, user, owner_id)
    if genero:
        query = query.filter(func.lower(models.Patient.genero) == genero.strip().lower())
    if edad_min is not None:
        query = query.filter(models.Patient.edad >= edad_min)
    if edad_max is not None:
        query = query.filter(models.Patient.edad <= edad_max)
    if causa:
        query = query.filter(models.Patient.causa_deficiencia == causa)
    if perfil is not None:
        query = query.filter(models.Patient.prediction_profile == perfil)
    return query.all()


def _latest_batch_rows(db: Session, patient_ids: List[int]) -> List[models.IcfSuggestion]:
    """Sugerencias del ultimo lote de cada paciente (regenerar conserva los lotes anteriores y no deben contarse dos veces)."""
    if not patient_ids:
        return []
    rows = (
        db.query(models.IcfSuggestion)
        .filter(models.IcfSuggestion.patient_id.in_(patient_ids))
        .order_by(models.IcfSuggestion.id)
        .all()
    )
    latest: Dict[int, str] = {}
    for row in rows:
        latest[row.patient_id] = row.batch_id  # el ultimo id de cada paciente define su lote vigente
    return [row for row in rows if latest[row.patient_id] == row.batch_id]


def _icf_summary(rows: List[models.IcfSuggestion]) -> Dict:
    by_status = Counter(row.status for row in rows)
    decided = sum(by_status[s] for s in DECIDED)
    accepted = by_status["aceptado"] + by_status["editado"]

    by_component = {}
    for comp in COMPONENTS:
        part = [r for r in rows if r.component == comp]
        counter = Counter(r.status for r in part)
        by_component[comp] = {
            "total": len(part),
            "aceptado": counter["aceptado"],
            "editado": counter["editado"],
            "rechazado": counter["rechazado"],
            "sugerido": counter["sugerido"],
            "acceptance_rate": _rate(counter["aceptado"] + counter["editado"], sum(counter[s] for s in DECIDED)),
        }

    codes: Dict[str, Dict] = {}
    for row in rows:
        entry = codes.setdefault(row.code, {"code": row.code, "title": row.title, "component": row.component,
                                            "count": 0, "accepted": 0, "rejected": 0})
        entry["count"] += 1
        entry["accepted"] += row.status in ("aceptado", "editado")
        entry["rejected"] += row.status == "rechazado"
    top = sorted(codes.values(), key=lambda e: (-e["count"], e["code"]))[:TOP_CODES]

    by_model = Counter(row.model or "Sin dato" for row in rows)
    by_origin = Counter(row.origin for row in rows)

    return {
        "patients_with_profile": len({r.patient_id for r in rows}),
        "suggestions": len(rows),
        "by_status": {s: by_status[s] for s in ("sugerido", "aceptado", "editado", "rechazado")},
        "decided": decided,
        "acceptance_rate": _rate(accepted, decided),
        "by_component": by_component,
        "by_origin": [{"key": k, "count": v} for k, v in sorted(by_origin.items(), key=lambda kv: (-kv[1], kv[0]))],
        "by_model": [{"key": k, "count": v} for k, v in sorted(by_model.items(), key=lambda kv: (-kv[1], kv[0]))],
        "top_codes": top,
    }


def build_summary(db: Session, user: models.User, **filters) -> Dict:
    patients = filter_patients(db, user, **filters)
    n = len(patients)
    ages = [p.edad for p in patients if p.edad is not None]
    globals_ = [p.nivel_global for p in patients if p.nivel_global is not None]
    predicted = [p for p in patients if p.prediction_profile is not None]

    domains = []
    for code, attr, name in DOMAINS:
        vals = [getattr(p, attr) for p in patients if getattr(p, attr) is not None]
        domains.append({"domain": code, "name": name, "mean": round(sum(vals) / len(vals), 1) if vals else None, "n": len(vals)})

    icf_rows = _latest_batch_rows(db, [p.id for p in patients])

    return {
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "scope": "global" if user.role == "admin" and filters.get("owner_id") is None else "propio",
        "filters": {k: v for k, v in filters.items() if v is not None},
        "totals": {
            "patients": n,
            "with_prediction": len(predicted),
            "prediction_rate": _rate(len(predicted), n),
            "mean_age": round(sum(ages) / len(ages), 1) if ages else None,
            "mean_global_level": round(sum(globals_) / len(globals_), 1) if globals_ else None,
            "with_icf_profile": len({r.patient_id for r in icf_rows}),
        },
        "distributions": {
            "profile": _counts([f"Perfil {p.prediction_profile}" for p in predicted]),
            "cat_fisica": _counts([p.cat_fisica for p in patients], SEVERITY_ORDER),
            "cat_psicosocial": _counts([p.cat_psicosocial for p in patients], SEVERITY_ORDER),
            "genero": _counts([_label(p.genero) for p in patients]),
            "age_group": _counts([_age_group(p.edad) for p in patients], [g[0] for g in AGE_GROUPS]),
            "cause": _counts([p.causa_deficiencia for p in patients])[:TOP_CAUSES],
        },
        "domains": domains,
        "icf": _icf_summary(icf_rows),
    }


def filter_options(db: Session, user: models.User) -> Dict:
    """Valores disponibles para los filtros del dashboard (solo los del alcance del usuario)."""
    patients = _scope_query(db, user, None).all()
    return {
        "genero": sorted({_label(p.genero) for p in patients if p.genero}),
        "cause": sorted({p.causa_deficiencia for p in patients if p.causa_deficiencia}),
        "profile": sorted({p.prediction_profile for p in patients if p.prediction_profile is not None}),
    }
