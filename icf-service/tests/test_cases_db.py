"""HU-07j - prueba de integracion de la memoria de casos contra PostgreSQL + pgvector reales.

Se omite si no hay base de pruebas (no necesita el catalogo de la OMS). Uso:
    ICF_TEST_DATABASE_URL=postgresql://user:pw@host:5432/db pytest tests/test_cases_db.py
"""
import os
from pathlib import Path

import pytest

from icf.cases import store_case
from icf.repository import PgRepo
from icf.schemas import CaseRecord, PatientContext

URL = os.environ.get("ICF_TEST_DATABASE_URL")
SQL = Path(__file__).resolve().parents[1] / "sql"
pytestmark = pytest.mark.skipif(not URL, reason="sin base de pruebas")

DIM = 1024


def vec(*head):
    return [*head] + [0.0] * (DIM - len(head))


@pytest.fixture()
def repo():
    import psycopg

    conn = psycopg.connect(URL, autocommit=True)
    conn.execute("DROP TABLE IF EXISTS icf_case_codes, icf_cases CASCADE")
    conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
    repo = PgRepo(conn)
    repo.ensure_case_schema()
    repo.ensure_case_schema()  # idempotente
    yield repo
    conn.execute("DROP TABLE IF EXISTS icf_case_codes, icf_cases CASCADE")
    conn.close()


def record(key="aaaaaaaa-1", ref=1, code="b730", component="b", status="aceptado", justification="Debilidad", **over):
    patient = PatientContext(age=40, cause="Accidente de transito", cat_fisica="Severa", cat_psicosocial="Leve",
                             levels={"D4": 60}, diag_cie="S14 Traumatismo medular", clinical_notes="Tetraparesia")
    return CaseRecord(case_key=key, item_ref=ref, component=component, code=code, status=status, qualifier=4,
                      qualifier_suggested=3, justification=justification, patient=patient, **over)


def test_store_search_update_and_remove(repo):
    assert store_case(record(), repo, lambda text: vec(1.0)) == "stored"
    assert store_case(record(ref=2, code="b760"), repo, lambda text: pytest.fail("no debe vectorizar de nuevo")) == "stored"
    assert store_case(record(key="bbbbbbbb-2", ref=3, code="s750", component="s"), repo, lambda text: vec(0.0, 1.0)) == "stored"

    found = repo.similar_cases(vec(1.0), limit=3, min_similarity=0.8)
    assert [c["case_key"] for c in found] == ["aaaaaaaa-1"]  # el otro caso es ortogonal
    assert found[0]["similarity"] == pytest.approx(1.0) and found[0]["diag"] == "Traumatismo medular"
    assert [c["code"] for c in found[0]["codes"]] == ["b730", "b760"]
    assert found[0]["codes"][0]["qualifier"] == 4 and found[0]["codes"][0]["justification"] == "Debilidad"

    assert len(repo.similar_cases(vec(1.0, 1.0), limit=3, min_similarity=0.5)) == 2
    assert repo.similar_cases(vec(1.0), limit=3, min_similarity=1.1) == []

    # volver a decidir el mismo codigo lo actualiza, no lo duplica
    store_case(record(status="editado", justification="Cambio"), repo, lambda text: vec(1.0))
    codes = repo.similar_cases(vec(1.0), 3, 0.8)[0]["codes"]
    assert [c["code"] for c in codes] == ["b730", "b760"] and codes[0]["justification"] == "Cambio"

    # rechazar retira el codigo; sin codigos el caso se borra
    assert store_case(record(status="rechazado"), repo, embed_fn=lambda t: vec(1.0)) == "removed"
    assert [c["code"] for c in repo.similar_cases(vec(1.0), 3, 0.8)[0]["codes"]] == ["b760"]
    store_case(record(ref=2, code="b760", status="rechazado"), repo, lambda t: vec(1.0))
    assert repo.similar_cases(vec(1.0), 3, 0.8) == []


def test_similar_cases_without_tables_returns_empty():
    import psycopg

    conn = psycopg.connect(URL, autocommit=True)
    conn.execute("DROP TABLE IF EXISTS icf_case_codes, icf_cases CASCADE")
    try:
        assert PgRepo(conn).similar_cases(vec(1.0), 3, 0.8) == []
    finally:
        conn.close()
