"""El cliente de Ollama frente a un servidor HTTP falso (sin Ollama real)."""
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from icf import ollama


@pytest.fixture
def fake_ollama():
    calls = []
    state = {"reject_schema": False}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            calls.append((self.path, body))
            if self.path == "/api/chat" and state["reject_schema"] and isinstance(body["format"], dict):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error":"invalid format"}')
                return
            payload = (
                {"embeddings": [[0.5, 0.25]]}
                if self.path == "/api/embed"
                else {"message": {"content": '{"d": ["d450"]}'}}
            )
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode())

    server = HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_port}", calls, state
    server.shutdown()


def test_embed_sends_model_and_returns_vector(fake_ollama):
    url, calls, _ = fake_ollama
    assert ollama.embed(url, "bge-m3", "texto", "30m") == [0.5, 0.25]
    path, body = calls[0]
    assert path == "/api/embed" and body["model"] == "bge-m3" and body["input"] == ["texto"]
    assert body["keep_alive"] == "30m"


def test_chat_uses_schema_and_deterministic_options(fake_ollama):
    url, calls, _ = fake_ollama
    schema = {"type": "object", "properties": {"d": {"type": "array"}}}
    out = ollama.chat_json(url, "qwen2.5:3b", [{"role": "user", "content": "hola"}], schema)
    assert json.loads(out) == {"d": ["d450"]}
    _, body = calls[0]
    assert body["format"] == schema and body["stream"] is False
    assert body["options"]["temperature"] == 0


def test_chat_retries_with_plain_json_when_schema_is_rejected(fake_ollama):
    url, calls, state = fake_ollama
    state["reject_schema"] = True
    out = ollama.chat_json(url, "qwen2.5:3b", [{"role": "user", "content": "hola"}], {"type": "object"})
    assert json.loads(out) == {"d": ["d450"]}
    assert [c[1]["format"] for c in calls] == [{"type": "object"}, "json"]
