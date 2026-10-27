"""Reglas fijas del motor (sin LLM): grupo de edad, calificadores y capitulos a revisar."""
import re
import unicodedata
from typing import Dict, List, Optional, Tuple

from .domain_map import MIN_AGE_FOR_DOMAINS, REVIEW_THRESHOLD, qualifier_from_level

MAX_PER_COMPONENT = 3

# Regla de vinculacion (HU-07g, 26-oct-2026): una dificultad en el dominio D4 (movilidad) se asocia con las funciones
# neuromusculoesqueleticas basicas del capitulo 7 (movilidad articular, fuerza, tono, control del movimiento voluntario
# y patron de la marcha). La busqueda por el texto del diagnostico no las traia (b730, b760 y b770 eran el 40 % de las
# omisiones). Entran como candidatos; el modelo decide si el caso las respalda.
MOBILITY_BODY_CODES = ("b710", "b730", "b735", "b760", "b770")
# Segunda version (26-oct-2026, tras la segunda ronda de la revision): la regla se disparaba con cualquier dificultad en D4
# y la medica rechazo 8 de 37 funciones nuevas en casos sin limitacion motora (hipoacusia, asma leve, TEPT, alcohol, Down,
# TEA; D4 entre 10 y 40). Ahora exige una limitacion de movilidad grave (calificador >= 3, nivel D4 >= 50) y una deficiencia
# fisica al menos moderada.
MOBILITY_MIN_LEVEL = 50
MOBILITY_MIN_CATEGORY = 2

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


def mobility_link_applies(cat_fisica: Optional[str], levels: Dict[str, int]) -> bool:
    """Vinculo D4 -> funciones neuromusculoesqueleticas: limitacion de movilidad grave y deficiencia fisica >= moderada."""
    physical = category_qualifier(cat_fisica)
    return (
        physical is not None
        and physical >= MOBILITY_MIN_CATEGORY
        and levels.get("D4", 0) >= MOBILITY_MIN_LEVEL
    )


def body_chapters(
    component: str, cat_fisica: Optional[str], cat_psicosocial: Optional[str], mental_link: bool = False
) -> List[int]:
    """Capitulos donde buscar funciones (b) o estructuras (s), segun las categorias de HAB.

    b1 (funciones mentales) depende de la categoria psicosocial; b2-b8 y todas las estructuras (s),
    de la fisica. Una categoria 'Ninguna' excluye sus capitulos; si no es reconocible, se incluyen.

    mental_link (26-oct-2026): sin deficiencia fisica pero con deficiencia psicosocial, las estructuras se buscan en el
    capitulo 1 (sistema nervioso: s110 cerebro), pues las funciones mentales (b1) se vinculan con estas estructuras
    (reglas de vinculacion, Cieza et al. 2005); la medica esperaba s110 en esquizofrenia, depresion y TEPT."""
    physical = category_qualifier(cat_fisica) != 0
    mental = category_qualifier(cat_psicosocial) != 0
    if component == "s":
        if physical:
            return list(range(1, 9))
        return [1] if (mental_link and mental) else []
    return ([1] if mental else []) + (list(range(2, 9)) if physical else [])


_CIE_PREFIX = re.compile(r"^\s*[A-Z]\d{2}(\.\d+)?\s*[:\-]?\s*", re.IGNORECASE)


def clean_diagnosis(text: Optional[str]) -> str:
    """Quita los codigos CIE ('G80.9 Paralisis cerebral; I50 Insuficiencia' -> 'Paralisis cerebral; Insuficiencia')."""
    if not text:
        return ""
    parts = [_CIE_PREFIX.sub("", part).strip() for part in re.split(r"[;\n]", text)]
    return "; ".join(part for part in parts if part)


def clinical_query(diag_cie: Optional[str], clinical_notes: Optional[str]) -> Optional[str]:
    """Texto de busqueda solo con lo clinico (diagnostico sin codigo + notas); None si el medico no escribio nada."""
    parts = [clean_diagnosis(diag_cie), (clinical_notes or "").strip()]
    text = ". ".join(part for part in parts if part)
    return text or None


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
