"""Evalua el motor con el set de referencia (reference/cases.json) y mide calidad y latencia.

Uso (en el servidor, con ICF_DATABASE_URL y OLLAMA_URL definidos; ver README):
    python scripts/evaluate.py                      # corre todos los casos
    python scripts/evaluate.py --output informe.json

Metricas que NO necesitan validacion medica: respuestas con JSON valido del modelo, codigos fuera del
catalogo y latencia p50/p95. La precision solo se calcula en los casos con "validated": true y "expected"
(codigos esperados por componente, completados por el medico).
"""
import argparse
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import psycopg  # noqa: E402

from icf import ollama  # noqa: E402
from icf.config import load_settings  # noqa: E402
from icf.repository import PgRepo  # noqa: E402
from icf.schemas import PatientContext  # noqa: E402
from icf.suggest import suggest  # noqa: E402

DEFAULT_CASES = ROOT / "reference" / "cases.json"


def percentile(values, pct):
    ordered = sorted(values)
    if not ordered:
        return None
    index = min(len(ordered) - 1, round(pct / 100 * (len(ordered) - 1)))
    return ordered[index]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    ap.add_argument("--output", type=Path, help="guarda el informe completo en JSON")
    args = ap.parse_args()

    settings = load_settings()
    if not settings.database_url:
        print("Falta ICF_DATABASE_URL", file=sys.stderr)
        return 2
    cases = json.loads(args.cases.read_text(encoding="utf-8"))["cases"]

    def embed_fn(text):
        return ollama.embed(settings.ollama_url, settings.embed_model, text, settings.keep_alive, settings.llm_timeout_s)

    def chat_fn(messages, schema):
        return ollama.chat_json(
            settings.ollama_url, settings.llm_model, messages, schema, settings.keep_alive, settings.llm_timeout_s
        )

    report, latencies = [], []
    llm_ok = llm_failed = invalid_codes = 0
    hits = {"b": [0, 0], "s": [0, 0], "d": [0, 0]}  # [aciertos, sugeridos] solo en casos validados

    with psycopg.connect(settings.database_url, autocommit=True) as conn:
        known = {row[0] for row in conn.execute("SELECT code FROM icf_codes").fetchall()}
        repo = PgRepo(conn)
        for case in cases:
            patient = PatientContext(**case["patient"])
            started = time.perf_counter()
            res = suggest(patient, repo, embed_fn, chat_fn, settings.llm_model)
            elapsed = round((time.perf_counter() - started) * 1000)
            if res.applicable:
                latencies.append(elapsed)
            if res.llm_used:
                llm_ok += 1
            elif res.llm_error:
                llm_failed += 1
            by_comp = {"b": res.functions, "s": res.structures, "d": res.activities}
            for items in by_comp.values():
                invalid_codes += sum(1 for item in items if item.code not in known)
            if case.get("validated") and case.get("expected"):
                for comp, items in by_comp.items():
                    expected = set(case["expected"].get(comp, []))
                    hits[comp][0] += sum(1 for item in items if item.code in expected)
                    hits[comp][1] += len(items)
            report.append({"id": case["id"], "ms": elapsed, "result": res.model_dump()})
            summary = ", ".join(f"{c}:" + "/".join(i.code for i in items) for c, items in by_comp.items() if items)
            flag = "LLM" if res.llm_used else ("sin-LLM" if res.applicable else "n/a")
            print(f"{case['id']:<6} {elapsed:>6} ms  {flag:<8} {summary or res.message or '-'}")

    invoked = llm_ok + llm_failed
    print("\n--- Resumen ---")
    print(f"casos: {len(cases)} | aplicables: {len(latencies)}")
    print(f"JSON valido del modelo: {llm_ok}/{invoked}" + (f" ({llm_ok / invoked:.0%})" if invoked else ""))
    print(f"codigos fuera del catalogo: {invalid_codes}")
    if latencies:
        print(
            f"latencia ms: p50={percentile(latencies, 50)} p95={percentile(latencies, 95)} "
            f"media={round(statistics.mean(latencies))} max={max(latencies)}"
        )
    validated = sum(1 for c in cases if c.get("validated") and c.get("expected"))
    if validated:
        for comp, (ok, total) in hits.items():
            print(f"precision {comp}: {ok}/{total}" + (f" ({ok / total:.0%})" if total else ""))
    else:
        print("precision: sin casos validados por el medico todavia (completar 'expected' y 'validated')")

    if args.output:
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"informe guardado en {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
