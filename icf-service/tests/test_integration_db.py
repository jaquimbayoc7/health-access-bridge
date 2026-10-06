"""Prueba de integracion contra PostgreSQL + pgvector reales.

Se omite si no hay base de pruebas. Uso:
    ICF_TEST_DATABASE_URL=postgresql://user:pw@host:5432/db pytest tests/test_integration_db.py
Los embeddings son aleatorios (solo se valida el SQL y el flujo, no la calidad semantica).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

URL = os.environ.get("ICF_TEST_DATABASE_URL")
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT.parent / "data" / "private" / "icf" / "catalog_cifia.tsv"

pytestmark = pytest.mark.skipif(
    not URL or not CATALOG.exists(), reason="sin base de pruebas o sin catalogo local"
)


@pytest.fixture(scope="module")
def conn():
    import psycopg

    env = dict(os.environ, ICF_DATABASE_URL=URL)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "load_catalog.py")], env=env, check=True, cwd=ROOT)
    c = psycopg.connect(URL, autocommit=True)
    c.execute(
        "UPDATE icf_codes SET embedding = (SELECT array_agg(random())::vector FROM generate_series(1, 1024)) "
        "WHERE embedding IS NULL"
    )
    yield c
    c.close()


def test_annex_candidates_by_chapter_and_age(conn):
    from icf.repository import PgRepo

    repo = PgRepo(conn)
    d4 = dict(repo.annex_candidates([4], "18+"))
    assert set(d4) == {"d4154", "d4104", "d4600", "d4602", "d4501"}
    assert d4["d4501"] == "Andar distancias largas"
    d4_young = repo.annex_candidates([4], "6-17")
    assert {c for c, _ in d4_young} == set(d4)
    # d520 solo esta en la tabla de 6-17; d7702 y d850 solo en la de 18+
    d5_young = {c for c, _ in repo.annex_candidates([5], "6-17")}
    d5_adult = {c for c, _ in repo.annex_candidates([5], "18+")}
    assert "d520" in d5_young and "d520" not in d5_adult
    # D2 no tiene candidatos del Anexo: se usa el capitulo
    assert repo.annex_candidates([2], "18+") == []
    assert {c for c, _ in repo.chapter_codes(2)} >= {"d210", "d220"}


def test_vector_search_respects_component_and_level(conn):
    from icf.repository import PgRepo

    repo = PgRepo(conn)
    for component in ("b", "s"):
        found = repo.search(component, [0.01] * 1024, 8)
        assert len(found) == 8
        assert all(code.startswith(component) and len(code) in (4, 5) for code, _ in found)


def test_full_flow_with_real_database(conn):
    from icf.repository import PgRepo
    from icf.schemas import PatientContext
    from icf.suggest import suggest

    def fake_chat(messages, schema):
        # elige el primer codigo permitido de cada lista: valida el esquema generado desde la base
        out = {}
        for key, spec in schema["properties"].items():
            if key == "d":
                out["d"] = spec["items"]["enum"][:2]
            else:
                out[key] = [{"code": spec["items"]["properties"]["code"]["enum"][0], "justificacion": "prueba"}]
        return json.dumps(out)

    patient = PatientContext(
        age=40, cat_fisica="Severa", cat_psicosocial="Moderada",
        levels={"D1": 30, "D2": 20, "D4": 70, "D5": 55},
        diag_cie="G80.9 Paralisis cerebral",
    )
    res = suggest(patient, PgRepo(conn), lambda t: [0.01] * 1024, fake_chat, "qwen2.5:3b")
    assert res.llm_used and res.activities and res.functions and res.structures
    known = {r[0] for r in conn.execute("SELECT code FROM icf_codes").fetchall()}
    for item in res.activities + res.functions + res.structures:
        assert item.code in known and item.title
    assert all(1 <= a.qualifier <= 4 for a in res.activities)
