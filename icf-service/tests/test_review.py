"""Pruebas de la logica de validacion clinica (HU-07g) y del Excel de la revisora."""
import importlib.util
import sys
from pathlib import Path

import pytest

from icf.review import (
    THRESHOLDS,
    compute_metrics,
    evaluate_thresholds,
    normalize_codes,
    normalize_rating,
    normalize_yes_no,
)

ROOT = Path(__file__).resolve().parents[1]


def test_normalize_codes_accepts_free_text_and_collapses_to_three_digits():
    assert normalize_codes("b730, B7301 y s750; d450") == {"b730", "s750", "d450"}
    assert normalize_codes("b 730") == {"b730"}
    assert normalize_codes(None) == set()
    assert normalize_codes("sin codigos") == set()


def test_rating_and_yes_no_normalization():
    assert normalize_rating(" Adecuado ") == "A"
    assert normalize_rating("aceptable") == "B"
    assert normalize_rating("No adecuado") == "C"
    assert normalize_rating("") is None and normalize_rating(None) is None
    assert normalize_yes_no("Sí") == 1.0 and normalize_yes_no("si") == 1.0
    assert normalize_yes_no("Parcial") == 0.5 and normalize_yes_no("No") == 0.0
    assert normalize_yes_no(None) is None


def _rows(spec):
    return [{"case": c, "component": comp, "code": code, "rating": r, "qualifier_ok": q} for c, comp, code, r, q in spec]


def test_metrics_precision_coverage_and_blind_recall():
    ratings = _rows([
        ("C01", "b", "b730", "A", 1.0),
        ("C01", "b", "b735", "B", 0.5),
        ("C01", "s", "s750", "C", 0.0),
        ("C02", "b", "b152", "A", 1.0),
        ("C02", "d", "d450", "A", 1.0),
        ("C02", "d", "d510", "C", None),
    ])
    missing = {"C01": {"b": {"b770"}, "s": set()}, "C02": {"b": set(), "s": set()}}
    blind = {"C01": {"b": {"b730", "b770"}, "s": {"s750"}}, "C02": {"b": {"b152"}, "s": set()}}
    suggested = {"C01": {"b": {"b730", "b735"}, "s": {"s750"}}, "C02": {"b": {"b152"}}}
    m = compute_metrics(ratings, missing, blind, suggested)

    assert m["cases_reviewed"] == 2
    b = m["components"]["b"]
    assert (b["adecuado"], b["aceptable"], b["no_adecuado"]) == (2, 1, 0)
    assert b["precision_strict"] == pytest.approx(0.667, abs=1e-3)
    assert b["precision_lenient"] == 1.0
    assert b["missing_codes"] == 1
    assert b["coverage"] == 0.75  # 3 buenos de 3 + 1 faltante
    assert m["components"]["d"]["precision_lenient"] == 0.5
    # a ciegas: eligio b730, b770, s750, b152 (4); la sugerencia tenia b730, s750, b152 (3)
    assert m["blind"]["expected_codes"] == 4 and m["blind"]["found_in_suggestion"] == 3
    assert m["blind"]["recall"] == 0.75
    # b+s: 4 valorados (A, B, C, A), 2 adecuados, 1 aceptable
    assert m["body"]["precision_strict"] == 0.5 and m["body"]["precision_lenient"] == 0.75


def test_verdict_cumple_no_cumple_e_incompleto():
    empty = compute_metrics([], {}, {}, {})
    assert evaluate_thresholds(empty)["veredicto"] == "INCOMPLETO"

    good = _rows([("C%02d" % i, comp, f"{comp}7{i:02d}", "A", 1.0) for i in range(1, 25) for comp in ("b", "s", "d")])
    blind = {"C%02d" % i: {"b": {f"b7{i:02d}"}, "s": {f"s7{i:02d}"}} for i in range(1, 25)}
    sug = {"C%02d" % i: {"b": {f"b7{i:02d}"}, "s": {f"s7{i:02d}"}, "d": {f"d7{i:02d}"}} for i in range(1, 25)}
    ok = evaluate_thresholds(compute_metrics(good, {}, blind, sug))
    assert ok["veredicto"] == "CUMPLE"

    bad = _rows([("C%02d" % i, comp, f"{comp}7{i:02d}", "C", 0.0) for i in range(1, 25) for comp in ("b", "s", "d")])
    no = evaluate_thresholds(compute_metrics(bad, {}, blind, sug))
    assert no["veredicto"] == "NO CUMPLE"
    assert THRESHOLDS["body_precision_strict"] < THRESHOLDS["body_precision_lenient"]


def test_excel_roundtrip_reads_what_the_reviewer_fills(tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    path = tmp_path / "hoja.xlsx"
    wb = openpyxl.Workbook()
    wb.active.title = "Instrucciones"
    wa = wb.create_sheet("Fase A (a ciegas)")
    wa.append(["Caso"] + [""] * 9 + ["b", "s", "c"])
    wa.append(["C02"] + [""] * 9 + ["b730, b735", "s110", ""])
    wbs = wb.create_sheet("Fase B (sugerencias)")
    wbs.append(["Caso", "Componente", "Código", "Título", "Calificador", "Origen", "Justificación", "Valoración", "¿Calificador correcto?", "Comentario"])
    wbs.append(["C02", "Función (b)", "b730", "Fuerza muscular", 3, "llm", "x", "Adecuado", "Sí", None])
    wbs.append(["C02", "Estructura (s)", "s110", "Cerebro", "3.88", "llm", "", "No adecuado", "No", None])
    wm = wb.create_sheet("Faltantes")
    wm.append(["Caso", "b", "s", "d", "c"])
    wm.append(["C02", "b770", None, None, None])
    wb.save(path)

    spec = importlib.util.spec_from_file_location("review_sheet", ROOT / "scripts" / "review_sheet.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["review_sheet"] = module
    spec.loader.exec_module(module)
    ratings, missing, blind, suggested = module.read_filled(path)

    assert [(r["code"], r["rating"], r["qualifier_ok"]) for r in ratings] == [("b730", "A", 1.0), ("s110", "C", 0.0)]
    assert blind["C02"] == {"b": {"b730", "b735"}, "s": {"s110"}}
    assert missing["C02"]["b"] == {"b770"}
    assert suggested["C02"] == {"b": {"b730"}, "s": {"s110"}}
