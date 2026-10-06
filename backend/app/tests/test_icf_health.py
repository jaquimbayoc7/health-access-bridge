"""
HU-07a — Pruebas del diagnostico de conexion con el servidor local de IA.
El servidor real no existe en CI: se simula fetch_tags.
"""
from urllib import error

from app.services import icf_client

SECRET_URL = "https://servidor-secreto.example.ts.net"
SECRET_TOKEN = "token-super-secreto-123"


def _configure(monkeypatch):
    monkeypatch.setenv("ICF_LLM_URL", SECRET_URL)
    monkeypatch.setenv("ICF_LLM_TOKEN", SECRET_TOKEN)
    monkeypatch.setenv("ICF_LLM_MODEL", "qwen2.5:3b")


def test_icf_health_requires_auth(client):
    assert client.get("/icf/health").status_code == 401


def test_icf_health_forbidden_for_medico(client, auth_headers_medico):
    resp = client.get("/icf/health", headers=auth_headers_medico)
    assert resp.status_code == 403


def test_icf_health_not_configured(client, auth_headers_admin, monkeypatch):
    monkeypatch.delenv("ICF_LLM_URL", raising=False)
    monkeypatch.delenv("ICF_LLM_TOKEN", raising=False)
    resp = client.get("/icf/health", headers=auth_headers_admin)
    assert resp.status_code == 200
    body = resp.json()
    assert body["configured"] is False
    assert body["reachable"] is False


def test_icf_health_ok(client, auth_headers_admin, monkeypatch):
    _configure(monkeypatch)
    monkeypatch.setattr(
        icf_client, "fetch_tags",
        lambda url, token, timeout: {"models": [{"name": "qwen2.5:3b"}, {"name": "gemma4:e4b"}]},
    )
    resp = client.get("/icf/health", headers=auth_headers_admin)
    assert resp.status_code == 200
    body = resp.json()
    assert body["configured"] is True
    assert body["reachable"] is True
    assert body["model_available"] is True
    assert body["error"] is None
    assert isinstance(body["latency_ms"], int)


def test_icf_health_model_missing(client, auth_headers_admin, monkeypatch):
    _configure(monkeypatch)
    monkeypatch.setattr(
        icf_client, "fetch_tags",
        lambda url, token, timeout: {"models": [{"name": "otro:1b"}]},
    )
    body = client.get("/icf/health", headers=auth_headers_admin).json()
    assert body["reachable"] is True
    assert body["model_available"] is False
    assert "no esta instalado" in body["error"]


def test_icf_health_token_rejected(client, auth_headers_admin, monkeypatch):
    _configure(monkeypatch)

    def _raise(url, token, timeout):
        raise error.HTTPError(url, 401, "Unauthorized", {}, None)

    monkeypatch.setattr(icf_client, "fetch_tags", _raise)
    body = client.get("/icf/health", headers=auth_headers_admin).json()
    assert body["reachable"] is False
    assert "401" in body["error"]


def test_icf_health_unreachable(client, auth_headers_admin, monkeypatch):
    _configure(monkeypatch)

    def _raise(url, token, timeout):
        raise error.URLError("connection refused")

    monkeypatch.setattr(icf_client, "fetch_tags", _raise)
    body = client.get("/icf/health", headers=auth_headers_admin).json()
    assert body["reachable"] is False
    assert body["latency_ms"] is None


def test_icf_health_never_leaks_url_or_token(client, auth_headers_admin, monkeypatch):
    _configure(monkeypatch)

    def _raise(url, token, timeout):
        raise error.URLError(f"fallo contra {url} con {token}")

    monkeypatch.setattr(icf_client, "fetch_tags", _raise)
    raw = client.get("/icf/health", headers=auth_headers_admin).text
    assert SECRET_TOKEN not in raw
    assert "servidor-secreto" not in raw
