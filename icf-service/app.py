"""Servicio ICF local (HU-07b): POST /suggest y GET /health. Escucha solo en 127.0.0.1; el acceso
desde internet pasa por Caddy (token) y Tailscale Funnel."""
import logging

import psycopg
from fastapi import FastAPI, HTTPException

from icf.config import load_settings
from icf.repository import PgRepo
from icf.runtime import OllamaFns
from icf.schemas import PatientContext, SuggestionResult
from icf.suggest import suggest

logger = logging.getLogger("icf-service")
settings = load_settings()
app = FastAPI(title="HAB ICF service", version="0.1.0")


def _connect():
    if not settings.database_url:
        raise HTTPException(status_code=503, detail="ICF_DATABASE_URL sin configurar")
    try:
        return psycopg.connect(settings.database_url, autocommit=True, connect_timeout=5)
    except psycopg.Error as exc:
        logger.error("No se pudo conectar a la base: %s", type(exc).__name__)
        raise HTTPException(status_code=503, detail="Base de datos no disponible") from exc


@app.get("/health")
def health():
    with _connect() as conn:
        total, with_vector = conn.execute("SELECT count(*), count(embedding) FROM icf_codes").fetchone()
    return {
        "status": "ok",
        "codes": total,
        "codes_with_embedding": with_vector,
        "llm_model": settings.llm_model,
        "embed_model": settings.embed_model,
    }


@app.post("/suggest", response_model=SuggestionResult)
def post_suggest(patient: PatientContext):
    fns = OllamaFns(settings)
    with _connect() as conn:
        return suggest(patient, PgRepo(conn), fns.embed, fns.chat, settings.llm_model, stats=fns.stats)
