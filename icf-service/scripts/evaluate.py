"""Evalua el motor con el set de referencia (reference/cases.json) y mide calidad y latencia.

Uso (en el servidor, con ICF_DATABASE_URL y OLLAMA_URL definidos; ver README):
    python scripts/evaluate.py                      # corre todos los casos
    python scripts/evaluate.py --output informe.json

Metricas que NO necesitan validacion medica: respuestas con JSON valido del modelo, codigos fuera del
catalogo, latencia p50/p95 y su desglose (embedding, busqueda, modelo). La precision solo se calcula en
los casos con "validated": true y "expected" (codigos esperados por componente, completados por el medico).
"""
import argparse
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import psycopg  # noqa: E402

from icf.config import load_settings  # noqa: E402
from icf.repository import PgRepo  # noqa: E402
from icf.runtime import OllamaFns  # noqa: E402
from icf.schemas import PatientContext  # noqa: E402
from icf.suggest import suggest  # noqa: E402

DEFAULT_CASES = ROOT / "reference" / "cases.json"


def percentile(values, pct):
    ordered = sorted(values)
    if not ordered:
        return None
    index = min(len(ordered) - 1, round(pct / 100 * (len(ordered) - 1)))
    return ordered[index]


def mean(values):
    return round(statistics.mean(values)) if values else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    ap.add_argument("--output", type=Path, help="guarda el informe completo en JSON")
    ap.add_argument("--limit", type=int, help="solo los primeros N casos")
    args = ap.parse_args()

    settings = load_settings()
    if not settings.database_url:
        print("Falta ICF_DATABASE_URL", file=sys.stderr)
        return 2
    cases = json.loads(args.cases.read_text(encoding="utf-8"))["cases"]
    if args.limit:
        cases = cases[: args.limit]

    report, latencies = [], []
    stage = {"embed": [], "search": [], "llm": []}
    tok_in, tok_out, gen_rate = [], [], []
    llm_ok = llm_failed = invalid_codes = 0
    hits = {"b": [0, 0], "s": [0, 0], "d": [0, 0]}  # [aciertos, sugeridos] solo en casos validados

    with psycopg.connect(settings.database_url, autocommit=True) as conn:
        known = {row[0] for row in conn.execute("SELECT code FROM icf_codes").fetchall()}
        repo = PgRepo(conn)
        for case in cases:
            patient = PatientContext(**case["patient"])
            fns = OllamaFns(settings)
            res = suggest(patient, repo, fns.embed, fns.chat, settings.llm_model, stats=fns.stats)
            if res.applicable:
                latencies.append(res.latency_ms)
                for key in stage:
                    if key in res.timings:
                        stage[key].append(res.timings[key])
                if "prompt_eval_count" in res.llm_stats:
                    tok_in.append(res.llm_stats["prompt_eval_count"])
                if res.llm_stats.get("eval_count") and res.llm_stats.get("eval_ms"):
                    tok_out.append(res.llm_stats["eval_count"])
                    gen_rate.append(res.llm_stats["eval_count"] / (res.llm_stats["eval_ms"] / 1000))
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
            report.append({"id": case["id"], "result": res.model_dump()})
            summary = ", ".join(f"{c}:" + "/".join(i.code for i in items) for c, items in by_comp.items() if items)
            flag = "LLM" if res.llm_used else ("sin-LLM" if res.applicable else "n/a")
            detail = " ".join(f"{k}={v}" for k, v in res.timings.items())
            print(f"{case['id']:<4} {res.latency_ms:>6} ms [{detail}] {flag:<8} {summary or res.message or '-'}")
            if res.llm_error:
                print(f"       error del modelo: {res.llm_error}")

    invoked = llm_ok + llm_failed
    print("\n--- Resumen ---")
    print(f"casos: {len(cases)} | aplicables: {len(latencies)}")
    print(f"JSON valido del modelo: {llm_ok}/{invoked}" + (f" ({llm_ok / invoked:.0%})" if invoked else ""))
    print(f"codigos fuera del catalogo: {invalid_codes}")
    if latencies:
        print(
            f"latencia total ms: p50={percentile(latencies, 50)} p95={percentile(latencies, 95)} "
            f"media={mean(latencies)} max={max(latencies)}"
        )
        print(
            f"desglose medio ms: embedding={mean(stage['embed'])} busqueda={mean(stage['search'])} modelo={mean(stage['llm'])}"
        )
    if tok_in:
        print(f"tokens: prompt medio={mean(tok_in)} | salida media={mean(tok_out)} | velocidad de salida={round(statistics.mean(gen_rate), 1) if gen_rate else '?'} tok/s")
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
