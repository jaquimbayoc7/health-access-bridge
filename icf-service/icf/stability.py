"""Repetibilidad del sistema (HU-07g): si se corre varias veces el mismo caso, ¿sugiere los mismos codigos?

El LLM no es determinista. Se mide con el kappa de Fleiss entre corridas (cada corrida es un «evaluador»), como en
Liu et al. 2026, y con el indice de Jaccard entre pares de corridas. Logica pura, sin base de datos ni Ollama.
"""
from itertools import combinations
from typing import Dict, List, Optional, Sequence, Set

CHAPTERS = {"b": 8, "s": 8, "d": 9}  # capitulos de primer nivel de la CIF por componente


def fleiss_kappa_binary(yes_counts: Sequence[int], raters: int) -> Optional[float]:
    """Kappa de Fleiss para decisiones si/no: yes_counts[i] = corridas (de `raters`) que dijeron «si» en el elemento i."""
    items = len(yes_counts)
    if not items or raters < 2:
        return None
    p_bar = sum((k * (k - 1) + (raters - k) * (raters - k - 1)) / (raters * (raters - 1)) for k in yes_counts) / items
    p_yes = sum(yes_counts) / (items * raters)
    p_exp = p_yes ** 2 + (1 - p_yes) ** 2
    if p_exp >= 1:
        return None
    return round((p_bar - p_exp) / (1 - p_exp), 3)


def jaccard(a: Set[str], b: Set[str]) -> float:
    return 1.0 if not a and not b else len(a & b) / len(a | b)


def compute_stability(runs: Dict[str, List[Dict[str, Set[str]]]]) -> Dict:
    """runs: {caso: [ {'b': {codigos}, 's': ..., 'd': ...} por corrida ]}. Todos los casos con el mismo numero de corridas (>= 2).

    - chapter_kappa: Fleiss entre corridas sobre presencia/ausencia de cada capitulo (universo fijo; comparable con el kappa por capitulo de la validacion).
    - code_kappa: igual por codigo, sobre los codigos que aparecieron en alguna corrida del caso (excluye codigos que nunca salen, por lo que es conservador).
    - mean_jaccard: parecido medio entre pares de corridas, promediado por caso y componente.
    - stable_code_share: de los codigos que salieron alguna vez, proporcion que salio en todas las corridas.
    """
    cases = {c: r for c, r in runs.items() if len(r) >= 2}
    if not cases:
        return {"cases": 0, "runs_per_case": 0, "chapter_kappa": None, "code_kappa": None, "mean_jaccard": None, "stable_code_share": None}
    n_runs = min(len(r) for r in cases.values())
    chapter_counts: List[int] = []
    code_counts: List[int] = []
    jaccards: List[float] = []
    union_total = stable_total = 0
    per_case: Dict[str, Dict] = {}
    for case, case_runs in cases.items():
        case_runs = case_runs[:n_runs]
        case_j: List[float] = []
        for comp, n_chapters in CHAPTERS.items():
            sets = [r.get(comp, set()) for r in case_runs]
            for ch in range(1, n_chapters + 1):
                chapter_counts.append(sum(1 for s in sets if any(c[:2] == f"{comp}{ch}" for c in s)))
            union = set().union(*sets)
            for code in union:
                k = sum(1 for s in sets if code in s)
                code_counts.append(k)
                union_total += 1
                stable_total += k == n_runs
            pair_j = [jaccard(a, b) for a, b in combinations(sets, 2)]
            jaccards.extend(pair_j)
            case_j.extend(pair_j)
        per_case[case] = {"mean_jaccard": round(sum(case_j) / len(case_j), 3)}
    return {
        "cases": len(cases),
        "runs_per_case": n_runs,
        "chapter_kappa": fleiss_kappa_binary(chapter_counts, n_runs),
        "code_kappa": fleiss_kappa_binary(code_counts, n_runs),
        "mean_jaccard": round(sum(jaccards) / len(jaccards), 3),
        "stable_code_share": round(stable_total / union_total, 3) if union_total else None,
        "per_case": per_case,
    }
