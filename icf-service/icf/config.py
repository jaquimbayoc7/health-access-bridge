"""Configuracion del servicio por variables de entorno.

ICF_MODE:
  calidad (por defecto): 12 candidatos por componente y justificacion corta del modelo; ~40 s.
  rapido:                6 candidatos y solo codigos; ~20 s.
Cada valor se puede forzar con ICF_BODY_CANDIDATES, ICF_LLM_JUSTIFY y ICF_LLM_NUM_PREDICT.
"""
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str
    ollama_url: str
    llm_model: str
    embed_model: str
    keep_alive: str
    llm_timeout_s: float
    mode: str = "calidad"
    body_candidates: int = 12
    justify: bool = True
    num_predict: int = 300
    num_ctx: int = 2048
    use_llm: bool = True  # False: funciones y estructuras solo por similitud (sin modelo de generacion)


def _flag(value: str) -> bool:
    return value.strip().lower() not in ("0", "false", "no", "")


def load_settings() -> Settings:
    mode = os.environ.get("ICF_MODE", "calidad").strip().lower()
    fast = mode == "rapido"
    return Settings(
        database_url=os.environ.get("ICF_DATABASE_URL", ""),
        ollama_url=os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/"),
        llm_model=os.environ.get("ICF_LLM_MODEL", "qwen2.5:3b"),
        embed_model=os.environ.get("ICF_EMBED_MODEL", "bge-m3"),
        keep_alive=os.environ.get("ICF_LLM_KEEP_ALIVE", "30m"),
        llm_timeout_s=float(os.environ.get("ICF_SERVICE_LLM_TIMEOUT_S", "120")),
        mode="rapido" if fast else "calidad",
        body_candidates=int(os.environ.get("ICF_BODY_CANDIDATES", "6" if fast else "12")),
        justify=_flag(os.environ.get("ICF_LLM_JUSTIFY", "false" if fast else "true")),
        num_predict=int(os.environ.get("ICF_LLM_NUM_PREDICT", "120" if fast else "300")),
        num_ctx=int(os.environ.get("ICF_LLM_NUM_CTX", "1024" if fast else "2048")),
        use_llm=_flag(os.environ.get("ICF_USE_LLM", "true")),
    )
