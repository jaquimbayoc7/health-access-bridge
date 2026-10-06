# Pruebas de HU-07 con el servidor físico y Qwen — resultados y decisión

**Proyecto:** Health Access Bridge · **Momento 3 · HU-07a / HU-07b**
**Fecha de las pruebas:** 5 y 6 de octubre de 2026
**Resultado en una frase:** un modelo local de ~3B parámetros (`qwen2.5:3b`) en el servidor físico del proyecto **no mejora la selección de códigos CIF sobre la búsqueda por similitud sola, y tarda de 24 a 46 segundos por sugerencia**; por eso HU-07 pasa a usar un modelo externo (Claude Sonnet 5.5) para la selección, manteniendo el catálogo y la búsqueda en el servidor propio.

Este documento reemplaza, en lo que se refiere al modelo de generación de HU-07, la decisión registrada en `INSIGHTS_REPORT4.md` §6.3 (Ollama sobre servidor propio con un modelo open-weight gratuito). Los informes de los momentos anteriores se conservan como fueron escritos.

---

## 1. Entorno de prueba

| Elemento | Valor |
|---|---|
| Equipo | Portátil con procesador Intel Core i3, 12 GB de RAM (11 GiB útiles), **sin GPU**, Ubuntu |
| Modelo de generación | `qwen2.5:3b` (3,1 B parámetros, cuantización Q4_K_M, 1,9 GB, contexto 32 768) |
| Modelo de embeddings | `bge-m3` (1,1 GB) |
| Motor de inferencia | Ollama, 100 % CPU; ambos modelos cargados a la vez con ~4 GB de memoria libre |
| Base de datos | PostgreSQL 16 con pgvector, en contenedor Docker, solo en `127.0.0.1` |
| Acceso desde Render | Tailscale Funnel → Caddy (exige token Bearer) → servicio ICF / Ollama |
| Catálogo | CIF-IA (OMS, 2011): **1.593 códigos** con título, extraídos de un PDF escaneado con OCR y revisados; 3 códigos sin definición en el libro quedan fuera |
| Casos de prueba | 25 casos **sintéticos** (no son personas reales) en `icf-service/reference/cases.json`; 21 tienen «pistas» en `retrieval_hints.json` |

**Qué son las pistas.** Son códigos de funciones (b) y estructuras (s) que, por la lógica de la CIF, se esperaría encontrar en cada caso (por ejemplo, fuerza muscular, tono y marcha para parálisis cerebral). **No las validó un médico.** Un código razonable que no figure en las pistas cuenta como fallo, y a todos los modos les afecta por igual. Sirven para **comparar variantes entre sí**; no miden la precisión clínica, que solo puede medir la revisión de un médico (HU-07g).

---

## 2. Conectividad y latencia base

| Medición | Resultado |
|---|---|
| Respuesta mínima de `qwen2.5:3b`, en red local, con el modelo cargado | 4,1 s (carga 0,12 s, lectura del prompt 0,95 s, escritura 2,5 s a ~11 tokens/s) |
| La misma llamada, a través de Tailscale Funnel | 8,8 s |
| Diagnóstico `GET /icf/health` desde Render QA (administrador) | `configured`, `reachable` y `model_available` en `true`; 943 ms |
| Token inválido o ausente en el túnel | 401 en todas las rutas (probado también con Caddy real; el bloque `route` es obligatorio para que el token se exija antes de cualquier ruta) |

La conexión Render → servidor propio funciona y está protegida. El problema no es la conectividad.

---

## 3. Latencia del motor de sugerencia

### 3.1 Primera versión (el modelo ordena actividades, funciones y estructuras con justificación)

| Caso | Total | Leer el prompt | Escribir la respuesta |
|---|---|---|---|
| C01 | 60,5 s | 38,6 s (773 tokens) | 17,9 s (180 tokens) |
| C02 | 55,3 s | 34,9 s (761 tokens) | 16,5 s (166 tokens) |
| C03 | 54,1 s | 34,6 s (758 tokens) | 15,8 s (165 tokens) |
| C04 | 52,7 s | 34,0 s (746 tokens) | 15,1 s (158 tokens) |

Media **55,6 s**, p95 60,5 s. El embedding tardó 0,63 s y la búsqueda en la base, 4 ms. **Lo que cuesta es el modelo:** en este equipo, leer cuesta ~0,05 s por token (21 tokens/s) y escribir ~0,1 s por token (10,2 tokens/s). El JSON Schema con los códigos como lista cerrada no influye en la velocidad (160 tokens en 15,3 s con esquema y 15,4 s con JSON simple).

*Nota de método:* el primer diagnóstico de velocidad envió dos veces el mismo prompt y mostraba una lectura casi instantánea (92 ms). Era un efecto de la caché de Ollama, no la velocidad real con un paciente nuevo; el script se corrigió para separar «prompt nuevo» de «prompt en caché».

### 3.2 Rediseño para reducir tokens

Las actividades (d) dejaron de pasar por el modelo (la lista cerrada del Anexo se ordena por calificador y por similitud con el embedding ya calculado), el modelo solo elige funciones y estructuras entre 6 candidatos y devuelve solo códigos, y la parte fija del prompt va primero.

| Medición | Resultado |
|---|---|
| Latencia | media **22,9 s**, p95 25,1 s |
| Prompt | 348 tokens en ~14,5 s |
| Salida | 65 tokens en ~6 s |
| JSON válido / códigos fuera del catálogo | 4/4 (100 %) / 0 |

### 3.3 Los tres modos, sobre los 21 casos con pistas

| Modo | Candidatos b y s | Salida del modelo | Latencia media | p95 |
|---|---|---|---|---|
| **similitud** (sin modelo de generación) | 12, los 3 más cercanos | — | **0,6 s** | 0,8 s |
| rápido | 6 | solo códigos | 24,0 s | 26,0 s |
| calidad | 12 | códigos con justificación | 46,0 s | 53,3 s |

---

## 4. Calidad de la búsqueda de funciones y estructuras

**Hallazgo.** La revisión de las salidas mostró candidatos pobres. Para parálisis cerebral salían *Dominancia lateral* y *Dolor generalizado* en lugar de fuerza, tono o control del movimiento. El modelo solo puede elegir lo que la búsqueda le ofrece, así que esa es la parte que decide la calidad.

Cobertura de las pistas entre los primeros candidatos (aciertos / pistas):

| Forma de buscar | Funciones @6 | Funciones @12 | Estructuras @6 | Estructuras @12 |
|---|---|---|---|---|
| Texto con todo (causa, categorías, diagnóstico con código CIE, notas), niveles 2 y 3 | 3/73 (4 %) | 7/73 (10 %) | 2/21 (10 %) | 3/21 (14 %) |
| Solo lo clínico (diagnóstico sin código CIE + notas), niveles 2 y 3 | 8/73 (11 %) | 14/73 (19 %) | 9/21 (43 %) | 10/21 (48 %) |
| **Solo códigos de 3 dígitos (nivel 2)**, texto clínico | **17/73 (23 %)** | **29/73 (40 %)** | **15/21 (71 %)** | **18/21 (86 %)** |
| Nivel 2 con embedding enriquecido con los títulos de los códigos hijos | 15/73 (21 %) | 24/73 (33 %) | 13/21 (62 %) | 15/21 (71 %) |

Otras variantes medidas solo con 6 candidatos: pedirle a Qwen que describiera el diagnóstico antes de buscar dio 3 % en funciones y 10 % en estructuras (inventaba estructuras, por ejemplo «glóbulos rojos» para esquizofrenia); limitar a 2 candidatos por capítulo dio 8 % y 43 %.

**Conclusiones de esta sección.** Buscar solo entre los códigos de 3 dígitos es lo que más mejora la cobertura (en el 76 % de los casos hay al menos una función esperada entre 12 candidatos, y en el 94 % una estructura). Los códigos de 4 y 5 dígitos llenaban la lista de hermanos casi idénticos (`b2800`, `b2801`, `b2802`). Con 12 candidatos se cubre bastante más que con 6. Enriquecer el texto no ayudó.

---

## 5. Comparación de modos contra las pistas (el resultado decisivo)

| Modo | Funciones: precisión | Funciones: cobertura | Estructuras: precisión | Estructuras: cobertura | Casos con ≥1 acierto (b / s) |
|---|---|---|---|---|---|
| **similitud** | 18/63 (29 %) | 18/73 (25 %) | 14/57 (25 %) | 14/21 (67 %) | 11/21 · 11/16 |
| rápido (Qwen) | 14/60 (23 %) | 14/73 (19 %) | 12/51 (24 %) | 12/21 (57 %) | 9/21 · 11/16 |
| calidad (Qwen) | 11/54 (20 %) | 11/73 (15 %) | 10/41 (24 %) | 10/21 (48 %) | 8/21 · 10/16 |

**El modelo local empeora la selección**, y cuanto más trabaja, peor: en funciones, 18 aciertos sin modelo, 14 con el modo rápido y 11 con el de calidad; en estructuras, 14, 12 y 10. Además cuesta de 40 a 80 veces más tiempo. Ejemplo: en el caso de autismo la similitud sola devuelve `b230 b240 b450` y el modo calidad `b147 b125`; en el de distrofia muscular, la similitud acierta `b730`, `b740`, `s750` y `s730` y el modo calidad pierde `b740` y `s730`.

---

## 6. Defectos encontrados y corregidos durante las pruebas

| Defecto | Efecto | Corrección |
|---|---|---|
| El filtro por categoría se aplicaba después de buscar | El caso solo psicosocial (esquizofrenia) no devolvía ninguna función | El filtro por capítulo va dentro de la búsqueda |
| Códigos «otros especificados» y «no especificados» (`b798`, `s199`, `d298`, `d299`) entre los candidatos | Sugerencias sin contenido | Se excluyen los códigos terminados en 8 y 9 (convención de la CIF); los títulos del catálogo vienen truncados por el OCR, por eso no bastaba filtrar por título |
| Una ruta nueva en Caddy podía quedar sin pedir el token | Servicio expuesto sin autenticación | Bloque `route` que fija el orden; probado con Caddy real |
| Timeout de 20 s en las variables de Render (`ICF_LLM_TIMEOUT_S`) | Una sugerencia de 40–55 s se cortaría | Se fija en 90 s dentro de HU-07c (pendiente de aplicar) |

---

## 7. Limitaciones de estas pruebas

- **Son 21 casos y 73 pistas.** La dirección es consistente en funciones, estructuras y casos, pero la muestra es pequeña; no se debe leer como concluyente estadísticamente.
- **Las pistas no son criterio clínico** (ver §1). Los porcentajes absolutos no son la confiabilidad del sistema.
- **La similitud tiene un sesgo:** para casi cualquier caso físico devuelve `s750 s770 s730`, y varios aciertos de estructuras se deben a que esos códigos de extremidades coinciden con las pistas, no a que el buscador entienda el diagnóstico. En funciones salen con frecuencia `b280`, `b147` y `b117`.
- El perfil resultante llega con un nivel menos de detalle en funciones y estructuras (por ejemplo `b730` en lugar de `b7300`).
- Se evaluó un solo modelo local (`qwen2.5:3b`). El modelo de 9,6 GB instalado en el servidor no cabe junto con el otro en 12 GB y no se evaluó (decisión del 06-oct-2026 de no comparar modelos locales).

---

## 8. Decisión y siguientes pasos

**Decisión (06-oct-2026):** el modelo que selecciona y justifica las funciones y estructuras pasa a ser **externo: Claude Sonnet 5.5**, llamado desde el servicio ICF del servidor propio. El catálogo, los embeddings, la búsqueda, las reglas y el respaldo por similitud siguen en el servidor propio.

**Costo estimado** (precios de la documentación oficial de Anthropic consultada el 6-oct-2026: Sonnet 5.5 a 2 USD por millón de tokens de entrada y 10 USD por millón de salida): unos 0,003 USD por sugerencia con una lista corta de candidatos y unos 0,0065 USD con la lista completa de 154 categorías de nivel 2; es decir, menos de un centavo de dólar por sugerencia. **Latencia esperada de 2 a 6 s: es una estimación, no una medición** (se mide en HU-07f).

**Condición pendiente — privacidad.** Con un modelo externo, el diagnóstico, las notas y los datos clínicos mínimos salen de la infraestructura propia. Los datos de salud son sensibles (Ley 1581 de 2012) y la combinación de diagnóstico, edad y notas libres puede permitir reidentificar a una persona. Propuesta, pendiente de confirmar por el responsable del proyecto: usar el proveedor externo **solo con datos sintéticos** (desarrollo y QA) hasta contar con revisión legal o ética y la autorización correspondiente, mantener el modo de solo similitud para producción con pacientes reales, y revisar los términos de retención y uso de datos del proveedor en su documentación oficial.

**Trabajo siguiente** (detalle en `BACKLOG.md`, HU-07):

| HU | Qué | Puntos |
|---|---|---|
| 07f | Proveedor de LLM externo (Sonnet 5.5) con respaldo a similitud, candidatos ampliados, y comparación contra similitud y Qwen con las mismas pistas, midiendo costo y latencia | 3 |
| 07g | Hoja de revisión para el médico y definición del umbral de confiabilidad clínica | 3 |
| 07c | Backend en Render hacia el servicio ICF (timeout de 90 s) | 5 |
| 07d | Pantalla «Perfil Funcional ICF» | 5 |
| 07e | Pruebas y documentación (incluye gestión de la clave y costos) | 2 |

---

## 9. Cómo reproducir las mediciones

Todo está en `icf-service/` (ver su `README.md`). Los comandos se ejecutan en el servidor con el `.env` del servicio:

| Qué mide | Script |
|---|---|
| Latencia, desglose por etapa y JSON válido sobre los casos | `scripts/evaluate.py [--ids C02,C03] [--verbose]` |
| Dónde se va el tiempo de una llamada al modelo (prompt nuevo vs. en caché) | `scripts/benchmark_llm.py` |
| Cobertura de las pistas según la forma de buscar | `scripts/probe_retrieval.py` |
| Comparación de modos (similitud, rápido, calidad) | `scripts/compare_modes.py` |

El catálogo CIF-IA tiene derechos de autor de la OMS y no está en el repositorio (`data/private/` está ignorado por git); las pruebas que lo necesitan se omiten si no está disponible.
