"""Prompt, esquema JSON y validacion de la respuesta del LLM. El LLM solo elige entre candidatos."""
import json
from typing import Any, Dict, List, Sequence, Tuple

from .rules import MAX_PER_COMPONENT

Pair = Tuple[str, str]
JUSTIFICATION_MAX = 160

SYSTEM_PROMPT = (
    "Eres un asistente de codificacion CIF-IA para apoyo clinico en Colombia. "
    "Solo puedes elegir codigos de las listas que se te dan; nunca inventes codigos. "
    "Responde unicamente con el JSON pedido, en espanol."
)


def build_schema(d_codes: Sequence[str], b_codes: Sequence[str], s_codes: Sequence[str]) -> Dict[str, Any]:
    """JSON Schema con los codigos candidatos como `enum`: el formato no permite ningun otro valor."""

    def coded_items(codes: Sequence[str]) -> Dict[str, Any]:
        return {
            "type": "array",
            "maxItems": MAX_PER_COMPONENT,
            "items": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "enum": list(codes)},
                    "justificacion": {"type": "string"},
                },
                "required": ["code", "justificacion"],
            },
        }

    properties: Dict[str, Any] = {}
    if d_codes:
        # Actividades: solo se ordenan por relevancia; la justificacion la arman las reglas.
        properties["d"] = {
            "type": "array",
            "maxItems": MAX_PER_COMPONENT,
            "items": {"type": "string", "enum": list(d_codes)},
        }
    if b_codes:
        properties["b"] = coded_items(b_codes)
    if s_codes:
        properties["s"] = coded_items(s_codes)
    return {"type": "object", "properties": properties, "required": list(properties)}


def _listing(title: str, pairs: Sequence[Pair]) -> str:
    return title + "\n" + "\n".join(f"- {code}: {name}" for code, name in pairs)


def build_messages(
    patient_summary: str,
    d_pairs: Sequence[Pair],
    b_pairs: Sequence[Pair],
    s_pairs: Sequence[Pair],
) -> List[Dict[str, str]]:
    blocks = [patient_summary]
    instructions = []
    if d_pairs:
        blocks.append(_listing("ACTIVIDADES Y PARTICIPACION (d):", d_pairs))
        instructions.append('"d": hasta 3 codigos de la lista d, del mas al menos relevante (solo los codigos)')
    if b_pairs:
        blocks.append(_listing("FUNCIONES CORPORALES (b):", b_pairs))
        instructions.append('"b": hasta 3 objetos {"code","justificacion"} de la lista b')
    if s_pairs:
        blocks.append(_listing("ESTRUCTURAS CORPORALES (s):", s_pairs))
        instructions.append('"s": hasta 3 objetos {"code","justificacion"} de la lista s')
    blocks.append(
        "Elige solo de las listas. Ordena por relevancia para este paciente. "
        "Cada justificacion tiene como maximo 12 palabras. Campos a devolver: " + "; ".join(instructions) + "."
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "\n\n".join(blocks)},
    ]


def _clean(text: Any) -> str:
    return " ".join(str(text).split())[:JUSTIFICATION_MAX]


def parse_response(
    text: str, d_codes: Sequence[str], b_codes: Sequence[str], s_codes: Sequence[str]
) -> Dict[str, List[Tuple[str, str]]]:
    """Valida la respuesta del LLM. Descarta cualquier codigo que no sea candidato y los repetidos.
    Lanza ValueError si el JSON no es valido o no queda ningun codigo valido."""
    try:
        data = json.loads(text)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"JSON invalido: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("la respuesta no es un objeto JSON")

    allowed = {"d": set(d_codes), "b": set(b_codes), "s": set(s_codes)}
    parsed: Dict[str, List[Tuple[str, str]]] = {"d": [], "b": [], "s": []}
    for key, valid in allowed.items():
        items = data.get(key)
        if not valid or not isinstance(items, list):
            continue
        seen = set()
        for item in items:
            if isinstance(item, dict):
                code, why = item.get("code"), item.get("justificacion", "")
            else:
                code, why = item, ""
            if not isinstance(code, str) or code not in valid or code in seen:
                continue
            seen.add(code)
            parsed[key].append((code, _clean(why)))
            if len(parsed[key]) == MAX_PER_COMPONENT:
                break
    if not any(parsed.values()):
        raise ValueError("la respuesta no contiene ningun codigo candidato")
    return parsed
