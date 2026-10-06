import json
from pathlib import Path

from icf.schemas import PatientContext

CASES = Path(__file__).resolve().parents[1] / "reference" / "cases.json"


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
