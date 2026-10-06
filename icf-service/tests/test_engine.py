"""HU-07b - pruebas del motor con repositorio, embeddings y LLM simulados."""
import json

import pytest
from pydantic import ValidationError

from icf import llm, rules
from icf.schemas import PatientContext
from icf.suggest import suggest

D4 = [
    ("d4154", "Permanecer de pie"),
    ("d4104", "Ponerse de pie"),
    ("d4600", "Desplazarse dentro de la casa"),
    ("d4602", "Desplazarse fuera del hogar y de otros edificios"),
    ("d4501", "Andar distancias largas"),
]
D1 = [("d155", "Adquisicion de habilidades"), ("d161", "Dirigir la atencion"), ("d175", "Resolver problemas")]
D5 = [("d510", "Lavarse"), ("d540", "Vestirse")]
D2_CHAPTER = [("d210", "Llevar a cabo una tarea unica"), ("d220", "Llevar a cabo tareas multiples")]
B = [
    ("b730", "Funciones relacionadas con la fuerza muscular"),
    ("b710", "Funciones de las articulaciones"),
    ("b280", "Sensacion de dolor"),
    ("b134", "Funciones del sueno"),
    ("b152", "Funciones emocionales"),
]
S = [("s750", "Estructura de la extremidad inferior"), ("s730", "Estructura de la extremidad superior")]


class FakeRepo:
    def __init__(self, similarity_order=None):
        self.searches = []
        self.limits = []
        self.ranked = []
        self.similarity_order = similarity_order  # codigos d de mayor a menor similitud

    def annex_candidates(self, chapters, age_group):
        table = {4: D4, 1: D1, 5: D5}
        return [pair for ch in chapters for pair in table.get(ch, [])]

    def chapter_codes(self, chapter):
        return D2_CHAPTER if chapter == 2 else []

    def search(self, component, embedding, limit, chapters=None, levels=(2,)):
        self.limits.append(limit)
        self.searches.append((component, None if chapters is None else list(chapters)))
        pairs = {"b": B, "s": S}[component]
        if chapters is not None:
            pairs = [(c, t) for c, t in pairs if int(c[1]) in chapters]
        return pairs[:limit]

    def rank_codes(self, codes, embedding):
        self.ranked.append(list(codes))
        if not self.similarity_order:
            return list(codes)
        first = [c for c in self.similarity_order if c in codes]
        return first + [c for c in codes if c not in first]


def patient(**overrides):
    base = dict(
        age=30,
        cause="Accidente de transito",
        cat_fisica="Severa",
        cat_psicosocial="Leve",
        levels={"D1": 3, "D2": 0, "D3": 0, "D4": 60, "D5": 10, "D6": 0},
        diag_cie="S78 Amputacion traumatica",
    )
    base.update(overrides)
    return PatientContext(**base)


def chat_returning(payload):
    return lambda messages, schema: payload if isinstance(payload, str) else json.dumps(payload)


def embed(_text):
    return [0.1, 0.2, 0.3]


def run(p, chat, repo=None, **kwargs):
    return suggest(p, repo or FakeRepo(), embed, chat, "qwen2.5:3b", **kwargs)


GOOD = {"b": ["b730"], "s": ["s750"]}


def test_under_six_not_applicable():
    res = run(patient(age=5), chat_returning(GOOD))
    assert res.applicable is False
    assert "6 años" in res.message
    assert not (res.functions or res.structures or res.activities)


def test_happy_path_titles_from_catalog_and_qualifiers_from_rules():
    res = run(patient(), chat_returning(GOOD))
    assert res.applicable and res.llm_used and res.llm_error is None
    # d: calificador del nivel D4 = 60 -> 3; titulo del catalogo
    assert res.activities and all(a.qualifier == 3 for a in res.activities)
    assert {a.code for a in res.activities} <= {c for c, _ in D4 + D5}
    top = next(a for a in res.activities if a.code == "d4154")
    assert top.title == "Permanecer de pie"
    # b: categoria fisica Severa -> 3
    assert res.functions[0].code == "b730" and res.functions[0].qualifier == 3
    assert res.functions[0].title == "Funciones relacionadas con la fuerza muscular"
    assert res.functions[0].origin == "llm"
    # s: magnitud 3, naturaleza y localizacion en 8
    s = res.structures[0]
    assert (s.qualifier, s.qualifier_cn, s.qualifier_cl) == (3, 8, 8)


def test_activities_never_call_the_llm():
    calls = []

    def chat(messages, schema):
        calls.append(schema)
        return json.dumps(GOOD)

    run(patient(), chat)
    assert len(calls) == 1
    assert "d" not in calls[0]["properties"]  # el esquema solo cubre b y s
    assert "d4501" not in json.dumps(calls[0]) and "d4501" not in json.dumps(calls)


def test_activities_ordered_by_qualifier_then_similarity():
    levels = {"D1": 30, "D4": 70, "D5": 10}  # D4 -> calificador 3, D1 -> 2, D5 -> 1
    repo = FakeRepo(similarity_order=["d175", "d4501", "d4600", "d510"])
    res = run(patient(levels=levels), chat_returning(GOOD), repo)
    # calificador 3 primero (d4501, d4600 por similitud), luego d4154 (q3), y recien despues D1
    assert [a.code for a in res.activities] == ["d4501", "d4600", "d4154"]
    assert [a.qualifier for a in res.activities] == [3, 3, 3]
    assert all(a.origin == "similarity" for a in res.activities)
    # una sola consulta de orden con todos los candidatos
    assert len(repo.ranked) == 1 and set(repo.ranked[0]) == {c for c, _ in D4 + D1 + D5}


def test_lower_chapter_comes_after_higher_qualifier():
    levels = {"D1": 30, "D4": 70}
    repo = FakeRepo(similarity_order=["d175", "d155", "d161"])  # D1 es lo mas similar
    res = run(patient(levels=levels), chat_returning(GOOD), repo)
    assert [a.code for a in res.activities][:3] == ["d4154", "d4104", "d4600"]  # D4 (q3) antes que D1 (q2)


def test_invalid_codes_are_dropped():
    payload = {"b": ["b999", "b730"], "s": ["s0000"]}
    res = run(patient(), chat_returning(payload))
    assert res.llm_used
    assert [f.code for f in res.functions] == ["b730"]
    # el unico codigo s del LLM era invalido: s cae a similitud
    assert all(s.origin == "similarity" for s in res.structures)


def test_duplicates_and_max_three():
    payload = {"b": ["b730", "b730", "b710", "b280", "b134"], "s": []}
    res = run(patient(), chat_returning(payload))
    assert [f.code for f in res.functions] == ["b730", "b710", "b280"]


def test_objects_with_code_are_tolerated():
    res = run(patient(), chat_returning({"b": [{"code": "b730", "justificacion": "Debilidad por la amputacion"}], "s": []}))
    assert res.llm_used and res.functions[0].code == "b730"
    assert res.functions[0].justification == "Debilidad por la amputacion"  # la del modelo, si la trae


@pytest.mark.parametrize("bad", ["no es json", "[]", '{"b": []}', "{}"])
def test_llm_garbage_falls_back_to_similarity(bad):
    res = run(patient(), chat_returning(bad))
    assert res.llm_used is False and res.llm_error
    assert res.activities  # las actividades no dependen del modelo
    assert res.functions and all(f.origin == "similarity" for f in res.functions)
    assert len(res.functions) <= 3
    assert any("no respondió de forma válida" in w for w in res.warnings)


def test_llm_exception_falls_back():
    def boom(messages, schema):
        raise TimeoutError("timed out")

    res = run(patient(), boom)
    assert res.llm_used is False and "TimeoutError" in res.llm_error
    assert res.activities and res.functions


def test_use_llm_false_skips_the_model():
    def never(messages, schema):
        raise AssertionError("no debe llamarse al modelo")

    res = run(patient(), never, use_llm=False)
    assert res.llm_used is False and res.llm_error is None
    assert res.functions and all(f.origin == "similarity" for f in res.functions)
    assert "llm" not in res.timings


def test_no_body_components_when_categories_are_ninguna():
    repo = FakeRepo()
    res = run(patient(cat_fisica="Ninguna", cat_psicosocial="Ninguna"), chat_returning(GOOD), repo)
    assert not res.functions and not res.structures
    assert repo.searches == []  # ni siquiera se busca
    assert any("Ninguna" in w for w in res.warnings)
    assert res.activities  # las actividades siguen


def test_mental_functions_use_psychosocial_category():
    # b152 y b134 son b1 (mentales): con psicosocial 'Ninguna' se excluyen; b730 usa la fisica 'Severa'.
    res = run(patient(cat_psicosocial="Ninguna"), chat_returning({"b": ["b730"]}))
    codes = [f.code for f in res.functions]
    assert "b730" in codes and "b152" not in codes and "b134" not in codes


def test_psychosocial_only_patient_gets_mental_functions_and_no_structures():
    """Caso C05 (esquizofrenia): sin deficiencia fisica solo aplican b1 y ninguna estructura."""
    repo = FakeRepo()
    res = run(patient(cat_fisica="Ninguna", cat_psicosocial="Severa", diag_cie="F20 Esquizofrenia"),
              chat_returning({"b": ["b152"]}), repo)
    assert [f.code for f in res.functions] == ["b152"] and res.functions[0].qualifier == 3
    assert res.structures == []
    assert ("b", [1]) in repo.searches and ("s", []) in repo.searches


def test_physical_only_patient_gets_no_mental_functions():
    repo = FakeRepo()
    res = run(patient(cat_fisica="Severa", cat_psicosocial="Ninguna"), chat_returning(GOOD), repo)
    assert ("b", list(range(2, 9))) in repo.searches
    assert all(not f.code.startswith("b1") for f in res.functions)


def test_body_chapters_rules():
    assert rules.body_chapters("b", "Severa", "Leve") == list(range(1, 9))
    assert rules.body_chapters("b", "Ninguna", "Severa") == [1]
    assert rules.body_chapters("b", "Severa", "Ninguna") == list(range(2, 9))
    assert rules.body_chapters("s", "Ninguna", "Severa") == []
    assert rules.body_chapters("s", "Si", "No") == list(range(1, 9))  # no reconocible: no se excluye nada


def test_clinical_query_drops_cie_codes_and_keeps_text():
    assert rules.clean_diagnosis("G80.9 Paralisis cerebral infantil") == "Paralisis cerebral infantil"
    assert rules.clean_diagnosis("S98 Amputacion traumatica del pie; F43.1 Trastorno de estres postraumatico") == (
        "Amputacion traumatica del pie; Trastorno de estres postraumatico"
    )
    assert rules.clean_diagnosis("Parkinson") == "Parkinson"
    assert rules.clinical_query("G20 Enfermedad de Parkinson", "Temblor en reposo") == (
        "Enfermedad de Parkinson. Temblor en reposo"
    )
    assert rules.clinical_query(None, None) is None and rules.clinical_query("  ", "") is None


def test_unrecognized_category_leaves_qualifier_unspecified():
    res = run(patient(cat_fisica="Si", cat_psicosocial="No"), chat_returning(GOOD))
    assert res.functions[0].qualifier is None
    assert any("asignarse manualmente" in w for w in res.warnings)


def test_generic_warning_without_clinical_text():
    res = run(patient(diag_cie=None, clinical_notes=None), chat_returning(GOOD))
    assert any("genéricas" in w for w in res.warnings)


def test_chapter_without_annex_codes_uses_chapter_fallback():
    p = patient(levels={"D2": 40}, cat_fisica="Ninguna", cat_psicosocial="Ninguna")
    res = run(p, chat_returning(GOOD))
    assert {a.code for a in res.activities} == {"d210", "d220"}
    assert all(a.qualifier == 2 for a in res.activities)


def test_no_levels_over_threshold():
    res = run(patient(levels={"D1": 2, "D4": 4}), chat_returning(GOOD))
    assert not res.activities
    assert any("nivel >= 5" in w for w in res.warnings)


def test_embedding_failure_keeps_activities_by_rules():
    def bad_embed(_):
        raise ConnectionError("ollama caido")

    res = suggest(patient(), FakeRepo(), bad_embed, chat_returning(GOOD), "qwen2.5:3b")
    assert res.activities and all(a.origin == "rules" for a in res.activities)
    assert not res.functions and not res.structures
    assert any("funciones y estructuras omitidas" in w for w in res.warnings)


def test_timings_and_llm_stats_are_reported():
    stats = {"prompt_eval_count": 250, "eval_count": 40}
    res = suggest(patient(), FakeRepo(), embed, chat_returning(GOOD), "qwen2.5:3b", stats=stats)
    assert set(res.timings) == {"embed", "rank", "search", "llm"}
    assert all(isinstance(v, int) and v >= 0 for v in res.timings.values())
    assert res.llm_stats == stats


def test_justify_mode_uses_objects_in_schema_and_a_different_system_prompt():
    schema = llm.build_schema(["b730"], ["s750"], justify=True)
    item = schema["properties"]["b"]["items"]
    assert item["properties"]["code"] == {"type": "string", "enum": ["b730"]}
    assert item["required"] == ["code", "justificacion"]
    msgs = llm.build_messages("Paciente 30 anios.", B[:1], S[:1], justify=True)
    assert msgs[0]["content"] == llm.SYSTEM_PROMPT_JUSTIFY and "justificacion" in msgs[0]["content"]
    assert llm.build_messages("x", B[:1], S[:1])[0]["content"] == llm.SYSTEM_PROMPT  # el modo rapido no cambia


def test_engine_passes_justify_and_candidate_count():
    seen = {}

    def chat(messages, schema):
        seen["system"], seen["schema"] = messages[0]["content"], schema
        return json.dumps({
            "b": [{"code": "b730", "justificacion": "Fuerza afectada por la amputacion"}],
            "s": [{"code": "s750", "justificacion": "Pierna amputada"}],
        })

    repo = FakeRepo()
    res = suggest(patient(), repo, embed, chat, "qwen2.5:3b", body_candidates=12, justify=True)
    assert repo.limits == [12, 12]
    assert seen["system"] == llm.SYSTEM_PROMPT_JUSTIFY
    assert seen["schema"]["properties"]["b"]["items"]["type"] == "object"
    assert res.functions[0].justification == "Fuerza afectada por la amputacion"
    assert res.structures[0].justification == "Pierna amputada"
    fast = FakeRepo()
    suggest(patient(), fast, embed, chat_returning(GOOD), "qwen2.5:3b", body_candidates=6)
    assert fast.limits == [6, 6]


def test_schema_only_allows_candidate_codes():
    schema = llm.build_schema(["b730"], ["s750"])
    assert schema["properties"]["b"]["items"] == {"type": "string", "enum": ["b730"]}
    assert schema["properties"]["s"]["maxItems"] == 3
    assert schema["required"] == ["b", "s"]
    assert llm.build_schema(["b730"], [])["required"] == ["b"]


def test_prompt_is_short_static_prefix_first_and_has_no_identifiers():
    msgs = llm.build_messages("Paciente 30 anios.", B[:2], S[:1])
    assert msgs[0]["role"] == "system" and msgs[0]["content"] == llm.SYSTEM_PROMPT  # prefijo fijo
    user = msgs[1]["content"]
    assert user.startswith("Paciente 30 anios.")
    assert "b730 Funciones relacionadas con la fuerza muscular" in user and "s750" in user
    assert "d4" not in user  # las actividades no viajan al modelo
    assert len(llm.SYSTEM_PROMPT) < 260


def test_levels_and_qualifier_rules():
    assert rules.activity_plan({"D1": 3, "D4": 60, "D6": 96}) == [(6, 96, 4), (4, 60, 3)]
    assert rules.age_group(5) is None and rules.age_group(6) == "6-17"
    assert rules.age_group(17) == "6-17" and rules.age_group(18) == "18+"
    assert rules.category_qualifier("Grave") == 3 and rules.category_qualifier("Sí") is None


def test_schema_rejects_identifiers_and_bad_levels():
    for extra in ("nombre_apellidos", "numero_documento", "orientacion_sexual"):
        with pytest.raises(ValidationError):
            PatientContext(age=30, **{extra: "x"})
    with pytest.raises(ValidationError):
        PatientContext(age=30, levels={"D1": 101})
    with pytest.raises(ValidationError):
        PatientContext(age=30, levels={"D9": 10})
