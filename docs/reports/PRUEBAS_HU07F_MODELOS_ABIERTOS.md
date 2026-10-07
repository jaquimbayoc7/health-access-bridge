# Pruebas de HU-07f — modelos abiertos locales (Gemma 4 y MedGemma) y mínimo viable

**Proyecto:** Health Access Bridge · **Momento 3 · HU-07f**
**Fecha de las pruebas:** 6 y 7 de octubre de 2026
**Resultado en una frase:** `gemma4:e4b` (6,6 GB) elige mejor que la búsqueda por similitud sola (funciones: precisión 43 % contra 29 %; estructuras: cobertura 86 % contra 67 %) y responde en unos 3,4 s con una GPU de 8 GB o en unos 15 s solo con CPU; los otros modelos probados (`gemma4:e2b`, `medgemma:4b`, `qwen2.5:3b`) no la superan de forma útil. **Se propone `gemma4:e4b` como modelo mínimo viable provisional**, pendiente de la validación clínica (HU-07g).

Este informe continúa a [`PRUEBAS_HU07_SERVIDOR_FISICO.md`](./PRUEBAS_HU07_SERVIDOR_FISICO.md), donde se midió `qwen2.5:3b` en el servidor i3 y se decidió probar modelos abiertos más grandes sin usar APIs externas (privacidad, Ley 1581 de 2012).

---

## 1. Entorno de prueba

| Elemento | Valor |
|---|---|
| Equipo | PC de pruebas: Intel Core i5-13450HX (10 núcleos, 16 hilos), 32 GB de RAM DDR5-4800, NVIDIA GeForce RTX 5050 Laptop con 8 GB de VRAM, Windows 11 |
| Motor de inferencia | Ollama 0.40.0 nativo en Windows (GPU NVIDIA) |
| Base de datos | PostgreSQL 16 con pgvector en un contenedor Docker local, solo en `127.0.0.1:5433` |
| Catálogo y embeddings | CIF-IA, 1.593 códigos con embedding `bge-m3` (1.593 de 1.593) |
| Servicio y scripts | `icf-service/` en un contenedor; el contenedor llega al Ollama de Windows por `host.docker.internal` |
| Casos | Los mismos 25 casos sintéticos y las mismas 21 «pistas orientativas» del informe anterior |
| Datos | Solo casos sintéticos; ningún dato real ni salida a internet durante las pruebas |

**Qué son las pistas.** Son códigos de funciones (b) y estructuras (s) que, por la lógica de la CIF, se esperaría encontrar en cada caso. **No las validó un médico.** Sirven para comparar modelos entre sí; no miden la precisión clínica, que solo mide la revisión de un médico (HU-07g).

**Modelos descargados:** `bge-m3`, `qwen2.5:3b`, `medgemma:4b`, `gemma4:e2b` y `gemma4:e4b`. **No se descargaron ni se midieron** `gemma4:12b`, `gemma4:26b`, `medgemma:27b` ni `gemma4:31b` (ver §6).

---

## 2. Dos defectos encontrados al medir Gemma 4

La primera corrida con Gemma 4 dio un resultado **inválido**: en los 21 casos el modelo «no respondió de forma válida» y el servicio usó la similitud como respaldo, por lo que las cifras eran idénticas a las de la similitud. La causa eran dos comportamientos de Gemma 4 que el motor no contemplaba:

| Defecto | Causa | Corrección |
|---|---|---|
| Respuesta no interpretable | Gemma 4 **ignora el formato JSON forzado** de Ollama y devuelve el JSON dentro de un bloque de código (```` ```json … ``` ````) | `parse_response` acepta el bloque de código (`icf/llm.py`) |
| Respuesta vacía o cortada | Gemma 4 es un modelo que **«razona» antes de responder** y gasta los tokens de salida en ese razonamiento | Variable `ICF_LLM_THINK=false` envía `think: false` a Ollama (`icf/ollama.py`) |

Se agregaron 2 pruebas automáticas (bloque de código y envío de `think`). El servicio queda con 70 pruebas (63 pasan y 7 se omiten sin base de datos de integración). **Lección:** un modelo que cae al respaldo en silencio parece «igual a la similitud»; el script ya avisa con un mensaje (`AVISO: el modelo no respondió…`), y se debe leer antes de interpretar una tabla.

Se agregó además `ICF_LLM_NUM_GPU` (por ejemplo `0` para forzar CPU) para dimensionar equipos sin GPU.

---

## 3. Calidad: comparación de modelos (21 casos con pistas)

Precisión = aciertos entre los códigos sugeridos; cobertura = aciertos entre las pistas. Resultados con el modelo en GPU y el razonamiento apagado.

| Modo / modelo | Funciones (b): precisión | b: cobertura | Estructuras (s): precisión | s: cobertura | Latencia media |
|---|---|---|---|---|---|
| **Similitud sola** | 29 % (18/63) | 25 % (18/73) | 25 % (14/57) | 67 % (14/21) | 0,1 s |
| `qwen2.5:3b` rápido | 27 % | 23 % | 25 % | 67 % | 6,6 s |
| `qwen2.5:3b` calidad | 19 % (12/63) | 16 % | 26 % | 67 % | 8,6 s |
| `medgemma:4b` rápido | 27 % | 23 % | 25 % | 67 % | 3,0 s |
| `medgemma:4b` calidad | 30 % (19/63) | 26 % | 28 % | 76 % | 4,9 s |
| `gemma4:e2b` rápido | 30 % | 26 % | 27 % | 71 % | 1,7 s |
| `gemma4:e2b` calidad | 32 % (20/63) | 27 % | 28 % | 76 % | 2,3 s |
| `gemma4:e4b` rápido | 33 % (21/63) | 29 % | 28 % | 76 % | 2,5 s |
| **`gemma4:e4b` calidad** | **43 % (27/63)** | **37 % (27/73)** | **32 % (18/57)** | **86 % (18/21)** | **3,4 s** |

**Lectura:**

- `gemma4:e4b` en modo calidad es el único que mejora con claridad sobre la similitud: unos 14 puntos de precisión en funciones y 19 puntos de cobertura en estructuras. En estructuras llega a 86 %, que es el **techo que permite la lista de 12 candidatos** (medido en el informe anterior): ahí no hay más que ganar cambiando de modelo.
- `gemma4:e2b` y `medgemma:4b` quedan apenas por encima de la similitud (1 a 3 puntos): una diferencia que con 21 casos no se distingue del ruido. No justifican un modelo de generación.
- `qwen2.5:3b` sigue siendo peor que la similitud también en este PC (funciones 19 % contra 29 %): el problema del informe anterior era el modelo, no solo el equipo lento.
- `medgemma:4b`, pese a ser un modelo orientado a medicina, no superó al generalista `gemma4:e4b`. Con un modelo de 4B, el dominio médico no compensó el menor tamaño efectivo.
- El modo `rápido` (6 candidatos, sin justificación) de `gemma4:e4b` mejora poco (33 % en funciones); la mejora grande viene del modo `calidad` (12 candidatos y justificación).

---

## 4. Velocidad y memoria

Medición directa contra Ollama con un prompt de ~450 tokens (el primer prompt de cada serie se descarta por la carga del modelo; las lecturas de prompt repetidas salen de la caché y no se reportan).

| Modelo | VRAM ocupada (GPU) | Escritura con GPU | Escritura solo CPU | Lectura de prompt solo CPU |
|---|---|---|---|---|
| `gemma4:e4b` | ~4,6 GB (100 % en GPU) | 63 tok/s | 16–18 tok/s | ~89 tok/s |
| `gemma4:e2b` | ~3,1 GB (100 % en GPU) | 90 tok/s | 46 tok/s | ~199 tok/s |

(VRAM = uso total de la GPU con el modelo cargado menos el uso base del equipo, ~0,3 GB; es una estimación redondeada.) Referencia del servidor i3: Qwen 3B escribía a 10 tok/s y leía a 21 tok/s, sin GPU.

**Latencia extremo a extremo** (motor completo, 5 casos con pistas; en CPU se forzó `ICF_LLM_NUM_GPU=0`):

| Modelo | Modo | Con GPU (21 casos) | Solo CPU, 10 núcleos (5 casos) |
|---|---|---|---|
| `gemma4:e4b` | rápido | 2,5 s | 9,3 s |
| `gemma4:e4b` | calidad | 3,4 s | 15,3 s |
| `gemma4:e2b` | rápido | 1,7 s | 5,6 s |
| `gemma4:e2b` | calidad | 2,3 s | 6,9 s |

Los resultados de calidad con solo CPU (5 casos) son consistentes con los de GPU (`e4b` calidad: precisión de funciones 47 %), pero son una muestra demasiado pequeña para comparar. `e2b` en CPU en modo calidad bajó a 36 % en funciones y 50 % de cobertura en estructuras: otra señal de que `e2b` no sostiene la calidad.

---

## 5. Mínimo viable propuesto (provisional)

**Modelo:** `gemma4:e4b` en modo `calidad`, con `ICF_LLM_THINK=false`. Es el más pequeño de los medidos que mejora de forma consistente sobre la similitud. Se descartan como mínimo: `gemma4:e2b` y `medgemma:4b` (mejora marginal) y `qwen2.5:3b` (peor que la similitud).

**Máquina:** el modelo ocupa 6,6 GB en disco y ~4,6 GB de VRAM. Hay dos opciones **medidas** y una **estimada**:

| Opción | Requisitos | Latencia por sugerencia | Estado |
|---|---|---|---|
| **A. Con GPU (recomendada)** | GPU NVIDIA de **8 GB de VRAM o más** (con 6 GB queda justo: el modelo usa ~4,6 GB más el contexto), 16 GB de RAM, CPU de 6 núcleos o más, SSD con 30 GB libres | ~3,4 s | Medida en la RTX 5050 de 8 GB |
| **B. Solo CPU** | CPU moderna de **8 núcleos o más** (como el i5-13450HX), **16 GB de RAM** (modelo 6,6 GB + `bge-m3` + base de datos + sistema), SSD | ~15 s (modo calidad) o ~9 s (rápido) | Medida en un CPU de 10 núcleos; un CPU más débil será más lento |
| C. El servidor i3 de 12 GB sin GPU | — | Estimación: más de 40 s | **No sirve:** el modelo de 6,6 GB deja poca RAM libre y el CPU es mucho más lento; es una estimación, no una medición |

**Qué cubre cada opción.** La opción B es utilizable si el médico acepta esperar unos 15 s (se puede mostrar la sugerencia por similitud al instante y la del modelo cuando llegue). La opción A es cómoda para el uso interactivo. En ambas, el servicio mantiene la similitud como respaldo. **Decisión del 07-oct-2026:** el PC de pruebas pasa a ser la máquina de producción (opción A), así que no se compra hardware; HU-07h documenta su despliegue y operación. Esta tabla no incluye precios porque no se verificaron.

**Alcance de la propuesta.** Es el mínimo **encontrado en esta escalera parcial**, no el mejor modelo posible. Para uno o pocos médicos a la vez, la opción A no se saturaría; con concurrencia alta habría que medirlo (no se midió).

---

## 6. Limitaciones

- **Son 21 casos y 73 pistas** (5 casos en las mediciones solo con CPU). La mejora de `gemma4:e4b` es consistente en funciones y estructuras, pero la muestra es pequeña.
- **Las pistas no son criterio clínico.** Los porcentajes absolutos no son la confiabilidad del sistema; esa la mide el médico (HU-07g).
- **No se midieron los modelos grandes** (`gemma4:12b`, `26b`, `31b`, `medgemma:27b`). En estructuras `e4b` ya alcanza el techo de los candidatos; en funciones (37 %) podría haber margen. Si la validación clínica con el médico muestra que `e4b` no alcanza el umbral, se mide la escalera superior.
- **Una sola máquina.** Las velocidades de CPU y GPU son las de este equipo. Otra GPU o CPU dará cifras distintas.
- **Licencias (verificadas el 07-oct-2026).** Gemma 4 es Apache 2.0 y se puede usar en producción; MedGemma se rige por los términos de Health AI Developer Foundations, que prohíben el uso clínico, así que no se usa. Detalle en `LICENCIAS_COMPONENTES_ICF.md`.
- **Determinismo.** Se fija `temperature: 0`; aun así, GPU y versión de Ollama pueden dar respuestas ligeramente distintas.

---

## 7. Decisión y siguientes pasos

**Decisión propuesta (07-oct-2026):** usar `gemma4:e4b` en modo `calidad` como modelo mínimo viable para implementar HU-07c, HU-07d y HU-07e, con la similitud como respaldo y sin APIs externas. Se confirma o se cambia con el resultado de la revisión del médico.

| HU | Qué |
|---|---|
| 07c | Backend en Render hacia el servicio ICF, con el modelo configurable por `ICF_LLM_MODEL` y un tiempo de espera de 90 s (cubre el caso solo CPU) |
| 07d | Pantalla «Perfil Funcional ICF»; si la latencia es de ~15 s, mostrar primero la similitud y luego la sugerencia del modelo |
| 07e | Pruebas y manual de operación: instalación de Ollama y de `gemma4:e4b`, y los requisitos de la máquina de este informe |
| 07g | Revisión del médico sobre los 25 casos y definición del umbral |
| 07h | Despliegue y operación en el PC de producción (sin compra de hardware) |

---

## 8. Cómo reproducir

Todo está en `icf-service/` (ver su `README.md`). Variables para Gemma 4: `ICF_LLM_MODEL=gemma4:e4b`, `ICF_LLM_THINK=false`; para forzar CPU: `ICF_LLM_NUM_GPU=0`. Ejemplo con Docker contra el Ollama de Windows:

```powershell
docker run --rm --network icf-net `
  -e ICF_DATABASE_URL=postgresql://icf_user:<clave-local>@icf-db:5432/icf `
  -e OLLAMA_URL=http://host.docker.internal:11434 `
  -e ICF_LLM_MODEL=gemma4:e4b -e ICF_LLM_THINK=false -e ICF_SERVICE_LLM_TIMEOUT_S=300 `
  -v "${PWD}:/work" -w /work/icf-service icf-service `
  python scripts/compare_modes.py --output /work/data/private/results/cmp_gemma4_e4b.json
```

Los resultados detallados por caso se guardan en `data/private/results/` (ruta ignorada por git).
