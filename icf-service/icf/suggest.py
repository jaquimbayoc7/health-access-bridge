"""Orquestador del motor de sugerencia (HU-07b).

Flujo: reglas fijas -> embedding del contexto clinico -> candidatos -> seleccion -> validacion.
  * Actividades y participacion (d): lista cerrada del Anexo para los capitulos con dificultad, ordenada
    por calificador y por similitud con el contexto. No usa el modelo de generacion.
  * Funciones (b) y estructuras (s): los candidatos mas cercanos por pgvector; el LLM elige y ordena
    entre ellos (solo codigos). Si el LLM falla o esta apagado, se usan los mas cercanos.
Titulos y calificadores nunca salen del LLM.
"""
import time
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from . import llm, rules
from .domain_map import HAB_DOMAINS
from .repository import Repo
from .schemas import PatientContext, SuggestedCode, SuggestionResult

Pair = Tuple[str, str]
EmbedFn = Callable[[str], Sequence[float]]
ChatFn = Callable[[List[Dict[str, str]], dict], str]

BODY_CANDIDATES = 6  # candidatos por busqueda semantica para b y s (menos tokens = menos espera)
UNSPECIFIED = 8  # "no especificada" en los calificadores de estructuras

_CHAPTER_NAME = {int(d.chapter_code[1]): d.chapter_name for d in HAB_DOMAINS}
_QUALIFIER_LABEL = {0: "ninguna", 1: "leve", 2: "moderada", 3: "severa", 4: "completa"}

_WHY_LLM = "Seleccionado por el modelo entre los códigos más cercanos al contexto clínico."
_WHY_SIMILARITY = "Mayor similitud con el contexto clínico."


def _patient_summary(patient: PatientContext, plan: List[Tuple[int, int, int]]) -> str:
    """Resumen breve para el modelo (sin acentos y sin relleno: cada token de entrada cuesta tiempo)."""
    lines = [f"Paciente {patient.age} anios."]
    if patient.cause:
        lines.append(f"Causa: {patient.cause}.")
    if patient.cat_fisica or patient.cat_psicosocial:
        lines.append(
            f"Fisica: {patient.cat_fisica or 'sin dato'}. Psicosocial: {patient.cat_psicosocial or 'sin dato'}."
        )
    if patient.diag_cie:
        lines.append(f"Dx: {patient.diag_cie}.")
    if patient.clinical_notes:
        lines.append(f"Notas: {patient.clinical_notes}")
    if plan:
        lines.append("Dificultad: " + ", ".join(f"{_CHAPTER_NAME[ch]} {level}" for ch, level, _ in plan) + ".")
    return "\n".join(lines)


def _body_items(
    component: str,
    chosen: List[Tuple[str, str]],  # (code, origin)
    titles: Dict[str, str],
    patient: PatientContext,
) -> Tuple[List[SuggestedCode], bool]:
    items, unspecified = [], False
    for code, origin in chosen:
        qualifier = rules.body_qualifier(code, patient.cat_fisica, patient.cat_psicosocial)
        unspecified = unspecified or qualifier is None
        items.append(
            SuggestedCode(
                code=code,
                title=titles[code],
                qualifier=qualifier,
                qualifier_cn=UNSPECIFIED if component == "s" else None,
                qualifier_cl=UNSPECIFIED if component == "s" else None,
                justification=_WHY_LLM if origin == "llm" else _WHY_SIMILARITY,
                origin=origin,
            )
        )
    return items, unspecified


def suggest(
    patient: PatientContext,
    repo: Repo,
    embed_fn: EmbedFn,
    chat_fn: ChatFn,
    model: str,
    stats: Optional[Dict[str, int]] = None,
    use_llm: bool = True,
) -> SuggestionResult:
    started = time.perf_counter()
    result = SuggestionResult(applicable=True, model=model)

    def finish() -> SuggestionResult:
        result.latency_ms = round((time.perf_counter() - started) * 1000)
        result.llm_stats = dict(stats or {})
        return result

    def timed(stage: str, fn, *args):
        t0 = time.perf_counter()
        try:
            return fn(*args)
        finally:
            result.timings[stage] = round((time.perf_counter() - t0) * 1000)

    group = rules.age_group(patient.age)
    if group is None:
        result.applicable = False
        result.message = (
            "Menor de 6 años: el Anexo 1239 no calcula niveles por dominio para esta edad, "
            "por lo que no se genera sugerencia basada en D1-D6."
        )
        return finish()

    # 1) Candidatos de actividades y participacion (d): lista cerrada del Anexo por capitulo con dificultad.
    plan = rules.activity_plan(patient.levels)
    d_titles: Dict[str, str] = {}
    d_meta: Dict[str, Tuple[int, int, int]] = {}  # codigo -> (capitulo, nivel, calificador)
    for chapter, level, qualifier in plan:
        for code, title in repo.annex_candidates([chapter], group) or repo.chapter_codes(chapter):
            if code not in d_titles:
                d_titles[code], d_meta[code] = title, (chapter, level, qualifier)
    if not plan:
        result.warnings.append("Ningún dominio D1-D6 tiene nivel >= 5: no hay actividades y participación por sugerir.")

    body_applies = rules.body_components_apply(patient.cat_fisica, patient.cat_psicosocial)
    if not body_applies:
        result.warnings.append(
            "Categorías física y psicosocial en 'Ninguna': no hay funciones ni estructuras con calificador >= 1."
        )

    # 2) Un solo embedding del contexto clinico sirve para ordenar d y para buscar b y s.
    vector: Optional[Sequence[float]] = None
    if d_titles or body_applies:
        context = rules.context_text(
            patient.cause, patient.cat_fisica, patient.cat_psicosocial, patient.diag_cie,
            patient.clinical_notes, [_CHAPTER_NAME[ch] for ch, _, _ in plan],
        )
        try:
            vector = timed("embed", embed_fn, context)
        except Exception as exc:  # Ollama o embeddings no disponibles
            detail = (
                "actividades ordenadas solo por reglas; funciones y estructuras omitidas."
                if body_applies
                else "actividades ordenadas solo por reglas."
            )
            result.warnings.append(f"No se pudo calcular la similitud con el contexto clínico ({type(exc).__name__}): {detail}")

    # 3) Actividades (d): calificador mas alto primero; a igual calificador, mayor similitud.
    d_order = list(d_titles)
    if vector is not None and d_order:
        ranked = timed("rank", repo.rank_codes, d_order, vector)
        d_order = sorted(d_order, key=lambda c: (-d_meta[c][2], ranked.index(c)))
    else:
        d_order = sorted(d_order, key=lambda c: (-d_meta[c][2], d_order.index(c)))
    d_origin = "similarity" if vector is not None else "rules"
    for code in d_order[: rules.MAX_PER_COMPONENT]:
        chapter, level, qualifier = d_meta[code]
        result.activities.append(
            SuggestedCode(
                code=code,
                title=d_titles[code],
                qualifier=qualifier,
                justification=(
                    f"Nivel interno D{chapter} de HAB = {level} "
                    f"(calificador {qualifier}, {_QUALIFIER_LABEL[qualifier]})."
                ),
                origin=d_origin,
            )
        )

    # 4) Funciones (b) y estructuras (s): candidatos por similitud; el LLM elige y ordena (solo codigos).
    b_pairs: List[Pair] = []
    s_pairs: List[Pair] = []
    if body_applies and vector is not None:
        # Solo cuentan b y s con calificador >= 1: los capitulos de una categoria 'Ninguna' se excluyen
        # dentro de la busqueda (filtrar despues dejaba la lista vacia, ej. esquizofrenia sin deficiencia fisica).
        t0 = time.perf_counter()
        b_pairs = repo.search("b", vector, BODY_CANDIDATES, rules.body_chapters("b", patient.cat_fisica, patient.cat_psicosocial))
        s_pairs = repo.search("s", vector, BODY_CANDIDATES, rules.body_chapters("s", patient.cat_fisica, patient.cat_psicosocial))
        result.timings["search"] = round((time.perf_counter() - t0) * 1000)
    b_titles, s_titles = dict(b_pairs), dict(s_pairs)

    parsed: Optional[Dict[str, List[str]]] = None
    if use_llm and (b_pairs or s_pairs):
        try:
            schema = llm.build_schema([c for c, _ in b_pairs], [c for c, _ in s_pairs])
            messages = llm.build_messages(_patient_summary(patient, plan), b_pairs, s_pairs)
            text = timed("llm", chat_fn, messages, schema)
            parsed = llm.parse_response(text, [c for c, _ in b_pairs], [c for c, _ in s_pairs])
            result.llm_used = True
        except Exception as exc:  # JSON invalido, timeout, servidor caido...
            result.llm_error = f"{type(exc).__name__}: {exc}"[:200]
            result.warnings.append("El modelo no respondió de forma válida: se usó la similitud con el contexto clínico.")

    unspecified = False
    for component, pairs, titles, target in (
        ("b", b_pairs, b_titles, result.functions),
        ("s", s_pairs, s_titles, result.structures),
    ):
        if parsed and parsed[component]:
            chosen = [(code, "llm") for code in parsed[component]]
        else:
            chosen = [(code, "similarity") for code, _ in pairs[: rules.MAX_PER_COMPONENT]]
        items, flag = _body_items(component, chosen, titles, patient)
        target.extend(items)
        unspecified = unspecified or flag

    if result.functions or result.structures:
        if not patient.diag_cie and not patient.clinical_notes:
            result.warnings.append(
                "Sin diagnóstico CIE ni notas clínicas: las funciones y estructuras sugeridas son genéricas."
            )
        if unspecified:
            result.warnings.append(
                "La categoría de discapacidad no indica una gravedad reconocible: "
                "el calificador de funciones y estructuras debe asignarse manualmente."
            )
    return finish()
