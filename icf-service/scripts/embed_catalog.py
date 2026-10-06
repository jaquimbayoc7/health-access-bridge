"""Calcula con Ollama (bge-m3) el embedding de cada codigo del catalogo y lo guarda en icf_codes.

Uso (desde icf-service/), despues de `ollama pull bge-m3` y de load_catalog.py:
    python scripts/embed_catalog.py          # embedding del titulo de todos los codigos (reanudable)
    python scripts/embed_catalog.py --rich   # embedding_rich de los codigos de nivel 2: titulo + titulos de sus hijos
Variables: ICF_DATABASE_URL, OLLAMA_URL (por defecto http://127.0.0.1:11434), ICF_EMBED_MODEL (por defecto bge-m3).
"""
import argparse
import json
import os
import sys
from urllib import request

BATCH = 32
MAX_CHILDREN = 12  # titulos de hijos que se agregan al texto enriquecido


def embed(texts, base_url, model):
    body = json.dumps({"model": model, "input": texts}).encode("utf-8")
    req = request.Request(
        f"{base_url}/api/embed", data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    with request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))["embeddings"]


def to_vector(values):
    return "[" + ",".join(str(x) for x in values) + "]"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rich", action="store_true", help="calcula embedding_rich (nivel 2, titulo + hijos)")
    args = ap.parse_args()

    import psycopg

    url = os.environ.get("ICF_DATABASE_URL")
    if not url:
        print("Falta la variable ICF_DATABASE_URL", file=sys.stderr)
        return 2
    base_url = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
    model = os.environ.get("ICF_EMBED_MODEL", "bge-m3")

    with psycopg.connect(url) as conn:
        if args.rich:
            conn.execute("ALTER TABLE icf_codes ADD COLUMN IF NOT EXISTS embedding_rich vector(1024)")
            conn.commit()
            rows = conn.execute(
                """SELECT p.code, p.title, array_remove(array_agg(c.title ORDER BY c.code), NULL)
                   FROM icf_codes p LEFT JOIN icf_codes c ON c.parent = p.code
                   WHERE p.level = 2 AND p.embedding_rich IS NULL
                   GROUP BY p.code, p.title ORDER BY p.code"""
            ).fetchall()
            items = [
                (code, f"{title}. Incluye: " + "; ".join(children[:MAX_CHILDREN]) if children else title)
                for code, title, children in rows
            ]
            column = "embedding_rich"
        else:
            rows = conn.execute(
                """SELECT c.code, c.title, p.title
                   FROM icf_codes c LEFT JOIN icf_codes p ON p.code = c.parent
                   WHERE c.embedding IS NULL ORDER BY c.code"""
            ).fetchall()
            # Titulo del codigo, con el del padre como contexto en los niveles inferiores.
            items = [(code, f"{title}. {parent}" if parent else title) for code, title, parent in rows]
            column = "embedding"
        print(f"{len(items)} codigos sin {column} (modelo {model})")
        done = 0
        for i in range(0, len(items), BATCH):
            chunk = items[i : i + BATCH]
            vectors = embed([text for _, text in chunk], base_url, model)
            for (code, _), vec in zip(chunk, vectors):
                conn.execute(f"UPDATE icf_codes SET {column} = %s::vector WHERE code = %s", (to_vector(vec), code))
            conn.commit()
            done += len(chunk)
            print(f"  {done}/{len(items)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
