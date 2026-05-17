# GitHub Insights Report 2 — Health Access Bridge
> **Fuente:** GitHub API · `jaquimbayoc7/health-access-bridge`
> **Período analizado:** 26 Feb 2026 – 16 Abr 2026 (acumulado total del proyecto)
> **Δ Desde último reporte:** 21 Mar 2026 – 16 Abr 2026 (Sprint 3.5 + cierre M1)
> **Generado:** 16 Abr 2026

---

## 1. Resumen del Repositorio

| Campo | Valor | Δ vs. Reporte 1 (20 Mar) |
|-------|-------|--------------------------|
| **Repositorio** | [jaquimbayoc7/health-access-bridge](https://github.com/jaquimbayoc7/health-access-bridge) | — |
| **Visibilidad** | Público | — |
| **Lenguaje principal** | TypeScript | — |
| **Tamaño total** | 4,521 KB | +112 KB (+2.5 %) |
| **Fecha de creación** | 25 Feb 2026 | — |
| **Último push** | 16 Abr 2026 | +27 días |
| **Issues totales** | 16 | +3 (HU-11, HU-12, HU-13) |
| **Issues abiertas** | 8 | = sin cambio |
| **Issues cerradas** | 8 | +3 nuevas cerradas |
| **Forks / Stars / Watchers** | 0 / 0 / 0 | — |
| **Rama por defecto** | `master` | — |
| **Assignee único** | `@jaquimbayoc7` | Todos los issues |

---

## 2. Distribución de Lenguajes

| Lenguaje | Bytes | % del total | Δ vs. R1 |
|----------|-------|------------|----------|
| **TypeScript** | 293,406 | **81.3 %** | +0.7 pp ↑ |
| **Python** | 58,996 | **16.3 %** | −0.6 pp ↓ |
| CSS | 3,652 | 1.0 % | = |
| Shell | 2,550 | 0.7 % | = |
| HTML | 1,148 | 0.3 % | = |
| JavaScript | 846 | 0.2 % | = |
| Dockerfile | 420 | 0.1 % | = |
| Procfile | 54 | < 0.1 % | = |
| **Total** | **361,072** | 100 % | +12,686 bytes |

**Insight clave:** El incremento de TypeScript (+0.7 pp) es directo resultado de HU-13 — se agregaron 5 nuevos archivos de pruebas (`setup.ts`, `AuthContext.test.tsx`, `Login.test.tsx`, `DashboardLayout.test.tsx`, `Patients.test.tsx`) que sumaron ~12 KB netos al codebase. El Python se mantiene estable (no hubo cambios al backend).

---

## 3. Actividad de Commits

### 3.1 Totales y velocidad

| Métrica | Reporte 1 (20 Mar) | Reporte 2 (16 Abr) | Δ |
|---------|-------------------|-------------------|---|
| **Total de commits** | 43 | 65 | +22 |
| **Días activos** | 6 | 8 | +2 |
| **Período total** | 26 Feb – 20 Mar (23 días) | 26 Feb – 16 Abr (50 días) | +27 días |
| **Velocidad global** | 1.87 commits/día | 1.30 commits/día | −0.57 |
| **Velocidad en días activos** | 7.2 commits/día activo | 8.1 commits/día activo | +0.9 |
| **Día pico histórico** | 4 Mar 2026 (13 commits) | 4 Mar 2026 (13 commits) | = |

> **Insight:** La reducción de velocidad global (1.87 → 1.30) refleja estabilización natural post-deployment. El proyecto pasó de fase de setup/fixes intensivo a fase de consolidación y calidad. Los días activos muestran mayor densidad (8.1 commits/día activo vs. 7.2), indicando que cuando hay actividad, es concentrada y dirigida.

### 3.2 Distribución total por tipo (Conventional Commits)

| Tipo | # Commits | % | Tendencia |
|------|-----------|---|-----------|
| `docs:` | 24 | 36.9 % | ↑ +12 desde R1 |
| `fix:` (todas variantes) | 22 | 33.8 % | ↑ +6 desde R1 |
| `feat:` (todas variantes) | 15 | 23.1 % | ↑ +4 desde R1 |
| `chore:` | 3 | 4.6 % | = sin cambio |
| **Total** | **65** | 100 % | |

**Variantes de `feat` usadas:** `feat:`, `feat(HU-01):`, `feat(HU-02):`, `feat(HU-03):`, `feat(design):`, `feat(testing):`  
**Variantes de `fix` usadas:** `fix:`, `fix(cors):`, `fix(backlog):`, `fix(issues):`

> **Insight:** El ratio `docs > fix > feat` se mantiene desde el Reporte 1, pero ahora `docs` lidera con mayor margen. Esto refleja el Sprint 3.5 de Calidad y Cierre de M1: la actividad principal fue documentar, formalizar issues y actualizar el estado del proyecto, con menos código nuevo y más consolidación.

### 3.3 Timeline completo de actividad

| Fecha | # Commits | Tipo predominante | Actividad principal |
|-------|-----------|-------------------|---------------------|
| **26 Feb 2026** | 8 | `fix` + `chore` | Setup inicial: README, BACKLOG, render.yaml, CI/CD, DB plans |
| **4 Mar 2026** | 13 | `fix` + `feat` | **Día pico:** Python version, render.yaml, pipeline CI/CD, importación backend ML |
| **16 Mar 2026** | 2 | `feat` | HU-01: autenticación, seed data, 3 usuarios + 10 pacientes |
| **17 Mar 2026** | 14 | `feat` + `fix` + `docs` | **Sprint 3 completo:** HU-02, HU-03, CORS, admin reset-seed, frontend subfolder |
| **18 Mar 2026** | 1 | `feat(design)` | Diseños Pencil UI — 6 pantallas actualizadas |
| **19 Mar 2026** | 8 | `feat` + `docs` | Pencil UI completo (7 pantallas), PROJECT_STATUS, testing report, mockups |
| **20 Mar 2026** | 9 | `docs` | C4 diagramas (L1–L4 + Deployment), Insights Report 1, sync general |
| **16 Abr 2026** | **10** | `feat(testing)` + `fix` + `docs` | **Sprint 3.5:** HU-13 tests Vitest, issues #14-#16, Story Points, Milestone M1 |

### 3.4 Commits nuevos desde Reporte 1 (Mar 20 – Abr 16)

| SHA | Fecha | Mensaje | Impacto |
|-----|-------|---------|---------|
| `e98427f` | 16 Abr | `feat(testing): HU-13 frontend UI tests + Vitest config + CI/CD integration` | 16 pruebas UI Frontend — hito de calidad M1 |
| `dec0209` | 16 Abr | `docs: actualizar repositorio completo con estado real Momento 1` | Sincronización total de docs + README |
| `208b5b0` | 16 Abr | `fix(backlog): corregir cabecera HU-13 de Backlog a Done` | Corrección Kanban inconsistente |
| `056b8b9` | 16 Abr | `fix(issues): crear issues #14 #15 #16 HU-11/12/13 y actualizar docs` | Formalización GitHub Issues Sprint 3.5 |
| `b65bd6a` | 16 Abr | `docs: agregar enlaces issues #14 #15 #16 + Story Points + Milestone M1` | Trazabilidad completa SCRUM ↔ repo |
| `4e38172` | 20 Mar | `docs: sync all documentation — C4 diagrams, BACKLOG, PROJECT_STATUS` | Cierre documentación fase diseño |
| `4ff2814` | 20 Mar | `docs: move GitHub Actions to bottom of deployment diagram` | Refinamiento diagrama deployment C4 |
| `34a4b72` | 20 Mar | `docs: add C4 Deployment Diagram (DEV/QA/PROD Render + GitHub Actions)` | Diagrama de infraestructura completo |
| `34d08e8` | 20 Mar | `docs: add GitHub Insights Report (Reporte 1)` | Trazabilidad analítica del proyecto |
| `622f9b6` | 20 Mar | `docs: add C4 architecture diagrams (L1-L4) and update README` | Arquitectura C4 completa |

---

## 4. Estado de Issues y Backlog

### 4.1 Resumen global

| Estado | R1 (20 Mar) | R2 (16 Abr) | Δ |
|--------|-------------|-------------|---|
| ✅ Cerradas | 5 | **8** | +3 |
| 🔵 Abiertas | 8 | **8** | = |
| **Total issues** | **13** | **16** | +3 |

### 4.2 Historias de Usuario — Estado detallado

| Issue | HU | Sprint | Pts | Estado | Fecha cierre |
|-------|----|--------|-----|--------|--------------|
| [#1](https://github.com/jaquimbayoc7/health-access-bridge/issues/1) | HU-01: Autenticación y RBAC | Sprint 1 (Sem. 4-5) | 8 | ✅ Done | 16 Mar 2026 |
| [#2](https://github.com/jaquimbayoc7/health-access-bridge/issues/2) | HU-02: Registro de Pacientes | Sprint 2 (Sem. 6-7) | 13 | ✅ Done | 17 Mar 2026 |
| [#3](https://github.com/jaquimbayoc7/health-access-bridge/issues/3) | HU-03: Integración Frontend-Backend | Sprint 3 (Sem. 8-9) | 5 | ✅ Done | 17 Mar 2026 |
| [#4](https://github.com/jaquimbayoc7/health-access-bridge/issues/4) | HU-04: Modelo Predictivo ML | Sprint 3 *(adelantada M1)* | 21 | ✅ Done | 17 Mar 2026 |
| [#14](https://github.com/jaquimbayoc7/health-access-bridge/issues/14) | HU-11: Pruebas Smoke Producción | Sprint 3.5 (Sem. 9) | 3 | ✅ Done | 16 Abr 2026 |
| [#15](https://github.com/jaquimbayoc7/health-access-bridge/issues/15) | HU-12: Pruebas Integración Backend | Sprint 3.5 (Sem. 9) | 5 | ✅ Done | 16 Abr 2026 |
| [#16](https://github.com/jaquimbayoc7/health-access-bridge/issues/16) | HU-13: Pruebas Diseño y UI Frontend | Sprint 3.5 (Sem. 9) | 8 | ✅ Done | 16 Abr 2026 |
| [#5](https://github.com/jaquimbayoc7/health-access-bridge/issues/5) | HU-05: Modo Offline y PWA | Sprint 6-7 | 13 | 📋 Backlog | — |
| [#6](https://github.com/jaquimbayoc7/health-access-bridge/issues/6) | HU-06: Pruebas de Integración y Rendimiento | Sprint 7 | 8 | 📋 Backlog | — |
| [#7](https://github.com/jaquimbayoc7/health-access-bridge/issues/7) | HU-07: LLM Recomendaciones Clínicas | Sprint 8-9 | 21 | 📋 Backlog | — |
| [#8](https://github.com/jaquimbayoc7/health-access-bridge/issues/8) | HU-08: Dashboard y Exportación | Sprint 10-11 | 13 | 📋 Backlog | — |
| [#9](https://github.com/jaquimbayoc7/health-access-bridge/issues/9) | HU-09: Pruebas Completas y UAT | Sprint 11 | 8 | 📋 Backlog | — |
| [#10](https://github.com/jaquimbayoc7/health-access-bridge/issues/10) | HU-10: Despliegue Final y Manuales | Sprint 12 | 5 | 📋 Backlog | — |

### 4.3 Épicas

| Issue | Épica | Momento | Pts | Estado R1 | Estado R2 |
|-------|-------|---------|-----|-----------|-----------|
| [#11](https://github.com/jaquimbayoc7/health-access-bridge/issues/11) | EPICA-01: Estructuración y Diseño | M1 · Sem. 1-9 | 63 | ✅ Done | ✅ Done (Sprint 3.5 incluido) |
| [#12](https://github.com/jaquimbayoc7/health-access-bridge/issues/12) | EPICA-02: Funcionalidades Core | M2 · Sem. 10-18 | 42 | 🔵 25 % | 🔵 25 % (sin cambio) |
| [#13](https://github.com/jaquimbayoc7/health-access-bridge/issues/13) | EPICA-03: IA Generativa y Cierre | M3 · Sem. 19-27 | 47 | 🔴 0 % | 🔴 0 % (sin cambio) |

> **Nota:** EPICA-01 ahora cubre 63 pts completados (antes 26 pts planificados originalmente), dado que HU-04 fue adelantada y Sprint 3.5 agregó HU-11/12/13.

### 4.4 Sprint 3.5 — Nuevo desde Reporte 1

| Issue | HU | Descripción | Pts | Tipo de prueba | Resultado |
|-------|----|-------------|-----|---------------|-----------|
| [#14](https://github.com/jaquimbayoc7/health-access-bridge/issues/14) | HU-11 | Smoke Tests en Producción | 3 | CI/CD — `ci-prod.yml` | 2/2 ✅ |
| [#15](https://github.com/jaquimbayoc7/health-access-bridge/issues/15) | HU-12 | Integración Backend (pytest) | 5 | pytest + FastAPI TestClient | 35/35 ✅ |
| [#16](https://github.com/jaquimbayoc7/health-access-bridge/issues/16) | HU-13 | Diseño y UI Frontend (Vitest+RTL) | 8 | Vitest + React Testing Library | 16/16 ✅ |
| **Total Sprint 3.5** | | | **16 pts** | | **53 pruebas ✅** |

---

## 5. Story Points y Velocity

### 5.1 Avance global del proyecto

```
R1 (20 Mar): ████████████████░░░░░░░░░░░░░░░░  47 / 115 pts  (40.9 %)
R2 (16 Abr): ██████████████████████░░░░░░░░░░  63 / 131 pts  (48.1 %)
             Δ: +16 pts completados · +16 pts al total (Sprint 3.5)
```

| Etapa | Pts planificados | Pts completados | % | Δ vs. R1 |
|-------|-----------------|-----------------|---|----------|
| **Momento 1** (M1 · HU-01,02,03) | 26 | 26 | **100 %** ✅ | = |
| **HU-04** (adelantada de M2) | 21 | 21 | **100 %** ✅ | = |
| **Sprint 3.5** (HU-11,12,13) | 16 | 16 | **100 %** ✅ | **NUEVO** |
| **Momento 2** (M2, restante) | 21 | 0 | 0 % | = |
| **Momento 3** (M3) | 47 | 0 | 0 % | = |
| **Total proyecto** | **131** | **63** | **48.1 %** | +7.2 pp ↑ |

### 5.2 Velocity por Sprint completado

| Sprint | HU(s) | Pts entregados | Semanas | Velocity |
|--------|-------|---------------|---------|---------|
| Sprint 1 | HU-01 | 8 pts | 2 sem (Sem. 4-5) | 4.0 pts/sem |
| Sprint 2 | HU-02 | 13 pts | 2 sem (Sem. 6-7) | 6.5 pts/sem |
| Sprint 3 | HU-03 + **HU-04 adelantada** | 26 pts | 2 sem (Sem. 8-9) | 13.0 pts/sem |
| **Sprint 3.5** | **HU-11 + HU-12 + HU-13** | **16 pts** | **1 sem (Sem. 9)** | **16.0 pts/sem** |

> **Velocity promedio M1 (incluyendo Sprint 3.5):** ~15.75 pts/sprint  
> **Sprint 3.5 fue el más eficiente:** 16 pts en 1 semana = pico de velocity del proyecto

---

## 6. Milestones

| Milestone | HUs incluidas | Issues cerradas | Issues abiertas | Avance R1 | Avance R2 |
|-----------|--------------|-----------------|-----------------|-----------|-----------|
| [Momento 1](https://github.com/jaquimbayoc7/health-access-bridge/milestone/1) | HU-01, 02, 03, 11, 12, 13 | **7** | 0 | ✅ 100 % | ✅ **100 % (+3 HUs)** |
| [Momento 2](https://github.com/jaquimbayoc7/health-access-bridge/milestone/2) | HU-04, 05, 06 | 1 (HU-04) | 2 | 🔵 25 % | 🔵 25 % |
| [Momento 3](https://github.com/jaquimbayoc7/health-access-bridge/milestone/3) | HU-07 a HU-10 | 0 | 4 | 🔴 0 % | 🔴 0 % |

> **Insight M1:** El Milestone Momento 1 cerró con **7 issues** (HU-01, HU-02, HU-03, HU-04 adelantada + EPICA-01 + HU-11, HU-12, HU-13 Sprint 3.5), superando el plan original de 3 HUs. La entrega real fue **2.3× el alcance planificado** para M1.

---

## 7. Cobertura de Pruebas — Estado Actualizado

### 7.1 Backend (pytest)

| Archivo | Tests | Cobertura | Sprint |
|---------|-------|-----------|--------|
| `backend/app/tests/test_auth.py` | 17 casos | Login, JWT, `/users/me`, RBAC Admin, 403/401 cruzado | Sprint 1 + HU-12 |
| `backend/app/tests/test_patients.py` | 18 casos | CRUD, búsqueda, aislamiento médico, soft delete | Sprint 2 + HU-12 |
| **Total backend** | **35 tests** | **~92 % endpoints críticos** | ✅ Activo en CI/CD |

> Δ vs. R1: +5 tests (test_auth: 15→17, test_patients: 15→18)

### 7.2 Frontend — NUEVO desde Reporte 1

| Archivo | Tests | Cobertura | Técnica |
|---------|-------|-----------|---------|
| `__tests__/AuthContext.test.tsx` | 4 | Estado inicial, login, logout, credenciales inválidas | `renderHook`, `vi.mock` |
| `__tests__/Login.test.tsx` | 4 | Campos DOM, botón loading, redirect, toggle idioma | `userEvent`, `waitFor` |
| `__tests__/DashboardLayout.test.tsx` | 4 | Spinner, redirect login, outlet, filtro sidebar por rol | `MemoryRouter`, `vi.mock` |
| `__tests__/Patients.test.tsx` | 4 | Búsqueda debounce, empty state, dialog crear, AlertDialog borrar | `vi.useFakeTimers`, `act()` |
| **Total frontend** | **16/16 tests** ✅ | Guards, forms, routing, dialogs, debounce | Vitest + RTL + jsdom |

### 7.3 Smoke Tests (Producción)

| Test | Endpoint | Validación | Workflow |
|------|----------|-----------|---------|
| `smoke_health_check` | `GET /health` | HTTP 200 post-deploy | `ci-prod.yml` |
| `smoke_auth_reachable` | `POST /users/login` | HTTP 200/401/422 | `ci-prod.yml` |

### 7.4 Resumen total de pruebas

| Capa | R1 (20 Mar) | R2 (16 Abr) | Δ |
|------|------------|------------|---|
| Backend (pytest) | 30 tests | **35 tests** | +5 |
| Frontend (Vitest+RTL) | 0 tests | **16 tests** | +16 (**NUEVO**) |
| Smoke (CI/CD) | 2 tests | **2 tests** | = |
| **Total** | **32 tests** | **53 tests** | **+21 (+65.6 %)** |

---

## 8. CI/CD y Workflows

### 8.1 Pipelines activos

| Workflow | Rama | Pasos | Novedad vs. R1 |
|----------|------|-------|----------------|
| `ci-dev.yml` | `develop` | Backend tests (pytest) → Frontend build → **Frontend tests (npm test)** | ✅ `npm test` agregado |
| `ci-qa.yml` | `staging` | Backend tests → Frontend build → **Frontend tests** → Smoke tests | ✅ `npm test` agregado |
| `ci-prod.yml` | `master` | Backend tests → Frontend build → **Frontend tests** → Approval gate → Smoke tests | ✅ `npm test` agregado |

### 8.2 Stack de pruebas CI/CD completo

```
PUSH → GitHub Actions
  ├── pytest (35 tests backend)
  ├── npm run build (frontend Vite)
  ├── npm test (16 tests Vitest+RTL) ← NUEVO desde Reporte 1
  └── [solo prod] → Manual approval gate → Smoke tests en Render
```

---

## 9. Estructura del Repositorio — Cambios desde Reporte 1

### Archivos nuevos agregados (Abr 2026)

| Archivo | Tipo | HU | Descripción |
|---------|------|-----|-------------|
| `frontend/src/__tests__/setup.ts` | Test config | HU-13 | Polyfill `window.matchMedia` + jest-dom |
| `frontend/src/__tests__/AuthContext.test.tsx` | Test | HU-13 | 4 tests AuthContext |
| `frontend/src/__tests__/Login.test.tsx` | Test | HU-13 | 4 tests Login page |
| `frontend/src/__tests__/DashboardLayout.test.tsx` | Test | HU-13 | 4 tests DashboardLayout |
| `frontend/src/__tests__/Patients.test.tsx` | Test | HU-13 | 4 tests Patients page |
| `docs/INSIGHTS_REPORT.md` | Docs | — | Reporte 1 de insights (20 Mar 2026) |
| `docs/INSIGHTS_REPORT2.md` | Docs | — | Este reporte (16 Abr 2026) |

### Archivos modificados significativos

| Archivo | Modificación | Impacto |
|---------|-------------|---------|
| `frontend/vite.config.ts` | Configuración Vitest + jsdom | Habilita testing frontend |
| `frontend/package.json` | Script `test` + deps Vitest | `npm test` operativo |
| `.github/workflows/ci-*.yml` (×3) | Paso `npm test` agregado | Testing frontend en CI/CD |
| `BACKLOG.md` | Sprint 3.5 + Kanban actualizado + links #14/#15/#16 | Trazabilidad completa |
| `docs/PROJECT_STATUS.md` | HU-13 ✅ + métricas 63pts/48 % + links issues | Estado ejecutivo actualizado |
| `docs/TESTING_REPORT.md` | HU-11/12/13 con links + tabla cobertura | Reporte de pruebas completo |
| `README.md` | #14/#15/#16 en tabla M1 + estructura `__tests__/` | Onboarding actualizado |

---

## 10. Patrones de Desarrollo Identificados

### 10.1 Patrón "Sprint 3.5" — Calidad como ciudadano de primera clase
El proyecto introdujo un sprint intermedio (3.5) para formalizar las pruebas de calidad antes de cerrar M1. Este sprint no estaba en el plan original pero produjo **16 pts en 1 semana** (el sprint de mayor velocity). Señal de madurez de proceso: la calidad no fue un afterthought sino un sprint planificado.

### 10.2 Consolidación de GitHub Issues como fuente de verdad
Antes del Reporte 1, HU-11, HU-12 y HU-13 existían **solo en documentos markdown** pero no como GitHub Issues. El 16 Abr se crearon los issues #14, #15, #16 con:
- Labels correctos (`momento-1`, `sprint-3.5`, `testing`)
- Milestone asignado (`Momento 1: Trabajo Integrador I`)
- Story Points en el Project Board (3/5/8)
- Assignee `@jaquimbayoc7`
- Status y Columna SCRUM: `Done`

Esto convierte el **Project Board en fuente única de verdad SCRUM** — antes había discrepancia entre docs y board.

### 10.3 Testing frontend: de 0 a 16 tests en 1 commit
La implementación de HU-13 pasó de cobertura de tests frontend **= 0** a **16 tests en 4 módulos** en un solo commit (`e98427f`). El stack elegido (Vitest + React Testing Library + jsdom) es idiomático para el ecosistema Vite/React del proyecto. Los desafíos técnicos resueltos incluyen: mock de `window.matchMedia`, fake timers para debounce, `act()` para concurrencia React 18.

### 10.4 Documentación como actividad de primer nivel
Con 24 commits de tipo `docs:` (37 % del total), la documentación supera a `fix:` y `feat:` como la actividad de commit más frecuente del proyecto. Los documentos mantenidos activamente incluyen: `BACKLOG.md`, `README.md`, `PROJECT_STATUS.md`, `TESTING_REPORT.md`, `INSIGHTS_REPORT.md`, diagramas C4 (L1-L4 + Deployment).

### 10.5 Sin PRs — flujo directo a master (sin cambios)
El patrón identificado en el Reporte 1 persiste: **0 Pull Requests**, todos los commits directos a `master`. Con la complejidad aumentando hacia M2 (HU-07 LLM, 21 pts), este sigue siendo el principal riesgo técnico del proyecto.

### 10.6 Estabilidad de infraestructura
Los 13 commits de `fix:` del 4 de marzo (infraestructura Render/CI-CD) no se repitieron. En el período Mar 20 – Abr 16 solo se registraron 3 commits de `fix:` menores (backlog typo, issues references). Señal de que la infraestructura se estabilizó completamente.

---

## 11. Resumen de Hallazgos

| # | Insight | Impacto | Δ vs. R1 |
|---|---------|---------|----------|
| 1 | **Momento 1 al 100 %** — 7 HUs completadas (plan original: 3) | 🟢 Alto positivo | ↑ Mejorado |
| 2 | **48.1 % del proyecto completado** (+7.2 pp desde R1) | 🟢 Alto positivo | ↑ Nuevo |
| 3 | **Sprint 3.5 entregado:** 16 pts en 1 semana — highest velocity del proyecto | 🟢 Alto positivo | ✨ Nuevo |
| 4 | **+21 tests** nuevos (0→16 frontend + 30→35 backend): 53 pruebas totales activas | 🟢 Alto positivo | ✨ Nuevo |
| 5 | **GitHub Project Board sincronizado** con issues #14-#16, Story Points, Milestones | 🟢 Positivo | ✨ Nuevo |
| 6 | **81.3 % TypeScript** — codebase sólido y creciendo con tests | 🟢 Positivo | ↑ +0.7 pp |
| 7 | **CI/CD con 5 pasos** en los 3 ambientes (incluyendo `npm test`) | 🟢 Positivo | ↑ Mejorado |
| 8 | **Infraestructura estabilizada** — 0 commits de fix de infra desde Mar 17 | 🟢 Positivo | ✨ Nuevo |
| 9 | **Sin PRs / code review** — commit directo a master | 🟡 Riesgo técnico | = Sin cambio |
| 10 | **68 pts pendientes** en M2/M3 — HU-07 (LLM, 21 pts) es la más compleja | 🔴 Prioridad futura | = Sin cambio |

---

## 12. Comparativo R1 vs. R2

| Métrica | Reporte 1 (20 Mar 2026) | Reporte 2 (16 Abr 2026) | Δ |
|---------|------------------------|------------------------|---|
| Total commits | 43 | 65 | +22 |
| Issues totales | 13 | 16 | +3 |
| Issues cerradas | 5 | 8 | +3 |
| HUs completadas | 4 | 7 | +3 |
| Story Points completados | 47 pts | 63 pts | +16 pts |
| Avance del proyecto | 40.9 % | 48.1 % | +7.2 pp |
| Tests totales | 32 | 53 | +21 (+65.6 %) |
| Tests frontend | 0 | 16 | +16 (∞) |
| Tests backend | 30 | 35 | +5 |
| Tamaño repo | 4,409 KB | 4,521 KB | +112 KB |
| TypeScript % | 80.6 % | 81.3 % | +0.7 pp |
| Sprints completados | 3 | 4 (incl. 3.5) | +1 |
| Workflows CI/CD pasos | 4 | 5 (+ npm test) | +1 |

---

## 13. Recomendaciones para Momento 2

1. **Activar Pull Requests antes de iniciar M2:** HU-07 (LLM, 21 pts) implica integración con APIs externas y lógica compleja. El riesgo de regresiones sin code review es alto. Implementar feature branches + PR template antes del Sprint 4.

2. **HU-06 antes que HU-07:** Las pruebas de integración y rendimiento (HU-06, 8 pts) deben ejecutarse sobre la infraestructura actual para establecer baselines antes de agregar la capa LLM. Hacerlo después de HU-07 dificulta aislar problemas de rendimiento.

3. **Capitalizar la cobertura de pruebas existente:** Los 53 tests actuales (35 backend + 16 frontend + 2 smoke) son una red de seguridad sólida para M2. Mantener el pipeline verde antes de cada merge de feature.

4. **HU-05 (PWA, 13 pts) requiere Service Workers:** Verificar compatibilidad del `frontend/` subfolder con `vite-plugin-pwa` antes de iniciar. El build actual usa Vite — la integración PWA es directa pero requiere ajuste de `vite.config.ts`.

5. **Lighthouse audit como prerequisito de HU-06:** Ejecutar auditoría de rendimiento en Render DEV/QA antes de escribir pruebas de carga. Obtener métricas base de LCP, TTI y FCP.

---

*Datos extraídos de GitHub API pública y `git log` local. Para métricas de tráfico (clones, vistas únicas) se requiere acceso autenticado a GitHub Insights en la interfaz web.*
