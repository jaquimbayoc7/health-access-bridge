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
    def __init__(self):
        self.searches = []

    def annex_candidates(self, chapters, age_group):
        table = {4: D4, 1: D1}
        return [pair for ch in chapters for pair in table.get(ch, [])]

    def chapter_codes(self, chapter):
        return D2_CHAPTER if chapter == 2 else []

    def search(self, component, embedding, limit):
        self.searches.append(component)
        return {"b": B, "s": S}[component][:limit]


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


def run(p, chat, repo=None):
    return suggest(p, repo or FakeRepo(), embed, chat, "qwen2.5:3b")


GOOD = {
    "d": ["d4501", "d4600"],
    "b": [{"code": "b730", "justificacion": "Compromiso de la fuerza"}],
    "s": [{"code": "s750", "justificacion": "Amputacion de pierna"}],
}


def test_under_six_not_applicable():
    res = run(patient(age=5), chat_returning(GOOD))
    assert res.applicable is False
    assert "6 anios" in res.message
    assert not (res.functions or res.structures or res.activities)


def test_happy_path_titles_from_catalog_and_qualifiers_from_rules():
    res = run(patient(), chat_returning(GOOD))
    assert res.applicable and res.llm_used and res.llm_error is None
    # d: orden del LLM, calificador del nivel D4 = 60 -> 3
    assert [a.code for a in res.activities] == ["d4501", "d4600"]
    assert all(a.qualifier == 3 and a.origin == "llm" for a in res.activities)
    assert res.activities[0].title == "Andar distancias largas"
    # b: categoria fisica Severa -> 3
    assert res.functions[0].code == "b730" and res.functions[0].qualifier == 3
    assert res.functions[0].title == "Funciones relacionadas con la fuerza muscular"
    # s: magnitud 3, naturaleza y localizacion en 8
    s = res.structures[0]
    assert (s.qualifier, s.qualifier_cn, s.qualifier_cl) == (3, 8, 8)


def test_timings_and_llm_stats_are_reported():
    stats = {"prompt_eval_count": 500, "eval_count": 40}
    res = suggest(patient(), FakeRepo(), embed, chat_returning(GOOD), "qwen2.5:3b", stats=stats)
    assert set(res.timings) == {"embed", "search", "llm"}
    assert all(isinstance(v, int) and v >= 0 for v in res.timings.values())
    assert res.llm_stats == stats


def test_llm_never_controls_titles():
    payload = dict(GOOD, d=["d4501"])
    payload["b"] = [{"code": "b730", "justificacion": "x", "title": "TITULO INVENTADO"}]
    res = run(patient(), chat_returning(payload))
    assert res.functions[0].title == "Funciones relacionadas con la fuerza muscular"


def test_invalid_codes_are_dropped():
    payload = {"d": ["d9999", "d4501"], "b": [{"code": "b999", "justificacion": "x"}], "s": []}
    res = run(patient(), chat_returning(payload))
    assert res.llm_used
    assert [a.code for a in res.activities] == ["d4501"]
    # el unico codigo b del LLM era invalido: b cae a similitud
    assert all(f.origin == "similarity" for f in res.functions)


def test_duplicates_and_max_three():
    payload = {"d": ["d4501", "d4501", "d4600", "d4602", "d4104"], "b": [], "s": []}
    res = run(patient(), chat_returning(payload))
    assert [a.code for a in res.activities] == ["d4501", "d4600", "d4602"]


@pytest.mark.parametrize("bad", ["no es json", "[]", '{"d": []}', "{}"])
def test_llm_garbage_falls_back_to_rules(bad):
    res = run(patient(), chat_returning(bad))
    assert res.llm_used is False and res.llm_error
    assert res.activities and all(a.origin == "rules" for a in res.activities)
    assert all(f.origin == "similarity" for f in res.functions)
    assert len(res.activities) <= 3
    assert any("no respondio de forma valida" in w for w in res.warnings)


def test_llm_exception_falls_back():
    def boom(messages, schema):
        raise TimeoutError("timed out")

    res = run(patient(), boom)
    assert res.llm_used is False and "TimeoutError" in res.llm_error
    assert res.activities  # el motor siempre entrega algo por reglas


def test_no_body_components_when_categories_are_ninguna():
    repo = FakeRepo()
    res = run(patient(cat_fisica="Ninguna", cat_psicosocial="Ninguna"), chat_returning(GOOD), repo)
    assert not res.functions and not res.structures
    assert repo.searches == []
    assert any("Ninguna" in w for w in res.warnings)
    assert res.activities  # las actividades siguen


def test_mental_functions_use_psychosocial_category():
    # b152 es b1 (mental): con psicosocial 'Ninguna' se excluye; b730 usa la fisica 'Severa'.
    repo = FakeRepo()
    res = run(patient(cat_psicosocial="Ninguna"), chat_returning({"b": [{"code": "b730", "justificacion": "x"}]}), repo)
    codes = [f.code for f in res.functions]
    assert "b730" in codes and "b152" not in codes and "b134" not in codes


def test_unrecognized_category_leaves_qualifier_unspecified():
    res = run(patient(cat_fisica="Si", cat_psicosocial="No"), chat_returning(GOOD))
    assert res.functions[0].qualifier is None
    assert any("asignarse manualmente" in w for w in res.warnings)


def test_generic_warning_without_clinical_text():
    res = run(patient(diag_cie=None, clinical_notes=None), chat_returning(GOOD))
    assert any("genericas" in w for w in res.warnings)


def test_chapter_without_annex_codes_uses_chapter_fallback():
    p = patient(levels={"D2": 40}, cat_fisica="Ninguna", cat_psicosocial="Ninguna")
    res = run(p, chat_returning({"d": ["d210"]}))
    assert [a.code for a in res.activities] == ["d210"]
    assert res.activities[0].qualifier == 2


def test_no_levels_over_threshold():
    res = run(patient(levels={"D1": 2, "D4": 4}), chat_returning(GOOD))
    assert not res.activities
    assert any("nivel >= 5" in w for w in res.warnings)


def test_embedding_failure_keeps_activities():
    def bad_embed(_):
        raise ConnectionError("ollama caido")

    res = suggest(patient(), FakeRepo(), bad_embed, chat_returning({"d": ["d4501"]}), "qwen2.5:3b")
    assert [a.code for a in res.activities] == ["d4501"]
    assert not res.functions and not res.structures
    assert any("funciones y estructuras" in w for w in res.warnings)


def test_schema_only_allows_candidate_codes():
    schema = llm.build_schema(["d4501"], ["b730"], ["s750"])
    assert schema["properties"]["d"]["items"]["enum"] == ["d4501"]
    assert schema["properties"]["b"]["items"]["properties"]["code"]["enum"] == ["b730"]
    assert schema["properties"]["s"]["maxItems"] == 3
    assert llm.build_schema([], ["b730"], [])["required"] == ["b"]


def test_prompt_lists_only_candidates_and_no_identifiers():
    msgs = llm.build_messages("Paciente de 30 anios.", D4, B[:1], [])
    text = msgs[1]["content"]
    assert "d4501: Andar distancias largas" in text and "b730" in text
    assert "ESTRUCTURAS" not in text
    assert msgs[0]["role"] == "system"


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
