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

# Candidatos del Anexo 1239 por dominio oficial: codigos CIF-IA de las preguntas de las tablas 9
# (6 a 17 anios) y 11 (WHODAS, 18 anios o mas), transcritos del original (resolucion del 21-jul-2022,
# hojas 29-33). Ages: "6-17" solo tabla 9, "18+" solo tabla 11, "both" en ambas.
# No se incluyen codigos de factores ambientales (e150, e155, e4): quedan fuera del perfil (solo b, s, d).
# Las tablas 7 y 8 (0-5 anios) no aplican: para menores de 6 anios no se calculan niveles por dominio.
ANNEX_CANDIDATES: List[Tuple[str, str, str]] = [
    # D1 Cognicion
    ("Cognicion", "b1400", "both"),
    ("Cognicion", "d161", "both"),
    ("Cognicion", "b144", "both"),
    ("Cognicion", "d175", "both"),
    ("Cognicion", "d155", "both"),
    ("Cognicion", "d310", "both"),
    ("Cognicion", "d350", "both"),
    # D2 Movilidad
    ("Movilidad", "d4154", "both"),
    ("Movilidad", "d4104", "both"),
    ("Movilidad", "d4600", "both"),
    ("Movilidad", "d4602", "both"),
    ("Movilidad", "d4501", "both"),
    # D3 Cuidado personal
    ("Cuidado personal", "d510", "both"),
    ("Cuidado personal", "d520", "6-17"),
    ("Cuidado personal", "d540", "both"),
    ("Cuidado personal", "d550", "both"),
    ("Cuidado personal", "d598", "both"),
    # D4 Relaciones
    ("Relaciones", "d730", "both"),
    ("Relaciones", "d7500", "both"),
    ("Relaciones", "d760", "both"),
    ("Relaciones", "d740", "6-17"),
    ("Relaciones", "d7702", "18+"),
    # D5 Actividades cotidianas (tareas domesticas, escuela y trabajo)
    ("Actividades cotidianas", "d640", "both"),
    ("Actividades cotidianas", "d820", "both"),
    ("Actividades cotidianas", "d825", "both"),
    ("Actividades cotidianas", "d830", "both"),
    ("Actividades cotidianas", "d850", "18+"),
    # D6 Participacion
    ("Participacion", "d910", "both"),
    ("Participacion", "d920", "both"),
    ("Participacion", "d570", "18+"),
    ("Participacion", "d879", "18+"),
    ("Participacion", "d940", "18+"),
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
