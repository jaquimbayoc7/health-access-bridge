"""Compara formas de armar la busqueda de funciones (b) y estructuras (s) y mide cuantas de las
'pistas' orientativas (reference/retrieval_hints.json, NO validadas por un medico) quedan entre los
primeros 6 y 12 candidatos. No mide precision clinica: sirve para elegir la mejor formulacion y
cuantos candidatos conviene pasarle al modelo.

Variantes (todas buscan con el texto 'clinico': diagnostico sin codigo CIE + notas):
  actual     texto con causa, categorias, diagnostico con codigo CIE y notas; codigos de nivel 2 y 3
  clinico    texto clinico; codigos de nivel 2 y 3
  n2         texto clinico; solo codigos de 3 digitos (nivel 2)  <- la busqueda que usa el motor

Uso (en el servidor):  python scripts/probe_retrieval.py [--verbose]
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import psycopg  # noqa: E402

from icf import ollama, rules  # noqa: E402
from icf.config import load_settings  # noqa: E402
from icf.repository import PgRepo  # noqa: E402
from icf.schemas import PatientContext  # noqa: E402
from icf.suggest import _CHAPTER_NAME  # noqa: E402

CASES = ROOT / "reference" / "cases.json"
HINTS = ROOT / "reference" / "retrieval_hints.json"
SIZES = (6, 12)

# variante -> (texto, niveles, columna de embedding)
VARIANTS = {
    "actual": ("actual", (2, 3), "embedding"),  # = la busqueda inicial (niveles 2 y 3, texto con todo)
    "clinico": ("clinico", (2, 3), "embedding"),
    "n2": ("clinico", (2,), "embedding"),
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true", help="muestra tambien los titulos de los candidatos")
    args = ap.parse_args()

    s = load_settings()
    cases = {c["id"]: c for c in json.loads(CASES.read_text(encoding="utf-8"))["cases"]}
    hints = json.loads(HINTS.read_text(encoding="utf-8"))["hints"]
    # totales[variante][componente][k] = [aciertos, pistas, casos con >=1 acierto, casos]
    totals = {v: {c: {k: [0, 0, 0, 0] for k in SIZES} for c in "bs"} for v in VARIANTS}

    def embed(text):
        return ollama.embed(s.ollama_url, s.embed_model, text, s.keep_alive, 60)

    with psycopg.connect(s.database_url, autocommit=True) as conn:
        repo = PgRepo(conn)
        for case_id, hint in hints.items():
            case = cases[case_id]
            p = PatientContext(**case["patient"])
            plan = rules.activity_plan(p.levels)
            texts = {
                "actual": rules.context_text(
                    p.cause, p.cat_fisica, p.cat_psicosocial, p.diag_cie, p.clinical_notes,
                    [_CHAPTER_NAME[ch] for ch, _, _ in plan],
                ),
            }
            texts["clinico"] = rules.clinical_query(p.diag_cie, p.clinical_notes) or texts["actual"]
            print(f"{case_id} {case['description']}")
            vectors = {name: embed(text) for name, text in texts.items()}
            for variant, (text_name, levels, _unused) in VARIANTS.items():
                line = []
                for comp in ("b", "s"):
                    wanted = set(hint[comp])
                    chapters = rules.body_chapters(comp, p.cat_fisica, p.cat_psicosocial)
                    found = repo.search(comp, vectors[text_name], max(SIZES), chapters, levels)
                    codes = [c for c, _ in found]
                    cells = []
                    for k in SIZES:
                        hit = [c for c in codes[:k] if c in wanted]
                        cells.append(f"@{k}:{len(hit)}/{len(wanted)}")
                        if wanted:
                            t = totals[variant][comp][k]
                            t[0] += len(hit); t[1] += len(wanted); t[2] += 1 if hit else 0; t[3] += 1
                    marks = " ".join(f"{c}{'*' if c in wanted else ''}" for c in codes[: SIZES[0]])
                    line.append(f"{comp} {' '.join(cells)} [{marks}]")
                    if args.verbose:
                        for code, title in found:
                            print(f"      {variant:<8} {comp} {code}{'*' if code in wanted else ' '} {title}")
                print(f"   {variant:<8} " + " | ".join(line))

    print("\n--- Cobertura de las pistas (orientativa, no es precision clinica): aciertos/pistas y % ---")
    head = f"{'variante':<9}" + "".join(f" {comp}@{k:<2} pistas  {comp}@{k:<2} casos " for comp in "bs" for k in SIZES)
    print(head)
    for v in VARIANTS:
        cells = []
        for comp in "bs":
            for k in SIZES:
                a, n, c, m = totals[v][comp][k]
                cells.append(f"{a}/{n} {round(100 * a / n) if n else 0:>3}%   {c}/{m} {round(100 * c / m) if m else 0:>3}%")
        print(f"{v:<9} " + "  ".join(cells))
    return 0


if __name__ == "__main__":
    sys.exit(main())
