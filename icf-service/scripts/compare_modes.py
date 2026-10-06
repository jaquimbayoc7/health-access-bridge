"""Compara los modos del motor con las pistas orientativas: ¿el modelo elige mejor que la similitud sola?

Modos:
  similitud  sin modelo de generacion: los 3 codigos mas cercanos por similitud (12 candidatos)   ~1 s
  rapido     6 candidatos, el modelo elige y devuelve solo codigos                                ~20 s
  calidad    12 candidatos, el modelo elige y justifica cada codigo                               ~40 s

Metricas por modo, sobre los casos con pistas (reference/retrieval_hints.json, NO validadas por un medico):
  precision  de los codigos sugeridos, cuantos son pista
  cobertura  de las pistas, cuantas aparecen entre los sugeridos
  casos      en cuantos casos hay al menos una pista acertada
Las pistas son estrechas (un codigo razonable que no figura en ellas cuenta como fallo): usar las cifras
para COMPARAR modos, no como precision clinica. La precision clinica se mide con 'expected' del medico.

Uso (en el servidor; los tres modos tardan unos 20 minutos, conviene correrlo en segundo plano):
    python scripts/compare_modes.py [--modes similitud,calidad] [--ids C02,C03] [--output comparacion.json]
"""
import argparse
import dataclasses
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

CASES = ROOT / "reference" / "cases.json"
HINTS = ROOT / "reference" / "retrieval_hints.json"

# modo -> parametros de suggest() y del cliente de Ollama
MODES = {
    "similitud": dict(use_llm=False, body_candidates=12, justify=False, num_predict=120, num_ctx=1024),
    "rapido": dict(use_llm=True, body_candidates=6, justify=False, num_predict=120, num_ctx=1024),
    "calidad": dict(use_llm=True, body_candidates=12, justify=True, num_predict=300, num_ctx=2048),
}


def pct(a, n):
    return f"{round(100 * a / n)}%" if n else "-"


def percentile(values, p):
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, round(p / 100 * (len(ordered) - 1)))] if ordered else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--modes", default="similitud,rapido,calidad", help="modos separados por coma")
    ap.add_argument("--ids", help="solo estos casos (ej. C02,C03)")
    ap.add_argument("--output", type=Path, help="guarda el detalle completo en JSON")
    args = ap.parse_args()

    modes = [m.strip() for m in args.modes.split(",") if m.strip()]
    unknown = [m for m in modes if m not in MODES]
    if unknown:
        print(f"Modo desconocido: {unknown}. Opciones: {list(MODES)}", file=sys.stderr)
        return 2

    base = load_settings()
    cases = {c["id"]: c for c in json.loads(CASES.read_text(encoding="utf-8"))["cases"]}
    hints = json.loads(HINTS.read_text(encoding="utf-8"))["hints"]
    ids = [i for i in hints if not args.ids or i in {x.strip() for x in args.ids.split(",")}]

    # acum[modo][componente] = [sugeridos, aciertos, pistas, casos con pista, casos con >=1 acierto]
    acum = {m: {c: [0, 0, 0, 0, 0] for c in "bs"} for m in modes}
    latencies = {m: [] for m in modes}
    failures = {m: 0 for m in modes}
    detail = []

    with psycopg.connect(base.database_url, autocommit=True) as conn:
        repo = PgRepo(conn)
        for case_id in ids:
            patient = PatientContext(**cases[case_id]["patient"])
            print(f"{case_id} {cases[case_id]['description']}", flush=True)
            for mode in modes:
                cfg = MODES[mode]
                settings = dataclasses.replace(base, num_predict=cfg["num_predict"], num_ctx=cfg["num_ctx"])
                fns = OllamaFns(settings)
                res = suggest(
                    patient, repo, fns.embed, fns.chat, settings.llm_model, stats=fns.stats,
                    use_llm=cfg["use_llm"], body_candidates=cfg["body_candidates"], justify=cfg["justify"],
                )
                latencies[mode].append(res.latency_ms)
                if cfg["use_llm"] and not res.llm_used:
                    failures[mode] += 1
                cells = []
                picks = {"b": [i.code for i in res.functions], "s": [i.code for i in res.structures]}
                for comp in "bs":
                    wanted = set(hints[case_id][comp])
                    hit = [c for c in picks[comp] if c in wanted]
                    a = acum[mode][comp]
                    a[0] += len(picks[comp]); a[1] += len(hit); a[2] += len(wanted)
                    if wanted:
                        a[3] += 1
                        a[4] += 1 if hit else 0
                    marks = " ".join(f"{c}{'*' if c in wanted else ''}" for c in picks[comp]) or "-"
                    cells.append(f"{comp}: {marks}")
                print(f"   {mode:<9} {res.latency_ms / 1000:>5.1f} s  " + " | ".join(cells), flush=True)
                detail.append({"case": case_id, "mode": mode, "latency_ms": res.latency_ms, "picks": picks,
                               "llm_used": res.llm_used, "justifications": {
                                   i.code: i.justification for i in res.functions + res.structures}})

    print("\n--- Comparacion de modos sobre las pistas orientativas (NO es precision clinica) ---")
    print(f"casos: {len(ids)}")
    print(f"{'modo':<10} {'b: precision':>13} {'b: cobertura':>13} {'b: casos':>9} {'s: precision':>13} {'s: cobertura':>13} {'s: casos':>9}"
          f" {'latencia media':>15} {'p95':>7}")
    for mode in modes:
        row = []
        for comp in "bs":
            sug, ok, pistas, casos, casos_ok = acum[mode][comp]
            row += [f"{ok}/{sug} {pct(ok, sug)}", f"{ok}/{pistas} {pct(ok, pistas)}", f"{casos_ok}/{casos}"]
        lat = latencies[mode]
        print(f"{mode:<10} {row[0]:>13} {row[1]:>13} {row[2]:>9} {row[3]:>13} {row[4]:>13} {row[5]:>9}"
              f" {statistics.mean(lat) / 1000:>13.1f} s {percentile(lat, 95) / 1000:>5.1f} s" if lat else mode)
    for mode in modes:
        if failures[mode]:
            print(f"AVISO: el modelo no respondio de forma valida en {failures[mode]} casos del modo {mode} (se uso similitud)")

    if args.output:
        args.output.write_text(json.dumps(detail, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"detalle guardado en {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
