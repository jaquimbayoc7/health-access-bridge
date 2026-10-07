# Release Plan — Health Access Bridge (HAB)

**Proyecto:** Health Access Bridge
**Metodología:** SCRUM · 3 Momentos Integradores · 27 semanas · 146 story points
**Última actualización:** Octubre 2026 (HU-07 reestimada el 05 y el 06-oct-2026)
**Documentos relacionados:** [`BACKLOG.md`](../../BACKLOG.md) · [`PROJECT_STATUS.md`](./PROJECT_STATUS.md) · [`PROJECT_STATUS_M2.md`](./PROJECT_STATUS_M2.md) · [`AGILE_PRACTICES.md`](./AGILE_PRACTICES.md) · [`test-report.md`](../test-report.md)

> Este documento formaliza el Release Plan que figuraba como pendiente desde la Épica 1 ([Issue #11](https://github.com/jaquimbayoc7/health-access-bridge/issues/11)). No introduce alcance nuevo: consolida en un solo artefacto las fechas, puntos y decisiones ya publicadas en el backlog maestro y los reportes de estado de cada Momento.

---

## 1. Visión general de releases

| Release | Momento | Semanas | Milestone GitHub | Épica | Puntos | Estado |
|---------|---------|---------|-------------------|-------|--------|--------|
| **R1 — MVP Clínico** | Momento 1 | 1-9 | [Milestone 1](https://github.com/jaquimbayoc7/health-access-bridge/milestone/1) | [EPICA-01 #11](https://github.com/jaquimbayoc7/health-access-bridge/issues/11) | 63 pts | ✅ Entregado |
| **R2 — Usabilidad y Calidad** | Momento 2 | 10-18 | [Milestone 2](https://github.com/jaquimbayoc7/health-access-bridge/milestone/2) | [EPICA-02 #12](https://github.com/jaquimbayoc7/health-access-bridge/issues/12) | 24 pts | ✅ Entregado |
| **R3 — IA Generativa y Cierre** | Momento 3 | 19-27 | [Milestone 3](https://github.com/jaquimbayoc7/health-access-bridge/milestone/3) | [EPICA-03 #13](https://github.com/jaquimbayoc7/health-access-bridge/issues/13) | 59 pts | 🟡 En progreso (HU-07a, HU-07b, HU-07c, HU-07d y HU-07f completadas) |

**Total del proyecto:** 146 pts · **Completado:** 117 pts (80,1%) · **Pendiente:** 29 pts (19,9%)

> **Nota (05-oct-2026):** HU-07 se reestimó de 21 a 25 pts tras revisar el Anexo Técnico de la Resolución 1239 del 21 de julio de 2022. El Momento 3 pasó de 47 a 51 pts y el total del proyecto de 134 a 138 pts. Las cifras de los reportes anteriores (Insights 1–4, estado del Momento 1) son instantáneas históricas y no se modifican.

> **Nota (06-oct-2026):** tras las pruebas con el servidor físico y Qwen (`docs/reports/PRUEBAS_HU07_SERVIDOR_FISICO.md`), HU-07 se mantiene con modelo local de pesos abiertos (se descartó un modelo externo por privacidad) y se reestima de 25 a 33 pts: +2 de 07f (escalera Gemma/MedGemma y modelo mínimo viable), +3 de 07g (validación clínica) y +3 de 07h (dimensionamiento de la máquina de producción). HU-07a y HU-07b (13 pts) quedan completadas. El Momento 3 pasa de 51 a 59 pts y el total del proyecto de 138 a 146 pts.

---

## 2. Release 1 — MVP Clínico (Semanas 1-9) ✅

**Objetivo de release:** entregar un producto mínimo viable desplegado en la nube, con autenticación por rol, gestión de pacientes y el modelo predictivo de discapacidad funcionando de extremo a extremo, más una base de calidad (pruebas automatizadas) antes de escalar funcionalidades.

**Alcance (HUs incluidas):**

| HU | Descripción | Puntos | Sprint |
|----|-------------|--------|--------|
| HU-01 | Autenticación y Roles (RBAC) | 8 | Sprint 1 |
| HU-02 | Registro y Precarga de Pacientes | 13 | Sprint 2 |
| HU-03 | Integración Frontend-Backend y Despliegue Cloud | 5 | Sprint 3 |
| HU-04 | Modelo Predictivo ML (HybridModelDisability) — *adelantada* | 21 | Sprint 3 |
| HU-11 | Pruebas Smoke en Producción | 3 | Sprint 3.5 |
| HU-12 | Pruebas de Integración Backend | 5 | Sprint 3.5 |
| HU-13 | Pruebas de Diseño y UI Frontend | 8 | Sprint 3.5 |

**Artefactos de release:**
- 3 ambientes desplegados en Render: `hab-frontend-dev`/`hab-backend-dev`, `hab-frontend-qa`/`hab-backend-qa`, `hab-frontend`/`hab-backend-szj1` (prod), cada uno con su propia base PostgreSQL 15.
- Pipeline CI/CD con 3 workflows (`ci-dev.yml`, `ci-qa.yml`, `ci-prod.yml`), gate de aprobación manual antes de producción.
- 8 mockups de alta fidelidad, 6 diagramas C4, reporte de insights GitHub, reporte de testing.

**Criterios de salida (Definition of Done de release):**
- ✅ Los 3 ambientes responden `GET /health` con HTTP 200.
- ✅ Login, CRUD de pacientes y predicción ML operativos en producción.
- ✅ Suite de pruebas automatizadas (35 backend + 16 frontend) en verde en CI/CD.
- ✅ Smoke tests post-deploy pasando en producción.

**Fecha de cierre real:** Semana 9 (Sprint 3.5) — 100% del alcance planificado, con HU-04 entregada antes de lo previsto.

---

## 3. Release 2 — Usabilidad y Calidad (Semanas 10-18) ✅

**Objetivo de release:** cerrar las brechas de usabilidad detectadas en la investigación HCI con usuarios reales, y validar con pruebas de integración y de carga que el sistema es estable antes de sumarle la complejidad del servidor LLM de Momento 3.

**Alcance (HUs incluidas):**

| HU | Descripción | Puntos | Sprint |
|----|-------------|--------|--------|
| HU-04 | Modelo Predictivo ML *(adelantada en R1, contabilizada en Momento 2 según planificación original)* | 21 | Sprint 4-5 |
| HU-05 | Mejoras de Usabilidad derivadas de Investigación HCI | 13 | Sprint 6-7 |
| HU-05b | Ayuda contextual (Help + Tooltips ICF) traducida por idioma | 3 | Sprint 6-7 |
| HU-06 | Pruebas de Integración Backend-Frontend y Rendimiento API | 8 | Sprint 7 |

**Puntos propios completados en esta release:** 24 pts (HU-05 + HU-05b + HU-06).

**Artefactos de release:**
- `docs/HCI/09_implementacion_hci_b.html` — 4 archivos nuevos, 8 modificados, 702 líneas, 10 tareas en 3 sprints internos (tooltips ICF, onboarding, Centro de Ayuda bilingüe, gestión de expiración de sesión).
- `backend/app/tests/test_predictions.py` (9 pruebas), `frontend/e2e/` (7 specs Playwright), `backend/tests/load/k6_load_test.js`.
- 4 bugs críticos de producción encontrados y corregidos (crash en `/users/login`, soft-delete no filtrado, rutas rotas en `ci-qa.yml`, `package-lock.json` desincronizado).

**Criterios de salida:**
- ✅ Suite backend en 44/44 pruebas (cobertura 83%).
- ✅ 7 specs E2E Playwright pasando.
- ⚠️ Prueba de carga de 200 usuarios concurrentes **ejecutada** el 18-sep-2026 contra QA — resultado real **no cumple** el umbral de latencia (`p95` = 54.6s vs. `<200ms` objetivo). Se documenta como hallazgo técnico y pasa a **deuda técnica priorizada al inicio de R3** (ver §5 y `BACKLOG.md`), sin bloquear el cierre de HU-06 porque el objetivo de la historia (construir y ejecutar la suite de integración/carga) sí se cumplió.

**Fecha de cierre real:** 11-18 septiembre 2026 (cierre de HU-05/HU-06 y auditoría de coherencia de GitHub).

---

## 4. Release 3 — IA Generativa y Cierre (Semanas 19-27) 🔴 Planificado

**Objetivo de release:** incorporar un servicio ICF en servidor propio (PostgreSQL/pgvector + embeddings con Ollama) con selección asistida por un modelo local de pesos abiertos (Gemma 4 / MedGemma en prueba; decisión del 06-oct-2026 de no usar APIs externas, tras las pruebas en el servidor físico: ver `docs/reports/PRUEBAS_HU07_SERVIDOR_FISICO.md`) que, mediante RAG sobre el catálogo CIF oficial y sin fine-tuning, sugiera códigos ICF/CIF-Colombia a partir de los niveles D1-D6 y la predicción de barreras, con una pantalla "Perfil Funcional ICF" donde el médico acepta, edita o rechaza cada código; completar los dashboards de análisis exportables, y cerrar el proyecto con pruebas de aceptación de usuario y documentación final.

**Alcance planificado (HUs):**

| HU | Descripción | Puntos | Sprint |
|----|-------------|--------|--------|
| DEUDA-TÉCNICA-01 | Resolver bottleneck de rendimiento API (ver §5) — *prerrequisito antes de sumar carga del LLM* | — (ver `BACKLOG.md`) | Inicio Sprint 8 |
| HU-07 | Perfil Funcional ICF con RAG y LLM local para sugerencia de códigos CIF-IA según el Anexo Técnico de la Resolución 1239 del 21 de julio de 2022 — sub-historias 07a (servidor y catálogo, 5, ✅), 07b (motor y evaluación, 8, ✅), 07c (backend, 5, ✅), 07d (frontend, 5, ✅), 07e (pruebas y docs, 2, ✅), 07f (escalera de modelos abiertos y modelo mínimo viable `gemma4:e4b`, 2, ✅), 07g (validación clínica y umbral de confiabilidad, 3, 🟡 instrumento listo, falta la revisión), 07h (despliegue y operación en el PC de producción, 3, ✅) | 33 (reestimado desde 21 el 05-oct-2026 y desde 25 el 06-oct-2026) | Sprint 8-9 |
| HU-08 | Dashboard de Análisis y Exportación | 13 | Sprint 10-11 |
| HU-09 | Pruebas Completas y Feedback de Usuarios (UAT) | 8 | Sprint 11 |
| HU-10 | Despliegue Final y Generación de Manuales | 5 | Sprint 12 |

**Criterios de salida (Definition of Done de release):**
- El servidor local queda operativo, con el catálogo CIF y los embeddings cargados, accesible desde el backend solo por un túnel autenticado (✅ verificado en QA el 06-oct-2026), y el modelo de generación (el mínimo viable de la escalera Gemma/MedGemma, HU-07f) corre en infraestructura propia, con respaldo por similitud si falla; hay una recomendación documentada de la máquina de producción (HU-07h).
- La confiabilidad clínica del motor queda medida con la revisión de un médico y el umbral de uso definido con él (HU-07g).
- Dado un registro con niveles D1-D6, el sistema sugiere el perfil de funcionamiento (máximo 3 códigos CIF-IA por componente: funciones, estructuras, actividades y participación) con calificador y justificación; el médico puede aceptarlos, editarlos o rechazarlos, y el reporte se presenta como borrador de apoyo, no como certificado.
- Dashboard de análisis exporta a Excel/PDF sin errores.
- Pruebas UAT documentadas con feedback de usuarios reales, corregido antes del cierre.
- Aplicación desplegada en producción con manuales técnicos y de usuario entregados.

**Dependencia de infraestructura física:** a diferencia de R1/R2 (100% cloud, Render), R3 usa un servidor propio para el catálogo CIF, los embeddings y la búsqueda; es la única release del proyecto con un componente fuera de la nube. El servidor ya está operativo (06-oct-2026). La inferencia de un modelo de generación útil no corre allí: las pruebas mostraron que el i3 sin GPU no da la velocidad ni la calidad necesarias; se prueban modelos abiertos en un PC con GPU (HU-07f) para dimensionar la máquina de producción (HU-07h), que no tiene presupuesto aprobado.

---

## 5. Riesgos y mitigación

| Riesgo | Impacto | Probabilidad | Mitigación | Estado |
|--------|---------|--------------|------------|--------|
| **Bottleneck de rendimiento API** bajo carga concurrente (`p95` real = 54.6s con 200 usuarios, ver `docs/test-report.md` §4) | Alto — el servidor LLM de HU-07 añadirá más carga de cómputo sobre la misma infraestructura | Confirmado (ya ocurrió en prueba real del 18-sep-2026) | Plan de escalado documentado con pricing real de Render: ajustar `--workers`/pool de conexiones ($0) → upgrade Web Service a Pro ($85/mes) → upgrade Postgres a Pro-8gb ($100/mes) → autoescalado horizontal opcional (+$85/mes). Repetir prueba de carga tras escalar. | 🔴 Pendiente — priorizado al inicio de R3 |
| **Dependencia de hardware físico** para el servidor ICF (HU-07) | Medio — el servidor propio guarda el catálogo, los embeddings y la búsqueda | Media | Equipo disponible y operativo desde el 06-oct-2026 (i3, 12 GB, sin GPU; suficiente para búsqueda y embeddings, no para un modelo de generación útil); la producción corre en el PC propio con RTX 5050 de 8 GB (decisión del 07-oct-2026), sin compra de hardware | ✅ Mitigado |
| **Latencia de inferencia del LLM local** incompatible con uso clínico | Alto | Confirmado | Medido el 06-oct-2026: 24 a 46 s por sugerencia con `qwen2.5:3b` (hasta 55 s en la primera versión). Se descarta Qwen 3B en el i3 como selector; se miden modelos abiertos más grandes en un PC con GPU (HU-07f) y se dimensiona la máquina (HU-07h); la similitud sola responde en 0,6 s y queda como respaldo | 🟡 En medición |
| **Calidad de las sugerencias con modelos pequeños (~3B)** (códigos inventados o títulos incorrectos) | Alto — error clínico si el médico confía en la sugerencia | Confirmado | En las pruebas del 06-oct-2026 Qwen empeoró la selección frente a la similitud sola (ver `PRUEBAS_HU07_SERVIDOR_FISICO.md`). Se mantienen la lista cerrada, el título desde el catálogo, el calificador por reglas y la validación contra el catálogo; la confiabilidad clínica se mide con un médico (HU-07g) | 🟡 Mitigado en diseño; medición clínica pendiente |
| **Privacidad:** los datos de salud son sensibles (Ley 1581 de 2012) | Alto | Baja (decisión del 06-oct-2026) | No se usan APIs externas: el modelo corre en infraestructura propia y las pruebas usan solo casos sintéticos; licencias verificadas el 07-oct-2026 (Gemma 4 Apache 2.0; MedGemma descartado) | ✅ Mitigado por diseño y licencias verificadas |
| **Producción en un PC portátil propio** (suspensión, energía, disponibilidad, copia de seguridad) | Medio | Media | Decisión del 07-oct-2026: producción en el PC con RTX 5050 de 8 GB, que cumple el mínimo medido; HU-07h documenta el arranque automático, la energía, las copias de la base y el respaldo por similitud si el equipo no responde | 🟡 Por operar |
| **Conexión Render ↔ servidor local** (caída del túnel o del servidor) | Medio — solo afecta la función de sugerencias | Media | Túnel autenticado con token (✅ operativo y probado el 06-oct-2026), timeout de 90 s y respuesta 503 con aviso claro en la pantalla; el resto de la aplicación no depende del servicio (HU-07c) | 🟡 Túnel resuelto; cliente en el backend pendiente |
| **Cobertura parcial del Anexo Técnico (Res. 1239/2022)**: HAB captura 2 de las 7 categorías de discapacidad y no tiene diagnóstico CIE; sus niveles D1–D6 no son los 6 dominios oficiales | Medio — las sugerencias de funciones/estructuras serán genéricas y las de visión, audición o intelectual limitadas | Alta (confirmado al revisar el Anexo) | Campos opcionales de diagnóstico CIE y notas, mapeo explícito de dominios, reporte rotulado como borrador de apoyo y limitación documentada (HU-07) | 🟡 Mitigado en diseño |
| **Desincronización de `package-lock.json`** rompiendo deploys silenciosamente (ya ocurrió en R2) | Medio | Baja (mitigado) | Verificación de lockfile agregada al pipeline CI/CD tras el hallazgo en R2 | ✅ Mitigado |
| **Alcance HCI reemplazado sin actualizar GitHub** (HU-05 cambió de "PWA offline" a "mejoras de usabilidad" sin reflejarse en la épica) | Bajo | Baja (mitigado) | Auditoría de coherencia de GitHub ejecutada en cierre de R2 (épicas, milestones, issues corregidos) | ✅ Mitigado |

---

## 6. Ambientes y estrategia de despliegue (aplica a las 3 releases)

| Ambiente | Rama | Frontend | Backend | Aprobación |
|----------|------|----------|---------|------------|
| DEV | `develop` | `hab-frontend-dev.onrender.com` | `hab-backend-dev.onrender.com` | Automática en cada push |
| QA | `staging` | `hab-frontend-qa.onrender.com` | `hab-backend-qa.onrender.com` | Automática en cada push |
| PROD | `master` | `hab-frontend.onrender.com` | `hab-backend-szj1.onrender.com` | Manual (gate de aprobación) + smoke tests post-deploy |

Cada release se promueve siguiendo el mismo flujo: `develop` → `staging` → `master`, validado por el pipeline CI/CD (`ci-dev.yml` / `ci-qa.yml` / `ci-prod.yml`) antes de avanzar al siguiente ambiente.

---

## 7. Trazabilidad

- Backlog maestro con detalle de historias, tareas y DoD por HU: [`BACKLOG.md`](../../BACKLOG.md).
- Estado de cierre por Momento: [`PROJECT_STATUS.md`](./PROJECT_STATUS.md) (M1), [`PROJECT_STATUS_M2.md`](./PROJECT_STATUS_M2.md) (M2).
- Evidencia de prácticas ágiles (roles, eventos, artefactos, métricas): [`AGILE_PRACTICES.md`](./AGILE_PRACTICES.md).
- Resultado real de la prueba de carga y plan de escalado: [`test-report.md`](../test-report.md) §4.
