r"""Informe de la memoria de casos confirmados (HU-07j): acuerdo entre la gravedad que sugirio el sistema y la que fijo el medico.

Es de solo lectura. Uso, en el PC del servicio (la base publica el puerto 5433 solo en 127.0.0.1; necesita `pip install psycopg[binary]`):
    $env:ICF_DATABASE_URL = "postgresql://icf_user:<clave>@127.0.0.1:5433/icf"   # la clave esta en %USERPROFILE%\.hab-icf\.env
    python icf-service/scripts/case_memory_report.py [--min-pairs 30] [--json salida.json]

Que mide: en los codigos de funciones (b) y estructuras (s) con gravedad sugerida y confirmada, la coincidencia exacta, la coincidencia a +-1 nivel y
el kappa ponderado (pesos lineales) con IC 95 % por remuestreo de casos. CUIDADO con la lectura: cuando el medico acepta con el boton, la
gravedad confirmada es la sugerida (efecto de anclaje), asi que el acuerdo medido aqui es una COTA SUPERIOR; solo informa si el medico la cambia. No
sustituye la validacion a ciegas (protocolo HU-07g). Con menos de --min-pairs pares el kappa no es concluyente y el informe lo dice.
"""
import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from icf.review import cluster_bootstrap_ci, weighted_kappa  # noqa: E402

MIN_PAIRS = 30  # el mismo minimo del protocolo de validacion (el IC del kappa con menos pares es demasiado ancho)

Row = Tuple[str, str, int, int, str]  # (case_key, component, sugerida, confirmada, estado)


def agreement(rows: Sequence[Row], min_pairs: int = MIN_PAIRS, reps: int = 2000) -> Dict:
    """Metricas de acuerdo sobre filas (case_key, componente, sugerida, confirmada, estado). Solo cuentan b y s."""
    body = [r for r in rows if r[1] in ("b", "s")]
    pairs = [(r[3], r[2]) for r in body]  # (medico, sistema), como en la validacion clinica
    n = len(pairs)
    changed = sum(1 for a, b in pairs if a != b)
    by_case: Dict[str, List[Tuple[int, int]]] = defaultdict(list)
    for r in body:
        by_case[r[0]].append((r[3], r[2]))
    kappa = weighted_kappa(pairs) if n else None
    ci = cluster_bootstrap_ci(list(by_case.values()), lambda s: weighted_kappa([p for c in s for p in c]), reps) if len(by_case) >= 2 else None
    report = {
        "pairs": n,
        "cases": len(by_case),
        "changed_by_doctor": changed,
        "changed_rate": round(changed / n, 3) if n else None,
        "exact": round(sum(1 for a, b in pairs if a == b) / n, 3) if n else None,
        "within_one": round(sum(1 for a, b in pairs if abs(a - b) <= 1) / n, 3) if n else None,
        "weighted_kappa": kappa,
        "weighted_kappa_ci95_cases": ci,
        "suggested_distribution": dict(sorted(Counter(b for _, b in pairs).items())),
        "confirmed_distribution": dict(sorted(Counter(a for a, _ in pairs).items())),
        "conclusive": n >= min_pairs,
        "note": (
            "Cota superior: al aceptar con el boton la gravedad confirmada coincide con la sugerida (anclaje). "
            "No sustituye la validacion a ciegas."
        ),
    }
    if n < min_pairs:
        report["warning"] = f"Menos de {min_pairs} pares: el kappa no es concluyente."
    return report


def load_rows(database_url: str) -> List[Row]:
    import psycopg

    with psycopg.connect(database_url, autocommit=True, connect_timeout=5) as conn:
        try:
            found = conn.execute(
                """SELECT case_key, component, qualifier_suggested, qualifier, status FROM icf_case_codes
                   WHERE component IN ('b', 's') AND qualifier_suggested IS NOT NULL AND qualifier IS NOT NULL"""
            ).fetchall()
        except psycopg.errors.UndefinedTable:  # la memoria aun no recibio ningun caso: las tablas se crean con el primero
            return []
    return [(k, c, int(s), int(q), st) for k, c, s, q, st in found]


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--min-pairs", type=int, default=MIN_PAIRS)
    parser.add_argument("--json", help="escribe el informe en este archivo")
    args = parser.parse_args(argv)
    url = os.environ.get("ICF_DATABASE_URL")
    if not url:
        print("Falta ICF_DATABASE_URL", file=sys.stderr)
        return 2
    report = agreement(load_rows(url), args.min_pairs)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    if args.json:
        Path(args.json).write_text(text, encoding="utf8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
