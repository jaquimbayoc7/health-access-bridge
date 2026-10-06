"""Reglas fijas del motor (sin LLM): grupo de edad, calificadores y capitulos a revisar."""
import unicodedata
from typing import Dict, List, Optional, Tuple

from .domain_map import MIN_AGE_FOR_DOMAINS, REVIEW_THRESHOLD, qualifier_from_level

MAX_PER_COMPONENT = 3

# Categoria de discapacidad de HAB (cat_fisica / cat_psicosocial) -> calificador generico de la CIF.
_CATEGORY_QUALIFIER = {
    "ninguna": 0,
    "leve": 1,
    "moderada": 2,
    "severa": 3,
    "grave": 3,
    "completa": 4,
}


def _normalize(text: Optional[str]) -> str:
    if not text:
        return ""
    decomposed = unicodedata.normalize("NFD", text.strip().lower())
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def category_qualifier(value: Optional[str]) -> Optional[int]:
    """Calificador 0-4 de una categoria de HAB; None si el valor no es una gravedad reconocible (ej. 'Si')."""
    return _CATEGORY_QUALIFIER.get(_normalize(value))


def age_group(age: int) -> Optional[str]:
    """'6-17' o '18+'; None para menores de 6 anios (no se calculan niveles por dominio)."""
    if age < MIN_AGE_FOR_DOMAINS:
        return None
    return "6-17" if age <= 17 else "18+"


def activity_plan(levels: Dict[str, int]) -> List[Tuple[int, int, int]]:
    """Capitulos d a revisar: [(capitulo, nivel_HAB, calificador)] con nivel >= 5, del mas afectado al menos."""
    plan = [
        (int(key[1]), level, qualifier_from_level(level))
        for key, level in levels.items()
        if level >= REVIEW_THRESHOLD
    ]
    return sorted(plan, key=lambda item: (-item[1], item[0]))


def body_qualifier(code: str, cat_fisica: Optional[str], cat_psicosocial: Optional[str]) -> Optional[int]:
    """Magnitud sugerida para una funcion (b) o estructura (s).

    Las funciones mentales (b1) usan la categoria psicosocial; el resto, la fisica. HAB no mide b ni s
    por separado, asi que es una aproximacion que el medico edita. None si la categoria no es reconocible.
    """
    mental = code.startswith("b1")
    return category_qualifier(cat_psicosocial if mental else cat_fisica)


def body_components_apply(cat_fisica: Optional[str], cat_psicosocial: Optional[str]) -> bool:
    """El Anexo solo cuenta funciones y estructuras con calificador >= 1: si ambas categorias son 'Ninguna', no aplican."""
    fisica, psico = category_qualifier(cat_fisica), category_qualifier(cat_psicosocial)
    return not (fisica == 0 and psico == 0)


def context_text(
    cause: Optional[str],
    cat_fisica: Optional[str],
    cat_psicosocial: Optional[str],
    diag_cie: Optional[str],
    clinical_notes: Optional[str],
    chapters: List[str],
) -> str:
    """Texto para el embedding de busqueda de funciones y estructuras."""
    parts = []
    if diag_cie:
        parts.append(f"Diagnostico: {diag_cie}")
    if clinical_notes:
        parts.append(f"Notas: {clinical_notes}")
    if cause:
        parts.append(f"Causa de la deficiencia: {cause}")
    if cat_fisica:
        parts.append(f"Deficiencia fisica: {cat_fisica}")
    if cat_psicosocial:
        parts.append(f"Deficiencia psicosocial: {cat_psicosocial}")
    if chapters:
        parts.append("Dificultad en: " + ", ".join(chapters))
    return ". ".join(parts) or "deficiencia de funciones y estructuras corporales"
