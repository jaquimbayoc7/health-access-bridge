# Release Plan — Health Access Bridge (HAB)

**Proyecto:** Health Access Bridge
**Metodología:** SCRUM · 3 Momentos Integradores · 27 semanas · 134 story points
**Última actualización:** Septiembre 2026
**Documentos relacionados:** [`BACKLOG.md`](../../BACKLOG.md) · [`PROJECT_STATUS.md`](./PROJECT_STATUS.md) · [`PROJECT_STATUS_M2.md`](./PROJECT_STATUS_M2.md) · [`AGILE_PRACTICES.md`](./AGILE_PRACTICES.md) · [`test-report.md`](../test-report.md)

> Este documento formaliza el Release Plan que figuraba como pendiente desde la Épica 1 ([Issue #11](https://github.com/jaquimbayoc7/health-access-bridge/issues/11)). No introduce alcance nuevo: consolida en un solo artefacto las fechas, puntos y decisiones ya publicadas en el backlog maestro y los reportes de estado de cada Momento.

---

## 1. Visión general de releases

| Release | Momento | Semanas | Milestone GitHub | Épica | Puntos | Estado |
|---------|---------|---------|-------------------|-------|--------|--------|
| **R1 — MVP Clínico** | Momento 1 | 1-9 | [Milestone 1](https://github.com/jaquimbayoc7/health-access-bridge/milestone/1) | [EPICA-01 #11](https://github.com/jaquimbayoc7/health-access-bridge/issues/11) | 63 pts | ✅ Entregado |
| **R2 — Usabilidad y Calidad** | Momento 2 | 10-18 | [Milestone 2](https://github.com/jaquimbayoc7/health-access-bridge/milestone/2) | [EPICA-02 #12](https://github.com/jaquimbayoc7/health-access-bridge/issues/12) | 24 pts | ✅ Entregado |
| **R3 — IA Generativa y Cierre** | Momento 3 | 19-27 | [Milestone 3](https://github.com/jaquimbayoc7/health-access-bridge/milestone/3) | [EPICA-03 #13](https://github.com/jaquimbayoc7/health-access-bridge/issues/13) | 47 pts | 🔴 Planificado |

**Total del proyecto:** 134 pts · **Completado:** 87 pts (64.9%) · **Pendiente:** 47 pts (35.1%)

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

**Objetivo de release:** incorporar un servidor físico on-premise con un LLM ajustado para sugerir códigos ICF/CIF-Colombia a partir de los niveles D1-D6, completar los dashboards de análisis exportables, y cerrar el proyecto con pruebas de aceptación de usuario y documentación final.

**Alcance planificado (HUs):**

| HU | Descripción | Puntos | Sprint |
|----|-------------|--------|--------|
| DEUDA-TÉCNICA-01 | Resolver bottleneck de rendimiento API (ver §5) — *prerrequisito antes de sumar carga del LLM* | — (ver `BACKLOG.md`) | Inicio Sprint 8 |
| HU-07 | Servidor Local Físico con LLM ajustado para sugerencia de códigos ICF (Colombia) | 21 | Sprint 8-9 |
| HU-08 | Dashboard de Análisis y Exportación | 13 | Sprint 10-11 |
| HU-09 | Pruebas Completas y Feedback de Usuarios (UAT) | 8 | Sprint 11 |
| HU-10 | Despliegue Final y Generación de Manuales | 5 | Sprint 12 |

**Criterios de salida (Definition of Done de release):**
- El servidor físico on-premise queda operativo en red interna, con el LLM sirviendo inferencias sin dependencia de internet.
- Dado un registro con niveles D1-D6, el LLM sugiere el código ICF/CIF correspondiente con justificación en lenguaje natural.
- Dashboard de análisis exporta a Excel/PDF sin errores.
- Pruebas UAT documentadas con feedback de usuarios reales, corregido antes del cierre.
- Aplicación desplegada en producción con manuales técnicos y de usuario entregados.

**Dependencia de infraestructura física:** a diferencia de R1/R2 (100% cloud, Render), R3 requiere aprovisionar hardware local (servidor con capacidad de inferencia) en la sede clínica — es la única release del proyecto con un componente fuera de la nube, y su cronograma depende de la disponibilidad de ese hardware.

---

## 5. Riesgos y mitigación

| Riesgo | Impacto | Probabilidad | Mitigación | Estado |
|--------|---------|--------------|------------|--------|
| **Bottleneck de rendimiento API** bajo carga concurrente (`p95` real = 54.6s con 200 usuarios, ver `docs/test-report.md` §4) | Alto — el servidor LLM de HU-07 añadirá más carga de cómputo sobre la misma infraestructura | Confirmado (ya ocurrió en prueba real del 18-sep-2026) | Plan de escalado documentado con pricing real de Render: ajustar `--workers`/pool de conexiones ($0) → upgrade Web Service a Pro ($85/mes) → upgrade Postgres a Pro-8gb ($100/mes) → autoescalado horizontal opcional (+$85/mes). Repetir prueba de carga tras escalar. | 🔴 Pendiente — priorizado al inicio de R3 |
| **Dependencia de hardware físico** para el servidor LLM (HU-07) | Alto — bloquea toda la HU si no hay servidor disponible a tiempo | Media | Definir con antelación las specs mínimas (CPU/GPU, RAM) y aprovisionar antes del Sprint 8; evaluar fallback con modelo más liviano si el hardware es limitado | 🔴 Por planificar |
| **Latencia de inferencia del LLM local** incompatible con uso clínico | Medio | Media | Definir umbral aceptable en pruebas (criterio de aceptación de HU-07) antes de seleccionar el tamaño del modelo | 🔴 Por planificar |
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
