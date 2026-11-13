"""Variantes D1/D2: el modelo propone la gravedad 0-4 de cada codigo b/s que la medica califico a ciegas.
Prompt fijado antes de ver resultados. D1 = solo el caso; D2 = el caso mas el calificador de la regla actual como referencia.
Uso: python scripts/qualifier_llm.py MODELO SALIDA.json"""
import json, sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent)); sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault("ICF_LLM_THINK", "false")
import qualifier_exploration as q
from icf.ollama import chat_json
from icf.rules import body_qualifier

SCALE = "0 = sin problema (0-4 %), 1 = leve (5-24 %), 2 = moderado (25-49 %), 3 = grave (50-95 %), 4 = completo (96-100 %)"
SCHEMA = {"type": "object", "properties": {"calificador": {"type": "integer", "minimum": 0, "maximum": 4}}, "required": ["calificador"]}

def prompt(r, with_rule):
    lv = ", ".join(f"{k} {v}" for k, v in r["levels"].items())
    kind = "funcion corporal" if r["comp"] == "b" else "estructura corporal"
    t = (f"Eres un profesional de salud que califica la CIF. Escala del calificador generico: {SCALE}.\n"
         f"Caso: {r['age']} anios. Diagnostico: {r['diag'] or 'no indicado'}. Notas: {r['notes'] or 'ninguna'}. "
         f"Deficiencia fisica: {r['cat_f']}. Deficiencia psicosocial: {r['cat_p']}. Niveles de dificultad por dominio (0-100): {lv}.\n"
         f"Asigna el calificador de gravedad (0-4) de la {kind} con codigo CIF {r['code']} para este paciente.")
    if with_rule:
        t += f" Referencia: la regla automatica a partir de la categoria sugiere {body_qualifier(r['code'], r['cat_f'], r['cat_p'])}; ajustala si el caso lo justifica."
    return t + ' Responde solo JSON: {"calificador": n}.'

model, out = sys.argv[1], sys.argv[2]
res = []
for i, r in enumerate(q.load_rows()):
    row = {"case": r["case"], "code": r["code"], "round": r["round"], "sev": r["sev"]}
    for tag, wr in (("d1", False), ("d2", True)):
        try:
            row[tag] = json.loads(chat_json("http://localhost:11434", model, [{"role": "user", "content": prompt(r, wr)}], SCHEMA, timeout=120, num_ctx=2048))["calificador"]
        except Exception as e:
            row[tag] = None
    res.append(row); print(i, row, flush=True)
json.dump(res, open(out, "w"))
