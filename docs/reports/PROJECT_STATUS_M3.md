# Estado del Proyecto Health Access Bridge — Momento Integrador III (corte parcial)

**Última actualización:** 26 de octubre de 2026 (cierre de HU-07g y de HU-08; el resto, al 7 de octubre)
**Momento actual:** Momento 3 - Trabajo Integrador III (en progreso: HU-07, HU-08 y HU-09 completas, 54 de 59 pts; HU-10 por iniciar)

> Este documento continúa a [`PROJECT_STATUS_M2.md`](./PROJECT_STATUS_M2.md) (cierre del Momento 2, septiembre de 2026). Es un **corte parcial**: el Momento 3 va a la mitad de HU-07 y las HU-08, HU-09 y HU-10 no han empezado. Para el análisis de lo ocurrido con el modelo local Qwen, ver [`INSIGHTS_REPORT5.md`](./INSIGHTS_REPORT5.md) y [`PRUEBAS_HU07_SERVIDOR_FISICO.md`](./PRUEBAS_HU07_SERVIDOR_FISICO.md).

---

## Resumen Ejecutivo

Al 26 de octubre el proyecto lleva **133 de 146 puntos (91,1 %)** (117 de 146 al 7 de octubre). En el Momento 3 se completaron **HU-07a** (servidor propio, túnel, catálogo y embeddings) y **HU-07b** (motor de sugerencia de códigos CIF y herramientas de evaluación), 13 de los 59 puntos del momento. El 7 de octubre se completó **HU-07f** (escalera de modelos abiertos): **15 de 59**. Ese mismo día se completaron **HU-07c** (backend de sugerencias) y **HU-07d** (pantalla): **25 de 59**. También ese día se completó **HU-07h** (producción en el PC propio, con Render, QA, reinicio y tapa verificados): **28 de 59**. También el 7 de octubre se completó **HU-07e** (E2E, pruebas del servicio ICF en CI, manual de operación y reportes): **30 de 59**.

El hallazgo central del período es que **el modelo local `qwen2.5:3b` no sirve para seleccionar códigos**: en el servidor físico (Intel i3, 12 GB, sin GPU) tardó de 24 a 46 s por sugerencia y **eligió peor que la búsqueda por similitud sola**, que responde en 0,6 s. Se evaluó pasar a un modelo externo por API (Claude Sonnet 5.5) y **se descartó por privacidad**: los datos de salud son sensibles (Ley 1581 de 2012) y todo debe quedar en infraestructura propia. La decisión del 6 de octubre es **buscar el modelo abierto mínimo viable**: probar la escalera Gemma 4 y MedGemma en un PC de pruebas con GPU (i5-13450HX, 32 GB de RAM, RTX 5050 de 8 GB) y, con esas medidas, recomendar la máquina de producción. HU-07 se reestima de 25 a **33 puntos**, con tres sub-historias nuevas: escalera de modelos abiertos (07f, 2 pts), validación clínica con un médico (07g, 3 pts) y dimensionamiento de la máquina (07h, 3 pts). **Decisión del 7 de octubre:** la producción corre en el PC propio (RTX 5050 de 8 GB), así que no se compra hardware. La revisión clínica (07g) la hará Emilly Maria Celis, profesional en salud.

Las **licencias** quedaron verificadas el 7 de octubre (`LICENCIAS_COMPONENTES_ICF.md`): Gemma 4 es Apache 2.0 y se puede usar; MedGemma no se usa porque sus términos prohíben el uso clínico.

**Resultado de HU-07f (7 de octubre):** en el PC de pruebas, `gemma4:e4b` (6,6 GB) mejora la selección sobre la similitud sola (funciones: precisión 43 % contra 29 %; estructuras: cobertura 86 % contra 67 %, contra las pistas orientativas no validadas por un médico) y responde en ~3,4 s con una GPU de 8 GB o ~15 s solo con CPU de 10 núcleos. Los otros modelos probados (`gemma4:e2b`, `medgemma:4b`, `qwen2.5:3b`) no la superan de forma útil. **Mínimo viable provisional: `gemma4:e4b`**; máquina mínima con GPU de 8 GB, 16 GB de RAM y 6 núcleos, o solo CPU de 8 núcleos con 16 GB de RAM. Los modelos de 12B a 31B no se midieron. Al medir se corrigieron dos defectos del motor con Gemma 4 (JSON en bloque de código y razonamiento previo). Detalle en [`PRUEBAS_HU07F_MODELOS_ABIERTOS.md`](./PRUEBAS_HU07F_MODELOS_ABIERTOS.md).

---

## Estado por Épicas

### 🟡 EPICA-03: IA Generativa, Dashboards y Cierre (EN PROGRESO)

**Periodo:** Semanas 19-27
**Puntos:** 59 pts (HU-07 33 + HU-08 13 + HU-09 8 + HU-10 5) — **54 pts completados (91,5 %)**

> **Nota de seguimiento:** el milestone «Momento 3» de GitHub muestra 0 % porque las sub-historias de HU-07 viven en el `BACKLOG.md` y no como issues. El avance real es el de este documento.

---

## Estado por Historias de Usuario

### 🟡 HU-07: Perfil Funcional ICF con RAG y LLM local
**Sprint:** 8-9 | **Puntos:** 33 (reestimada de 21 → 25 → 33) | **Estado:** ✅ COMPLETADA — 33 de 33 pts (07g acreditada el 26-oct-2026)

| Sub-historia | Alcance | Pts | Estado |
|---|---|---|---|
| **07a** | Servidor propio, túnel autenticado, catálogo CIF-IA (1.593 códigos), embeddings y tabla de candidatos del Anexo | 5 | ✅ Completada 6-oct |
| **07b** | Motor de sugerencia, búsqueda, modos calidad y rápido, 25 casos de referencia y herramientas de evaluación; evaluación de Qwen | 8 | ✅ Completada 6-oct |
| 07c | Backend en Render hacia el servicio ICF (timeout de 90 s, tabla `icf_suggestions`, aceptar/editar/rechazar) | 5 | ✅ Completada 7-oct (38 pruebas nuevas; la normalización de la causa pasa a 07d) |
| 07d | Pantalla «Perfil Funcional ICF» | 5 | ✅ Completada 7-oct (12 pruebas nuevas; causas oficiales en el formulario) |
| 07e | Pruebas, manual de operación (Ollama, modelos y requisitos de la máquina) y reportes | 2 | ✅ Completada 7-oct: 5 E2E (5/5 contra DEV), job `icf-service-test` en CI, `docs/manuals/MANUAL_ICF.md` y reportes actualizados |
| 07f | Escalera de modelos abiertos (Gemma 4 / MedGemma) en el PC de pruebas y modelo mínimo viable: `gemma4:e4b` | 2 | ✅ Completada 7-oct |
| 07g | Validación clínica con un médico y umbral de confiabilidad | 3 | ✅ Instrumento listo (7-oct), criterios sustentados (21-oct) y **revisión de Emilly Maria Celis devuelta el 26-oct: veredicto NO CUMPLE** (precisión estricta 59,1 % y flexible 78,8 % de b+s, cobertura 55,2 %; el κ del calificador, 0,576, y las actividades, 100 %, sí cumplen). Causas: las estructuras completan la cuota de 3 y la búsqueda no trae las funciones motoras (b730, b760, b770); detalle y sustento en el protocolo, secciones 8 y 9. 3 pts sin acreditar |
| 07h | Despliegue y operación en el PC de producción (i5-13450HX, 32 GB, RTX 5050 de 8 GB) | 3 | ✅ Completada (07-oct-2026): servicio y túnel operativos en el PC, Render configurado, prueba en QA, reinicio y tapa verificados |

**Logros técnicos del período:**
- Catálogo CIF-IA de **1.593 códigos** extraído de un PDF escaneado con OCR y revisado (3 códigos sin definición en el libro quedan fuera, pendientes de resolver).
- **Servidor propio operativo:** Ollama (`qwen2.5:3b` y `bge-m3`), PostgreSQL con pgvector en contenedor, Caddy con token y Tailscale Funnel. Los tres servicios arrancan solos al reiniciar. **Verificado desde Render QA:** `GET /icf/health` responde en 943 ms con el token válido y 401 sin él.
- **Embeddings:** 1.593 de 1.593 códigos con vector.
- **Motor:** reglas fijas (edad, calificador, capítulos), actividades desde la lista cerrada del Anexo (32 códigos), funciones y estructuras por búsqueda semántica entre los códigos de 3 dígitos, validación contra el catálogo y respaldo por similitud.
- **Mediciones:** latencia, calidad de la búsqueda y comparación de tres modos, documentadas con su método y sus limitaciones.

**Tercera ronda (26-oct), 24 casos nuevos con reglas fijadas antes de ver las sugerencias:** precisión estricta 62,7 %, flexible 86,3 %, cobertura 69,0 % y actividades 100 % cumplen; el calificador (κ ponderado 0,312) no cumple: NO CUMPLE por un solo criterio (protocolo, secciones 12 y 13). **Cierre (26-oct):** el responsable deja las métricas tal como están y acredita los 3 pts; 33 de 59 en el Momento 3. Reporte final: `docs/presentation/reporte-afinamiento-icf.html`. **Segunda ronda (26-oct):** la médica valoró las sugerencias nuevas; el motor corregido da precisión estricta 71,0 %, flexible 87,1 % y κ 0,540 (cumplen) y cobertura 58,2 % (no cumple por 1,8 puntos): NO CUMPLE por un solo criterio; ver protocolo, sección 11. **Avance (26-oct):** el motor ya incluye estructuras solo con evidencia y el vínculo de movilidad para funciones (medición preliminar: cobertura de 0,52–0,55 a 0,58–0,60; protocolo, sección 10). Producción ya actualizada (26-oct). **Recomendado tras el cierre (no bloquea):** segunda revisora, calificador con rango 0–4, apagar `ICF_MENTAL_LINK` y una cuarta ronda con casos nuevos; ver `PROTOCOLO_VALIDACION_CLINICA_HU07G.md`, secciones 13 y 14.

### 📋 HU-08, HU-09, HU-10
**HU-08 (completada el 26-oct, 13 pts):** dashboard de análisis con 10 gráficos, filtros, pestaña del perfil funcional ICF (tasa de aceptación de las sugerencias) y exportación a Excel (5 hojas) y PDF con gráficos; backend `/analytics/summary` y `/analytics/filters` con datos agregados; 18 pruebas de backend, 23 de frontend y 5 E2E, estos últimos también contra el frontend DEV desplegado (detalle en `BACKLOG.md`). **HU-09 (completada el 27-oct, 8 pts):** 18 escenarios de aceptación por rol (18/18 en DEV), accesibilidad WCAG 2.2 AA con axe-core (0 violaciones en 14 pantallas tras corregir 7 grupos de hallazgos) y sesión de usabilidad con 10 participantes (SUS medio 81,25; ver `REPORTE_FINAL_PRUEBAS_HU09.md`). En curso: Despliegue final y manuales (HU-10, 5 pts): los tres manuales (usuario, técnico y servicio ICF) están escritos y pendientes de revisión; falta el despliegue final, los reportes finales y la documentación integral del proceso bajo la plantilla del Trabajo Integrador II.

---

## Infraestructura y ambientes

| Elemento | Estado (6-oct-2026) |
|---|---|
| Backend QA / PROD | ✅ responden 200 en `/health` |
| Frontend QA / PROD | ✅ responden 200 |
| CI/CD | ✅ últimos workflows en verde en `develop`, `staging` y `master`; runners `ubuntu-26.04`; disparo manual (`workflow_dispatch`) en los tres |
| Despliegue a Render | ✅ job `deploy-qa` con hooks opcionales (si faltan los secretos, solo avisa); auto-despliegue de Render activo |
| Servicio ICF | ✅ contenedor en el servidor propio, solo en `127.0.0.1`; acceso externo únicamente por Caddy con token |
| Flujo de ramas | `develop` → `staging` → `master`; `staging` y `master` quedaron idénticas el 6-oct tras tres PRs que se saltaron `staging` |

---

## Hallazgos y decisiones de este período (5-6 Oct 2026)

| # | Hallazgo o decisión | Detalle |
|---|---|---|
| 1 | **Modelo local descartado como selector** | Peor que la similitud sola y de 24 a 46 s por sugerencia (ver `PRUEBAS_HU07_SERVIDOR_FISICO.md`) |
| 2 | **La calidad depende de la búsqueda** | Buscar solo en códigos de 3 dígitos subió la cobertura de las pistas de 11 % a 40 % (funciones) y de 48 % a 86 % (estructuras) con 12 candidatos |
| 3 | **Sin APIs externas; probar modelos abiertos** | Se descartó Claude Sonnet 5.5 por privacidad. La escalera Gemma 4 / MedGemma se prueba en un PC con GPU para hallar el modelo mínimo viable (07f) y dimensionar la máquina de producción (07h) |
| 4 | **Anexo Técnico de la Resolución 1239** | HU-07 se ajustó: 3 códigos por componente, estructuras con 3 calificadores, mapeo de dominios y campos de diagnóstico y notas |
| 5 | **Catálogo no publicable** | Los derechos de autor de la OMS impiden subirlo al repositorio; vive en `data/private/` (ignorado por git) |
| 6 | **Defectos corregidos al leer salidas reales** | Filtro por categoría posterior a la búsqueda, códigos «otros/no especificados» y una ruta de Caddy sin token |

---

## Métricas del Proyecto (corte 6-oct-2026)

| Métrica | Valor |
|---------|-------|
| **Puntos completados** | 133 pts |
| **Puntos pendientes** | 13 pts |
| **Total del proyecto** | 146 pts |
| **Avance general** | 91,1 % |
| **Momento 1** | ✅ 100 % (63 pts) |
| **Momento 2** | ✅ 100 % (24 pts) |
| **Momento 3** | 🟡 78,0 % (46 de 59 pts) |
| **Commits** | 249 en `master` (236 en `develop`; 56 son merges de promoción) en 22 días activos; 70 de ellos el 5 y 6 de octubre (93 si se cuenta el 7) |
| **Pull Requests mergeados** | 55 de 56 abiertos (corte 7-oct-2026) |
| **Pruebas automáticas** | backend 123 · frontend 61 · servicio ICF 101 (92 en CI) · **285 en total**; E2E 17 casos |
| **Tamaño del repositorio** | 8.140 KB (TypeScript 63 %, Python 34 %) |

*Las cifras del R4 y de `PROJECT_STATUS_M2.md` son instantáneas históricas y no se modifican.*

---

## Riesgos abiertos

| Riesgo | Estado |
|---|---|
| **Privacidad:** con modelo local los datos no salen de la infraestructura propia (Ley 1581 de 2012) | 🟢 Mitigado por diseño; licencias verificadas (Gemma 4 Apache 2.0; MedGemma descartado) |
| **Confiabilidad clínica:** la revisión de la médica (26-oct) dio NO CUMPLE; estructuras con precisión estricta de 44 % y funciones con cobertura de 44 % | 🟡 Medida en tres rondas y corregida; con casos nuevos cumplen 5 de 6 criterios, falla el calificador (κ 0,312). HU-07g cerrada el 26-oct como borrador de apoyo, sin uso clínico |
| **Producción en un PC portátil propio:** puede suspenderse o quedar sin internet, sin redundancia | 🟢 Mitigado (HU-07h): respaldo por similitud, arranque automático, energía sin suspensión y reinicio probado |
| **Las pruebas del servicio ICF no se ejecutaban en CI** | 🟢 Resuelto en HU-07e: job `icf-service-test` en dev, qa y prod (67 pasan; 8 de integración con el catálogo local se omiten) |
| **Protección de rama eludida** (17 bypass del propietario) y exceso de PRs de promoción | 🟡 Pendiente decidir la política |
| **Seguimiento en GitHub desfasado** (milestone en 0 %, issue #7 con el alcance viejo) | 🟡 Crear las sub-historias como issues |
| **Rendimiento de la API de Render** (DEUDA-01, riesgo aceptado el 23-sep) | 🟡 Sin cambios; el servicio ICF corre fuera de Render |

---

## Próximos Pasos

1. **Hecho (6-oct):** se confirmó el enfoque local sin APIs y la reestimación de HU-07 a 33 pts. Sin presupuesto aprobado para hardware.
2. **HU-07f (hecho, 7-oct):** `gemma4:e4b` es el mínimo viable provisional (ver `PRUEBAS_HU07F_MODELOS_ABIERTOS.md`); los modelos grandes se miden solo si la validación clínica lo exige.
3. **HU-07g (hecha, 26-oct):** tres rondas con la profesional de salud, corrección del motor y reporte final de la fase.
4. **HU-07c, HU-07d y HU-07e (hechas, 7-oct):** backend, pantalla, E2E, CI y manual listos; HU-07g quedó cerrada el 26 de octubre (ver arriba).
5. **HU-08 (hecha, 26-oct) y HU-09 (hecha, 27-oct)**; sigue **HU-10** según el orden de `BACKLOG.md`.
6. **Higiene de proceso:** crear los issues de 07a–07g, actualizar el issue #7, agrupar las promociones entre ramas y definir la política de la protección de rama.

---

## Enlaces Importantes

- [Repositorio GitHub](https://github.com/jaquimbayoc7/health-access-bridge)
- [SCRUM Board](https://github.com/users/jaquimbayoc7/projects/1)
- [Backlog](../../BACKLOG.md)
- [Plan de release](./RELEASE_PLAN.md)
- [Insight Report 5](./INSIGHTS_REPORT5.md) — el episodio del modelo local Qwen y el proceso del período
- [Pruebas de HU-07 con el servidor físico](./PRUEBAS_HU07_SERVIDOR_FISICO.md)
- [Pruebas de HU-07f con modelos abiertos](./PRUEBAS_HU07F_MODELOS_ABIERTOS.md)
- [Diseño del RAG](../diagrams/rag-icf-postgresql.md)
- [Servicio ICF](../../icf-service/README.md)
- [Estado del Proyecto — Momento 2](./PROJECT_STATUS_M2.md)
- [Estado del Proyecto — Momento 1](./PROJECT_STATUS.md)
