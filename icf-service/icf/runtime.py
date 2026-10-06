"""Funciones de embeddings y chat sobre Ollama, con las estadisticas de la ultima llamada.
Se crea una instancia por peticion; la usan el servicio (app.py) y la evaluacion (scripts/evaluate.py)."""
from typing import Dict, List, Sequence

from . import ollama
from .config import Settings


class OllamaFns:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.stats: Dict[str, int] = {}

    def embed(self, text: str) -> Sequence[float]:
        s = self.settings
        return ollama.embed(s.ollama_url, s.embed_model, text, s.keep_alive, s.llm_timeout_s)

    def chat(self, messages: List[Dict[str, str]], schema: dict) -> str:
        s = self.settings
        return ollama.chat_json(
            s.ollama_url, s.llm_model, messages, schema, s.keep_alive, s.llm_timeout_s,
            num_predict=s.num_predict, stats=self.stats, num_ctx=s.num_ctx,
        )
