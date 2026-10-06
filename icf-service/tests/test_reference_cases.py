import json
from pathlib import Path

from icf.schemas import PatientContext

CASES = Path(__file__).resolve().parents[1] / "reference" / "cases.json"


HINTS = Path(__file__).resolve().parents[1] / "reference" / "retrieval_hints.json"
CATALOG = Path(__file__).resolve().parents[2] / "data" / "private" / "icf" / "catalog_cifia.tsv"


def test_retrieval_hints_match_cases_and_catalog():
    hints = json.loads(HINTS.read_text(encoding="utf-8"))["hints"]
    ids = {c["id"] for c in json.loads(CASES.read_text(encoding="utf-8"))["cases"]}
    assert set(hints) <= ids and len(hints) >= 15
    for case_id, hint in hints.items():
        assert set(hint) == {"b", "s"}
        assert all(c.startswith("b") for c in hint["b"]) and all(c.startswith("s") for c in hint["s"])
        assert hint["b"], f"{case_id} sin pistas de funciones"
    if CATALOG.exists():  # el catalogo con copyright solo existe en local
        from icf.catalog import parse_catalog

        known = {c.code for c in parse_catalog(CATALOG)}
        missing = [c for h in hints.values() for c in h["b"] + h["s"] if c not in known]
        assert not missing, f"pistas que no existen en el catalogo: {missing}"


def test_reference_cases_are_valid_and_anonymous():
    data = json.loads(CASES.read_text(encoding="utf-8"))
    cases = data["cases"]
    assert 20 <= len(cases) <= 30
    assert len({c["id"] for c in cases}) == len(cases)
    for case in cases:
        PatientContext(**case["patient"])  # lanza si hay campos no permitidos o niveles invalidos
        assert case["validated"] in (True, False)
        if case["validated"]:
            assert case["expected"], f"{case['id']} validado sin 'expected'"
    # El set cubre: menor de 6 anios, sin dificultad, y adultos mayores.
    ages = [c["patient"]["age"] for c in cases]
    assert min(ages) < 6 and max(ages) >= 70
