"""Cliente minimo de Ollama con la libreria estandar (embeddings y chat con salida estructurada)."""
import json
import os
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
    schema: Union[Dict[str, Any], str, None],
    keep_alive: str = "30m",
    timeout: float = 60,
    num_predict: int = 400,
    stats: Optional[Dict[str, int]] = None,
    num_ctx: int = 2048,
) -> str:
    """Devuelve el contenido (texto JSON) de la respuesta. Si el Ollama del servidor no acepta un
    JSON Schema como `format`, reintenta con el modo JSON simple. Si se pasa `stats`, se llena con los
    tokens y las duraciones (ms) que reporta Ollama, para ver donde se va el tiempo."""
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
        "format": schema,
        "keep_alive": keep_alive,
        "options": {"temperature": 0, "num_ctx": num_ctx, "num_predict": num_predict},
    }
    if schema is None:  # sin formato forzado (solo para diagnostico de velocidad)
        payload.pop("format")
    think = os.environ.get("ICF_LLM_THINK", "").strip().lower()  # modelos con razonamiento (Gemma 4): "false" lo apaga
    if think in ("true", "false"):
        payload["think"] = think == "true"
    num_gpu = os.environ.get("ICF_LLM_NUM_GPU", "").strip()  # "0" fuerza CPU (dimensionar equipos sin GPU)
    if num_gpu.lstrip("-").isdigit():
        payload["options"]["num_gpu"] = int(num_gpu)
    try:
        data = _post(base_url, "/api/chat", payload, timeout)
    except error.HTTPError as exc:
        if exc.code != 400 or schema == "json":
            raise
        payload["format"] = "json"
        data = _post(base_url, "/api/chat", payload, timeout)
    if stats is not None:
        for key in ("prompt_eval_count", "eval_count"):
            if key in data:
                stats[key] = int(data[key])
        for key in ("load_duration", "prompt_eval_duration", "eval_duration", "total_duration"):
            if key in data:
                stats[key.replace("duration", "ms")] = round(int(data[key]) / 1_000_000)
    return data["message"]["content"]
