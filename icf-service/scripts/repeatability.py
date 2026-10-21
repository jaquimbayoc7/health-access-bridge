"""Repetibilidad del sistema (HU-07g): corre N veces cada caso y mide cuan estables son los codigos sugeridos.

Uso (en un equipo con ICF_DATABASE_URL, OLLAMA_URL e ICF_LLM_MODEL):
    python scripts/repeatability.py --runs 5 --output informe_repetibilidad.json

Usa la misma configuracion que produccion (modelo, temperatura, candidatos). No necesita a la revisora.
El informe trae solo codigos (no titulos del catalogo); aun asi se guarda en data/private/.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from icf.stability import compute_stability  # noqa: E402

DEFAULT_CASES = ROOT / "reference" / "cases.json"


def interpret(kappa):
    """Lectura de McHugh 2012: por debajo de 0,60 el acuerdo es inadecuado."""
    if kappa is None:
        return "sin dato"
    return "fuerte (>= 0,80)" if kappa >= 0.80 else "moderado (0,60-0,79)" if kappa >= 0.60 else "inadecuado (< 0,60)"


def collect(args):
    import psycopg

    from icf.config import load_settings
    from icf.repository import PgRepo
    from icf.runtime import OllamaFns
    from icf.schemas import PatientContext
    from icf.suggest import suggest

    settings = load_settings()
    if not settings.database_url:
        print("Falta ICF_DATABASE_URL", file=sys.stderr)
        return None
    cases = json.loads(args.cases.read_text(encoding="utf-8"))["cases"]
    runs = {}
    with psycopg.connect(settings.database_url, autocommit=True) as conn:
        repo = PgRepo(conn)
        for case in cases:
            patient = PatientContext(**case["patient"])
            for i in range(args.runs):
                fns = OllamaFns(settings)
                res = suggest(
                    patient, repo, fns.embed, fns.chat, settings.llm_model, stats=fns.stats, use_llm=settings.use_llm,
                    body_candidates=settings.body_candidates, justify=settings.justify,
                )
                if not res.applicable:
                    print(f"{case['id']}: no aplica; se omite")
                    break
                by_comp = {"b": res.functions, "s": res.structures, "d": res.activities}
                runs.setdefault(case["id"], []).append({comp: {it.code.lower()[:4] for it in items} for comp, items in by_comp.items()})
            print(f"{case['id']}: {len(runs.get(case['id'], []))} corridas")
    return runs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runs", type=int, default=5, help="corridas por caso (minimo 2)")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.runs < 2:
        parser.error("--runs debe ser al menos 2")
    runs = collect(args)
    if runs is None:
        return 2
    report = compute_stability(runs)
    print(f"\nCasos: {report['cases']} | corridas por caso: {report['runs_per_case']}")
    print(f"Kappa de Fleiss por capitulo: {report['chapter_kappa']} -> {interpret(report['chapter_kappa'])}")
    print(f"Kappa de Fleiss por codigo:   {report['code_kappa']} -> {interpret(report['code_kappa'])}")
    print(f"Jaccard medio entre corridas: {report['mean_jaccard']}")
    print(f"Codigos estables (en todas las corridas): {report['stable_code_share']}")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"informe guardado en {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
