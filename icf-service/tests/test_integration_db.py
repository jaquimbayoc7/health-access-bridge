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


def _start_fake_ollama():
    """Ollama simulado: embeddings fijos y un chat que respeta el esquema y reporta estadisticas."""
    import threading
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            if self.path == "/api/embed":
                payload = {"embeddings": [[0.01] * 1024]}
            else:
                fmt, content = body.get("format"), {"d": ["d4501"]}
                if isinstance(fmt, dict):
                    content = {}
                    for key, spec in fmt["properties"].items():
                        if "items" not in spec:  # esquema simple (ej. prueba minima)
                            content[key] = True
                        else:
                            content[key] = spec["items"]["enum"][:2]
                payload = {
                    "message": {"content": json.dumps(content)},
                    "prompt_eval_count": 500, "prompt_eval_duration": 2_000_000_000,
                    "eval_count": 40, "eval_duration": 4_000_000_000,
                    "load_duration": 1_000_000, "total_duration": 6_100_000_000,
                }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode())

    server = HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def _load_script(name):
    import importlib.util

    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_evaluate_and_benchmark_scripts_run_end_to_end(conn, monkeypatch, capsys):
    server = _start_fake_ollama()
    try:
        monkeypatch.setenv("ICF_DATABASE_URL", URL)
        monkeypatch.setenv("OLLAMA_URL", f"http://127.0.0.1:{server.server_port}")

        monkeypatch.setattr(sys, "argv", ["evaluate.py", "--ids", "C02,C03", "--verbose"])
        assert _load_script("evaluate").main() == 0
        out = capsys.readouterr().out
        assert "casos: 2" in out and "actividades" in out and "Andar" in out or "Permanecer" in out

        monkeypatch.setattr(sys, "argv", ["evaluate.py", "--limit", "6"])
        assert _load_script("evaluate").main() == 0
        out = capsys.readouterr().out
        assert "--- Resumen ---" in out and "JSON valido del modelo: " in out
        assert "desglose medio ms" in out and "codigos fuera del catalogo: 0" in out

        monkeypatch.setattr(sys, "argv", ["benchmark_llm.py"])
        assert _load_script("benchmark_llm").main() == 0
        out = capsys.readouterr().out
        assert "A actual" in out and "C sin formato forzado" in out and "E solo funciones" in out
        assert "nuevo" in out and "cache" in out
    finally:
        server.shutdown()


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
        # elige los dos primeros codigos permitidos de cada lista: valida el esquema generado desde la base
        return json.dumps({key: spec["items"]["enum"][:2] for key, spec in schema["properties"].items()})

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
    # d sale de la lista del Anexo (D4 y D5 para este paciente), con calificador mas alto primero
    assert res.activities[0].qualifier == 3 and res.activities[0].origin == "similarity"
    assert res.timings.keys() >= {"embed", "rank", "search", "llm"}


def test_rank_codes_orders_by_distance_and_keeps_missing_last(conn):
    from icf.repository import PgRepo

    repo = PgRepo(conn)
    conn.execute("UPDATE icf_codes SET embedding = NULL WHERE code = 'd4154'")
    conn.execute(
        "UPDATE icf_codes SET embedding = (SELECT array_agg(0.5)::vector FROM generate_series(1, 1024)) WHERE code = 'd4501'"
    )
    ranked = repo.rank_codes(["d4154", "d4600", "d4501"], [0.5] * 1024)
    assert ranked[0] == "d4501" and ranked[-1] == "d4154" and set(ranked) == {"d4154", "d4600", "d4501"}
    assert repo.rank_codes([], [0.5] * 1024) == []
