"""Carga el catalogo CIF-IA, el mapeo D1-D6 y los candidatos del Anexo en PostgreSQL.

Uso (desde icf-service/):
    python scripts/load_catalog.py --dry-run          # solo valida el TSV
    python scripts/load_catalog.py                    # valida y carga (usa ICF_DATABASE_URL)
"""
import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from icf.catalog import parse_catalog, validate  # noqa: E402
from icf.domain_map import ANNEX_CANDIDATES, HAB_DOMAINS, hab_domain_of  # noqa: E402

DEFAULT_CATALOG = ROOT.parent / "data" / "private" / "icf" / "catalog_cifia.tsv"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    ap.add_argument("--dry-run", action="store_true", help="solo valida, no escribe en la base")
    args = ap.parse_args()

    if not args.catalog.exists():
        print(f"No existe el catalogo: {args.catalog}", file=sys.stderr)
        return 2

    codes = parse_catalog(args.catalog)
    problems = validate(codes)
    known = {c.code for c in codes}
    missing = [code for _, code, _ in ANNEX_CANDIDATES if code not in known]
    problems += [f"candidato del Anexo ausente del catalogo: {code}" for code in missing]
    print(f"{len(codes)} codigos leidos de {args.catalog}")
    if problems:
        print(f"{len(problems)} problemas:", file=sys.stderr)
        for p in problems[:30]:
            print(f"  - {p}", file=sys.stderr)
        return 1
    if args.dry_run:
        print("Catalogo valido (dry-run, no se escribio nada).")
        return 0

    import psycopg  # import tardio: el dry-run no necesita la base

    url = os.environ.get("ICF_DATABASE_URL")
    if not url:
        print("Falta la variable ICF_DATABASE_URL", file=sys.stderr)
        return 2
    schema = (ROOT / "sql" / "001_schema.sql").read_text(encoding="utf-8")

    with psycopg.connect(url) as conn:
        conn.execute(schema)
        # Padres primero (nivel ascendente) para respetar la clave foranea.
        ordered = sorted(codes, key=lambda c: (c.level, c.code))
        with conn.cursor() as cur:
            cur.executemany(
                """INSERT INTO icf_codes (code, component, chapter, level, parent, title, source)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT (code) DO UPDATE SET
                     component = EXCLUDED.component, chapter = EXCLUDED.chapter, level = EXCLUDED.level,
                     parent = EXCLUDED.parent, title = EXCLUDED.title, source = EXCLUDED.source""",
                [(c.code, c.component, c.chapter, c.level, c.parent, c.title, c.source) for c in ordered],
            )
            cur.executemany(
                """INSERT INTO icf_hab_domains (hab_domain, chapter_code, chapter_name, official_domain, note)
                   VALUES (%s, %s, %s, %s, %s)
                   ON CONFLICT (hab_domain) DO UPDATE SET
                     chapter_code = EXCLUDED.chapter_code, chapter_name = EXCLUDED.chapter_name,
                     official_domain = EXCLUDED.official_domain, note = EXCLUDED.note""",
                [(d.hab_domain, d.chapter_code, d.chapter_name, d.official_domain, d.note) for d in HAB_DOMAINS],
            )
            cur.executemany(
                """INSERT INTO icf_domain_map (official_domain, code, hab_domain, ages)
                   VALUES (%s, %s, %s, %s)
                   ON CONFLICT (official_domain, code) DO UPDATE SET
                     hab_domain = EXCLUDED.hab_domain, ages = EXCLUDED.ages""",
                [(dom, code, hab_domain_of(code), ages) for dom, code, ages in ANNEX_CANDIDATES],
            )
        conn.commit()
        n = conn.execute("SELECT count(*) FROM icf_codes").fetchone()[0]
    print(f"Carga completa: {n} codigos en icf_codes, {len(HAB_DOMAINS)} dominios HAB, {len(ANNEX_CANDIDATES)} candidatos del Anexo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
