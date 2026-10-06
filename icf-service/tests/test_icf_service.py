from pathlib import Path

import pytest

from icf.catalog import level_of, parent_of, parse_catalog, validate
from icf.domain_map import (
    ANNEX_CANDIDATES,
    HAB_DOMAINS,
    chapters_to_review,
    hab_domain_of,
    qualifier_from_level,
)

REAL_CATALOG = Path(__file__).resolve().parents[2] / "data" / "private" / "icf" / "catalog_cifia.tsv"

HEADER = '"Code"\t"Level"\t"Component"\t"Parent"\t"Title"\t"Source"\n'


def _write(tmp_path, lines):
    p = tmp_path / "cat.tsv"
    p.write_text(HEADER + "".join(lines), encoding="utf-8")
    return p


def test_level_and_parent():
    assert level_of("d450") == 2
    assert level_of("d4500") == 3
    assert level_of("d53000") == 4
    assert parent_of("d450") is None
    assert parent_of("d4500") == "d450"
    assert parent_of("d53000") == "d5300"


def test_parse_and_validate_ok(tmp_path):
    p = _write(tmp_path, [
        '"d450"\t"2"\t"d"\t""\t"Andar"\t"ocr"\n',
        '"d4500"\t"3"\t"d"\t"d450"\t"Andar distancias cortas"\t"ocr"\n',
    ])
    codes = parse_catalog(p)
    assert [c.code for c in codes] == ["d450", "d4500"]
    assert codes[1].chapter == 4 and codes[1].parent == "d450"
    assert validate(codes) == []


def test_validate_detects_orphan_and_bad_code(tmp_path):
    p = _write(tmp_path, [
        '"d4500"\t"3"\t"d"\t"d450"\t"Andar distancias cortas"\t"ocr"\n',
        '"x999"\t"2"\t"x"\t""\t"Malo"\t"ocr"\n',
    ])
    problems = validate(parse_catalog(p))
    assert any("huerfano" in x and "d4500" in x for x in problems)
    assert any("formato invalido" in x for x in problems)


@pytest.mark.parametrize("level,expected", [
    (0, 0), (4, 0), (5, 1), (24, 1), (25, 2), (49, 2), (50, 3), (95, 3), (96, 4), (100, 4),
])
def test_qualifier_scale(level, expected):
    assert qualifier_from_level(level) == expected


@pytest.mark.parametrize("bad", [-1, 101])
def test_qualifier_out_of_range(bad):
    with pytest.raises(ValueError):
        qualifier_from_level(bad)


def test_chapters_to_review():
    assert chapters_to_review({"D1": 70, "D2": 4, "D4": 5, "D3": 0}) == ["D1", "D4"]


def test_hab_domain_of():
    assert hab_domain_of("d4501") == "D4"
    assert hab_domain_of("d161") == "D1"
    assert hab_domain_of("d750") is None
    assert hab_domain_of("b1400") is None


def test_hab_domains_cover_d1_to_d6():
    assert [d.hab_domain for d in HAB_DOMAINS] == ["D1", "D2", "D3", "D4", "D5", "D6"]
    assert [d.chapter_code for d in HAB_DOMAINS] == ["d1", "d2", "d3", "d4", "d5", "d6"]


@pytest.mark.skipif(not REAL_CATALOG.exists(), reason="catalogo local (con copyright) no disponible")
def test_real_catalog_is_consistent():
    codes = parse_catalog(REAL_CATALOG)
    by_code = {c.code: c for c in codes}
    assert len(codes) == 1593
    assert validate(codes) == []
    # Los 3 codigos sin definicion en el libro quedan fuera hasta resolverse.
    assert not {"b1125", "b239", "d341"} & set(by_code)
    # d450 siempre es "Andar" (el error del mockup que el RAG debe evitar).
    assert by_code["d450"].title == "Andar"
    # Todos los candidatos del Anexo ya confirmados existen.
    assert all(code in by_code for _, code, _ in ANNEX_CANDIDATES)
    # El perfil solo lleva b, s y d: no hay factores ambientales entre los candidatos.
    assert all(not code.startswith("e") for _, code, _ in ANNEX_CANDIDATES)


def test_annex_candidates_structure():
    assert len(ANNEX_CANDIDATES) == len({(d, c) for d, c, _ in ANNEX_CANDIDATES})
    assert {a for _, _, a in ANNEX_CANDIDATES} == {"both", "6-17", "18+"}
    assert {d for d, _, _ in ANNEX_CANDIDATES} == {
        "Cognicion", "Movilidad", "Cuidado personal", "Relaciones",
        "Actividades cotidianas", "Participacion",
    }
    by_age = {a: [c for _, c, x in ANNEX_CANDIDATES if x == a] for a in ("6-17", "18+")}
    assert by_age["6-17"] == ["d520", "d740"]
    assert by_age["18+"] == ["d7702", "d850", "d570", "d879", "d940"]
