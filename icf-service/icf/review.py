"""Metricas de la validacion clinica (HU-07g). Logica pura, sin Excel ni base de datos.

La revisora (profesional en salud) trabaja en dos fases:
  Fase A (a ciegas): escribe los codigos de funciones (b) y estructuras (s) que ella elegiria, sin ver la sugerencia.
  Fase B: valora cada codigo sugerido (Adecuado / Aceptable / No adecuado), si el calificador es correcto y que codigos faltan.

Los codigos se comparan por su codigo de 3 digitos (letra + 3 numeros): la busqueda del motor solo propone
codigos de ese nivel, y un codigo mas especifico de la revisora (b7301) cuenta para su codigo de 3 digitos (b730).
"""
import re
from typing import Dict, Iterable, List, Optional, Set

COMPONENTS = ("b", "s", "d")
RATINGS = {"adecuado": "A", "aceptable": "B", "no adecuado": "C"}
RATING_OPTIONS = ("Adecuado", "Aceptable", "No adecuado")
YES_NO_OPTIONS = ("Sí", "Parcial", "No")

# Umbrales PROPUESTOS (a confirmar con la revisora y el responsable antes de usarlos como criterio de aprobacion).
# Se aplican a funciones y estructuras (b y s); las actividades (d) salen de una lista cerrada del Anexo y se miden aparte.
THRESHOLDS = {
    "min_cases_reviewed": 20,  # de 24 casos aplicables
    "body_precision_strict": 0.60,  # solo "Adecuado"
    "body_precision_lenient": 0.80,  # "Adecuado" + "Aceptable"
    "body_blind_recall": 0.60,  # de lo que ella eligio a ciegas, cuanto estaba en la sugerencia
    "qualifier_ok": 0.80,  # calificadores "Sí" (los "Parcial" cuentan la mitad)
    "activities_precision_lenient": 0.80,
}

CODE_RE = re.compile(r"\b([bsd])\s*(\d{3,5})\b", re.IGNORECASE)


def normalize_codes(text: Optional[str]) -> Set[str]:
    """'b730, B7301 y s750' -> {'b730', 's750'}: letra + 3 digitos, sin duplicados."""
    if not text:
        return set()
    return {f"{m.group(1).lower()}{m.group(2)[:3]}" for m in CODE_RE.finditer(str(text))}


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


def compute_metrics(
    ratings: Iterable[Dict],
    missing: Dict[str, Dict[str, Set[str]]],
    blind: Dict[str, Dict[str, Set[str]]],
    suggested: Dict[str, Dict[str, Set[str]]],
) -> Dict:
    """Calcula las metricas.

    ratings:   [{'case', 'component', 'code', 'rating': 'A|B|C|None', 'qualifier_ok': 1/0.5/0/None}]
    missing:   {case: {'b': {codigos que faltan}, 's': ...}} (Fase B, hoja Faltantes)
    blind:     {case: {'b': {codigos que ella eligio a ciegas}, 's': ...}} (Fase A)
    suggested: {case: {'b': {codigos sugeridos}, 's': ..., 'd': ...}}
    """
    ratings = list(ratings)
    out: Dict = {"components": {}, "cases_reviewed": 0}
    reviewed_cases = {r["case"] for r in ratings if r["rating"]}
    out["cases_reviewed"] = len(reviewed_cases)

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
    blind_hits = blind_expected = 0
    blind_cases = 0
    for case, comps in blind.items():
        counted = False
        for comp in ("b", "s"):
            expected = comps.get(comp, set())
            if not expected:
                continue
            counted = True
            sug = suggested.get(case, {}).get(comp, set())
            hits = len(expected & sug)
            blind_hits += hits
            blind_expected += len(expected)
        if counted:
            blind_cases += 1
    out["blind"] = {
        "cases": blind_cases,
        "expected_codes": blind_expected,
        "found_in_suggestion": blind_hits,
        "recall": _ratio(blind_hits, blind_expected),
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
        "precision_lenient": _ratio(a_bs + b_bs, tot),
        "qualifier_ok": _ratio(sum(q_all), len(q_all)),
    }
    return out


def evaluate_thresholds(metrics: Dict, thresholds: Dict = THRESHOLDS) -> Dict:
    """Compara con los umbrales. Devuelve cada criterio y el veredicto."""
    t = thresholds
    d = metrics["components"]["d"]
    checks: List[Dict] = [
        ("Casos revisados", metrics["cases_reviewed"], t["min_cases_reviewed"]),
        ("Precision estricta b+s", metrics["body"]["precision_strict"], t["body_precision_strict"]),
        ("Precision flexible b+s", metrics["body"]["precision_lenient"], t["body_precision_lenient"]),
        ("Cobertura a ciegas b+s", metrics["blind"]["recall"], t["body_blind_recall"]),
        ("Calificadores correctos b+s", metrics["body"]["qualifier_ok"], t["qualifier_ok"]),
        ("Precision flexible d", d["precision_lenient"], t["activities_precision_lenient"]),
    ]
    rows = []
    for name, value, minimum in checks:
        status = "sin datos" if value is None else ("cumple" if value >= minimum else "no cumple")
        rows.append({"criterio": name, "valor": value, "minimo": minimum, "estado": status})
    if any(r["estado"] == "sin datos" for r in rows):
        verdict = "INCOMPLETO"
    elif all(r["estado"] == "cumple" for r in rows):
        verdict = "CUMPLE"
    else:
        verdict = "NO CUMPLE"
    return {"criterios": rows, "veredicto": verdict}
