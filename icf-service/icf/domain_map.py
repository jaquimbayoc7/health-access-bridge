"""Reglas fijas de HU-07 (sin LLM): mapeo de niveles D1-D6 de HAB, calificador y candidatos del Anexo 1239."""
from dataclasses import dataclass
from typing import List, Optional, Tuple

# Menores de 6 anios: el Anexo no calcula niveles por dominio.
MIN_AGE_FOR_DOMAINS = 6
# Un capitulo se revisa cuando el nivel de HAB (0-100) es >= 5 (hay algun problema).
REVIEW_THRESHOLD = 5


@dataclass(frozen=True)
class HabDomain:
    hab_domain: str  # D1..D6
    chapter_code: str  # d1..d6
    chapter_name: str
    official_domain: Optional[str]
    note: str


HAB_DOMAINS: List[HabDomain] = [
    HabDomain("D1", "d1", "Aprendizaje y aplicacion del conocimiento", "Cognicion", ""),
    HabDomain("D2", "d2", "Tareas y demandas generales", None, "Sin equivalente directo en los dominios oficiales"),
    HabDomain("D3", "d3", "Comunicacion", None, "Parcial: d310 y d350 estan en Cognicion"),
    HabDomain("D4", "d4", "Movilidad", "Movilidad", ""),
    HabDomain("D5", "d5", "Autocuidado", "Cuidado personal", ""),
    HabDomain("D6", "d6", "Vida domestica", "Actividades cotidianas", "d640 (tareas domesticas)"),
]

# Candidatos del Anexo 1239 ya confirmados (dominio oficial, codigo).
# PENDIENTE: transcribir el resto de las tablas 7-9 y 11 del Anexo revisando el original.
ANNEX_CANDIDATES: List[Tuple[str, str]] = [
    ("Movilidad", "d4154"),
    ("Movilidad", "d4104"),
    ("Movilidad", "d4600"),
    ("Movilidad", "d4602"),
    ("Movilidad", "d4501"),
    ("Cognicion", "b1400"),
    ("Cognicion", "d161"),
    ("Cognicion", "b144"),
    ("Cognicion", "d175"),
    ("Cognicion", "d155"),
    ("Cognicion", "d310"),
    ("Cognicion", "d350"),
]


def hab_domain_of(code: str) -> Optional[str]:
    """Dominio HAB (D1..D6) de un codigo de actividades y participacion; None para b, s, e o d7-d9."""
    if code.startswith("d") and code[1] in "123456":
        return f"D{code[1]}"
    return None


def qualifier_from_level(level: int) -> int:
    """Escala generica de la CIF aplicada al nivel de HAB 0-100: 0-4 -> 0, 5-24 -> 1, 25-49 -> 2, 50-95 -> 3, 96-100 -> 4."""
    if not 0 <= level <= 100:
        raise ValueError(f"nivel fuera de rango 0-100: {level}")
    if level <= 4:
        return 0
    if level <= 24:
        return 1
    if level <= 49:
        return 2
    if level <= 95:
        return 3
    return 4


def chapters_to_review(levels: dict) -> List[str]:
    """Dominios HAB con nivel >= 5, p. ej. {'D1': 70, 'D4': 2} -> ['D1']."""
    return [d for d in sorted(levels) if levels[d] >= REVIEW_THRESHOLD]
