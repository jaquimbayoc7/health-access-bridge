r"""Mide si la memoria de casos mejora las sugerencias, dejando un caso fuera cada vez (HU-07j).

Contra la verdad a ciegas de la profesional (los codigos b y s que escribio en la Fase A) en los casos validados, compara el motor sin memoria con el motor con
memoria a distintos umbrales de similitud. En cada caso la memoria se consulta SIN ese caso (leave-one-out), para no medir de forma circular.

Necesita una base con el catalogo (icf_codes con embeddings) y la memoria cargada con scripts/load_validated_cases.py, mas Ollama. Ejemplo con una base de prueba:
    $env:ICF_DATABASE_URL = "postgresql://postgres:pw@127.0.0.1:55434/icf"; $env:ICF_LLM_THINK = "false"
    python icf-service/scripts/evaluate_memory.py --thresholds 0.80,0.70,0.60 --json resultado.json

Limites que conviene leer: son 46 casos sinteticos con una sola revisora, cada caso suele ser de una condicion distinta (pocos vecinos parecidos), el motor se midio
antes con estos mismos casos (los umbrales NO se reajustan con ellos: es un analisis exploratorio) y una mejora de cobertura no implica una mejora clinica.
"""
import argparse
import json
import random
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))


class LeaveOneOut:
    """Envuelve el repositorio y deja fuera de la memoria el caso que se esta evaluando."""

    def __init__(self, repo, exclude: str):
        self._repo, self._exclude = repo, exclude

    def __getattr__(self, name):
        return getattr(self._repo, name)

    def similar_cases(self, embedding, limit, min_similarity):
        found = self._repo.similar_cases(embedding, limit + 1, min_similarity)
        return [c for c in found if c["case_key"] != self._exclude][:limit]


def expected_by_case(records) -> Dict[str, Dict[str, set]]:
    """{id del caso: {'b': {codigos}, 's': {codigos}}} con lo que la profesional eligio a ciegas (sin gravedad 0)."""
    out: Dict[str, Dict[str, set]] = {}
    for r in records:
        out.setdefault(r.case_key.replace("medica-", ""), {"b": set(), "s": set()})[r.component].add(r.code)
    return out


def summarize(rows: List[dict]) -> dict:
    """Cobertura (de lo que ella eligio, cuanto sugirio el motor) y precision frente a lo que ella eligio, por componente."""
    total = {"expected": 0, "hits": 0, "suggested": 0, "with_examples": 0}
    comp = {"b": [0, 0, 0], "s": [0, 0, 0]}  # aciertos, esperados, sugeridos
    for row in rows:
        total["with_examples"] += 1 if row["examples"] else 0
        for c in ("b", "s"):
            exp, got = row["expected"][c], row["got"][c]
            comp[c][0] += len(exp & got)
            comp[c][1] += len(exp)
            comp[c][2] += len(got)
    total["hits"] = comp["b"][0] + comp["s"][0]
    total["expected"] = comp["b"][1] + comp["s"][1]
    total["suggested"] = comp["b"][2] + comp["s"][2]
    total["coverage"] = round(total["hits"] / total["expected"], 3) if total["expected"] else None
    total["precision_vs_blind"] = round(total["hits"] / total["suggested"], 3) if total["suggested"] else None
    total["by_component"] = {c: {"hits": v[0], "expected": v[1], "suggested": v[2]} for c, v in comp.items()}
    return total


def paired_delta_ci(base_rows: List[dict], rows: List[dict], reps: int = 2000, seed: int = 1) -> Optional[list]:
    """Diferencia de cobertura (memoria menos base) con IC 95 % por remuestreo de casos."""
    per_case = []
    for b, r in zip(base_rows, rows):
        exp = len(b["expected"]["b"]) + len(b["expected"]["s"])
        hb = len(b["expected"]["b"] & b["got"]["b"]) + len(b["expected"]["s"] & b["got"]["s"])
        hr = len(r["expected"]["b"] & r["got"]["b"]) + len(r["expected"]["s"] & r["got"]["s"])
        per_case.append((hr - hb, exp))
    if len(per_case) < 2:
        return None
    rng, values = random.Random(seed), []
    for _ in range(reps):
        sample = [per_case[rng.randrange(len(per_case))] for _ in per_case]
        den = sum(e for _, e in sample)
        if den:
            values.append(sum(d for d, _ in sample) / den)
    values.sort()
    return [round(values[int(0.025 * (len(values) - 1))], 3), round(values[int(0.975 * (len(values) - 1))], 3)]


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--thresholds", default="0.80,0.70,0.60")
    parser.add_argument("--examples", type=int, default=3)
    parser.add_argument("--json")
    args = parser.parse_args(argv)

    import os

    import psycopg

    from icf.config import load_settings
    from icf.repository import PgRepo
    from icf.runtime import OllamaFns
    from icf.schemas import PatientContext
    from icf.suggest import suggest
    from load_validated_cases import load_validated

    settings = load_settings()
    if not settings.database_url:
        print("Falta ICF_DATABASE_URL", file=sys.stderr)
        return 2
    records = load_validated()
    expected = expected_by_case(records)
    cases = {}
    for r in records:
        cases[r.case_key.replace("medica-", "")] = r.patient
    thresholds = [float(t) for t in args.thresholds.split(",") if t]
    variants = [("sin memoria", 0, 0.0)] + [(f"memoria >= {t:.2f}", args.examples, t) for t in thresholds]
    results: Dict[str, List[dict]] = {name: [] for name, _, _ in variants}

    with psycopg.connect(settings.database_url, autocommit=True, connect_timeout=5) as conn:
        repo = PgRepo(conn)
        for case_id in sorted(cases):
            patient: PatientContext = cases[case_id]
            for name, n_examples, threshold in variants:
                fns = OllamaFns(settings)
                res = suggest(
                    patient, LeaveOneOut(repo, f"medica-{case_id}"), fns.embed, fns.chat, settings.llm_model, stats=fns.stats,
                    use_llm=settings.use_llm, body_candidates=settings.body_candidates, justify=settings.justify,
                    s_evidence=settings.s_evidence, motor_link=settings.motor_link, mental_link=settings.mental_link,
                    case_examples=n_examples, case_min_similarity=threshold,
                )
                results[name].append({
                    "case": case_id, "expected": expected[case_id], "examples": res.case_examples,
                    "got": {"b": {i.code for i in res.functions}, "s": {i.code for i in res.structures}},
                })
            print(f"{case_id} ok", flush=True)

    report = {}
    base = results["sin memoria"]
    for name, _, _ in variants:
        report[name] = summarize(results[name])
        if name != "sin memoria":
            report[name]["coverage_delta_vs_base_ci95_cases"] = paired_delta_ci(base, results[name])
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.json:
        Path(args.json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
