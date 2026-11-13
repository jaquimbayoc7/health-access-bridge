"""Exploracion del calificador de gravedad sin acceso a la revisora (HU-07g, tras la ronda 3).

Carga la gravedad 0-4 que la medica escribio a ciegas (rondas 1 y 3) junto a los datos del paciente y compara
variantes de la regla del calificador. ES EXPLORATORIO: no cambia el veredicto oficial de la ronda 3 y no valida nada
clinicamente (una sola revisora, casos sinteticos). Uso: python scripts/qualifier_exploration.py dump
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
PRIVATE = ROOT.parent / "data" / "private" / "icf" / "review"

SHEETS = (("hoja_revision_v2.xlsx", "reference/cases.json", "R1"), ("hoja_ronda3.xlsx", "reference/cases_ronda2.json", "R3"))


def load_rows():
    import review_sheet

    rows = []
    for sheet, cases_file, rnd in SHEETS:
        _r, _m, blind, _s, blind_q, _sq = review_sheet.read_filled(PRIVATE / sheet)
        cases = {c["id"]: c for c in json.loads((ROOT / cases_file).read_text(encoding="utf8"))["cases"]}
        for case, qs in blind_q.items():
            if case not in cases:
                continue
            p = cases[case]["patient"]
            for code, sev in qs.items():
                if code[0] not in "bs":
                    continue
                rows.append(dict(round=rnd, case=case, code=code, comp=code[0], chapter=code[:2], sev=sev,
                                 cat_f=p.get("cat_fisica"), cat_p=p.get("cat_psicosocial"), levels=p["levels"],
                                 age=p.get("age"), diag=p.get("diag_cie"), notes=p.get("clinical_notes")))
    return rows


if __name__ == "__main__":
    rows = load_rows()
    print(len(rows), "codigos b/s con gravedad a ciegas")
    json.dump(rows, open(sys.argv[2] if len(sys.argv) > 2 else "/dev/stdout", "w", encoding="utf8"), ensure_ascii=False)
