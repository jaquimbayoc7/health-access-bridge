from fastapi.testclient import TestClient

import app as app_module

client = TestClient(app_module.app)


def test_suggest_rejects_identifying_fields():
    resp = client.post("/suggest", json={"age": 30, "nombre_apellidos": "Juan Perez"})
    assert resp.status_code == 422


def test_suggest_rejects_invalid_level():
    resp = client.post("/suggest", json={"age": 30, "levels": {"D1": 500}})
    assert resp.status_code == 422


def test_suggest_without_database_returns_503(monkeypatch):
    monkeypatch.setattr(app_module, "settings", app_module.settings.__class__(
        database_url="", ollama_url="http://127.0.0.1:1", llm_model="m", embed_model="e",
        keep_alive="1m", llm_timeout_s=1,
    ))
    resp = client.post("/suggest", json={"age": 30, "levels": {"D4": 60}})
    assert resp.status_code == 503
