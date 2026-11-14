r"""Carga en la memoria de casos (HU-07j) los casos que la profesional de salud valido a ciegas en la validacion clinica (HU-07g).

Para cada caso con diagnostico o notas toma lo que ella escribio en la Fase A (sin ver la sugerencia): los codigos de funciones (b) y estructuras (s) con su
gravedad, y los guarda como un caso confirmado (case_key «medica-<id>»). La gravedad cero («no hay problema») no se carga. Como no hay sugerencia del sistema
en una Fase A a ciegas, `qualifier_suggested` queda vacio y estos codigos no entran al informe de acuerdo (case_memory_report.py).

Los casos son sinteticos (C01-C25 y N01-N24) y la hoja con las respuestas de ella es privada (data/private/, fuera del repositorio).

Uso, en el PC del servicio (necesita openpyxl, psycopg y Ollama con bge-m3):
    python icf-service/scripts/load_validated_cases.py --dry-run
    python icf-service/scripts/load_validated_cases.py --sql-out casos_medica.sql
    docker exec -i icf-db psql -U icf_user -d icf < casos_medica.sql        # no necesita la clave de la base
o directo contra la base (ICF_DATABASE_URL):
    python icf-service/scripts/load_validated_cases.py --database-url postgresql://icf_user:<clave>@127.0.0.1:5433/icf

ADVERTENCIA de medicion: estos casos son los mismos con los que se midio el motor. Con ellos en la memoria, volver a medir el motor sobre C01-C25 o N01-N24
exige excluir el propio caso (scripts/evaluate_memory.py lo hace: deja uno fuera). Sin esa exclusion la medicion seria circular.
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
REVIEW = ROOT.parent / "data" / "private" / "icf" / "review"

from icf.schemas import CaseRecord, PatientContext  # noqa: E402

SHEETS = (
    (REVIEW / "hoja_revision_v2.xlsx", ROOT / "reference" / "cases.json"),  # rondas 1 y 2: C01-C25
    (REVIEW / "hoja_ronda3.xlsx", ROOT / "reference" / "cases_ronda2.json"),  # ronda 3: N01-N24
)


def records_for_case(case: dict, blind: Dict[str, List[str]], severity: Dict[str, int]) -> List[CaseRecord]:
    """Codigos b y s que la revisora eligio a ciegas en un caso, con su gravedad, como registros de la memoria.
    Se omiten los de gravedad 0 y los placeholders (b000, s000). Devuelve [] si el caso no tiene diagnostico ni notas."""
    patient = PatientContext(**case["patient"])
    if not (patient.diag_cie or patient.clinical_notes):
        return []
    out: List[CaseRecord] = []
    ref = 0
    for component in ("b", "s"):
        for code in sorted(blind.get(component, [])):
            level = severity.get(code)
            if code.endswith("000") or level == 0:
                continue
            ref += 1
            out.append(CaseRecord(
                case_key=f"medica-{case['id']}", item_ref=ref, component=component, code=code, status="aceptado",
                qualifier=level, qualifier_suggested=None, justification=None, patient=patient,
            ))
    return out


def load_validated(sheets: Iterable[Tuple[Path, Path]] = SHEETS) -> List[CaseRecord]:
    import review_sheet

    records: List[CaseRecord] = []
    for sheet, cases_file in sheets:
        _ratings, _missing, blind, _suggested, blind_q, _sq = review_sheet.read_filled(sheet)
        cases = {c["id"]: c for c in json.loads(Path(cases_file).read_text(encoding="utf8"))["cases"]}
        for case_id, comps in blind.items():
            if case_id in cases:
                records += records_for_case(cases[case_id], {k: sorted(v) for k, v in comps.items()}, blind_q.get(case_id, {}))
    return records


# ------------------------------------------------------------------ salida en SQL (para cargar sin la clave de la base)
def _q(value) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


class SqlWriter:
    """Imita al repositorio de la memoria pero escribe sentencias SQL: sirve para cargar con `docker exec -i icf-db psql`."""

    def __init__(self):
        self.lines: List[str] = []
        self._contexts: Dict[str, str] = {}

    def case_context(self, case_key: str) -> Optional[str]:
        return self._contexts.get(case_key)

    def upsert_case(self, case_key, context, diag, age_group, embedding):
        self._contexts[case_key] = context
        if embedding is None:
            return
        vector = "[" + ",".join(str(x) for x in embedding) + "]"
        self.lines.append(
            f"INSERT INTO icf_cases (case_key, context, diag, age_group, embedding) VALUES ({_q(case_key)}, {_q(context)}, {_q(diag)}, {_q(age_group)}, '{vector}'::vector) "
            "ON CONFLICT (case_key) DO UPDATE SET context = EXCLUDED.context, diag = EXCLUDED.diag, age_group = EXCLUDED.age_group, embedding = EXCLUDED.embedding, updated_at = now();"
        )

    def upsert_case_code(self, case_key, item_ref, fields):
        cols = ["case_key", "item_ref"] + list(fields)
        vals = [_q(case_key), _q(item_ref)] + [_q(fields[k]) for k in fields]
        self.lines.append(
            f"INSERT INTO icf_case_codes ({', '.join(cols)}) VALUES ({', '.join(vals)}) "
            "ON CONFLICT (case_key, item_ref) DO UPDATE SET component = EXCLUDED.component, code = EXCLUDED.code, status = EXCLUDED.status, "
            "qualifier = EXCLUDED.qualifier, qualifier_cn = EXCLUDED.qualifier_cn, qualifier_cl = EXCLUDED.qualifier_cl, "
            "qualifier_suggested = EXCLUDED.qualifier_suggested, justification = EXCLUDED.justification, updated_at = now();"
        )

    def delete_case_code(self, case_key, item_ref):  # no se usa: aqui solo se agregan casos
        raise NotImplementedError

    def script(self, schema_sql: str) -> str:
        return "BEGIN;\n" + schema_sql + "\n" + "\n".join(self.lines) + "\nCOMMIT;\n"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--dry-run", action="store_true", help="solo cuenta lo que se cargaria")
    parser.add_argument("--sql-out", help="escribe un script SQL en vez de conectarse a la base")
    parser.add_argument("--database-url", help="carga directo en la base (por defecto, ICF_DATABASE_URL)")
    args = parser.parse_args(argv)

    records = load_validated()
    cases = sorted({r.case_key for r in records})
    print(f"{len(records)} codigos b/s de {len(cases)} casos validados a ciegas por la profesional")
    if args.dry_run:
        return 0

    from icf.cases import store_case
    from icf.config import load_settings
    from icf.runtime import OllamaFns

    fns = OllamaFns(load_settings())
    if args.sql_out:
        writer = SqlWriter()
        for r in records:
            store_case(r, writer, fns.embed)
        schema = (ROOT / "sql" / "002_cases.sql").read_text(encoding="utf8")
        Path(args.sql_out).write_text(writer.script(schema), encoding="utf8")
        print(f"script escrito en {args.sql_out}: cargalo con `docker exec -i icf-db psql -U icf_user -d icf < {args.sql_out}` y luego borralo (es texto clinico sintetico, pero privado)")
        return 0

    import os

    import psycopg

    from icf.repository import PgRepo

    url = args.database_url or os.environ.get("ICF_DATABASE_URL")
    if not url:
        print("Falta --database-url, ICF_DATABASE_URL o --sql-out", file=sys.stderr)
        return 2
    with psycopg.connect(url, autocommit=True, connect_timeout=5) as conn:
        repo = PgRepo(conn)
        repo.ensure_case_schema()
        for r in records:
            store_case(r, repo, fns.embed)
    print("casos cargados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
