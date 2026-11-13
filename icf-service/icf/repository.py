"""Consultas a PostgreSQL/pgvector del motor. Cada metodo devuelve [(codigo, titulo)]."""
from typing import List, Optional, Protocol, Sequence, Tuple

Pair = Tuple[str, str]


class Repo(Protocol):
    def annex_candidates(self, chapters: Sequence[int], age_group: str) -> List[Pair]: ...

    def chapter_codes(self, chapter: int) -> List[Pair]: ...

    def search(
        self,
        component: str,
        embedding: Sequence[float],
        limit: int,
        chapters: Optional[Sequence[int]] = None,
        levels: Sequence[int] = (2,),
    ) -> List[Pair]: ...

    def rank_codes(self, codes: Sequence[str], embedding: Sequence[float]) -> List[str]: ...

    def titles(self, codes: Sequence[str]) -> List[Pair]: ...

    def similar_cases(self, embedding: Sequence[float], limit: int, min_similarity: float) -> List[dict]: ...


class PgRepo:
    def __init__(self, conn):
        self.conn = conn

    def annex_candidates(self, chapters: Sequence[int], age_group: str) -> List[Pair]:
        """Codigos del Anexo ligados a los capitulos d indicados, validos para el grupo de edad."""
        if not chapters:
            return []
        domains = [f"D{n}" for n in chapters]
        rows = self.conn.execute(
            """SELECT m.code, c.title
               FROM icf_domain_map m JOIN icf_codes c ON c.code = m.code
               WHERE c.component = 'd' AND m.hab_domain = ANY(%s) AND m.ages IN ('both', %s)
               ORDER BY m.code""",
            (domains, age_group),
        ).fetchall()
        return [(code, title) for code, title in rows]

    def chapter_codes(self, chapter: int) -> List[Pair]:
        """Categorias de segundo nivel de un capitulo d (respaldo cuando el Anexo no trae candidatos).
        Sin los 'otros especificados / no especificados' (terminados en 8 y 9, ej. d298 y d299): no aportan."""
        rows = self.conn.execute(
            """SELECT code, title FROM icf_codes
               WHERE component = 'd' AND chapter = %s AND level = 2 AND code !~ '[89]$'
               ORDER BY code""",
            (chapter,),
        ).fetchall()
        return [(code, title) for code, title in rows]

    def rank_codes(self, codes: Sequence[str], embedding: Sequence[float]) -> List[str]:
        """Ordena los codigos dados por cercania al vector; los que no tienen embedding quedan al final."""
        if not codes:
            return []
        vector = "[" + ",".join(str(x) for x in embedding) + "]"
        rows = self.conn.execute(
            """SELECT code FROM icf_codes
               WHERE code = ANY(%s) AND embedding IS NOT NULL
               ORDER BY embedding <=> %s::vector""",
            (list(codes), vector),
        ).fetchall()
        ranked = [code for (code,) in rows]
        return ranked + [code for code in codes if code not in ranked]

    def search(
        self,
        component: str,
        embedding: Sequence[float],
        limit: int,
        chapters: Optional[Sequence[int]] = None,
        levels: Sequence[int] = (2,),
    ) -> List[Pair]:
        """Categorias mas cercanas al vector (distancia coseno), de los niveles y capitulos indicados.

        Por defecto solo nivel 2 (codigos de 3 digitos, ej. b730): medido con las pistas de referencia, buscar
        entre los de 4 y 5 digitos llena la lista de hermanos casi identicos (b2800, b2801, b2802...) y deja
        fuera los temas generales. Se excluyen las categorias 'otras especificadas / no especificadas', que
        no aportan: en la CIF los codigos terminados en 8 son 'otros especificados' y en 9 'no especificados'
        (los titulos del catalogo vienen truncados por el OCR, por eso no basta con filtrar por titulo). El filtro de capitulos va dentro de la consulta: filtrar despues puede dejar la lista vacia."""
        if chapters is not None and not chapters:
            return []
        vector = "[" + ",".join(str(x) for x in embedding) + "]"
        chap = list(chapters) if chapters is not None else None
        rows = self.conn.execute(
            """SELECT code, title FROM icf_codes
               WHERE component = %s AND level = ANY(%s::int[]) AND embedding IS NOT NULL
                 AND (%s::int[] IS NULL OR chapter = ANY(%s::int[]))
                 AND code !~ '[89]$'
                 AND title !~* '(otr[oa]s?[ ,]+especificad|no especificad)'
               ORDER BY embedding <=> %s::vector LIMIT %s""",
            (component, list(levels), chap, chap, vector, limit),
        ).fetchall()
        return [(code, title) for code, title in rows]

    def titles(self, codes: Sequence[str]) -> List[Pair]:
        """Codigos y titulos del catalogo, en el orden pedido; los que no existen se omiten."""
        rows = dict(self.conn.execute("SELECT code, title FROM icf_codes WHERE code = ANY(%s)", (list(codes),)).fetchall())
        return [(code, rows[code]) for code in codes if code in rows]

    # ---- memoria de casos confirmados por el medico (HU-07j) --------------------------------------------
    def ensure_case_schema(self) -> None:
        from pathlib import Path

        self.conn.execute(Path(__file__).resolve().parent.parent.joinpath("sql", "002_cases.sql").read_text(encoding="utf8"))

    def case_context(self, case_key: str) -> Optional[str]:
        row = self.conn.execute("SELECT context FROM icf_cases WHERE case_key = %s", (case_key,)).fetchone()
        return row[0] if row else None

    def upsert_case(self, case_key: str, context: str, diag: Optional[str], age_group: Optional[str],
                    embedding: Optional[Sequence[float]]) -> None:
        """Crea el caso o refresca su texto; `embedding` es None cuando el texto no cambio (se conserva el vector)."""
        if embedding is None:
            self.conn.execute("UPDATE icf_cases SET updated_at = now() WHERE case_key = %s", (case_key,))
            return
        vector = "[" + ",".join(str(x) for x in embedding) + "]"
        self.conn.execute(
            """INSERT INTO icf_cases (case_key, context, diag, age_group, embedding)
               VALUES (%s, %s, %s, %s, %s::vector)
               ON CONFLICT (case_key) DO UPDATE SET context = EXCLUDED.context, diag = EXCLUDED.diag,
                 age_group = EXCLUDED.age_group, embedding = EXCLUDED.embedding, updated_at = now()""",
            (case_key, context, diag, age_group, vector),
        )

    def upsert_case_code(self, case_key: str, item_ref: int, fields: dict) -> None:
        self.conn.execute(
            """INSERT INTO icf_case_codes (case_key, item_ref, component, code, status, qualifier, qualifier_cn,
                 qualifier_cl, qualifier_suggested, justification)
               VALUES (%(case_key)s, %(item_ref)s, %(component)s, %(code)s, %(status)s, %(qualifier)s, %(qualifier_cn)s,
                 %(qualifier_cl)s, %(qualifier_suggested)s, %(justification)s)
               ON CONFLICT (case_key, item_ref) DO UPDATE SET component = EXCLUDED.component, code = EXCLUDED.code,
                 status = EXCLUDED.status, qualifier = EXCLUDED.qualifier, qualifier_cn = EXCLUDED.qualifier_cn,
                 qualifier_cl = EXCLUDED.qualifier_cl, qualifier_suggested = EXCLUDED.qualifier_suggested,
                 justification = EXCLUDED.justification, updated_at = now()""",
            {"case_key": case_key, "item_ref": item_ref, **fields},
        )

    def delete_case_code(self, case_key: str, item_ref: int) -> None:
        """Quita un codigo (el medico lo rechazo despues de confirmarlo); si el caso queda vacio, se borra."""
        self.conn.execute("DELETE FROM icf_case_codes WHERE case_key = %s AND item_ref = %s", (case_key, item_ref))
        self.conn.execute(
            "DELETE FROM icf_cases c WHERE c.case_key = %s AND NOT EXISTS (SELECT 1 FROM icf_case_codes k WHERE k.case_key = c.case_key)",
            (case_key,),
        )

    def similar_cases(self, embedding: Sequence[float], limit: int, min_similarity: float) -> List[dict]:
        """Casos confirmados cuyo texto clinico se parece al vector (similitud coseno >= minimo), del mas al menos
        parecido, con sus codigos b y s. Si las tablas aun no existen devuelve []."""
        vector = "[" + ",".join(str(x) for x in embedding) + "]"
        try:
            cases = self.conn.execute(
                """SELECT case_key, diag, 1 - (embedding <=> %s::vector) AS similarity FROM icf_cases
                   WHERE 1 - (embedding <=> %s::vector) >= %s
                   ORDER BY embedding <=> %s::vector LIMIT %s""",
                (vector, vector, min_similarity, vector, limit),
            ).fetchall()
            if not cases:
                return []
            rows = self.conn.execute(
                """SELECT case_key, component, code, qualifier, justification FROM icf_case_codes
                   WHERE case_key = ANY(%s) AND component IN ('b', 's') ORDER BY item_ref""",
                ([key for key, _, _ in cases],),
            ).fetchall()
        except Exception as exc:  # tablas inexistentes u otro fallo: el motor sigue sin ejemplos
            if "UndefinedTable" in type(exc).__name__ or "does not exist" in str(exc):
                return []
            raise
        by_case: dict = {}
        for key, component, code, qualifier, justification in rows:
            by_case.setdefault(key, []).append(
                {"component": component, "code": code, "qualifier": qualifier, "justification": justification}
            )
        return [
            {"case_key": key, "diag": diag, "similarity": float(similarity), "codes": by_case.get(key, [])}
            for key, diag, similarity in cases if by_case.get(key)
        ]
