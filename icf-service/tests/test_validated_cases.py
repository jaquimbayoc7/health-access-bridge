"""HU-07j - carga de los casos validados por la profesional y su evaluacion dejando uno fuera."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import evaluate_memory as ev  # noqa: E402
import load_validated_cases as lv  # noqa: E402
from icf.cases import store_case  # noqa: E402

CASE = {
    "id": "N99",
    "patient": {
        "age": 40, "cause": "Accidente de transito", "cat_fisica": "Severa", "cat_psicosocial": "Leve",
        "levels": {"D4": 60}, "diag_cie": "S14 Traumatismo medular", "clinical_notes": "Tetraparesia",
    },
}


def test_records_keep_her_blind_codes_with_her_severity_and_skip_zero_and_placeholders():
    blind = {"b": ["b730", "b760", "b000"], "s": ["s110", "s750"], "d": ["d450"]}
    severity = {"b730": 4, "b760": 3, "s110": 0, "s750": 4}
    records = lv.records_for_case(CASE, blind, severity)
    assert [(r.component, r.code, r.qualifier) for r in records] == [("b", "b730", 4), ("b", "b760", 3), ("s", "s750", 4)]
    assert {r.case_key for r in records} == {"medica-N99"} and [r.item_ref for r in records] == [1, 2, 3]
    assert all(r.qualifier_suggested is None and r.status == "aceptado" for r in records)  # a ciegas: no hay sugerencia


def test_cases_without_diagnosis_or_notes_are_not_loaded():
    case = {"id": "C01", "patient": {"age": 35, "cat_fisica": "Severa", "levels": {"D4": 60}}}
    assert lv.records_for_case(case, {"b": ["b730"]}, {"b730": 3}) == []


def test_sql_writer_produces_idempotent_statements_and_escapes_quotes():
    writer = lv.SqlWriter()
    records = lv.records_for_case({**CASE, "patient": {**CASE["patient"], "clinical_notes": "Dolor d'cadera"}}, {"b": ["b730", "b760"]}, {"b730": 4, "b760": 3})
    for r in records:
        store_case(r, writer, lambda text: [0.5, 0.25])
    sql = writer.script("-- esquema")
    assert sql.startswith("BEGIN;") and sql.rstrip().endswith("COMMIT;")
    assert sql.count("INSERT INTO icf_cases") == 1  # el caso se vectoriza una sola vez
    assert sql.count("INSERT INTO icf_case_codes") == 2 and sql.count("ON CONFLICT") == 3
    assert "Dolor d''cadera" in sql and "'[0.5,0.25]'::vector" in sql


def test_leave_one_out_removes_the_evaluated_case_and_keeps_the_limit():
    class Repo:
        def similar_cases(self, embedding, limit, min_similarity):
            self.asked = (limit, min_similarity)
            return [{"case_key": k} for k in ("medica-A", "medica-B", "medica-C", "medica-D")][:limit]

        def titles(self, codes):
            return ["t"]

    repo = Repo()
    wrapped = ev.LeaveOneOut(repo, "medica-A")
    assert [c["case_key"] for c in wrapped.similar_cases([0.1], 3, 0.8)] == ["medica-B", "medica-C", "medica-D"]
    assert repo.asked == (4, 0.8)  # pide uno de mas para poder descartar el propio caso
    assert wrapped.titles(["b730"]) == ["t"]  # lo demas pasa al repositorio real


def test_summary_and_paired_delta():
    def row(exp_b, got_b, exp_s=(), got_s=(), examples=0):
        return {"expected": {"b": set(exp_b), "s": set(exp_s)}, "got": {"b": set(got_b), "s": set(got_s)}, "examples": examples}

    base = [row({"b730", "b760"}, {"b730"}, {"s110"}, {"s110"}), row({"b152"}, {"b280"}, {"s110"}, set())]
    mem = [row({"b730", "b760"}, {"b730", "b760"}, {"s110"}, {"s110"}, 1), row({"b152"}, {"b152"}, {"s110"}, set(), 2)]
    a, b = ev.summarize(base), ev.summarize(mem)
    assert (a["hits"], a["expected"], a["coverage"]) == (2, 5, 0.4) and (b["hits"], b["coverage"]) == (4, 0.8)
    assert b["with_examples"] == 2 and a["with_examples"] == 0 and b["by_component"]["b"]["suggested"] == 3
    ci = ev.paired_delta_ci(base, mem, reps=200)
    assert ci is not None and ci[0] <= 0.4 <= ci[1]
    assert ev.paired_delta_ci(base[:1], mem[:1]) is None
