"""Calcula con Ollama (bge-m3) el embedding de cada codigo del catalogo y lo guarda en icf_codes.embedding.

Uso (desde icf-service/), despues de `ollama pull bge-m3` y de load_catalog.py:
    python scripts/embed_catalog.py
Variables: ICF_DATABASE_URL, OLLAMA_URL (por defecto http://127.0.0.1:11434), ICF_EMBED_MODEL (por defecto bge-m3).
Es reanudable: solo procesa los codigos que aun no tienen embedding.
"""
import json
import os
import sys
from urllib import request

BATCH = 32


def embed(texts, base_url, model):
    body = json.dumps({"model": model, "input": texts}).encode("utf-8")
    req = request.Request(
        f"{base_url}/api/embed", data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    with request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))["embeddings"]


def main() -> int:
    import psycopg

    url = os.environ.get("ICF_DATABASE_URL")
    if not url:
        print("Falta la variable ICF_DATABASE_URL", file=sys.stderr)
        return 2
    base_url = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
    model = os.environ.get("ICF_EMBED_MODEL", "bge-m3")

    with psycopg.connect(url) as conn:
        rows = conn.execute(
            """SELECT c.code, c.title, p.title
               FROM icf_codes c LEFT JOIN icf_codes p ON p.code = c.parent
               WHERE c.embedding IS NULL ORDER BY c.code"""
        ).fetchall()
        print(f"{len(rows)} codigos sin embedding (modelo {model})")
        done = 0
        for i in range(0, len(rows), BATCH):
            chunk = rows[i : i + BATCH]
            # Texto del codigo: titulo, con el titulo del padre como contexto en los niveles inferiores.
            texts = [f"{title}. {parent}" if parent else title for _, title, parent in chunk]
            vectors = embed(texts, base_url, model)
            for (code, _, _), vec in zip(chunk, vectors):
                conn.execute(
                    "UPDATE icf_codes SET embedding = %s::vector WHERE code = %s",
                    ("[" + ",".join(str(x) for x in vec) + "]", code),
                )
            conn.commit()
            done += len(chunk)
            print(f"  {done}/{len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
