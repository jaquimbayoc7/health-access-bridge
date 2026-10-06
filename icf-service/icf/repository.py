"""Consultas a PostgreSQL/pgvector del motor. Cada metodo devuelve [(codigo, titulo)]."""
from typing import List, Protocol, Sequence, Tuple

Pair = Tuple[str, str]


class Repo(Protocol):
    def annex_candidates(self, chapters: Sequence[int], age_group: str) -> List[Pair]: ...

    def chapter_codes(self, chapter: int) -> List[Pair]: ...

    def search(self, component: str, embedding: Sequence[float], limit: int) -> List[Pair]: ...


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
        """Categorias de segundo nivel de un capitulo d (respaldo cuando el Anexo no trae candidatos)."""
        rows = self.conn.execute(
            "SELECT code, title FROM icf_codes WHERE component = 'd' AND chapter = %s AND level = 2 ORDER BY code",
            (chapter,),
        ).fetchall()
        return [(code, title) for code, title in rows]

    def search(self, component: str, embedding: Sequence[float], limit: int) -> List[Pair]:
        """Categorias de nivel 2 y 3 mas cercanas al vector (distancia coseno)."""
        vector = "[" + ",".join(str(x) for x in embedding) + "]"
        rows = self.conn.execute(
            """SELECT code, title FROM icf_codes
               WHERE component = %s AND level IN (2, 3) AND embedding IS NOT NULL
               ORDER BY embedding <=> %s::vector LIMIT %s""",
            (component, vector, limit),
        ).fetchall()
        return [(code, title) for code, title in rows]
