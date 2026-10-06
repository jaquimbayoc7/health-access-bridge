"""Prompt, esquema JSON y validacion de la respuesta del LLM. El LLM solo elige entre candidatos.

Medido en el servidor (i3 sin GPU): leer el prompt cuesta ~0,05 s por token y escribir la respuesta ~0,1 s
por token. Hay dos modos:
  * rapido:  pocos candidatos y solo codigos (~20 s).
  * calidad: mas candidatos y una justificacion corta por codigo (~40 s).
Las actividades (d) se ordenan por reglas y similitud, sin LLM.
"""
import json
from typing import Any, Dict, List, Sequence, Tuple

from .rules import MAX_PER_COMPONENT

Pair = Tuple[str, str]
JUSTIFICATION_MAX = 160

# Parte fija y al inicio del prompt.
SYSTEM_PROMPT = (
    "Codificador CIF-IA. Elige solo codigos de las listas dadas; no inventes codigos. "
    "Para b y s devuelve hasta 3 codigos por lista, del mas al menos relevante para el paciente, "
    "como JSON."
)
SYSTEM_PROMPT_JUSTIFY = (
    "Codificador CIF-IA. Elige solo codigos de las listas dadas; no inventes codigos. "
    "Para b y s devuelve hasta 3 objetos {code, justificacion} por lista, del mas al menos relevante "
    "para el paciente; la justificacion une el diagnostico o las notas con la funcion o estructura, "
    "en maximo 12 palabras. Responde como JSON."
)


def system_prompt(justify: bool) -> str:
    return SYSTEM_PROMPT_JUSTIFY if justify else SYSTEM_PROMPT


def build_schema(b_codes: Sequence[str], s_codes: Sequence[str], justify: bool = False) -> Dict[str, Any]:
    """JSON Schema con los codigos candidatos como `enum`: el formato no permite ningun otro valor."""

    def code_list(codes: Sequence[str]) -> Dict[str, Any]:
        code = {"type": "string", "enum": list(codes)}
        items: Dict[str, Any] = code
        if justify:
            items = {
                "type": "object",
                "properties": {"code": code, "justificacion": {"type": "string"}},
                "required": ["code", "justificacion"],
            }
        return {"type": "array", "maxItems": MAX_PER_COMPONENT, "items": items}

    properties: Dict[str, Any] = {}
    if b_codes:
        properties["b"] = code_list(b_codes)
    if s_codes:
        properties["s"] = code_list(s_codes)
    return {"type": "object", "properties": properties, "required": list(properties)}


def _listing(title: str, pairs: Sequence[Pair]) -> str:
    return title + "\n" + "\n".join(f"{code} {name}" for code, name in pairs)


def build_messages(
    patient_summary: str, b_pairs: Sequence[Pair], s_pairs: Sequence[Pair], justify: bool = False
) -> List[Dict[str, str]]:
    blocks = [patient_summary]
    if b_pairs:
        blocks.append(_listing("b:", b_pairs))
    if s_pairs:
        blocks.append(_listing("s:", s_pairs))
    return [
        {"role": "system", "content": system_prompt(justify)},
        {"role": "user", "content": "\n".join(blocks)},
    ]


def _clean(text: Any) -> str:
    return " ".join(str(text).split())[:JUSTIFICATION_MAX]


def parse_response(
    text: str, b_codes: Sequence[str], s_codes: Sequence[str]
) -> Dict[str, List[Tuple[str, str]]]:
    """Valida la respuesta del LLM y devuelve {componente: [(codigo, justificacion)]}. Descarta cualquier codigo
    que no sea candidato y los repetidos. Cada elemento puede ser texto (justificacion vacia) o un objeto
    {"code", "justificacion"}. Lanza ValueError si el JSON no es valido o no queda ningun codigo valido."""
    try:
        data = json.loads(text)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"JSON invalido: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("la respuesta no es un objeto JSON")

    allowed = {"b": set(b_codes), "s": set(s_codes)}
    parsed: Dict[str, List[Tuple[str, str]]] = {"b": [], "s": []}
    for key, valid in allowed.items():
        items = data.get(key)
        if not valid or not isinstance(items, list):
            continue
        seen = set()
        for item in items:
            if isinstance(item, dict):
                code, why = item.get("code"), _clean(item.get("justificacion", ""))
            else:
                code, why = item, ""
            if not isinstance(code, str) or code not in valid or code in seen:
                continue
            seen.add(code)
            parsed[key].append((code, why))
            if len(parsed[key]) == MAX_PER_COMPONENT:
                break
    if not any(parsed.values()):
        raise ValueError("la respuesta no contiene ningun codigo candidato")
    return parsed
