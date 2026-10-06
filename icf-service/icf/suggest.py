"""Orquestador del motor de sugerencia (HU-07b).

Flujo: reglas fijas -> candidatos (Anexo + SQL + pgvector) -> LLM elige y ordena entre candidatos ->
validacion y armado del resultado. Titulos y calificadores nunca salen del LLM. Si el LLM falla, el
motor devuelve igual una sugerencia por reglas y similitud, marcada con su origen.
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

BODY_CANDIDATES = 8  # candidatos por busqueda semantica para b y s
ACTIVITY_CANDIDATES = 12  # tope de candidatos d en el prompt
UNSPECIFIED = 8  # "no especificada" en los calificadores de estructuras

_CHAPTER_NAME = {int(d.chapter_code[1]): d.chapter_name for d in HAB_DOMAINS}
_QUALIFIER_LABEL = {0: "ninguna", 1: "leve", 2: "moderada", 3: "severa", 4: "completa"}


def _patient_summary(patient: PatientContext, plan: List[Tuple[int, int, int]]) -> str:
    lines = [f"Paciente de {patient.age} anios."]
    if patient.gender:
        lines.append(f"Genero: {patient.gender}.")
    if patient.cause:
        lines.append(f"Causa de la deficiencia: {patient.cause}.")
    if patient.cat_fisica or patient.cat_psicosocial:
        lines.append(
            f"Categoria fisica: {patient.cat_fisica or 'sin dato'}. "
            f"Categoria psicosocial: {patient.cat_psicosocial or 'sin dato'}."
        )
    if plan:
        lines.append(
            "Dificultad por dominio (0-100): "
            + ", ".join(f"{_CHAPTER_NAME[ch]} {level}" for ch, level, _ in plan)
            + "."
        )
    if patient.prediction_description:
        lines.append(f"Perfil de barreras: {patient.prediction_description}.")
    if patient.diag_cie:
        lines.append(f"Diagnostico CIE: {patient.diag_cie}.")
    if patient.clinical_notes:
        lines.append(f"Notas clinicas: {patient.clinical_notes}")
    return "\n".join(lines)


def _body_items(
    component: str,
    chosen: List[Tuple[str, str, str]],  # (code, justification, origin)
    titles: Dict[str, str],
    patient: PatientContext,
) -> Tuple[List[SuggestedCode], bool]:
    items, unspecified = [], False
    for code, why, origin in chosen:
        qualifier = rules.body_qualifier(code, patient.cat_fisica, patient.cat_psicosocial)
        unspecified = unspecified or qualifier is None
        items.append(
            SuggestedCode(
                code=code,
                title=titles[code],
                qualifier=qualifier,
                qualifier_cn=UNSPECIFIED if component == "s" else None,
                qualifier_cl=UNSPECIFIED if component == "s" else None,
                justification=why or "Coincide con el contexto clinico del paciente.",
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
) -> SuggestionResult:
    started = time.perf_counter()
    result = SuggestionResult(applicable=True, model=model)

    def finish() -> SuggestionResult:
        result.latency_ms = round((time.perf_counter() - started) * 1000)
        return result

    group = rules.age_group(patient.age)
    if group is None:
        result.applicable = False
        result.message = (
            "Menor de 6 anios: el Anexo 1239 no calcula niveles por dominio para esta edad, "
            "por lo que no se genera sugerencia basada en D1-D6."
        )
        return finish()

    # 1) Actividades y participacion (d): candidatos del Anexo para los capitulos con dificultad.
    plan = rules.activity_plan(patient.levels)
    d_titles: Dict[str, str] = {}
    d_meta: Dict[str, Tuple[int, int, int]] = {}  # codigo -> (capitulo, nivel, calificador)
    d_pairs: List[Pair] = []
    for chapter, level, qualifier in plan:
        pairs = repo.annex_candidates([chapter], group) or repo.chapter_codes(chapter)
        for code, title in pairs:
            if code not in d_titles:
                d_titles[code] = title
                d_meta[code] = (chapter, level, qualifier)
                d_pairs.append((code, title))
    d_pairs = d_pairs[:ACTIVITY_CANDIDATES]
    if not plan:
        result.warnings.append("Ningun dominio D1-D6 tiene nivel >= 5: no hay actividades y participacion por sugerir.")

    # 2) Funciones (b) y estructuras (s): busqueda semantica con el contexto clinico.
    b_pairs: List[Pair] = []
    s_pairs: List[Pair] = []
    if rules.body_components_apply(patient.cat_fisica, patient.cat_psicosocial):
        context = rules.context_text(
            patient.cause,
            patient.cat_fisica,
            patient.cat_psicosocial,
            patient.diag_cie,
            patient.clinical_notes,
            [_CHAPTER_NAME[ch] for ch, _, _ in plan],
        )
        try:
            vector = embed_fn(context)
            keep = lambda pairs: [  # noqa: E731 - solo calificador >= 1 cuenta en b y s
                (c, t)
                for c, t in pairs
                if rules.body_qualifier(c, patient.cat_fisica, patient.cat_psicosocial) != 0
            ]
            b_pairs = keep(repo.search("b", vector, BODY_CANDIDATES))
            s_pairs = keep(repo.search("s", vector, BODY_CANDIDATES))
        except Exception as exc:  # embeddings o base no disponibles: se sigue solo con actividades
            result.warnings.append(f"No se pudieron buscar funciones y estructuras ({type(exc).__name__}).")
    else:
        result.warnings.append(
            "Categorias fisica y psicosocial en 'Ninguna': no hay funciones ni estructuras con calificador >= 1."
        )
    b_titles, s_titles = dict(b_pairs), dict(s_pairs)

    # 3) El LLM elige y ordena entre los candidatos (una sola llamada).
    parsed: Optional[Dict[str, List[Tuple[str, str]]]] = None
    if d_pairs or b_pairs or s_pairs:
        try:
            schema = llm.build_schema([c for c, _ in d_pairs], [c for c, _ in b_pairs], [c for c, _ in s_pairs])
            messages = llm.build_messages(_patient_summary(patient, plan), d_pairs, b_pairs, s_pairs)
            text = chat_fn(messages, schema)
            parsed = llm.parse_response(
                text, [c for c, _ in d_pairs], [c for c, _ in b_pairs], [c for c, _ in s_pairs]
            )
            result.llm_used = True
        except Exception as exc:  # JSON invalido, timeout, servidor caido...
            result.llm_error = f"{type(exc).__name__}: {exc}"[:200]
            result.warnings.append("El modelo no respondio de forma valida: se uso la seleccion por reglas y similitud.")

    # 4) Armado del resultado: titulos del catalogo, calificadores por reglas.
    d_chosen = [code for code, _ in parsed["d"]] if parsed and parsed["d"] else None
    d_origin = "llm" if d_chosen else "rules"
    for code in (d_chosen or [c for c, _ in d_pairs])[: rules.MAX_PER_COMPONENT]:
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

    fallback = "Mayor similitud con el contexto clinico (sin respuesta valida del modelo)."
    unspecified = False
    for component, pairs, titles, target in (
        ("b", b_pairs, b_titles, result.functions),
        ("s", s_pairs, s_titles, result.structures),
    ):
        if parsed and parsed[component]:
            chosen = [(code, why, "llm") for code, why in parsed[component]]
        else:
            chosen = [(code, fallback, "similarity") for code, _ in pairs[: rules.MAX_PER_COMPONENT]]
        items, flag = _body_items(component, chosen, titles, patient)
        target.extend(items)
        unspecified = unspecified or flag

    if result.functions or result.structures:
        if not patient.diag_cie and not patient.clinical_notes:
            result.warnings.append(
                "Sin diagnostico CIE ni notas clinicas: las funciones y estructuras sugeridas son genericas."
            )
        if unspecified:
            result.warnings.append(
                "La categoria de discapacidad no indica una gravedad reconocible: "
                "el calificador de funciones y estructuras debe asignarse manualmente."
            )
    return finish()
