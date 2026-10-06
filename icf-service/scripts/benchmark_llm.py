"""Diagnostico de velocidad del paso con modelo (funciones b y estructuras s).

Usa el prompt real del motor (candidatos de la base) y lo envia a Ollama en varias variantes. Cada una se
manda dos veces: la 1.a con prompt nuevo (lo que vive un paciente real) y la 2.a identica (Ollama la
reutiliza en cache). Muestra los tokens y las duraciones que reporta Ollama.

Uso (en el servidor, con las variables del .env):  python scripts/benchmark_llm.py
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import psycopg  # noqa: E402

from icf import llm, ollama, rules  # noqa: E402
from icf.config import load_settings  # noqa: E402
from icf.repository import PgRepo  # noqa: E402
from icf.schemas import PatientContext  # noqa: E402
from icf.suggest import BODY_CANDIDATES, _patient_summary  # noqa: E402

PATIENT = PatientContext(
    age=35, cause="Accidente de transito", cat_fisica="Severa", cat_psicosocial="Moderada",
    levels={"D1": 10, "D4": 60, "D5": 55}, diag_cie="S78 Amputacion traumatica de miembro inferior",
)


def main() -> int:
    s = load_settings()
    t0 = time.perf_counter()
    context = rules.context_text(
        PATIENT.cause, PATIENT.cat_fisica, PATIENT.cat_psicosocial, PATIENT.diag_cie, None, ["Movilidad", "Autocuidado"]
    )
    vector = ollama.embed(s.ollama_url, s.embed_model, context, s.keep_alive)
    print(f"embedding (bge-m3): {round((time.perf_counter() - t0) * 1000)} ms")
    with psycopg.connect(s.database_url, autocommit=True) as conn:
        repo = PgRepo(conn)
        t0 = time.perf_counter()
        b, sx = repo.search("b", vector, BODY_CANDIDATES), repo.search("s", vector, BODY_CANDIDATES)
        print(f"busqueda b y s: {round((time.perf_counter() - t0) * 1000)} ms -> modo solo similitud ~ embedding + busqueda\n")
    plan = rules.activity_plan(PATIENT.levels)
    print(f"candidatos: b={len(b)} s={len(sx)} | num_ctx={s.num_ctx} num_predict={s.num_predict}\n")

    def variant(name, b_, s_, schema_fn, num_ctx=None):
        msgs = llm.build_messages(_patient_summary(PATIENT, plan), b_, s_)
        schema = schema_fn(llm.build_schema([c for c, _ in b_], [c for c, _ in s_]))
        for attempt in (1, 2):
            stats = {}
            t = time.perf_counter()
            ollama.chat_json(
                s.ollama_url, s.llm_model, msgs, schema, s.keep_alive, 180,
                num_predict=s.num_predict, stats=stats, num_ctx=num_ctx or s.num_ctx,
            )
            wall = round((time.perf_counter() - t) * 1000)
            ev = stats.get("eval_ms") or 1
            label = "nuevo" if attempt == 1 else "cache"
            print(
                f"{name:<30} {label:<5} total {wall:>6} ms | lee {stats.get('prompt_eval_count', '?'):>4} tok en {stats.get('prompt_eval_ms', '?'):>6} ms"
                f" | escribe {stats.get('eval_count', '?'):>4} tok en {stats.get('eval_ms', '?'):>6} ms"
                f" ({round(stats.get('eval_count', 0) / (ev / 1000), 1)} tok/s)"
            )

    variant("A actual (schema, codigos)", b, sx, lambda sc: sc)
    variant("B formato json simple", b, sx, lambda sc: "json")
    variant("C sin formato forzado", b, sx, lambda sc: None)
    variant("D 4 candidatos por lista", b[:4], sx[:4], lambda sc: sc)
    variant("E solo funciones (b)", b, [], lambda sc: sc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
