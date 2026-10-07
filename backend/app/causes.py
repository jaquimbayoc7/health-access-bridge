# app/causes.py
"""
Causa de la deficiencia segun el Anexo Tecnico de la Resolucion 1239 de 2022 (criterio 3 del perfil
de funcionamiento): 21 opciones en 3 grupos, de seleccion unica.

"Enfermedad laboral" y "Accidente de trabajo" solo deben seleccionarse si hay dictamen de origen de
perdida de la capacidad laboral y ocupacional (lo verifica el equipo clinico, no el sistema).
"""
import unicodedata
from typing import Dict, List, Optional

NACIMIENTO = "De nacimiento"
ADQUIRIDA = "Adquirida"
NO_SE_IDENTIFICA = "No se identifica"

OFFICIAL_CAUSES: List[Dict[str, str]] = [
    {"name": "Alteración genética o hereditaria", "group": NACIMIENTO},
    {"name": "Alteración del desarrollo embrionario", "group": NACIMIENTO},
    {"name": "Complicaciones durante el parto", "group": NACIMIENTO},
    {"name": "Condiciones de salud de la madre durante el embarazo", "group": NACIMIENTO},
    {"name": "Enfermedad general", "group": ADQUIRIDA},
    {"name": "Enfermedad laboral", "group": ADQUIRIDA},
    {"name": "Accidente de tránsito", "group": ADQUIRIDA},
    {"name": "Accidente en el hogar", "group": ADQUIRIDA},
    {"name": "Accidente en el centro educativo", "group": ADQUIRIDA},
    {"name": "Accidente de trabajo", "group": ADQUIRIDA},
    {"name": "Accidente deportivo", "group": ADQUIRIDA},
    {"name": "Desastre natural", "group": ADQUIRIDA},
    {"name": "Intoxicación", "group": ADQUIRIDA},
    {"name": "Envejecimiento", "group": ADQUIRIDA},
    {"name": "Consumo de sustancias psicoactivas", "group": ADQUIRIDA},
    {"name": "Lesión auto infligida", "group": ADQUIRIDA},
    {"name": "Conflicto armado", "group": ADQUIRIDA},
    {"name": "Violencia intrafamiliar", "group": ADQUIRIDA},
    {"name": "Violencia por delincuencia común", "group": ADQUIRIDA},
    {"name": "Otra", "group": ADQUIRIDA},
    {"name": "No se identifica causa", "group": NO_SE_IDENTIFICA},
]


def _key(text: str) -> str:
    """Minusculas, sin tildes y con espacios simples, para comparar sin depender de la escritura."""
    base = unicodedata.normalize("NFD", text.strip().lower())
    return " ".join("".join(c for c in base if unicodedata.category(c) != "Mn").split())


# Valores no oficiales que traen los datos semilla u otras versiones del formulario, con una
# correspondencia clara. Lo ambiguo (p. ej. "Enfermedad congenita", que puede ser genetica o del desarrollo
# embrionario; "Paralisis cerebral", que es una condicion y no una causa) NO se mapea: se deja como esta.
_ALIASES: Dict[str, str] = {
    "accidente laboral": "Accidente de trabajo",
    "lesion deportiva": "Accidente deportivo",
    "enfermedad degenerativa": "Enfermedad general",
    "enfermedad autoinmune": "Enfermedad general",
    "enfermedad cardiovascular": "Enfermedad general",
    "lesion autoinfligida": "Lesión auto infligida",
    "genetica": "Alteración genética o hereditaria",
    "hereditaria": "Alteración genética o hereditaria",
}

_BY_KEY: Dict[str, str] = {_key(c["name"]): c["name"] for c in OFFICIAL_CAUSES}


def normalize_cause(value: Optional[str]) -> Optional[str]:
    """Devuelve la opcion oficial que corresponde a `value`, o `value` sin cambios (recortado) si no hay una
    correspondencia clara. Devuelve None si no hay valor."""
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    key = _key(text)
    return _BY_KEY.get(key) or _ALIASES.get(key) or text


def is_official(value: Optional[str]) -> bool:
    return value is not None and _key(value) in _BY_KEY
