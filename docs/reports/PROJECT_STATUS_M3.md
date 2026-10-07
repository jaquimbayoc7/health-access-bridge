# Estado del Proyecto Health Access Bridge — Momento Integrador III (corte parcial)

**Última actualización:** 6 de octubre de 2026
**Momento actual:** Momento 3 - Trabajo Integrador III (en progreso: HU-07a y HU-07b completadas)

> Este documento continúa a [`PROJECT_STATUS_M2.md`](./PROJECT_STATUS_M2.md) (cierre del Momento 2, septiembre de 2026). Es un **corte parcial**: el Momento 3 va a la mitad de HU-07 y las HU-08, HU-09 y HU-10 no han empezado. Para el análisis de lo ocurrido con el modelo local Qwen, ver [`INSIGHTS_REPORT5.md`](./INSIGHTS_REPORT5.md) y [`PRUEBAS_HU07_SERVIDOR_FISICO.md`](./PRUEBAS_HU07_SERVIDOR_FISICO.md).

---

## Resumen Ejecutivo

El proyecto lleva **100 de 144 puntos (69,4 %)**. En el Momento 3 se completaron **HU-07a** (servidor propio, túnel, catálogo y embeddings) y **HU-07b** (motor de sugerencia de códigos CIF y herramientas de evaluación), 13 de los 57 puntos del momento.

El hallazgo central del período es que **el modelo local `qwen2.5:3b` no sirve para seleccionar códigos**: en el servidor físico (Intel i3, 12 GB, sin GPU) tardó de 24 a 46 s por sugerencia y **eligió peor que la búsqueda por similitud sola**, que responde en 0,6 s. Por eso, el 6 de octubre se decidió que la selección pase a un **modelo externo (Claude Sonnet 5.5)**, manteniendo el catálogo, los embeddings y la búsqueda en el servidor propio. Esa decisión **reemplaza** la tomada el 23 de septiembre (modelo open-weight gratuito en servidor propio) y reestima HU-07 de 25 a **31 puntos**, con dos sub-historias nuevas: proveedor externo y comparación (07f) y validación clínica con un médico (07g).

Hay un tema **abierto y sin resolver**: con un modelo externo, los datos clínicos salen de la infraestructura propia (datos de salud sensibles, Ley 1581 de 2012). La propuesta es usarlo solo con datos sintéticos hasta contar con revisión legal o ética; **está pendiente de confirmar por el responsable del proyecto**.

---

## Estado por Épicas

### 🟡 EPICA-03: IA Generativa, Dashboards y Cierre (EN PROGRESO)

**Periodo:** Semanas 19-27
**Puntos:** 57 pts (HU-07 31 + HU-08 13 + HU-09 8 + HU-10 5) — **13 pts completados (22,8 %)**

> **Nota de seguimiento:** el milestone «Momento 3» de GitHub muestra 0 % porque las sub-historias de HU-07 viven en el `BACKLOG.md` y no como issues. El avance real es el de este documento.

---

## Estado por Historias de Usuario

### 🟡 HU-07: Perfil Funcional ICF con RAG y LLM externo
**Sprint:** 8-9 | **Puntos:** 31 (reestimada de 21 → 25 → 31) | **Estado:** 🟡 EN PROGRESO — 13 de 31 pts

| Sub-historia | Alcance | Pts | Estado |
|---|---|---|---|
| **07a** | Servidor propio, túnel autenticado, catálogo CIF-IA (1.593 códigos), embeddings y tabla de candidatos del Anexo | 5 | ✅ Completada 6-oct |
| **07b** | Motor de sugerencia, búsqueda, modos calidad y rápido, 25 casos de referencia y herramientas de evaluación; evaluación de Qwen | 8 | ✅ Completada 6-oct |
| 07c | Backend en Render hacia el servicio ICF (timeout de 90 s, tabla `icf_suggestions`, aceptar/editar/rechazar) | 5 | 📋 Pendiente |
| 07d | Pantalla «Perfil Funcional ICF» | 5 | 📋 Pendiente |
| 07e | Pruebas, manual de operación (clave y costos) y reportes | 2 | 📋 Pendiente |
| 07f | Proveedor de LLM externo (Claude Sonnet 5.5), candidatos ampliados y comparación | 3 | 📋 Pendiente (**nueva**) |
| 07g | Validación clínica con un médico y umbral de confiabilidad | 3 | 📋 Pendiente (**nueva**) |

**Logros técnicos del período:**
- Catálogo CIF-IA de **1.593 códigos** extraído de un PDF escaneado con OCR y revisado (3 códigos sin definición en el libro quedan fuera, pendientes de resolver).
- **Servidor propio operativo:** Ollama (`qwen2.5:3b` y `bge-m3`), PostgreSQL con pgvector en contenedor, Caddy con token y Tailscale Funnel. Los tres servicios arrancan solos al reiniciar. **Verificado desde Render QA:** `GET /icf/health` responde en 943 ms con el token válido y 401 sin él.
- **Embeddings:** 1.593 de 1.593 códigos con vector.
- **Motor:** reglas fijas (edad, calificador, capítulos), actividades desde la lista cerrada del Anexo (32 códigos), funciones y estructuras por búsqueda semántica entre los códigos de 3 dígitos, validación contra el catálogo y respaldo por similitud.
- **Mediciones:** latencia, calidad de la búsqueda y comparación de tres modos, documentadas con su método y sus limitaciones.

**Pendiente de la HU:** medir un modelo externo, medir la confiabilidad con un médico y construir backend y pantalla.

### 📋 HU-08, HU-09, HU-10
Sin cambios: Dashboard de análisis y exportación (13 pts), Pruebas completas y feedback de usuarios (8 pts) y Despliegue final y manuales (5 pts). HU-10 suma el manual de operación del servicio ICF.

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
| 3 | **Modelo externo: Claude Sonnet 5.5** | Reemplaza la decisión del 23-sep; costo estimado de menos de un centavo de dólar por sugerencia (por confirmar en 07f) |
| 4 | **Anexo Técnico de la Resolución 1239** | HU-07 se ajustó: 3 códigos por componente, estructuras con 3 calificadores, mapeo de dominios y campos de diagnóstico y notas |
| 5 | **Catálogo no publicable** | Los derechos de autor de la OMS impiden subirlo al repositorio; vive en `data/private/` (ignorado por git) |
| 6 | **Defectos corregidos al leer salidas reales** | Filtro por categoría posterior a la búsqueda, códigos «otros/no especificados» y una ruta de Caddy sin token |

---

## Métricas del Proyecto (corte 6-oct-2026)

| Métrica | Valor |
|---------|-------|
| **Puntos completados** | 100 pts |
| **Puntos pendientes** | 44 pts |
| **Total del proyecto** | 144 pts |
| **Avance general** | 69,4 % |
| **Momento 1** | ✅ 100 % (63 pts) |
| **Momento 2** | ✅ 100 % (24 pts) |
| **Momento 3** | 🟡 22,8 % (13 de 57 pts) |
| **Commits (`master`)** | 221 en 21 días activos (0,99 por día; 65 de ellos el 5 y 6 de octubre) |
| **Pull Requests mergeados** | 42 (39 en este período, 16 solo el 6 de octubre) |
| **Pruebas automáticas** | backend 52 · frontend 16 · servicio ICF 68 · **136 en total**; E2E 7 specs |
| **Tamaño del repositorio** | 8.140 KB (TypeScript 63 %, Python 34 %) |

*Las cifras del R4 y de `PROJECT_STATUS_M2.md` son instantáneas históricas y no se modifican.*

---

## Riesgos abiertos

| Riesgo | Estado |
|---|---|
| **Privacidad con el modelo externo** (datos de salud sensibles, Ley 1581 de 2012) | 🔴 Pendiente de decisión del responsable; propuesta: solo datos sintéticos hasta la revisión legal o ética |
| **Confiabilidad clínica sin medir:** las cifras actuales usan pistas no validadas por un médico | 🟡 Se mide en HU-07g |
| **Dependencia, costo y clave de un servicio externo** | 🟡 Límite de gasto mensual, clave solo en el servidor, respaldo por similitud |
| **Las 68 pruebas del servicio ICF no se ejecutan en CI** (hoy corren solo en local) | 🟡 Se agregan al pipeline en HU-07e |
| **Protección de rama eludida** (17 bypass del propietario) y exceso de PRs de promoción | 🟡 Pendiente decidir la política |
| **Seguimiento en GitHub desfasado** (milestone en 0 %, issue #7 con el alcance viejo) | 🟡 Crear las sub-historias como issues |
| **Rendimiento de la API de Render** (DEUDA-01, riesgo aceptado el 23-sep) | 🟡 Sin cambios; el servicio ICF corre fuera de Render |

---

## Próximos Pasos

1. **Decisiones previas (responsable del proyecto):** política de privacidad para el modelo externo, creación de la clave de API con límite de gasto, y confirmar la reestimación de HU-07 a 31 pts.
2. **HU-07f:** proveedor externo con respaldo por similitud, comparación contra la similitud y Qwen con las mismas pistas, medición de costo y latencia, y decisión del diseño de candidatos.
3. **HU-07g (en paralelo parcial):** hoja de revisión para el médico, medición de la confiabilidad clínica y definición del umbral de uso.
4. **HU-07c, HU-07d y HU-07e:** backend, pantalla y cierre con documentación.
5. **HU-08, HU-09 y HU-10** según el orden de `BACKLOG.md`.
6. **Higiene de proceso:** crear los issues de 07a–07g, actualizar el issue #7, agrupar las promociones entre ramas y definir la política de la protección de rama.

---

## Enlaces Importantes

- [Repositorio GitHub](https://github.com/jaquimbayoc7/health-access-bridge)
- [SCRUM Board](https://github.com/users/jaquimbayoc7/projects/1)
- [Backlog](../../BACKLOG.md)
- [Plan de release](./RELEASE_PLAN.md)
- [Insight Report 5](./INSIGHTS_REPORT5.md) — el episodio del modelo local Qwen y el proceso del período
- [Pruebas de HU-07 con el servidor físico](./PRUEBAS_HU07_SERVIDOR_FISICO.md)
- [Diseño del RAG](../diagrams/rag-icf-postgresql.md)
- [Servicio ICF](../../icf-service/README.md)
- [Estado del Proyecto — Momento 2](./PROJECT_STATUS_M2.md)
- [Estado del Proyecto — Momento 1](./PROJECT_STATUS.md)
