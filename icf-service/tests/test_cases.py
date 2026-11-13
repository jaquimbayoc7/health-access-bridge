"""HU-07j - memoria de casos confirmados por el medico: guardado, retiro y uso como ejemplos."""
import json

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

import app as app_module
from icf import llm
from icf.cases import store_case
from icf.schemas import CaseRecord, PatientContext
from icf.suggest import case_context, suggest

from test_engine import B, S, FakeRepo, chat_returning, embed, patient

KEY = "11111111-2222-3333-4444-555555555555"


class MemoryRepo(FakeRepo):
    """FakeRepo con la memoria de casos en listas."""

    def __init__(self, cases=None, **kwargs):
        super().__init__(**kwargs)
        self.cases = cases or []
        self.contexts, self.saved_cases, self.saved_codes, self.deleted = {}, [], [], []
        self.case_queries = []

    def similar_cases(self, embedding, limit, min_similarity):
        self.case_queries.append((limit, min_similarity))
        return self.cases[:limit]

    def case_context(self, case_key):
        return self.contexts.get(case_key)

    def upsert_case(self, case_key, context, diag, age_group, embedding):
        self.contexts[case_key] = context
        self.saved_cases.append((case_key, context, diag, age_group, embedding))

    def upsert_case_code(self, case_key, item_ref, fields):
        self.saved_codes.append((case_key, item_ref, fields))

    def delete_case_code(self, case_key, item_ref):
        self.deleted.append((case_key, item_ref))


def record(**over):
    base = dict(
        case_key=KEY, item_ref=7, component="b", code="b730", status="aceptado", qualifier=4, qualifier_suggested=3,
        justification="Debilidad de ambas piernas", patient=patient(clinical_notes="Tetraparesia").model_dump(),
    )
    base.update(over)
    return CaseRecord(**base)


# ------------------------------------------------------------------ guardado
def test_stores_the_clinical_text_and_the_confirmed_code():
    repo, calls = MemoryRepo(), []
    out = store_case(record(), repo, lambda text: calls.append(text) or [0.1, 0.2])
    assert out == "stored" and len(calls) == 1
    key, context, diag, group, embedding = repo.saved_cases[0]
    assert key == KEY and "Tetraparesia" in context and diag == "Amputacion traumatica" and group == "18+"
    assert embedding == [0.1, 0.2]
    _, ref, fields = repo.saved_codes[0]
    assert ref == 7 and fields["code"] == "b730" and fields["qualifier"] == 4 and fields["qualifier_suggested"] == 3
    assert fields["justification"] == "Debilidad de ambas piernas"


def test_does_not_embed_again_when_the_case_text_did_not_change():
    repo, calls = MemoryRepo(), []
    fn = lambda text: calls.append(text) or [0.1]
    store_case(record(), repo, fn)
    store_case(record(item_ref=8, code="b760"), repo, fn)
    assert len(calls) == 1 and repo.saved_cases[1][4] is None and len(repo.saved_codes) == 2


def test_case_without_diagnosis_or_notes_is_skipped():
    repo = MemoryRepo()
    rec = record(patient=patient(diag_cie=None).model_dump())
    assert store_case(rec, repo, embed) == "skipped" and not repo.saved_codes


def test_rejecting_removes_the_code():
    repo = MemoryRepo()
    assert store_case(record(status="rechazado"), repo, embed) == "removed"
    assert repo.deleted == [(KEY, 7)] and not repo.saved_codes


def test_blank_justification_is_stored_as_null():
    repo = MemoryRepo()
    store_case(record(justification="   "), repo, embed)
    assert repo.saved_codes[0][2]["justification"] is None


def test_record_rejects_identifying_fields_and_bad_values():
    with pytest.raises(ValidationError):
        record(patient={"age": 30, "nombre_apellidos": "Juan Perez"})
    with pytest.raises(ValidationError):
        record(nombre="Juan")
    with pytest.raises(ValidationError):
        record(code="x730")
    with pytest.raises(ValidationError):
        record(status="sugerido")


def test_case_context_matches_what_suggest_searches_with():
    p = patient(clinical_notes="Tetraparesia")
    seen = []
    suggest(p, FakeRepo(), lambda text: seen.append(text) or [0.1], chat_returning({"b": ["b730"], "s": ["s750"]}), "m")
    assert case_context(p) == seen[0]
    assert case_context(patient(diag_cie=None)) is None


# ------------------------------------------------------------------ ejemplos en /suggest
CASE = {
    "case_key": "a", "diag": "S14 Traumatismo medular", "similarity": 0.91,
    "codes": [{"component": "b", "code": "b760", "qualifier": 3, "justification": "x"},
              {"component": "s", "code": "s730", "qualifier": 3, "justification": "y"}],
}


def run_with(repo, **kw):
    sent = []

    def chat(messages, schema):
        sent.append((messages, schema))
        return json.dumps({"b": ["b760"], "s": ["s730"]})

    result = suggest(patient(), repo, embed, chat, "m", case_examples=3, case_min_similarity=0.8, **kw)
    return result, sent


def test_examples_are_shown_to_the_model_and_their_codes_become_candidates():
    repo = MemoryRepo([CASE])
    result, sent = run_with(repo)
    messages, schema = sent[0]
    prompt = messages[1]["content"]
    assert llm.EXAMPLES_HEADER in prompt and "S14 Traumatismo medular: b760, s730" in prompt
    assert "b760" in schema["properties"]["b"]["items"]["enum"] and "s730" in schema["properties"]["s"]["items"]["enum"]
    assert result.case_examples == 1 and repo.case_queries == [(3, 0.8)]
    assert [f.code for f in result.functions] == ["b760"]  # el modelo puede elegirlo; el titulo sigue saliendo del catalogo
    assert result.functions[0].title == "Control de los movimientos voluntarios"


def test_no_examples_when_disabled_or_nothing_is_similar():
    repo = MemoryRepo([CASE])
    result = suggest(patient(), repo, embed, chat_returning({"b": ["b730"], "s": ["s750"]}), "m")
    assert result.case_examples == 0 and repo.case_queries == []  # apagado por defecto en el motor
    empty = MemoryRepo([])
    result, sent = run_with(empty)
    assert result.case_examples == 0 and llm.EXAMPLES_HEADER not in sent[0][0][1]["content"]


def test_example_codes_from_chapters_that_do_not_apply_are_ignored():
    # categoria fisica 'Ninguna': no hay capitulos b2-b8 ni estructuras; el ejemplo con b760 no aplica
    p = patient(cat_fisica="Ninguna", cat_psicosocial="Moderada")
    repo = MemoryRepo([CASE])
    result = suggest(p, repo, embed, chat_returning({"b": ["b152"]}), "m", case_examples=3)
    assert result.case_examples == 0


def test_a_failing_memory_never_blocks_a_suggestion():
    class Broken(MemoryRepo):
        def similar_cases(self, *a):
            raise RuntimeError("boom")

    result, _ = run_with(Broken())
    assert result.llm_used and result.functions and result.case_examples == 0


def test_examples_block_is_short_and_skips_empty_cases():
    block = llm.examples_block([{"diag": "x" * 200, "codes": ["b730"]}, {"diag": "y", "codes": []}])
    lines = block.splitlines()
    assert len(lines) == 2 and len(lines[1]) < 100
    assert llm.examples_block([]) == ""


# ------------------------------------------------------------------ endpoint
client = TestClient(app_module.app)


def test_post_cases_rejects_identifying_data():
    resp = client.post("/cases", json={**record().model_dump(), "patient": {"age": 30, "numero_documento": "1"}})
    assert resp.status_code == 422


def test_post_cases_can_be_disabled(monkeypatch):
    monkeypatch.setattr(app_module, "settings", app_module.settings.__class__(
        database_url="", ollama_url="http://127.0.0.1:1", llm_model="m", embed_model="e", keep_alive="1m",
        llm_timeout_s=1, case_memory=False,
    ))
    assert client.post("/cases", json=record().model_dump()).json() == {"status": "disabled"}


def test_post_cases_without_database_returns_503(monkeypatch):
    monkeypatch.setattr(app_module, "settings", app_module.settings.__class__(
        database_url="", ollama_url="http://127.0.0.1:1", llm_model="m", embed_model="e", keep_alive="1m", llm_timeout_s=1,
    ))
    assert client.post("/cases", json=record().model_dump()).status_code == 503


def test_post_cases_stores_through_the_repository(monkeypatch):
    repo = MemoryRepo()

    class Conn:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    monkeypatch.setattr(app_module, "_connect", lambda: Conn())
    monkeypatch.setattr(app_module, "PgRepo", lambda conn: repo)
    repo.ensure_case_schema = lambda: None
    monkeypatch.setattr(app_module.OllamaFns, "embed", lambda self, text: [0.5])
    resp = client.post("/cases", json=json.loads(record().model_dump_json()))
    assert resp.status_code == 200 and resp.json() == {"status": "stored"} and repo.saved_codes
