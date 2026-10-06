"""Cliente minimo de Ollama con la libreria estandar (embeddings y chat con salida estructurada)."""
import json
from typing import Any, Dict, List, Optional, Union
from urllib import error, request


def _post(base_url: str, path: str, payload: Dict[str, Any], timeout: float) -> Dict[str, Any]:
    req = request.Request(
        f"{base_url.rstrip('/')}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def embed(base_url: str, model: str, text: str, keep_alive: str = "30m", timeout: float = 60) -> List[float]:
    data = _post(base_url, "/api/embed", {"model": model, "input": [text], "keep_alive": keep_alive}, timeout)
    return data["embeddings"][0]


def chat_json(
    base_url: str,
    model: str,
    messages: List[Dict[str, str]],
    schema: Union[Dict[str, Any], str],
    keep_alive: str = "30m",
    timeout: float = 60,
    num_predict: int = 400,
) -> str:
    """Devuelve el contenido (texto JSON) de la respuesta. Si el Ollama del servidor no acepta un
    JSON Schema como `format`, reintenta con el modo JSON simple."""
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
        "format": schema,
        "keep_alive": keep_alive,
        "options": {"temperature": 0, "num_ctx": 2048, "num_predict": num_predict},
    }
    try:
        data = _post(base_url, "/api/chat", payload, timeout)
    except error.HTTPError as exc:
        if exc.code != 400 or schema == "json":
            raise
        payload["format"] = "json"
        data = _post(base_url, "/api/chat", payload, timeout)
    return data["message"]["content"]
