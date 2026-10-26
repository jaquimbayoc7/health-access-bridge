"""Metricas de la validacion clinica (HU-07g). Logica pura, sin Excel ni base de datos.

La revisora (profesional en salud) trabaja en dos fases:
  Fase A (a ciegas): escribe los codigos de funciones (b) y estructuras (s) que ella elegiria, sin ver la sugerencia,
    con la gravedad 0-4 tras un punto (b730.3). Esa gravedad se compara con la del sistema (kappa ponderado).
  Fase B: valora cada codigo sugerido (Adecuado / Aceptable / No adecuado), si el calificador es correcto y que codigos faltan.

Los codigos se comparan por su codigo de 3 digitos (letra + 3 numeros): la busqueda del motor solo propone
codigos de ese nivel, y un codigo mas especifico de la revisora (b7301) cuenta para su codigo de 3 digitos (b730).
"""
import math
import random
import re
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Set, Tuple

COMPONENTS = ("b", "s", "d")
RATINGS = {"adecuado": "A", "aceptable": "B", "no adecuado": "C"}
RATING_OPTIONS = ("Adecuado", "Aceptable", "No adecuado")
YES_NO_OPTIONS = ("Sí", "Parcial", "No")

# Umbrales aprobados por el responsable del proyecto el 07-oct-2026; se presentan a la revisora en la reunion de la semana siguiente.
# Se aplican a funciones y estructuras (b y s); las actividades (d) salen de una lista cerrada del Anexo y se miden aparte.
THRESHOLDS = {
    "min_cases_reviewed": 20,  # de 24 casos aplicables
    "body_precision_strict": 0.60,  # solo "Adecuado"
    "body_precision_lenient": 0.80,  # "Adecuado" + "Aceptable"
    "body_blind_recall": 0.60,  # de lo que ella eligio a ciegas, cuanto estaba en la sugerencia
    "qualifier_weighted_kappa": 0.50,  # kappa ponderado del calificador 0-4 en los codigos que coinciden; 0,50 = limite inferior del rango de expertos CIF (Chen 2016) y cercano a la mediana humana (Okochi 2005); ver protocolo 4.6
    "min_qualifier_pairs": 30,  # con menos codigos coincidentes el IC del kappa es demasiado ancho (~0,6 con 10 pares, ~0,33 con 30); ver protocolo 4.4
    "activities_precision_lenient": 0.80,
}

# IC por bootstrap de casos (Field y Welsh 2007): se remuestrean los casos, no los codigos, porque los codigos de un caso estan correlacionados.
BOOTSTRAP_REPS = 2000
BOOTSTRAP_SEED = 20261021  # semilla fija: el mismo informe da siempre el mismo IC

# Piso para el limite inferior del IC 95 % (Wilson), nivel minimo aceptable segun Flahault 2005 / Koo y Li 2016. Evita aprobar con muy pocos codigos.
# Los valores son criterio del proyecto (sustento y analisis de potencia en docs/reports/PROTOCOLO_VALIDACION_CLINICA_HU07G.md, 4.3); pendientes de aprobacion del responsable.
CI_FLOORS = {
    "body_precision_strict": 0.40,
    "body_precision_lenient": 0.60,
    "body_blind_recall": 0.40,
    "activities_precision_lenient": 0.60,
}

CODE_RE = re.compile(r"\b([bsd])\s*(\d{3,5})\b", re.IGNORECASE)
CODE_QUALIFIER_RE = re.compile(r"\b([bsd])\s*(\d{3,5})(?:\s*[.:]\s*([0-4]))?", re.IGNORECASE)
QUALIFIER_LEVELS = 5  # calificador de gravedad 0-4


def normalize_codes(text: Optional[str]) -> Set[str]:
    """'b730, B7301 y s750' -> {'b730', 's750'}: letra + 3 digitos, sin duplicados."""
    if not text:
        return set()
    return {f"{m.group(1).lower()}{m.group(2)[:3]}" for m in CODE_RE.finditer(str(text))}


def parse_code_qualifiers(text: Optional[str]) -> Dict[str, int]:
    """'b730.3, b735, s750.2' -> {'b730': 3, 's750': 2}: gravedad 0-4 que la revisora escribe tras el codigo (los sin calificador se omiten)."""
    if not text:
        return {}
    out: Dict[str, int] = {}
    for m in CODE_QUALIFIER_RE.finditer(str(text)):
        if m.group(3) is not None:
            out[f"{m.group(1).lower()}{m.group(2)[:3]}"] = int(m.group(3))
    return out


def parse_severity(value) -> Optional[int]:
    """Gravedad 0-4 de la celda «Calificador» de la hoja: 3 -> 3, '3.88' (estructuras) -> 3; 8/9 (sin especificar) -> None."""
    if value is None:
        return None
    m = re.match(r"\s*([0-4])(?:\D|$)", str(value))
    return int(m.group(1)) if m else None


def normalize_rating(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    return RATINGS.get(str(value).strip().lower())


def normalize_yes_no(value: Optional[str]) -> Optional[float]:
    """Sí = 1, Parcial = 0.5, No = 0; vacio = sin evaluar."""
    if value is None:
        return None
    key = str(value).strip().lower().replace("í", "i")
    return {"si": 1.0, "parcial": 0.5, "no": 0.0}.get(key)


def _ratio(num: float, den: float) -> Optional[float]:
    return round(num / den, 3) if den else None


def wilson_interval(successes: int, total: int, z: float = 1.96) -> Optional[Tuple[float, float]]:
    """IC 95 % de Wilson para una proporcion. Los codigos de un mismo caso no son independientes, asi que es una cota optimista."""
    if not total:
        return None
    p = successes / total
    denom = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denom
    half = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denom
    return round(max(0.0, centre - half), 3), round(min(1.0, centre + half), 3)


def cohen_kappa_binary(pairs: Iterable[Tuple[bool, bool]]) -> Optional[float]:
    """Kappa de Cohen para decisiones si/no de dos evaluadores. None si no hay datos o el azar esperado es 1."""
    pairs = list(pairs)
    n = len(pairs)
    if not n:
        return None
    both = sum(1 for a, b in pairs if a and b)
    neither = sum(1 for a, b in pairs if not a and not b)
    observed = (both + neither) / n
    a_yes = sum(1 for a, _ in pairs if a) / n
    b_yes = sum(1 for _, b in pairs if b) / n
    expected = a_yes * b_yes + (1 - a_yes) * (1 - b_yes)
    if expected >= 1:
        return None
    return round((observed - expected) / (1 - expected), 3)


def _chapters(codes: Set[str]) -> Set[str]:
    """{'b730', 'b152'} -> {'b7', 'b1'}: primer nivel de la CIF (capitulo)."""
    return {c[:2] for c in codes}


def weighted_kappa(pairs: Iterable[Tuple[int, int]], levels: int = QUALIFIER_LEVELS) -> Optional[float]:
    """Kappa ponderado de Cohen (1968) con pesos lineales para una escala ordinal 0..levels-1. None si no hay datos o no hay variacion."""
    pairs = list(pairs)
    n = len(pairs)
    if not n:
        return None
    observed = [[0.0] * levels for _ in range(levels)]
    for a, b in pairs:
        observed[a][b] += 1 / n
    row = [sum(observed[i]) for i in range(levels)]
    col = [sum(observed[i][j] for i in range(levels)) for j in range(levels)]
    obs_dis = exp_dis = 0.0
    for i in range(levels):
        for j in range(levels):
            w = abs(i - j) / (levels - 1)
            obs_dis += w * observed[i][j]
            exp_dis += w * row[i] * col[j]
    if exp_dis == 0:
        return None
    return round(1 - obs_dis / exp_dis, 3)


def cluster_bootstrap_ci(
    clusters: Sequence,
    statistic: Callable[[Sequence], Optional[float]],
    reps: int = BOOTSTRAP_REPS,
    seed: int = BOOTSTRAP_SEED,
) -> Optional[Tuple[float, float]]:
    """IC 95 % por percentiles remuestreando clusters (casos) con reemplazo.

    clusters: un elemento por caso; statistic(lista de clusters) -> valor o None.
    Devuelve None con menos de 2 casos o si mas del 10 % de las remuestras no permiten calcular el estadistico.
    """
    clusters = list(clusters)
    n = len(clusters)
    if n < 2 or reps < 1:
        return None
    rng = random.Random(seed)
    values: List[float] = []
    for _ in range(reps):
        value = statistic([clusters[rng.randrange(n)] for _ in range(n)])
        if value is not None:
            values.append(value)
    if len(values) < 0.9 * reps:
        return None
    values.sort()
    last = len(values) - 1
    return round(values[int(0.025 * last)], 3), round(values[math.ceil(0.975 * last)], 3)


def _ratio_of_sums(num_idx: int, den_idx: int) -> Callable[[Sequence], Optional[float]]:
    """Estadistico razon sum(num)/sum(den) sobre tuplas por caso."""
    def stat(sample):
        den = sum(c[den_idx] for c in sample)
        return sum(c[num_idx] for c in sample) / den if den else None
    return stat


def _qualifier_pairs_by_case(blind_q: Dict, suggested_q: Dict, blind: Dict, suggested: Dict) -> Dict[str, List[Tuple[int, int]]]:
    """Gravedad a ciegas vs gravedad del sistema, solo en codigos b y s que ambos eligieron y que tienen gravedad 0-4 en ambos."""
    by_case: Dict[str, List[Tuple[int, int]]] = {}
    for case, comps in blind.items():
        for comp in ("b", "s"):
            for code in comps.get(comp, set()) & suggested.get(case, {}).get(comp, set()):
                mine, system = blind_q.get(case, {}).get(code), suggested_q.get(case, {}).get(code)
                if mine is not None and system is not None:
                    by_case.setdefault(case, []).append((mine, system))
    return by_case


def _qualifier_agreement(by_case: Dict[str, List[Tuple[int, int]]], reps: int = BOOTSTRAP_REPS) -> Dict:
    pairs = [p for case_pairs in by_case.values() for p in case_pairs]
    n = len(pairs)
    return {
        "pairs": n,
        "cases": len(by_case),
        "exact": _ratio(sum(1 for a, b in pairs if a == b), n),
        "within_one": _ratio(sum(1 for a, b in pairs if abs(a - b) <= 1), n),
        "weighted_kappa": weighted_kappa(pairs),
        "weighted_kappa_ci95_cases": cluster_bootstrap_ci(
            list(by_case.values()), lambda sample: weighted_kappa([p for c in sample for p in c]), reps
        ),
    }


def compute_metrics(
    ratings: Iterable[Dict],
    missing: Dict[str, Dict[str, Set[str]]],
    blind: Dict[str, Dict[str, Set[str]]],
    suggested: Dict[str, Dict[str, Set[str]]],
    blind_qualifiers: Optional[Dict[str, Dict[str, int]]] = None,
    suggested_qualifiers: Optional[Dict[str, Dict[str, int]]] = None,
    bootstrap_reps: int = BOOTSTRAP_REPS,
) -> Dict:
    """Calcula las metricas.

    ratings:   [{'case', 'component', 'code', 'rating': 'A|B|C|None', 'qualifier_ok': 1/0.5/0/None}]
    missing:   {case: {'b': {codigos que faltan}, 's': ...}} (Fase B, hoja Faltantes)
    blind:     {case: {'b': {codigos que ella eligio a ciegas}, 's': ...}} (Fase A)
    suggested: {case: {'b': {codigos sugeridos}, 's': ..., 'd': ...}}
    bootstrap_reps: remuestras del IC por casos (0 lo desactiva).
    """
    ratings = list(ratings)
    out: Dict = {"components": {}, "cases_reviewed": 0}
    reviewed_cases = {r["case"] for r in ratings if r["rating"]}
    out["cases_reviewed"] = len(reviewed_cases)

    def by_case_tallies(components: Sequence[str]) -> List[Tuple[int, int, int]]:
        """(adecuado + aceptable, adecuado, valorados) por caso, para el bootstrap."""
        tallies: Dict[str, List[int]] = {}
        for r in ratings:
            if r["component"] in components and r["rating"]:
                t = tallies.setdefault(r["case"], [0, 0, 0])
                t[0] += r["rating"] in ("A", "B")
                t[1] += r["rating"] == "A"
                t[2] += 1
        return [tuple(t) for t in tallies.values()]  # type: ignore[misc]

    for comp in COMPONENTS:
        rows = [r for r in ratings if r["component"] == comp and r["rating"]]
        total = len(rows)
        a = sum(1 for r in rows if r["rating"] == "A")
        b = sum(1 for r in rows if r["rating"] == "B")
        c = sum(1 for r in rows if r["rating"] == "C")
        q_rows = [r["qualifier_ok"] for r in ratings if r["component"] == comp and r.get("qualifier_ok") is not None]
        miss = sum(len(v.get(comp, set())) for v in missing.values())
        out["components"][comp] = {
            "suggested_rated": total,
            "adecuado": a,
            "aceptable": b,
            "no_adecuado": c,
            "precision_strict": _ratio(a, total),
            "precision_lenient": _ratio(a + b, total),
            "missing_codes": miss,
            "coverage": _ratio(a + b, a + b + miss) if (a + b + miss) else None,
            "qualifier_ok": _ratio(sum(q_rows), len(q_rows)),
        }

    # Fase A: a ciegas, solo b y s
    blind_hits = blind_expected = blind_suggested = 0
    blind_cases = 0
    blind_by_case: List[Tuple[int, int]] = []  # (aciertos, elegidos a ciegas) por caso, para el bootstrap
    chapter_pairs: List[Tuple[bool, bool]] = []
    chapter_hits = chapter_expected = 0
    for case, comps in blind.items():
        counted = False
        case_hits = case_expected = 0
        for comp in ("b", "s"):
            expected = comps.get(comp, set())
            sug = suggested.get(case, {}).get(comp, set())
            if expected:
                counted = True
                blind_hits += len(expected & sug)
                blind_expected += len(expected)
                case_hits += len(expected & sug)
                case_expected += len(expected)
        if counted:
            blind_cases += 1
            blind_by_case.append((case_hits, case_expected))
        # precision y kappa por capitulo se miden en los casos donde la revisora trabajo (eligio codigos o valoro la sugerencia)
        if counted or case in reviewed_cases:
            for comp in ("b", "s"):
                expected = comps.get(comp, set())
                sug = suggested.get(case, {}).get(comp, set())
                blind_suggested += len(sug)
                exp_ch, sug_ch = _chapters(expected), _chapters(sug)
                chapter_hits += len(exp_ch & sug_ch)
                chapter_expected += len(exp_ch)
                for n in range(1, 9):
                    ch = f"{comp}{n}"
                    chapter_pairs.append((ch in exp_ch, ch in sug_ch))
    # Acuerdo positivo especifico = F1 (Hripcsak & Rothschild 2005): util cuando no hay "negativos" definidos entre codigos
    precision = _ratio(blind_hits, blind_suggested)
    recall = _ratio(blind_hits, blind_expected)
    if precision is None or recall is None:
        f1 = None
    else:
        f1 = round(2 * precision * recall / (precision + recall), 3) if precision + recall else 0.0
    out["blind"] = {
        "cases": blind_cases,
        "expected_codes": blind_expected,
        "found_in_suggestion": blind_hits,
        "recall": recall,
        "recall_ci95": wilson_interval(blind_hits, blind_expected),
        "recall_ci95_cases": cluster_bootstrap_ci(blind_by_case, _ratio_of_sums(0, 1), bootstrap_reps),
        "suggested_codes": blind_suggested,
        "precision": precision,
        "f1": f1,
        "chapter_recall": _ratio(chapter_hits, chapter_expected),
        "chapter_kappa": cohen_kappa_binary(chapter_pairs),
    }

    # b + s juntos
    bs = [out["components"][c] for c in ("b", "s")]
    tot = sum(x["suggested_rated"] for x in bs)
    a_bs = sum(x["adecuado"] for x in bs)
    b_bs = sum(x["aceptable"] for x in bs)
    q_all = [r["qualifier_ok"] for r in ratings if r["component"] in ("b", "s") and r.get("qualifier_ok") is not None]
    out["body"] = {
        "suggested_rated": tot,
        "precision_strict": _ratio(a_bs, tot),
        "precision_strict_ci95": wilson_interval(a_bs, tot),
        "precision_lenient": _ratio(a_bs + b_bs, tot),
        "precision_lenient_ci95": wilson_interval(a_bs + b_bs, tot),
        "qualifier_ok": _ratio(sum(q_all), len(q_all)),
    }
    d = out["components"]["d"]
    d["precision_lenient_ci95"] = wilson_interval(d["adecuado"] + d["aceptable"], d["suggested_rated"])
    body_cases = by_case_tallies(("b", "s"))
    out["body"]["precision_strict_ci95_cases"] = cluster_bootstrap_ci(body_cases, _ratio_of_sums(1, 2), bootstrap_reps)
    out["body"]["precision_lenient_ci95_cases"] = cluster_bootstrap_ci(body_cases, _ratio_of_sums(0, 2), bootstrap_reps)
    d["precision_lenient_ci95_cases"] = cluster_bootstrap_ci(by_case_tallies(("d",)), _ratio_of_sums(0, 2), bootstrap_reps)
    pairs_by_case = _qualifier_pairs_by_case(blind_qualifiers or {}, suggested_qualifiers or {}, blind, suggested)
    out["qualifier_agreement"] = _qualifier_agreement(pairs_by_case, bootstrap_reps)
    return out


def evaluate_thresholds(metrics: Dict, thresholds: Dict = THRESHOLDS, floors: Dict = CI_FLOORS) -> Dict:
    """Compara con los umbrales. Un criterio con IC solo cumple si el valor alcanza la meta Y el limite inferior del IC 95 % (Wilson) alcanza el piso.

    El IC por bootstrap de casos se informa en cada criterio (`ic95_casos`) pero no decide: con el tamano de muestra previsto la simulacion
    (protocolo 4.4) da el mismo resultado que Wilson, porque manda alcanzar la meta.
    """
    t = thresholds
    d = metrics["components"]["d"]
    body, blind, qa = metrics["body"], metrics["blind"], metrics["qualifier_agreement"]
    kappa_w = qa["weighted_kappa"] if qa["pairs"] >= t["min_qualifier_pairs"] else None
    # (nombre, valor, meta, IC95 Wilson, piso del limite inferior, IC95 bootstrap de casos)
    checks: List[Tuple[str, Optional[float], float, Optional[Tuple[float, float]], Optional[float], Optional[Tuple[float, float]]]] = [
        ("Casos revisados", metrics["cases_reviewed"], t["min_cases_reviewed"], None, None, None),
        ("Precision estricta b+s", body["precision_strict"], t["body_precision_strict"], body.get("precision_strict_ci95"), floors.get("body_precision_strict"), body.get("precision_strict_ci95_cases")),
        ("Precision flexible b+s", body["precision_lenient"], t["body_precision_lenient"], body.get("precision_lenient_ci95"), floors.get("body_precision_lenient"), body.get("precision_lenient_ci95_cases")),
        ("Cobertura a ciegas b+s", blind["recall"], t["body_blind_recall"], blind.get("recall_ci95"), floors.get("body_blind_recall"), blind.get("recall_ci95_cases")),
        ("Calificador b+s (kappa ponderado)", kappa_w, t["qualifier_weighted_kappa"], None, None, qa.get("weighted_kappa_ci95_cases")),
        ("Precision flexible d", d["precision_lenient"], t["activities_precision_lenient"], d.get("precision_lenient_ci95"), floors.get("activities_precision_lenient"), d.get("precision_lenient_ci95_cases")),
    ]
    rows = []
    for name, value, minimum, ci, floor, ci_cases in checks:
        if value is None:
            status, reason = "sin datos", None
        elif value < minimum:
            status, reason = "no cumple", "valor bajo la meta"
        elif ci is not None and floor is not None and ci[0] < floor:
            status, reason = "no cumple", "limite inferior del IC bajo el piso"
        else:
            status, reason = "cumple", None
        rows.append({"criterio": name, "valor": value, "minimo": minimum, "ic95": ci, "piso_ic95": floor, "ic95_casos": ci_cases, "estado": status, "motivo": reason})
    if any(r["estado"] == "sin datos" for r in rows):
        verdict = "INCOMPLETO"
    elif all(r["estado"] == "cumple" for r in rows):
        verdict = "CUMPLE"
    else:
        verdict = "NO CUMPLE"
    return {"criterios": rows, "veredicto": verdict}
