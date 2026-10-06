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
        levels: Sequence[int] = (2, 3),
        column: str = "embedding",
    ) -> List[Pair]: ...

    def rank_codes(self, codes: Sequence[str], embedding: Sequence[float]) -> List[str]: ...


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

    EMBEDDING_COLUMNS = ("embedding", "embedding_rich")  # lista cerrada: el nombre va en el SQL

    def search(
        self,
        component: str,
        embedding: Sequence[float],
        limit: int,
        chapters: Optional[Sequence[int]] = None,
        levels: Sequence[int] = (2, 3),
        column: str = "embedding",
    ) -> List[Pair]:
        """Categorias mas cercanas al vector (distancia coseno), de los niveles y capitulos indicados.
        El filtro va dentro de la consulta: filtrar despues puede dejar la lista vacia.
        `column`: 'embedding' (titulo) o 'embedding_rich' (titulo + titulos de sus hijos, solo nivel 2)."""
        if column not in self.EMBEDDING_COLUMNS:
            raise ValueError(f"columna de embedding no permitida: {column}")
        if chapters is not None and not chapters:
            return []
        vector = "[" + ",".join(str(x) for x in embedding) + "]"
        chap = list(chapters) if chapters is not None else None
        rows = self.conn.execute(
            f"""SELECT code, title FROM icf_codes
               WHERE component = %s AND level = ANY(%s::int[]) AND {column} IS NOT NULL
                 AND (%s::int[] IS NULL OR chapter = ANY(%s::int[]))
               ORDER BY {column} <=> %s::vector LIMIT %s""",
            (component, list(levels), chap, chap, vector, limit),
        ).fetchall()
        return [(code, title) for code, title in rows]
