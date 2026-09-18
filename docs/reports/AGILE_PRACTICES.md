# Evidencia de Prácticas Ágiles (SCRUM) — Health Access Bridge

**Proyecto:** Health Access Bridge
**Metodología:** SCRUM adaptado a proyecto académico individual (equipo de 1 persona en rol Product Owner + Dev Team)
**Última actualización:** Septiembre 2026
**Documentos relacionados:** [`BACKLOG.md`](../../BACKLOG.md) · [`RELEASE_PLAN.md`](./RELEASE_PLAN.md) · [`PROJECT_STATUS.md`](./PROJECT_STATUS.md) · [`PROJECT_STATUS_M2.md`](./PROJECT_STATUS_M2.md) · [`INSIGHTS_REPORT3.md`](./INSIGHTS_REPORT3.md)

> Este documento no describe prácticas nuevas: mapea explícitamente el marco SCRUM (roles, eventos, artefactos) contra evidencia ya versionada en el repositorio, para que sea verificable por un tercero sin depender de actas externas.

---

## 1. Roles

| Rol SCRUM | Responsable | Evidencia |
|-----------|-------------|-----------|
| **Product Owner** | `@jaquimbayoc7` | Prioriza y redacta las historias de usuario en [`BACKLOG.md`](../../BACKLOG.md), decide alcance de cada release en [`RELEASE_PLAN.md`](./RELEASE_PLAN.md) |
| **Development Team** | `@jaquimbayoc7` (equipo unipersonal) | Autor único de commits (`INSIGHTS_REPORT3.md` §1 — "Assignee único") |
| **Scrum Master** | Rol distribuido — autogestión con apoyo de rúbrica académica como marco de control de proceso | Auditorías de coherencia documentadas en `PROJECT_STATUS_M2.md` ("Hallazgos de esta auditoría") |
| **Stakeholders / usuarios** | Dra. Emilly Maria Celis Barreto (SST — ICBF), Laura Cangrejo Perafan (Alcaldía) | Entrevistas y test de usuario documentados en [`docs/HCI/`](../HCI/) (guías de entrevista, fichas, diagrama de afinidad) |

---

## 2. Eventos SCRUM

| Evento | Cómo se aplicó | Evidencia verificable |
|--------|-----------------|------------------------|
| **Sprint Planning** | Cada HU se estima en story points antes de iniciar el sprint, con historia (Como/Deseo/Para), criterios de aceptación, tareas y Definition of Done definidos por adelantado | [`BACKLOG.md`](../../BACKLOG.md) — cada HU documenta su estimación y tareas antes del estado "Done" |
| **Daily Scrum** | Adaptado a formato asíncrono: commits frecuentes agrupados por sesiones de trabajo (patrón de "sprints reales" en bloques, propio de proyecto académico) | [`INSIGHTS_REPORT3.md`](./INSIGHTS_REPORT3.md) §3 — timeline de actividad por commit con tipo (`feat`/`fix`/`docs`/`test`) |
| **Sprint Review** | Cada HU se demuestra desplegada y accesible en los 3 ambientes (dev/qa/prod) antes de marcarse Done, no solo con revisión de código | `render.yaml` + 3 workflows CI/CD + smoke tests post-deploy en producción |
| **Sprint Retrospective** | Inspección y adaptación documentada al cierre de cada Momento: bugs encontrados, causas raíz y correcciones aplicadas | `PROJECT_STATUS_M2.md` §"Hallazgos de esta auditoría" (4 bugs críticos corregidos, coherencia de GitHub restaurada) |
| **Backlog Refinement** | Historias re-priorizadas y re-alcanzadas con base en investigación de usuario real (HCI), no solo supuestos iniciales | HU-05 cambió de "Modo Offline y PWA" a "Mejoras de Usabilidad HCI" documentado en `BACKLOG.md` y validado con [`docs/HCI/07_user_story_mapping.md`](../HCI/07_user_story_mapping.md) |

---

## 3. Artefactos SCRUM

| Artefacto | Implementación | Ubicación |
|-----------|-----------------|-----------|
| **Product Backlog** | Lista priorizada y ordenada de épicas e historias con story points | [`BACKLOG.md`](../../BACKLOG.md) |
| **Sprint Backlog** | Tareas técnicas desglosadas por HU dentro de cada sprint | Sección "Tareas" de cada HU en `BACKLOG.md` |
| **Incremento** | Software potencialmente entregable al final de cada sprint, verificado con despliegue real + pruebas automatizadas | 3 ambientes activos en Render + 87/134 pts con demo funcional |
| **Definition of Done (DoD)** | Criterio de cierre explícito por HU (código en main, pruebas pasando, documentación) | Campo "DoD" en cada HU de `BACKLOG.md` |
| **Definition of Ready (DoR)** | Criterio de entrada al sprint: historia + criterios de aceptación + estimación + sin dependencias bloqueantes | Sección "Definition of Ready" en `BACKLOG.md` |
| **Burndown / Tablero Kanban** | Estado visual Done / En Progreso / Backlog por HU y story points | Tabla "Tablero Kanban" en `BACKLOG.md` + GitHub Project board ([`projects/1`](https://github.com/users/jaquimbayoc7/projects/1)) |
| **Release Plan** | Plan de entregas por Momento con fechas, alcance y riesgos | [`RELEASE_PLAN.md`](./RELEASE_PLAN.md) |

---

## 4. Métricas ágiles

| Métrica | Valor | Fuente |
|---------|-------|--------|
| **Velocity promedio** | 14.5 SP/sprint | Sección "Seguimiento de Sprints" en `docs/presentation/index.html` |
| **Sprint efficiency** | 100% (SP planificados = SP completados en M1 y M2) | `docs/presentation/index.html` §sprints |
| **Story points completados** | 87 / 134 (64.9%) | `BACKLOG.md`, `RELEASE_PLAN.md` |
| **HUs + épicas cerradas** | 11 de 16 issues de GitHub | `INSIGHTS_REPORT3.md` §1 |
| **Distribución de commits (Conventional Commits)** | `fix` 32.8% · `docs` 28.9% · `feat` 25.8% · `chore` 7.0% · otros 5.5% | `INSIGHTS_REPORT3.md` §3.2 |
| **Cobertura de pruebas automatizadas** | Backend 44/44 (83% cobertura) · Frontend 16/16 · E2E 7 specs | `PROJECT_STATUS_M2.md`, `docs/test-report.md` |

---

## 5. Herramientas de soporte a la práctica ágil

| Herramienta | Uso |
|-------------|-----|
| **GitHub Issues** | 1 issue por HU/épica, con checklist de criterios de aceptación ([`.github/issues/`](../../.github/issues/)) |
| **GitHub Milestones** | 1 milestone por Momento (M1/M2/M3), agrupando issues y % de avance |
| **GitHub Projects (board)** | Tablero visual de HUs por estado ([`projects/1`](https://github.com/users/jaquimbayoc7/projects/1)) |
| **GitHub Actions (CI/CD)** | 3 workflows que automatizan el "Incremento potencialmente entregable" en cada push (`ci-dev.yml`, `ci-qa.yml`, `ci-prod.yml`) |
| **GitHub Insights (reportes)** | 3 reportes históricos (`INSIGHTS_REPORT.md`, `INSIGHTS_REPORT2.md`, `INSIGHTS_REPORT3.md`) usados como insumo de retrospectiva cuantitativa |
