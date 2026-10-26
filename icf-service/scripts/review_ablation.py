"""Analisis de sensibilidad sobre la hoja de revision llena (HU-07g, protocolo secciones 9.2 y 9.4).

Recalcula las metricas del `score` en dos escenarios, SIN modificar la hoja ni `reference/cases.json`:
  * recortar la lista de funciones (b) y de estructuras (s) a las primeras N por caso (orden de la Fase B);
  * excluir de lo esperado los codigos que la revisora califico con gravedad 0 (la CIF: 0 = "no hay problema").

Es un analisis exploratorio y post hoc: se hace sobre los mismos casos que miden el sistema, asi que no valida ningun
ajuste (Cawley y Talbot 2010; Kapoor y Narayanan 2023). Los umbrales no se tocan.

Uso:
    python scripts/review_ablation.py ../data/private/icf/review/hoja_revision_v2.xlsx
"""
import argparse
import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import review_sheet  # noqa: E402

from icf.review import compute_metrics, evaluate_thresholds  # noqa: E402

REPS = 500  # remuestras del bootstrap por casos (el IC no decide)


def truncated(ratings, suggested, top_b, top_s):
    """Deja solo las primeras `top_b` funciones y `top_s` estructuras de cada caso (orden de la Fase B)."""
    limit = {"b": top_b, "s": top_s, "d": 99}
    seen, kept = {}, []
    for r in ratings:
        key = (r["case"], r["component"])
        seen[key] = seen.get(key, 0) + 1
        if seen[key] <= limit[r["component"]]:
            kept.append(r)
    kept_codes = {(r["case"], r["component"]): set() for r in kept}
    for r in kept:
        kept_codes[(r["case"], r["component"])].add(r["code"])
    reduced = copy.deepcopy(suggested)
    for case, comps in reduced.items():
        for comp in ("b", "s"):
            if (case, comp) in kept_codes:
                comps[comp] = comps.get(comp, set()) & kept_codes[(case, comp)]
    return kept, reduced


def without_zero_severity(blind, blind_q):
    zero = {case: {code for code, level in q.items() if level == 0} for case, q in blind_q.items()}
    return {
        case: {comp: {c for c in codes if c not in zero.get(case, set())} for comp, codes in comps.items()}
        for case, comps in blind.items()
    }


def report(label, ratings, missing, blind, suggested, blind_q, suggested_q):
    metrics = compute_metrics(ratings, missing, blind, suggested, blind_q, suggested_q, bootstrap_reps=REPS)
    verdict = evaluate_thresholds(metrics)
    values = [c["valor"] for c in verdict["criterios"]]
    print(f"{label:<44} {verdict['veredicto']:<11} casos/estricta/flexible/cobertura/kappa/flex d = {values}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("sheet", help="hoja de revision llena (.xlsx)")
    args = parser.parse_args()

    ratings, missing, blind, suggested, blind_q, suggested_q = review_sheet.read_filled(args.sheet)

    print("Recorte de la lista (orden de la Fase B):")
    for top_b, top_s in ((3, 3), (3, 2), (3, 1), (2, 2), (2, 1)):
        kept, reduced = truncated(ratings, suggested, top_b, top_s)
        report(f"  b hasta {top_b}, s hasta {top_s}", kept, missing, blind, reduced, blind_q, suggested_q)

    print("Sin los codigos esperados con gravedad 0:")
    blind0 = without_zero_severity(blind, blind_q)
    for top_b, top_s in ((3, 3), (3, 2)):
        kept, reduced = truncated(ratings, suggested, top_b, top_s)
        report(f"  b hasta {top_b}, s hasta {top_s}", kept, missing, blind0, reduced, blind_q, suggested_q)
    return 0


if __name__ == "__main__":
    sys.exit(main())
