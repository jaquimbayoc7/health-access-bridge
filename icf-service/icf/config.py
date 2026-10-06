"""Configuracion del servicio por variables de entorno."""
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
    num_predict: int = 120
    num_ctx: int = 1024
    use_llm: bool = True  # False: funciones y estructuras solo por similitud (sin modelo de generacion)


def load_settings() -> Settings:
    return Settings(
        database_url=os.environ.get("ICF_DATABASE_URL", ""),
        ollama_url=os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/"),
        llm_model=os.environ.get("ICF_LLM_MODEL", "qwen2.5:3b"),
        embed_model=os.environ.get("ICF_EMBED_MODEL", "bge-m3"),
        keep_alive=os.environ.get("ICF_LLM_KEEP_ALIVE", "30m"),
        llm_timeout_s=float(os.environ.get("ICF_SERVICE_LLM_TIMEOUT_S", "90")),
        num_predict=int(os.environ.get("ICF_LLM_NUM_PREDICT", "120")),
        num_ctx=int(os.environ.get("ICF_LLM_NUM_CTX", "1024")),
        use_llm=os.environ.get("ICF_USE_LLM", "true").strip().lower() not in ("0", "false", "no"),
    )
