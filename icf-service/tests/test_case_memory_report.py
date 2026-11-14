"""HU-07j - informe de acuerdo de la memoria de casos (scripts/case_memory_report.py)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import case_memory_report as report  # noqa: E402


def rows(pairs, case="c"):
    # (case_key, componente, sugerida, confirmada, estado)
    return [(f"{case}{i % 4}", "b", s, q, "aceptado" if s == q else "editado") for i, (s, q) in enumerate(pairs)]


def test_perfect_agreement_when_the_doctor_accepts_everything():
    data = rows([(2, 2), (3, 3), (1, 1), (4, 4), (2, 2), (3, 3)])
    out = report.agreement(data, min_pairs=5)
    assert out["pairs"] == 6 and out["exact"] == 1.0 and out["within_one"] == 1.0
    assert out["changed_by_doctor"] == 0 and out["weighted_kappa"] == 1.0 and out["conclusive"] is True
    assert "Cota superior" in out["note"]


def test_counts_changes_and_distributions():
    data = rows([(3, 4), (3, 4), (3, 3), (2, 2), (2, 3), (3, 3), (1, 1), (4, 4)])
    out = report.agreement(data, min_pairs=5)
    assert out["changed_by_doctor"] == 3 and out["changed_rate"] == 0.375
    assert out["exact"] == 0.625 and out["within_one"] == 1.0
    assert out["suggested_distribution"] == {1: 1, 2: 2, 3: 4, 4: 1}
    assert out["confirmed_distribution"] == {1: 1, 2: 1, 3: 3, 4: 3}
    assert 0 < out["weighted_kappa"] < 1


def test_few_pairs_is_inconclusive_and_says_so():
    out = report.agreement(rows([(2, 3), (3, 3)]))
    assert out["conclusive"] is False and "no es concluyente" in out["warning"]


def test_only_functions_and_structures_count_and_empty_is_safe():
    data = [("c1", "d", 3, 3, "aceptado"), ("c1", "s", 3, 4, "editado")]
    out = report.agreement(data, min_pairs=1)
    assert out["pairs"] == 1 and out["changed_by_doctor"] == 1
    empty = report.agreement([])
    assert empty["pairs"] == 0 and empty["weighted_kappa"] is None and empty["exact"] is None


def test_main_needs_the_database_url(monkeypatch, capsys):
    monkeypatch.delenv("ICF_DATABASE_URL", raising=False)
    assert report.main([]) == 2
    assert "ICF_DATABASE_URL" in capsys.readouterr().err
