"""Lectura y validacion del catalogo CIF-IA (solo local, no esta en el repositorio)."""
import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

CODE_RE = re.compile(r"^[bsde]\d{3,5}$")


@dataclass(frozen=True)
class IcfCode:
    code: str
    component: str
    chapter: int
    level: int  # 2 = categoria (3 digitos), 3 = 4 digitos, 4 = 5 digitos
    parent: Optional[str]
    title: str
    source: str


def level_of(code: str) -> int:
    return len(code) - 2


def parent_of(code: str) -> Optional[str]:
    """El padre es el codigo sin su ultimo digito; las categorias de nivel 2 no tienen padre en el catalogo."""
    return code[:-1] if level_of(code) >= 3 else None


def parse_catalog(path: Path) -> List[IcfCode]:
    """Lee el TSV (Code, Level, Component, Parent, Title, Source) y lo devuelve ordenado por codigo."""
    rows: List[IcfCode] = []
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for raw in csv.DictReader(fh, delimiter="\t"):
            code = raw["Code"].strip()
            rows.append(
                IcfCode(
                    code=code,
                    component=code[0],
                    chapter=int(code[1]),
                    level=level_of(code),
                    parent=parent_of(code),
                    title=raw["Title"].strip(),
                    source=(raw.get("Source") or "").strip(),
                )
            )
    return sorted(rows, key=lambda r: r.code)


def validate(codes: List[IcfCode]) -> List[str]:
    """Devuelve la lista de problemas encontrados (vacia si el catalogo es consistente)."""
    problems: List[str] = []
    seen: Dict[str, int] = {}
    for c in codes:
        seen[c.code] = seen.get(c.code, 0) + 1
    problems += [f"codigo duplicado: {k}" for k, n in seen.items() if n > 1]
    for c in codes:
        if not CODE_RE.match(c.code):
            problems.append(f"formato invalido: {c.code}")
        if not c.title:
            problems.append(f"sin titulo: {c.code}")
        if c.parent and c.parent not in seen:
            problems.append(f"huerfano: {c.code} (falta {c.parent})")
    return problems
