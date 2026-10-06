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


def load_settings() -> Settings:
    return Settings(
        database_url=os.environ.get("ICF_DATABASE_URL", ""),
        ollama_url=os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/"),
        llm_model=os.environ.get("ICF_LLM_MODEL", "qwen2.5:3b"),
        embed_model=os.environ.get("ICF_EMBED_MODEL", "bge-m3"),
        keep_alive=os.environ.get("ICF_LLM_KEEP_ALIVE", "30m"),
        llm_timeout_s=float(os.environ.get("ICF_SERVICE_LLM_TIMEOUT_S", "90")),
    )
