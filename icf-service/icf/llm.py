"""Prompt, esquema JSON y validacion de la respuesta del LLM. El LLM solo elige entre candidatos.

Diseno por velocidad (medido en el servidor, i3 sin GPU): leer el prompt cuesta ~0,05 s por token y
escribir la respuesta ~0,1 s por token. Por eso el modelo solo interviene en funciones (b) y
estructuras (s), recibe pocos candidatos y devuelve solo codigos, sin justificacion. Las actividades (d)
se ordenan por reglas y similitud, sin LLM.
"""
import json
from typing import Any, Dict, List, Sequence, Tuple

from .rules import MAX_PER_COMPONENT

Pair = Tuple[str, str]

# Parte fija y al inicio: Ollama reutiliza el prefijo ya calculado entre peticiones.
SYSTEM_PROMPT = (
    "Codificador CIF-IA. Elige solo codigos de las listas dadas; no inventes codigos. "
    "Para b y s devuelve hasta 3 codigos por lista, del mas al menos relevante para el paciente, "
    "como JSON."
)


def build_schema(b_codes: Sequence[str], s_codes: Sequence[str]) -> Dict[str, Any]:
    """JSON Schema con los codigos candidatos como `enum`: el formato no permite ningun otro valor."""

    def code_list(codes: Sequence[str]) -> Dict[str, Any]:
        return {
            "type": "array",
            "maxItems": MAX_PER_COMPONENT,
            "items": {"type": "string", "enum": list(codes)},
        }

    properties: Dict[str, Any] = {}
    if b_codes:
        properties["b"] = code_list(b_codes)
    if s_codes:
        properties["s"] = code_list(s_codes)
    return {"type": "object", "properties": properties, "required": list(properties)}


def _listing(title: str, pairs: Sequence[Pair]) -> str:
    return title + "\n" + "\n".join(f"{code} {name}" for code, name in pairs)


def build_messages(patient_summary: str, b_pairs: Sequence[Pair], s_pairs: Sequence[Pair]) -> List[Dict[str, str]]:
    blocks = [patient_summary]
    if b_pairs:
        blocks.append(_listing("b:", b_pairs))
    if s_pairs:
        blocks.append(_listing("s:", s_pairs))
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "\n".join(blocks)},
    ]


def parse_response(text: str, b_codes: Sequence[str], s_codes: Sequence[str]) -> Dict[str, List[str]]:
    """Valida la respuesta del LLM. Descarta cualquier codigo que no sea candidato y los repetidos.
    Acepta cada elemento como texto o como objeto {"code": ...}. Lanza ValueError si el JSON no es
    valido o no queda ningun codigo valido."""
    try:
        data = json.loads(text)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"JSON invalido: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("la respuesta no es un objeto JSON")

    allowed = {"b": set(b_codes), "s": set(s_codes)}
    parsed: Dict[str, List[str]] = {"b": [], "s": []}
    for key, valid in allowed.items():
        items = data.get(key)
        if not valid or not isinstance(items, list):
            continue
        for item in items:
            code = item.get("code") if isinstance(item, dict) else item
            if not isinstance(code, str) or code not in valid or code in parsed[key]:
                continue
            parsed[key].append(code)
            if len(parsed[key]) == MAX_PER_COMPONENT:
                break
    if not any(parsed.values()):
        raise ValueError("la respuesta no contiene ningun codigo candidato")
    return parsed
