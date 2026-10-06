# app/services/icf_client.py
"""
Cliente HTTP hacia el servidor local de IA (Ollama detras de Caddy + Tailscale Funnel).

HU-07a: solo verificacion de conectividad. La llamada de sugerencia llega en HU-07c.
Se usa urllib de la libreria estandar para no agregar dependencias al despliegue.
Nunca se devuelve ni se registra la URL completa ni el token.
"""
import json
import os
import time
from typing import Any, Dict
from urllib import error, request

DEFAULT_MODEL = "qwen2.5:3b"
DEFAULT_TIMEOUT_S = 20.0


def _config() -> Dict[str, Any]:
    try:
        timeout = float(os.getenv("ICF_LLM_TIMEOUT_S", str(DEFAULT_TIMEOUT_S)))
    except ValueError:
        timeout = DEFAULT_TIMEOUT_S
    return {
        "url": os.getenv("ICF_LLM_URL", "").strip().rstrip("/"),
        "token": os.getenv("ICF_LLM_TOKEN", "").strip(),
        "model": os.getenv("ICF_LLM_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL,
        "timeout": timeout,
    }


def fetch_tags(url: str, token: str, timeout: float) -> Dict[str, Any]:
    """GET {url}/api/tags con el token Bearer. Lanza la excepcion de urllib si falla."""
    req = request.Request(
        f"{url}/api/tags",
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    with request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def check_health() -> Dict[str, Any]:
    """Comprueba que el servidor local responde, que el token es valido y que el modelo existe."""
    cfg = _config()
    result: Dict[str, Any] = {
        "configured": bool(cfg["url"] and cfg["token"]),
        "reachable": False,
        "model": cfg["model"],
        "model_available": False,
        "latency_ms": None,
        "error": None,
    }
    if not result["configured"]:
        result["error"] = "ICF_LLM_URL o ICF_LLM_TOKEN sin configurar"
        return result

    start = time.perf_counter()
    try:
        data = fetch_tags(cfg["url"], cfg["token"], cfg["timeout"])
    except error.HTTPError as exc:
        hint = " (token rechazado)" if exc.code in (401, 403) else ""
        result["error"] = f"El servidor respondio HTTP {exc.code}{hint}"
        return result
    except (error.URLError, TimeoutError, OSError, ValueError) as exc:
        result["error"] = f"No se pudo conectar con el servidor ({type(exc).__name__})"
        return result

    result["latency_ms"] = round((time.perf_counter() - start) * 1000)
    result["reachable"] = True
    names = [m.get("name") for m in data.get("models", []) if isinstance(m, dict)]
    result["model_available"] = cfg["model"] in names
    if not result["model_available"]:
        result["error"] = f"El modelo {cfg['model']} no esta instalado en el servidor"
    return result
