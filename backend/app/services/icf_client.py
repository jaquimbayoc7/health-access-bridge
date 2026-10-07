# app/services/icf_client.py
"""
Cliente HTTP hacia el servidor local de IA (Ollama detras de Caddy + Tailscale Funnel).

HU-07a: verificacion de conectividad. HU-07c: llamada de sugerencia (POST /suggest del servicio ICF).
Se usa urllib de la libreria estandar para no agregar dependencias al despliegue.
Nunca se devuelve ni se registra la URL completa ni el token.
"""
import json
import os
import time
from typing import Any, Dict, Optional
from urllib import error, request

DEFAULT_MODEL = "gemma4:e4b"  # minimo viable provisional (HU-07f)
DEFAULT_TIMEOUT_S = 20.0  # diagnostico de conexion
DEFAULT_SUGGEST_TIMEOUT_S = 90.0  # una sugerencia: ~3 s con GPU, ~15 s solo CPU; con holgura para la carga del modelo


def _config() -> Dict[str, Any]:
    try:
        timeout = float(os.getenv("ICF_LLM_TIMEOUT_S", str(DEFAULT_TIMEOUT_S)))
    except ValueError:
        timeout = DEFAULT_TIMEOUT_S
    try:
        suggest_timeout = float(os.getenv("ICF_SUGGEST_TIMEOUT_S", str(DEFAULT_SUGGEST_TIMEOUT_S)))
    except ValueError:
        suggest_timeout = DEFAULT_SUGGEST_TIMEOUT_S
    return {
        "url": os.getenv("ICF_LLM_URL", "").strip().rstrip("/"),
        "token": os.getenv("ICF_LLM_TOKEN", "").strip(),
        "model": os.getenv("ICF_LLM_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL,
        "timeout": timeout,
        "suggest_timeout": suggest_timeout,
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


class IcfServiceError(Exception):
    """El servicio ICF no esta disponible o respondio algo inutilizable. El mensaje es seguro para el cliente."""


def build_patient_context(patient: Any, diag_cie: Optional[str], clinical_notes: Optional[str]) -> Dict[str, Any]:
    """Arma lo unico que viaja al servicio ICF. NUNCA incluye nombre, documento ni orientacion sexual:
    se construye campo por campo (lista blanca), no se copia el paciente."""
    levels = {f"D{i}": getattr(patient, f"nivel_d{i}") for i in range(1, 7) if getattr(patient, f"nivel_d{i}") is not None}
    context: Dict[str, Any] = {
        "age": patient.edad,
        "gender": patient.genero,
        "cause": patient.causa_deficiencia,
        "cat_fisica": patient.cat_fisica,
        "cat_psicosocial": patient.cat_psicosocial,
        "levels": levels,
        "prediction_description": patient.prediction_description,
        "diag_cie": (diag_cie or "").strip() or None,
        "clinical_notes": (clinical_notes or "").strip() or None,
    }
    return {key: value for key, value in context.items() if value is not None}


def post_suggest(url: str, token: str, payload: Dict[str, Any], timeout: float) -> Dict[str, Any]:
    """POST {url}/suggest con el token Bearer. Lanza la excepcion de urllib si falla."""
    req = request.Request(
        f"{url}/suggest",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def request_suggestion(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Pide la sugerencia al servicio ICF. Cualquier fallo se convierte en IcfServiceError con un mensaje
    generico: nunca se devuelve la URL ni el token."""
    cfg = _config()
    if not (cfg["url"] and cfg["token"]):
        raise IcfServiceError("El servicio de sugerencias ICF no esta configurado")
    try:
        data = post_suggest(cfg["url"], cfg["token"], payload, cfg["suggest_timeout"])
    except error.HTTPError as exc:
        hint = " (acceso rechazado)" if exc.code in (401, 403) else ""
        raise IcfServiceError(f"El servicio de sugerencias respondio HTTP {exc.code}{hint}") from None
    except (error.URLError, TimeoutError, OSError):
        raise IcfServiceError("El servicio de sugerencias no esta disponible en este momento") from None
    except ValueError:
        raise IcfServiceError("El servicio de sugerencias devolvio una respuesta no valida") from None
    if not isinstance(data, dict):
        raise IcfServiceError("El servicio de sugerencias devolvio una respuesta no valida")
    return data


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
