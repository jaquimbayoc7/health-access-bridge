"""Compara formas de armar la busqueda de funciones (b) y estructuras (s) y mide cuantas de las
'pistas' orientativas (reference/retrieval_hints.json, NO validadas por un medico) quedan entre los 6
candidatos que ve el modelo. No mide precision clinica: sirve para elegir la mejor formulacion.

Variantes:
  actual     texto con causa, categorias, diagnostico (con codigo CIE), notas y dominios con dificultad
  clinico    solo diagnostico sin codigo CIE + notas (si no hay, cae a 'actual')
  expandido  el modelo (qwen) describe en una linea las funciones/estructuras afectadas; se busca con eso
  diverso    como 'clinico', pero maximo 2 candidatos por capitulo (evita que un tema acapare los 6)

Uso (en el servidor):  python scripts/probe_retrieval.py [--no-expansion] [--k 6] [--verbose]
"""
import argparse
import json
import sys
import time
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


def diversify(pairs, per_chapter=2, k=6):
    chosen, count = [], {}
    for code, title in pairs:
        chapter = code[1]
        if count.get(chapter, 0) < per_chapter:
            chosen.append((code, title))
            count[chapter] = count.get(chapter, 0) + 1
        if len(chosen) == k:
            break
    return chosen


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--k", type=int, default=6, help="candidatos por componente (6 = lo que ve el modelo)")
    ap.add_argument("--no-expansion", action="store_true", help="omite la variante que usa el modelo (mas rapido)")
    ap.add_argument("--verbose", action="store_true", help="muestra tambien los titulos de los candidatos")
    args = ap.parse_args()

    s = load_settings()
    cases = {c["id"]: c for c in json.loads(CASES.read_text(encoding="utf-8"))["cases"]}
    hints = json.loads(HINTS.read_text(encoding="utf-8"))["hints"]
    variants = ["actual", "clinico"] + ([] if args.no_expansion else ["expandido"]) + ["diverso"]
    totals = {v: {"b": [0, 0, 0, 0], "s": [0, 0, 0, 0]} for v in variants}  # aciertos, pistas, casos con >=1, casos

    def embed(text):
        return ollama.embed(s.ollama_url, s.embed_model, text, s.keep_alive, 60)

    def expand(dx, notes):
        prompt = (
            f"Diagnostico: {dx}. Notas: {notes or 'sin notas'}. "
            "En una sola linea y sin explicaciones, menciona las funciones corporales y las estructuras "
            "corporales afectadas, separadas por comas (maximo 25 palabras)."
        )
        text = ollama.chat_json(
            s.ollama_url, s.llm_model,
            [{"role": "system", "content": "Eres un asistente clinico."}, {"role": "user", "content": prompt}],
            None, s.keep_alive, 120, num_predict=60, num_ctx=1024,
        )
        return " ".join(text.split())

    with psycopg.connect(s.database_url, autocommit=True) as conn:
        repo = PgRepo(conn)
        for case_id, hint in hints.items():
            case = cases[case_id]
            p = PatientContext(**case["patient"])
            plan = rules.activity_plan(p.levels)
            actual = rules.context_text(
                p.cause, p.cat_fisica, p.cat_psicosocial, p.diag_cie, p.clinical_notes,
                [_CHAPTER_NAME[ch] for ch, _, _ in plan],
            )
            clinico = rules.clinical_query(p.diag_cie, p.clinical_notes) or actual
            texts = {"actual": actual, "clinico": clinico, "diverso": clinico}
            if "expandido" in variants:
                t0 = time.perf_counter()
                expanded = expand(rules.clean_diagnosis(p.diag_cie), p.clinical_notes)
                texts["expandido"] = f"{expanded}. {clinico}"
                print(f"{case_id} expansion ({round((time.perf_counter() - t0) * 1000)} ms): {expanded}")
            print(f"{case_id} {case['description']}")
            for variant in variants:
                vector = embed(texts[variant])
                line = []
                for comp in ("b", "s"):
                    wanted = set(hint[comp])
                    chapters = rules.body_chapters(comp, p.cat_fisica, p.cat_psicosocial)
                    if variant == "diverso":
                        found = diversify(repo.search(comp, vector, 40, chapters), 2, args.k)
                    else:
                        found = repo.search(comp, vector, args.k, chapters)
                    codes = [c for c, _ in found]
                    hit = [c for c in codes if c in wanted]
                    if wanted:
                        t = totals[variant][comp]
                        t[0] += len(hit); t[1] += len(wanted); t[2] += 1 if hit else 0; t[3] += 1
                    marks = " ".join(f"{c}{'*' if c in wanted else ''}" for c in codes)
                    line.append(f"{comp} {len(hit)}/{len(wanted)} [{marks}]")
                    if args.verbose:
                        for code, title in found:
                            print(f"      {variant:<9} {comp} {code}{'*' if code in wanted else ' '} {title}")
                print(f"   {variant:<9} " + " | ".join(line))

    print(f"\n--- Cobertura de las pistas en los {args.k} candidatos (orientativa, no es precision clinica) ---")
    print(f"{'variante':<10} {'b: pistas':>12} {'b: casos':>10} {'s: pistas':>12} {'s: casos':>10}")
    for v in variants:
        b, sx = totals[v]["b"], totals[v]["s"]
        pct = lambda a, n: f"{a}/{n} {round(100 * a / n) if n else 0}%"  # noqa: E731
        print(f"{v:<10} {pct(b[0], b[1]):>12} {pct(b[2], b[3]):>10} {pct(sx[0], sx[1]):>12} {pct(sx[2], sx[3]):>10}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
