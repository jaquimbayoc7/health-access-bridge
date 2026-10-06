"""Diagnostico de velocidad: donde se va el tiempo de una sugerencia y que variante de prompt es mas rapida.

Usa el mismo prompt real del motor (candidatos de la base) y lo envia a Ollama en varias variantes,
cada una dos veces (la primera calienta el modelo). Muestra los tokens y las duraciones que reporta Ollama.

Uso (en el servidor, con las variables del .env):  python scripts/benchmark_llm.py
"""
import copy
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


def codes_only(schema):
    """Misma estructura pero b y s como listas de codigos, sin justificacion generada por el modelo."""
    out = copy.deepcopy(schema)
    for key in ("b", "s"):
        if key in out["properties"]:
            enum = out["properties"][key]["items"]["properties"]["code"]["enum"]
            out["properties"][key]["items"] = {"type": "string", "enum": enum}
    return out


def main() -> int:
    s = load_settings()
    started = time.perf_counter()
    vector = ollama.embed(s.ollama_url, s.embed_model, "Diagnostico: S78 Amputacion traumatica. Deficiencia fisica: Severa", s.keep_alive)
    print(f"embedding (bge-m3): {round((time.perf_counter() - started) * 1000)} ms\n")

    with psycopg.connect(s.database_url, autocommit=True) as conn:
        repo = PgRepo(conn)
        plan = rules.activity_plan(PATIENT.levels)
        d = []
        for ch, _, _ in plan:
            d += repo.annex_candidates([ch], "18+") or repo.chapter_codes(ch)
        b, sx = repo.search("b", vector, 8), repo.search("s", vector, 8)

    def variant(name, d_, b_, s_, schema_fn, num_ctx=2048):
        msgs = llm.build_messages(_patient_summary(PATIENT, plan), d_, b_, s_)
        schema = schema_fn(llm.build_schema([c for c, _ in d_], [c for c, _ in b_], [c for c, _ in s_]))
        for attempt in (1, 2):
            stats = {}
            t0 = time.perf_counter()
            text = ollama.chat_json(s.ollama_url, s.llm_model, msgs, schema, s.keep_alive, 180, stats=stats, num_ctx=num_ctx)
            wall = round((time.perf_counter() - t0) * 1000)
            ev = stats.get("eval_ms") or 1
            # 1.a llamada = prompt nuevo (lo que ve un paciente real); 2.a = Ollama reutiliza el prompt en cache.
            label = "nuevo" if attempt == 1 else "cache"
            print(
                f"{name:<34} {label:<5} total {wall:>6} ms | lee {stats.get('prompt_eval_count', '?'):>4} tok en {stats.get('prompt_eval_ms', '?'):>6} ms"
                f" | escribe {stats.get('eval_count', '?'):>4} tok en {stats.get('eval_ms', '?'):>6} ms"
                f" ({round(stats.get('eval_count', 0) / (ev / 1000), 1)} tok/s) | carga {stats.get('load_ms', '?')} ms"
            )
            if attempt == 2:
                return text

    ident = lambda sc: sc  # noqa: E731
    print(f"candidatos: d={len(d)} b={len(b)} s={len(sx)}\n")
    variant("A actual (schema, con justificacion)", d, b, sx, ident)
    variant("B formato json simple", d, b, sx, lambda sc: "json")
    variant("C schema, b/s solo codigos", d, b, sx, codes_only)
    variant("D C + 5 candidatos por lista", d[:5], b[:5], sx[:5], codes_only)
    variant("E C + contexto 1024", d, b, sx, codes_only, num_ctx=1024)
    variant("F sin formato forzado", d, b, sx, lambda sc: None)

    # Linea base del servidor: prompt minimo (el mismo de la prueba del 05-oct: 4,1 s).
    stats = {}
    for _ in (1, 2):
        stats = {}
        ollama.chat_json(
            s.ollama_url, s.llm_model, [{"role": "user", "content": "Responde solo JSON con campo ok true."}],
            {"type": "object", "properties": {"ok": {"type": "boolean"}}, "required": ["ok"]}, s.keep_alive, 120, stats=stats,
        )
    print(f"\nlinea base (prompt minimo): total {stats.get('total_ms')} ms | salida {stats.get('eval_count')} tok en {stats.get('eval_ms')} ms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
