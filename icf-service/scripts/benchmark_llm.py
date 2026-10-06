"""Diagnostico de velocidad del paso con modelo (funciones b y estructuras s).

Usa el prompt real del motor (candidatos de la base) y lo envia a Ollama en los dos modos y en una variante
sin formato forzado. Cada una se manda dos veces: la 1.a con prompt nuevo (lo que vive un paciente real) y la
2.a identica (Ollama la reutiliza en cache). Muestra los tokens y las duraciones que reporta Ollama.

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
from icf.suggest import _patient_summary  # noqa: E402

PATIENT = PatientContext(
    age=35, cause="Accidente de transito", cat_fisica="Severa", cat_psicosocial="Moderada",
    levels={"D1": 10, "D4": 60, "D5": 55}, diag_cie="S78 Amputacion traumatica de miembro inferior",
)


def main() -> int:
    s = load_settings()
    t0 = time.perf_counter()
    vector = ollama.embed(s.ollama_url, s.embed_model, rules.clinical_query(PATIENT.diag_cie, None), s.keep_alive)
    print(f"embedding (bge-m3): {round((time.perf_counter() - t0) * 1000)} ms")
    with psycopg.connect(s.database_url, autocommit=True) as conn:
        repo = PgRepo(conn)
        t0 = time.perf_counter()
        b = repo.search("b", vector, 12, rules.body_chapters("b", PATIENT.cat_fisica, PATIENT.cat_psicosocial))
        sx = repo.search("s", vector, 12, rules.body_chapters("s", PATIENT.cat_fisica, PATIENT.cat_psicosocial))
        print(f"busqueda b y s: {round((time.perf_counter() - t0) * 1000)} ms -> modo solo similitud ~ embedding + busqueda\n")
    plan = rules.activity_plan(PATIENT.levels)

    def variant(name, b_, s_, justify, forced=True, num_predict=300, num_ctx=2048):
        msgs = llm.build_messages(_patient_summary(PATIENT, plan), b_, s_, justify)
        schema = llm.build_schema([c for c, _ in b_], [c for c, _ in s_], justify) if forced else None
        for attempt in (1, 2):
            stats = {}
            t = time.perf_counter()
            ollama.chat_json(
                s.ollama_url, s.llm_model, msgs, schema, s.keep_alive, 240,
                num_predict=num_predict, stats=stats, num_ctx=num_ctx,
            )
            wall = round((time.perf_counter() - t) * 1000)
            ev = stats.get("eval_ms") or 1
            label = "nuevo" if attempt == 1 else "cache"
            print(
                f"{name:<32} {label:<5} total {wall:>6} ms | lee {stats.get('prompt_eval_count', '?'):>4} tok en {stats.get('prompt_eval_ms', '?'):>6} ms"
                f" | escribe {stats.get('eval_count', '?'):>4} tok en {stats.get('eval_ms', '?'):>6} ms"
                f" ({round(stats.get('eval_count', 0) / (ev / 1000), 1)} tok/s)"
            )

    print(f"modo configurado: {s.mode} ({s.body_candidates} candidatos, justificacion={s.justify})\n")
    variant("A rapido (6 cand., codigos)", b[:6], sx[:6], False, num_predict=120, num_ctx=1024)
    variant("B calidad (12 cand., justif.)", b, sx, True)
    variant("C 12 cand., solo codigos", b, sx, False, num_predict=120)
    variant("D calidad sin formato forzado", b, sx, True, forced=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
