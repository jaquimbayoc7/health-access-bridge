# Backlog Maestro: Health Access Bridge (HAB)

**Proyecto:** Health Access Bridge  
**Metodología:** SCRUM  
**Duración Total:** 27 Semanas  
**Última actualización:** Septiembre 2026 · Momento 1 y Momento 2 completados (HU-06 cerrada) · DEUDA-01 cerrada con riesgo aceptado (23-sep-2026) · Protección de rama y flujo de PR activados (23-sep-2026) · Hallazgo post-cierre de flakiness E2E corregido y validado en CI (24-sep-2026) · HU-07 redefinida con RAG y dividida en 07a–07e para iniciar Momento 3 (05-oct-2026) · HU-07 ajustada al Anexo Técnico de la Resolución 1239 de 2022 (05-oct-2026) · HU-07 reestimada a 25 pts y total del proyecto en 138 pts (05-oct-2026) · Ver [`docs/reports/INSIGHTS_REPORT4.md`](docs/reports/INSIGHTS_REPORT4.md) para el detalle completo de esta sesión.

---

## Riesgos de proceso resueltos

- **Sin PRs / code review** (detectado en `docs/reports/INSIGHTS_REPORT3.md` §9, ítem 10) — ✅ Resuelto 23-sep-2026: se activó protección de rama en GitHub para `develop`, `staging` y `master` (requiere Pull Request + checks de CI en verde — `Backend Tests` y `Frontend Build` del ambiente correspondiente — antes de mergear; sin forzar un segundo revisor dado que hay un único desarrollador). Se agregó plantilla de PR (`.github/PULL_REQUEST_TEMPLATE.md`). Configuración reproducible en `.github/scripts/branch-protection-*.json`. Validado end-to-end con [PR #18](https://github.com/jaquimbayoc7/health-access-bridge/pull/18) y [PR #19](https://github.com/jaquimbayoc7/health-access-bridge/pull/19).
- **`package-lock.json` desincronizado rompió deploys silenciosamente** (bug #4 de HU-06, ver `docs/reports/INSIGHTS_REPORT3.md` §8) — ✅ Mitigado 23-sep-2026: se agregó un paso explícito "Verificar sincronía package.json / package-lock.json" (`npm ci --dry-run`) al inicio de `frontend-build` en `ci-dev.yml`, `ci-qa.yml` y `ci-prod.yml`, que falla rápido con un mensaje claro si el lockfile queda desincronizado. Combinado con la protección de rama (punto anterior), un desync ya no puede llegar a `master` sin bloquear el merge.
- **`develop`/`staging` desincronizadas de `master` por meses** (descubierto al validar el flujo de PR, ver `docs/reports/INSIGHTS_REPORT4.md` §6.5) — ✅ Resuelto 23-sep-2026: verificado que el contenido único de esas ramas eran duplicados ya presentes en `master`, y sincronizadas las 3 al mismo commit.

---

## Tablero Kanban — Estado General

| ✅ Done | 🟡 En Progreso | 📋 Backlog |
|---------|---------------|-----------|
| EPICA-01 Estructuración y Diseño | DEUDA-01 Escalado de Rendimiento API (ver §5 Release Plan) | EPICA-03 IA Generativa y Cierre |
| HU-01 Autenticación y Roles (8 pts) | — | EPICA-03 IA Generativa y Cierre |
| HU-02 Registro y Precarga de Pacientes (13 pts) | — | HU-07 Perfil Funcional ICF con RAG y LLM local (25 pts, sub-historias 07a–07e) |
| HU-03 Integración Frontend-Backend y Despliegue Cloud (5 pts) | — | — |
| HU-04 Modelo Predictivo ML (21 pts) *(adelantada en M1)* | — | — |
| — | — | HU-08 Dashboard de Análisis y Exportación (13 pts) |
| [#14 HU-11](https://github.com/jaquimbayoc7/health-access-bridge/issues/14) Pruebas Smoke en Producción (3 pts) | — | HU-09 Pruebas Completas y Feedback (8 pts) |
| [#15 HU-12](https://github.com/jaquimbayoc7/health-access-bridge/issues/15) Pruebas de Integración Backend (5 pts) | — | HU-10 Despliegue Final y Manuales (5 pts) |
| [#16 HU-13](https://github.com/jaquimbayoc7/health-access-bridge/issues/16) Pruebas de Diseño y UI Frontend (8 pts) | — | — |
| HU-05 Mejoras de Usabilidad (HCI) (13 pts) | — | — |
| HU-05b Ayuda contextual traducida (3 pts) | — | — |
| [#6 HU-06](https://github.com/jaquimbayoc7/health-access-bridge/issues/6) Pruebas de Integración y Rendimiento (8 pts) | — | — |

**Puntos completados: 87 pts · Puntos pendientes: 51 pts · Total: 138 pts** *(HU-07 reestimada de 21 a 25 pts el 05-oct-2026; antes 47 pendientes y 134 en total)*  
**Avance general: 63% · Momento 1 100% completado (Sprint 3.5 incluido) · Momento 2 100% completado**

---

## Criterios de Priorización

El orden del backlog (qué HU va en qué sprint) se define combinando tres criterios, en este orden de peso:

1. **Dependencia técnica** — una HU que es prerrequisito de otras se prioriza primero (ej. HU-01 Auth antes que HU-02 Pacientes, porque el CRUD requiere RBAC; la deuda técnica de rendimiento se prioriza antes que HU-07 porque el servidor LLM añade carga sobre la misma API).
2. **Valor de negocio / riesgo clínico** — historias que habilitan el flujo clínico central (registro de paciente, predicción de perfil) se priorizan sobre historias de soporte (dashboards, exportación).
3. **Riesgo de usabilidad validado con usuarios reales** — hallazgos de investigación HCI (entrevistas, test de usuario, ver [`docs/HCI/07_user_story_mapping.md`](docs/HCI/07_user_story_mapping.md)) pueden re-priorizar o redefinir el alcance de una HU ya planificada (así se redefinió HU-05, de "Modo Offline y PWA" a "Mejoras de Usabilidad HCI").

Detalle completo de esta técnica de priorización y su trazabilidad con evidencia de repo: [`docs/reports/AGILE_PRACTICES.md`](docs/reports/AGILE_PRACTICES.md).

## Definition of Ready (DoR)

Una HU entra a un sprint solo si cumple:
- Historia redactada en formato Como/Deseo/Para.
- Criterios de aceptación definidos y verificables.
- Estimación en story points acordada (Planning Poker informal por complejidad relativa a HUs ya completadas).
- Sin dependencias bloqueantes de otra HU aún no completada.
- Definition of Done (DoD) explícita para saber cuándo se considera cerrada.

## MOMENTO 1: TRABAJO INTEGRADOR I (Semanas 1-9) - Avance 100% ✅

### Épica 1: Estructuración y Diseño (Semanas 1-3) ✅ Done
*Artefactos completados:*
- ✅ **Mockups de Diseño** - 8 pantallas en `frontend/design/images/`: Login, Dashboard, Pacientes, Predicciones, Admin Panel, Análisis, Guía Predictiva, Perfil Funcional ICF
- ✅ **Arquitectura C4** - 6 diagramas HTML en `docs/`: L1 Context, L2 Container, L3 Component, L4 Code (Backend), L4 Code (Frontend), Deployment
- ✅ **Reporte de Insights GitHub** - `docs/INSIGHTS_REPORT.md`
- ✅ **Reporte de Testing** - `docs/TESTING_REPORT.md`
- 📋 BPM (pendiente)
- ✅ **Release Plan** - [`docs/reports/RELEASE_PLAN.md`](docs/reports/RELEASE_PLAN.md)

### Sprint 1: Gestión de Usuarios y Estructura Backend (Semanas 4-5) ✅ Done

#### HU-01: Sistema de Autenticación y Roles (RBAC) ✅ Done
- **Como** Administrador del sistema
- **Deseo** gestionar el acceso mediante roles (Admin, Médico)
- **Para** asegurar que solo personal autorizado acceda a la información clínica.

**Detalles:**
- **Entradas:** Email, password, selección de rol.
- **Proceso:** Encriptación de claves (Bcrypt), generación de JWT.
- **Salida:** Token de sesión con claims de rol.

**Criterios de Aceptación:**
- El Admin puede crear cuentas para Médicos.
- El Médico no puede acceder a funciones de configuración global.
- Login falla con credenciales erróneas.

**Tareas:**
- Configurar boilerplate de Python/FastAPI.
- Implementar Middleware de autorización por roles.
- Crear vista de Login en React.

**DoD:** Código en main, pruebas de login exitosas, documentación de endpoints.  
**Estimación:** 8 puntos.  
**Estado:** ✅ Completado — Backend (JWT, RBAC, Bcrypt) + Frontend (Login por roles, rutas protegidas, sidebar diferenciada por rol) desplegados en los 3 ambientes.

---

### Sprint 2: Gestión de Pacientes y Base de Datos (Semanas 6-7) ✅ Done

#### HU-02: Registro y Precarga de Datos de Pacientes ✅ Done
- **Como** Médico
- **Deseo** visualizar y gestionar pacientes con datos precargados
- **Para** agilizar la consulta médica y no empezar desde cero con cada registro.

**Detalles:**
- **Entradas:** Script de migración/seed con datos demográficos base.
- **Proceso:** CRUD completo (Create, Read, Update, Delete) en base de datos relacional.
- **Salida:** Lista de pacientes con buscador y filtros.

**Criterios de Aceptación:**
- Al iniciar la app, deben existir al menos 10 pacientes de prueba.
- El Médico puede editar la historia clínica de un paciente existente.

**Tareas:**
- Diseñar esquema de base de datos (SQL).
- Crear script de "Seeding" para precarga de datos.
- Desarrollar componentes de tabla y formulario de edición.

**DoD:** CRUD funcional al 100%, base de datos normalizada, validación de campos obligatorios.  
**Estimación:** 13 puntos.  
**Estado:** ✅ Completado — Seed con 10 pacientes (5 por médico), CRUD en backend (FastAPI+PostgreSQL) y frontend (tabla, formulario, búsqueda, exportación Excel/PDF). Admin ve todos los pacientes; médico solo los propios.

---

### Sprint 3: V1 Funcional y Pruebas (Semanas 8-9) ✅ Done

#### HU-03: Integración Frontend-Backend y Despliegue Cloud ✅ Done
- **Como** Desarrollador
- **Deseo** integrar las capas de la aplicación y realizar pruebas de estrés
- **Para** garantizar la estabilidad de la versión 1.0.

**Criterios de Aceptación:**
- ✅ El frontend consume datos reales del API en todos los ambientes.
- ✅ Pruebas unitarias ejecutadas en CI con cobertura de endpoints críticos.
- ✅ Pipeline CI/CD operativo con gate de aprobación en producción.
- ✅ Smoke tests automáticos pasan en producción (`/health` 200, `/users/login` 200).

**DoD:** Despliegue en la nube (Render) en 3 ambientes independientes, pruebas de integración automáticas, CORS resuelto.  
**Estimación:** 5 puntos.  
**Estado:** ✅ Completado — Frontend consume API real (`VITE_API_BASE_URL`). CORS configurado con orígenes explícitos por ambiente. Pipeline CI/CD con 3 workflows GitHub Actions (dev/qa/prod). Smoke tests automáticos en producción. Desplegado en Render: 3 backends + 3 frontends + 3 BDs PostgreSQL independientes. `build.sh` con detección automática de cambios de esquema.

---

### Sprint 3.5: Calidad y Pruebas — Cierre Momento 1 (Semana 9) ✅ Done

#### [HU-11 — Issue #14](https://github.com/jaquimbayoc7/health-access-bridge/issues/14): Pruebas Smoke en Producción (CI/CD) ✅ Done · 3 pts · Sprint 3.5
- **Como** DevOps / QA
- **Deseo** que el pipeline valide automáticamente que la app esté viva después de cada deploy a producción
- **Para** detectar fallos críticos antes de que lleguen a los usuarios finales.

**Pruebas implementadas** (`.github/workflows/ci-prod.yml` → job `api-smoke-tests-prod`):

| # | Test | Endpoint | Validación |
|---|------|----------|-----------|
| 1 | `smoke_health_check` | `GET /health` | HTTP 200 |
| 2 | `smoke_auth_reachable` | `POST /users/login` | HTTP 200/401/422 |

**Criterios de Aceptación:**
- ✅ `/health` retorna HTTP 200 post-deploy en PROD.
- ✅ `/users/login` es alcanzable (acepta 200, 401 o 422).
- ✅ Pipeline falla automáticamente si alguno de los smoke tests falla.
- ✅ Espera a que Render termine el deploy antes de ejecutar: sondea `/health` cada 10 s hasta 10 minutos (PROD) y 8 minutos (QA), y falla si no responde 200.

**DoD:** Job `api-smoke-tests-prod` operativo en ci-prod.yml · Validado en cada push a master.  
**Estimación:** 3 puntos.  
**Estado:** ✅ Completado — Smoke tests automáticos activos en producción desde Sprint 3.

---

#### [HU-12 — Issue #15](https://github.com/jaquimbayoc7/health-access-bridge/issues/15): Pruebas de Integración Backend (pytest) ✅ Done · 5 pts · Sprint 3.5
- **Como** QA / Desarrollador
- **Deseo** un conjunto completo de pruebas de integración automatizadas para el backend
- **Para** garantizar que cada endpoint responde correctamente antes de promover a producción.

**Pruebas implementadas** (`backend/app/tests/`):

| Archivo | Casos | Cobertura |
|---------|-------|-----------|
| `test_auth.py` | 17 casos | Login, JWT, `/users/me`, RBAC Admin |
| `test_patients.py` | 18 casos | CRUD, búsqueda, aislamiento médico, soft delete |

**Criterios de Aceptación:**
- ✅ 35+ pruebas pasan en los 3 ambientes (dev/qa/prod) de forma automática.
- ✅ Aislamiento total: SQLite en memoria, sin dependencia de BD real.
- ✅ Fixtures reutilizables en `conftest.py` (admin/médico users, tokens, headers).
- ✅ RBAC validado: Admin 403/401 en rutas de médico y viceversa.

**DoD:** pytest pasa sin errores en CI/CD · Cobertura ~90% endpoints críticos · Documentado en `docs/TESTING_REPORT.md`.  
**Estimación:** 5 puntos.  
**Estado:** ✅ Completado — 35 pruebas pasan en 12.34s. Documentadas en `docs/TESTING_REPORT.md`.

---

#### [HU-13 — Issue #16](https://github.com/jaquimbayoc7/health-access-bridge/issues/16): Pruebas de Diseño y UI Frontend (Vitest + RTL) ✅ Done · 8 pts · Sprint 3.5
- **Como** QA / Desarrollador Frontend
- **Deseo** pruebas automatizadas que validen el comportamiento visual y funcional de los componentes React
- **Para** detectar regresiones de UI y garantizar que los flujos de usuario funcionen correctamente.

**Stack:** Vitest + React Testing Library + jsdom + `@testing-library/user-event`

**Criterios de Aceptación:**
- 16 casos de prueba distribuidos en 4 módulos (`AuthContext`, `Login`, `DashboardLayout`, `Patients`).
- `npm run test` operativo y pasando en los 3 workflows CI/CD.
- Cobertura de: guards de ruta, redirección por rol, formularios, debounce, diálogos, estado vacío.

**Tareas:**
- Configurar Vitest en `vite.config.ts` con entorno `jsdom`.
- Crear `frontend/src/__tests__/AuthContext.test.tsx` (4 tests).
- Crear `frontend/src/__tests__/Login.test.tsx` (4 tests).
- Crear `frontend/src/__tests__/DashboardLayout.test.tsx` (4 tests).
- Crear `frontend/src/__tests__/Patients.test.tsx` (4 tests).
- Agregar `npm run test` a los 3 workflows GitHub Actions.

**DoD:** 16 tests pasando · Script `npm run test` operativo · Integrado al CI/CD.  
**Estimación:** 8 puntos.  
**Estado:** ✅ Completado — 16/16 tests pasando en 8.36s. Vitest configurado con jsdom. Integrado a los 3 workflows CI/CD (dev/qa/prod). Commit `e98427f`.

---

## MOMENTO 2: TRABAJO INTEGRADOR II (Semanas 10-18) - Avance parcial 🟡

### Sprint 4 & 5: Inteligencia Predictiva (Semanas 10-13) ✅ Done (adelantado en M1)

#### HU-04: Integración del Modelo Predictivo de Discapacidad (HybridModelDisability) ✅ Done
- **Como** Médico
- **Deseo** ejecutar el modelo predictivo sobre los datos del paciente
- **Para** obtener su perfil de barreras de acceso a la salud y recomendaciones personalizadas.

**Detalles:**
- **Backend:** Modelo ML embebido en el backend (`model_pipeline.joblib`), entrenado con K-Means + Gradient Boosting. Endpoint `POST /patients/{id}/predict` serializa datos del paciente, ejecuta inferencia y persiste resultado en BD.
- **Frontend:** Página `Predictions.tsx` con selector de paciente, ejecución de predicción y visualización de historial. Página `PredictiveGuide.tsx` con guía clínica de los 3 perfiles.

**Criterios de Aceptación:**
- ✅ El backend responde con predicción (perfil 0, 1 o 2 + descripción).
- ✅ El frontend muestra el perfil, badge coloreado y descripción clínica.
- ✅ El resultado se persiste en el registro del paciente (campos `prediction_profile` y `prediction_description`).
- ✅ La página de Analytics muestra distribución de perfiles con gráfica de torta.

**Tareas completadas:**
- ✅ Endpoint `POST /patients/{id}/predict` en backend.
- ✅ Modelo ML cargado con lazy loading desde `model_pipeline.joblib`.
- ✅ Página `Predictions.tsx` con historial y ejecución.
- ✅ Página `PredictiveGuide.tsx` con interpretación clínica de perfiles.
- ✅ Página `Analytics.tsx` con estadísticas y gráfica de distribución.

**DoD:** Predicción integrada, UI responsiva, resultado persistido en BD.  
**Estimación:** 21 puntos.  
**Estado:** ✅ Completado (implementado en M1 adelantando el Sprint 4-5 — funcionalidad desplegada en producción).

---

### Sprint 6 & 7: Mejoras de Usabilidad (HCI) y Rendimiento (Semanas 14-17)

#### HU-05: Mejoras de Usabilidad derivadas de Investigación HCI ✅ Done
- **Como** Médico
- **Deseo** que la plataforma resuelva las fricciones de usabilidad detectadas en las entrevistas y el test de usuario
- **Para** reducir errores, inseguridad al operar el sistema y mejorar la curva de aprendizaje.

**Detalles:**
Reemplaza el alcance original de "Modo Offline y PWA" (no ejecutado). En su lugar se implementó el plan de mejoras salido de la investigación de usuarios HCI (`docs/HCI/`), documentado en `docs/HCI/09_implementacion_hci_b.html`: 4 archivos nuevos, 8 modificados, 702 líneas insertadas, 10 tareas completadas en 3 sprints.

**Tareas completadas:**
- ✅ **Sprint 1 — Correcciones críticas de usabilidad:**
  - `ICFTooltip.tsx` (nuevo) — tooltips contextuales reutilizables para los campos ICF D1–D6 (nombre oficial, descripción, ejemplos y escala 0–100).
  - `AlertDialog` de eliminación de paciente ahora muestra nombre y documento del paciente (reconocimiento en lugar de recuerdo).
  - Interceptor centralizado de errores HTTP (401/403/422/500) en `api.ts` con mensajes en español.
  - Toast de sesión expirada + logout automático ante 401.
- ✅ **Sprint 2 — Onboarding y Centro de Ayuda:**
  - `OnboardingModal.tsx` (nuevo) — guía de 4 pasos en el primer login.
  - `Help.tsx` (nuevo) — Centro de Ayuda con glosario ICF, guía de roles, perfiles de predicción y FAQ.
  - Ruta `/help` agregada en `App.tsx` y `AppSidebar.tsx`.
  - Breadcrumbs dinámicos en `DashboardLayout.tsx`.
- ✅ **Sprint 3 — Accesibilidad y gestión de sesión:**
  - Labels ICF completos + atributos `aria-*` en `Patients.tsx`.
  - `useJWTExpiry.ts` (nuevo) — alerta al usuario 5 minutos antes de que expire la sesión.

**DoD:** Cambios desplegados en frontend, documentados en `docs/HCI/09_implementacion_hci_b.html`, heurísticas de Nielsen atendidas.  
**Estimación:** 13 puntos.  
**Estado:** ✅ Completado — ver inventario completo de archivos y commits en `docs/HCI/09_implementacion_hci_b.html`.
**Pendiente detectado:** el Centro de Ayuda (`Help.tsx`) y los tooltips ICF (`ICFTooltip.tsx`) quedaron con texto fijo en español y no reaccionan al selector de idioma (`LanguageContext`) — ver corrección en HU-05b.

---

#### HU-05b: Ayuda contextual (Help + Tooltips ICF) traducida según idioma ✅ Done
- **Como** Usuario (médico o administrador) que cambia el idioma de la interfaz
- **Deseo** que el Centro de Ayuda y los tooltips de ayuda ICF cambien de idioma junto con el resto de la app
- **Para** tener una experiencia consistente sin textos de ayuda "atrapados" en español.

**Tareas:**
- Migrar `ICF_INFO` (`ICFTooltip.tsx`) y el contenido de `Help.tsx` (glosario ICF, perfiles de predicción, guía de roles, atajos, FAQ) a claves de `LanguageContext.tsx`.
- Reemplazar textos hardcodeados por `t('...')` usando `useLanguage()`.
- Verificar que el cambio de idioma desde el selector actualiza la ayuda delimitada sin recargar la página.

**DoD:** Ayuda 100% bilingüe (en/es), sin textos fijos.  
**Estimación:** 3 puntos.  
**Estado:** ✅ Completado.

---

### Sprint 7: Pruebas de Integración y Rendimiento

#### HU-06: Pruebas de integración backend-frontend y rendimiento API ✅ Done
- **Como** QA
- **Deseo** validar que la integración entre frontend y backend es estable y rápida
- **Para** asegurar la calidad y experiencia de usuario.

**Tareas completadas:**
- ✅ `backend/app/tests/test_predictions.py` — 9 pruebas de integración del flujo completo de predicción ML (`POST /patients/{id}/predict`), con modelo dummy vía `monkeypatch`.
- ✅ `frontend/e2e/` — 7 specs E2E con Playwright: login (éxito/fallo), pacientes (listado, crear, cancelar), predicciones (carga, ejecución).
- ✅ `backend/tests/load/k6_load_test.js` — script de carga con k6: rampa 0→30 usuarios concurrentes *(ajustado el 23-sep-2026 al límite real del pool de conexiones; ejecutado originalmente a 200 VUs el 18-sep-2026)*, thresholds `p95<200ms` y `error rate<1%`.
- ✅ 4 bugs críticos encontrados y corregidos: crash 500 en `/users/login` con body inválido (`FormData` no serializable), paciente con soft-delete seguía accesible por ID (`crud.get_patient` no filtraba `is_active`), rutas incorrectas en smoke tests de `ci-qa.yml` (`/api/v1/...` inexistente) + `PLAYWRIGHT_BASE_URL` mal configurado, y `package-lock.json` desincronizado que rompió 6+ deploys de frontend silenciosamente. Este último bug quedó **mitigado con un check de CI dedicado** (`npm ci --dry-run` en `frontend-build`, ver §Riesgos de proceso resueltos) y **blindado por la protección de rama** activada el 23-sep-2026.
- ✅ Causa raíz del bottleneck de carga confirmada en código y **refinada el 23-sep-2026**: no es solo el pool de 30 conexiones (a 30 VUs exactos, sin saturar el pool, `p95` sigue en 17.04s) — el limitante dominante es la **CPU fraccional del tier Starter (0.5 CPU)**, agravada por el costo computacional de `bcrypt` en el login. Detalle en `docs/test-report.md` §4 y §4.1.
- ✅ Reporte documentado en `docs/test-report.md`.

**Criterios de Aceptación:**
- ✅ Pruebas automatizadas de integración pasan al 100% (44/44 backend).
- ❌ API responde en menos de 200ms bajo carga simulada — **no cumple ni a 200 VUs (18-sep, p95=54.6s) ni a 30 VUs (23-sep, p95=17.04s, límite real del pool).** Ver hallazgo y recomendaciones en `docs/test-report.md` §4 y §4.1. **Decisión final (23-sep-2026): no se escalará la infraestructura de Render por ahora — riesgo aceptado** (ver DEUDA-01 en Momento 3, ahora cerrado). No bloquea el cierre de esta HU.

**Hecho (ya no pendiente):**
1. ✅ Prueba de carga con **200 usuarios concurrentes** ejecutada contra QA (`hab-backend-qa.onrender.com`), 18 Sep 2026.
2. ✅ `docs/reports/INSIGHTS_REPORT3.md` generado con el estado actual del proyecto.
3. ✅ `docs/reports/PROJECT_STATUS_M2.md` generado — Estado del Proyecto para Momento Integrador II posterior a la prueba de carga.
4. ✅ Prueba de carga repetida a **30 usuarios concurrentes** (límite real del pool) contra QA, 23-sep-2026 — confirma que la CPU, no el pool, es el limitante dominante.
5. ✅ `docs/reports/INSIGHTS_REPORT4.md` generado — cierre de DEUDA-01, activación de flujo de PR/protección de rama, check de CI de lockfile, sincronización de ramas develop/staging/master.
6. ✅ **Hallazgo post-cierre (24-sep-2026):** suite E2E (`patients.spec.ts`) fallaba de forma intermitente en CI por un `OnboardingModal` global que compite por `role="dialog"` con los diálogos bajo prueba. Corregido deshabilitando el modal en `frontend/e2e/utils.ts` (Bug 5, ver `docs/test-report.md` §2 y §3.1); validado con 2 corridas completas y consecutivas del pipeline de QA — 7/7 specs sin reintentos.

**DoD:** Reporte de pruebas (`docs/test-report.md`), corrección de bugs críticos.  
**Estimación:** 8 puntos.  
**Estado:** ✅ Completado — ver detalle completo en `docs/test-report.md`. Hallazgo de rendimiento bajo carga **cerrado** con decisión explícita de aceptar el riesgo (ver DEUDA-01), sin escalar infraestructura por ahora.

---

## MOMENTO 3: TRABAJO INTEGRADOR III (Semanas 19-27) - Avance 0% 🔴

### Sprint 8: Deuda Técnica de Rendimiento (previo a Sprint 8 & 9)

#### DEUDA-01: Escalado de Rendimiento de la API antes de sumar carga del LLM ✅ Cerrado (riesgo aceptado)
- **Como** equipo del proyecto
- **Deseo** resolver el cuello de botella de rendimiento detectado en producción/QA
- **Para** que el servidor LLM local de HU-07 no agrave una API que ya no cumple el umbral de latencia.

**Detalles:**
- **Hallazgo inicial:** prueba de carga de 200 usuarios concurrentes ejecutada el 18-sep-2026 contra QA — `p95` real = 54.6s (umbral definido: <200ms). Tasa de error 0.98% (sí cumple <1%). Causa raíz atribuida a: 1 worker de Uvicorn + pool SQLAlchemy de 30 conexiones + servicio en tier Starter/Basic de Render. Detalle completo en `docs/test-report.md` §4.
- **Hallazgo refinado (23-sep-2026):** se repitió la prueba igualando la concurrencia al límite real del pool (30 VUs, ver `docs/test-report.md` §4.1). Resultado: 0% de errores y `p95` mejora a 17.04s (vs. 54.6s), pero **sigue sin cumplir <200ms** incluso sin saturar el pool. Esto descarta al pool de conexiones como única causa raíz — el cuello de botella dominante es la **CPU fraccional del tier Starter (0.5 CPU)**, agravado por el costo computacional de `bcrypt` (12 rounds) en `POST /users/login`, que compite por esa CPU compartida con el resto de requests síncronos (incluso `GET /health`, sin BD, degrada a p95=592ms bajo la misma carga).
- **Origen:** descubierto durante HU-06 (Sprint 7), pasado a este ítem independiente de backlog para no bloquear el cierre de HU-06.

**Criterios de Aceptación:**
- Ajustar `--workers` de Uvicorn y `pool_size`/`max_overflow` de SQLAlchemy (mejora concurrencia, no resuelve el cuello de CPU).
- Evaluar upgrade de Web Service (Starter → Pro, más CPU) como acción prioritaria dado que el cuello de botella es de cómputo, no solo de conexiones.
- Repetir la prueba de carga (30 VUs primero, luego 200 VUs) y confirmar `p95 < 200ms`.

**Tareas:**
- ✅ Ajustar y repetir la prueba de carga a 30 VUs (límite del pool) — hecho 23-sep-2026, confirma que la CPU (no el pool) es el limitante dominante.
- Ajustar configuración de workers/pool (costo $0) — pendiente, mejora esperada menor dado el hallazgo de CPU.
- Documentar decisión de upgrade de plan Render (costo real: ver `docs/reports/RELEASE_PLAN.md` §5), priorizando CPU del Web Service.
- Repetir prueba de carga k6 (30 y 200 VUs) tras el upgrade y comparar contra baseline de `docs/test-report.md`.

**DoD:** Prueba de carga repetida con `p95 < 200ms` documentada, o decisión explícita de aceptar el riesgo con justificación de costo/beneficio.
**Estimación:** 5 puntos (spike + ajuste de configuración; no incluye el costo recurrente de infraestructura, que es una decisión de negocio, no de esfuerzo de desarrollo).
**Decisión final (23-sep-2026):** el equipo decide **no** escalar la infraestructura de Render (Web Service ni PostgreSQL) por ahora — se acepta el riesgo de latencia degradada bajo alta concurrencia (>30 usuarios simultáneos) como limitación conocida y documentada, dado que HU-07 se reorienta a un servidor local propio con Ollama (ver HU-07 más abajo), lo cual reduce la urgencia de escalar la API en la nube: el cómputo pesado del LLM ya no correrá sobre el mismo Web Service de Render.
**Estado:** ✅ Cerrado — prueba de línea base a 30 VUs completada y documentada (23-sep-2026); causa raíz identificada (CPU fraccional + bcrypt); decisión explícita de no invertir en upgrade de infraestructura por ahora. Riesgo residual aceptado y documentado en `docs/test-report.md` §4.1.

---

### Sprint 8 & 9: Servidor Local y Codificación ICF (Semanas 19-22)

#### HU-07: Perfil Funcional ICF con RAG y LLM local para Sugerencia de Códigos CIF (Colombia)
- **Como** Médico
- **Deseo** generar desde la pantalla "Perfil Funcional ICF" una sugerencia de códigos CIF/ICF a partir de los datos del paciente, sus niveles de actividad D1–D6 y la predicción de barreras, y poder **aceptar, editar o rechazar** cada código sugerido
- **Para** documentar el perfil de funcionamiento según el Anexo Técnico de la Resolución 1239 del 21 de julio de 2022, aplicable a toda la población con discapacidad de Colombia (certificación de discapacidad, CIF-IA) con razonamiento en lenguaje natural, manteniendo el criterio clínico del médico como decisión final y el procesamiento de IA en un servidor propio. El reporte es un **borrador de apoyo**: el certificado oficial lo emite el equipo multidisciplinario en el aplicativo RLCPD.

**Diseño:** [`docs/diagrams/rag-icf-postgresql.md`](docs/diagrams/rag-icf-postgresql.md) — RAG sobre PostgreSQL/pgvector, sin entrenar el modelo.

**Detalles:**
- **Enfoque (decisión 05-oct-2026):** **RAG sin fine-tuning.** No hay datos etiquetados para entrenar y un modelo de ~3B solo inventaría códigos. En cada consulta se buscan en PostgreSQL los códigos CIF candidatos y se entregan al LLM, que solo puede elegir entre ellos.
- **Reglas fijas (sin LLM):** los niveles D1–D6 de HAB corresponden a los capítulos d1–d6 de la CIF (Aprendizaje, Tareas generales, Comunicación, Movilidad, Autocuidado, Vida doméstica). **No son los 6 dominios oficiales del Anexo** (Cognición, Movilidad, Cuidado personal, Relaciones, Actividades cotidianas, Participación); decisión del 05-oct-2026: se mantienen los niveles de HAB (los usan el modelo predictivo, el formulario y los datos) con una **tabla de mapeo explícita** HAB → capítulo CIF-IA → dominio oficial, y el reporte los rotula como "niveles internos de HAB", no como el "nivel de dificultad en el desempeño" oficial. El código decide qué capítulos revisar (nivel ≥ 5) y calcula el calificador 0–4 con la escala genérica de la CIF (0–4 → 0, 5–24 → 1, 25–49 → 2, 50–95 → 3, 96–100 → 4). Es una aproximación: oficialmente el calificador sale de cada pregunta del instrumento, por lo que queda marcado como sugerido y editable. El LLM no decide la gravedad.
- **Salida oficial del perfil:** máximo **3 códigos por componente** — funciones corporales (b), estructuras corporales (s) y actividades y participación (d) — ordenados por relevancia, hasta el tercer nivel de la CIF-IA, cada uno con su calificador (un código sin calificador está incompleto). En funciones y estructuras solo cuentan calificadores ≥ 1.
- **Estructuras corporales (s) (decisión 05-oct-2026):** se incluyen con tres calificadores (magnitud, naturaleza del cambio, localización). HAB solo permite sugerir la magnitud; naturaleza y localización quedan en **8 (no especificada)** por defecto y el médico las edita.
- **Campos clínicos opcionales (decisión 05-oct-2026):** en la pantalla Perfil Funcional, "Diagnóstico CIE" y "Notas clínicas", porque el Anexo identifica funciones y estructuras desde la historia clínica (CIE, soportes, causa) y HAB solo tiene causa y 2 categorías. Se envían al servicio y se guardan como instantánea de entrada junto a la sugerencia en `icf_suggestions`; **no se agregan columnas a `patients`** (no hay migraciones y `build.sh` solo revisa un conjunto fijo de columnas).
- **Candidatos por reglas:** las tablas 7–9 y 11 del Anexo ligan cada dominio con códigos CIF-IA concretos (ej. Movilidad: d4154, d4104, d4600, d4602, d4501). Se transcriben a una tabla de candidatos como pre-filtro antes de pgvector; el PDF escaneado se lee mal en varios códigos, por lo que se transcriben revisando el original.
- **Causa de la deficiencia:** el Anexo define una lista oficial de 21 opciones en 3 grupos (selección única; "Enfermedad laboral" y "Accidente de trabajo" exigen dictamen de pérdida de capacidad laboral). El formulario de HAB ofrece 5 opciones válidas, pero los datos semilla de QA traen valores no oficiales; se normalizan.
- **Limitaciones conocidas:** HAB captura 2 de las 7 categorías de discapacidad del Anexo (física y psicosocial), por lo que la sugerencia cubrirá mejor lo físico y psicosocial que lo visual, auditivo o intelectual; y para pacientes **menores de 6 años** no hay niveles por dominio, por lo que se avisa y no se genera la sugerencia basada en D1–D6.
- **Servicio local (`icf-service/`):** FastAPI + Ollama (modelos de generación Qwen y Gemma disponibles en el servidor, más un modelo de embeddings) + PostgreSQL con pgvector y la tabla `icf_codes` (catálogo CIF oficial). Salida del LLM en JSON con lista cerrada de códigos y `temperature 0`; el título de cada código sale del catálogo, nunca del LLM.
- **Backend en Render:** nueva tabla `icf_suggestions` (columnas simples, compatible con SQLite de los tests), cliente HTTP hacia el servicio local y endpoints para generar, consultar y decidir (aceptar/editar/rechazar) cada sugerencia, con la misma regla de acceso que pacientes (médico solo los suyos, admin supervisa).
- **Conexión (decisión 05-oct-2026):** túnel autenticado (Cloudflare Tunnel o Tailscale) con token compartido entre Render y el servidor local.
- **Privacidad:** los datos identificables (nombre, documento) permanecen en Render. Al servicio local solo viajan edad, género, causa, categorías física/psicosocial, niveles D1–D6, perfil de barreras y los campos clínicos opcionales; **no se envía la orientación sexual** (no aporta a la codificación). Como las notas clínicas son texto libre, la pantalla advierte no incluir datos identificables. Esto reemplaza el criterio anterior de que "los datos nunca salen de la red local".
- **Frontend:** nueva página `FunctionalProfile` (ruta `/functional-profile`) según el mockup: selector de paciente, datos, niveles, predicción, campos opcionales de diagnóstico CIE y notas, y botón "Generar Perfil Funcional"; panel de reporte con 3 códigos por componente (b, s, d), calificador y justificación, acciones aceptar/editar/rechazar por fila, y Copiar/Descargar con encabezado "Resolución 1239 del 21 de julio de 2022" y la leyenda de borrador de apoyo.
- **Fuente del catálogo:** **CIF-IA** (versión infancia y adolescencia, OMS 2011), referencia que exige el Anexo, en PDF/Excel disponible; se carga hasta el tercer nivel con un script único.
- **Estado del catálogo (05-oct-2026):** confirmado que el archivo es la **CIF-IA** (OMS 2011, ISBN 978-92-4-354732-9, 371 páginas). Unas 175 páginas del cuerpo son imagen escaneada, por lo que se extrajeron con OCR y se revisaron contra el índice alfabético del libro y las páginas renderizadas. Resultado: **1.593 códigos con título** (b, s, d, e), sin códigos huérfanos y con los 68 códigos evaluados del Anexo 1239 presentes. Hay 3 códigos solo citados en el índice (b1125, b239, d341) sin definición en el cuerpo: no se les inventa título y **quedan fuera del catálogo, pendientes de resolver** (se agregan cuando se confirme su definición). El catálogo se guarda solo en local, en `data/private/icf/catalog_cifia.tsv` (ruta ignorada por git). Los hijos de e5750 están impresos con «d» en el libro (errata) y se normalizan a e57501–e57509. El PDF, el texto extraído y el catálogo derivado **no se publican en el repositorio** (copyright de la OMS). Detalle visual del uso de los códigos: [`docs/diagrams/cif-ia-codigos.svg`](docs/diagrams/cif-ia-codigos.svg) y apartado «Códigos CIF» de la página de presentación.
- **Aclaraciones del Anexo 1239:** el perfil lleva un **único calificador** en actividades y participación (la CIF base usa dos); los factores ambientales (e) quedan fuera del perfil del certificado (solo b, s, d); las estructuras (s) no traen definición en el cuerpo de la CIF-IA, solo título, por lo que el diagnóstico CIE y las notas pesan más en su sugerencia.
- **Fuera de alcance:** fine-tuning, y usar casos aceptados como ejemplos en el prompt (mejora posterior).

**Criterios de Aceptación:**
- El servidor local queda operativo con el LLM y el catálogo cargados, y es accesible desde el backend de Render solo mediante el túnel autenticado (token inválido → 401).
- Dado un paciente con niveles D1–D6, el sistema sugiere códigos CIF con calificador y una justificación breve; **100 % de las respuestas con JSON válido y 0 códigos que no existan en el catálogo** sobre el set de referencia validado por un médico.
- El título de cada código proviene del catálogo oficial y el calificador del cálculo por reglas (ej. d450 se muestra siempre como "Andar").
- El reporte presenta como máximo 3 códigos por componente (b, s, d); las estructuras (s) muestran los tres calificadores, con naturaleza y localización en 8 por defecto.
- El reporte indica que es un borrador de apoyo que no sustituye el certificado del RLCPD y cita la Resolución 1239 del 21 de julio de 2022.
- Para un paciente menor de 6 años, la pantalla avisa que no aplica la sugerencia basada en D1–D6.
- La petición al servicio local **no incluye nombre ni documento** del paciente.
- El médico puede aceptar, editar o rechazar cada código y la decisión queda guardada con el modelo que la sugirió.
- Si el servicio local no responde, la pantalla muestra un aviso claro y el resto de la aplicación sigue funcionando.
- Latencia de la sugerencia dentro de un umbral aceptable para uso clínico (a fijar con el médico durante 07b).
- Documentación de instalación y mantenimiento del servidor.

**Sub-historias (división de HU-07, Sprint 8 & 9):**

| ID | Alcance | Pts | Depende de |
|----|---------|-----|-----------|
| **HU-07a** | **Servidor local y catálogo:** directorio `icf-service/` con docker-compose (Ollama + PostgreSQL/pgvector), modelos Qwen/Gemma y de embeddings, tabla `icf_codes` y script de carga del catálogo **CIF-IA hasta el tercer nivel** (mínimo capítulos d1–d6, funciones corporales b y estructuras s de las causas del seed), tabla de mapeo HAB D1–D6 → capítulo CIF-IA → dominio oficial y tabla de candidatos por dominio transcrita del Anexo, túnel autenticado con token | 5 | — |
| **HU-07b** | **Motor de sugerencia y evaluación (spike de calidad):** reglas de capítulo/calificador, salida de máx. 3 códigos por componente (b, s, d) con estructuras de 3 calificadores (naturaleza/localización en 8), pre-filtro por candidatos del Anexo + búsqueda híbrida SQL + pgvector, uso de diagnóstico CIE y notas como contexto, llamada a Ollama con JSON Schema y lista cerrada, validación contra catálogo; set de referencia de 20–30 casos validado por un médico; comparación Qwen vs. Gemma (precisión, JSON válido, códigos inexistentes, latencia p50/p95) y decisión documentada del modelo | 8 | 07a |
| **HU-07c** | **Backend en Render:** modelo y esquemas `IcfSuggestion` (incluye instantánea de diagnóstico CIE y notas), CRUD, `services/icf_client.py` (túnel, token, timeout, sin nombre/documento/orientación sexual), router `icf` con generar/consultar/decidir, rechazo de pacientes menores de 6 años, normalización de la causa de la deficiencia a la lista oficial (incluidos los datos semilla), variables de entorno por ambiente en `render.yaml`, respuesta 503 si el servicio local no responde, pruebas pytest con cliente mockeado | 5 | 07b (puede avanzar en paralelo con un mock) |
| **HU-07d** | **Frontend "Perfil Funcional ICF":** página `FunctionalProfile.tsx` con campos opcionales de diagnóstico CIE y notas, tabla de 3 códigos por componente con aceptar/editar/rechazar (incluye edición de los 3 calificadores de estructuras), Copiar/Descargar (jsPDF) con encabezado Resolución 1239 del 21 de julio de 2022 y leyenda de borrador de apoyo, lista oficial de causa de deficiencia en el formulario de pacientes, ruta, menú lateral, breadcrumb, claves es/en, servicio de API, estados de carga/error/sin predicción/menor de 6 años | 5 | contrato de 07c |
| **HU-07e** | **Pruebas y documentación:** pruebas Vitest de la pantalla, spec E2E con respuesta del servicio mockeada (`page.route`, porque el servicio local no existe en QA/CI), documentación de instalación/mantenimiento, actualización de reportes y página principal | 2 | 07c, 07d |

**Avance de HU-07a (06-oct-2026):** servidor operativo (Ollama con `qwen2.5:3b`, Caddy con token y Tailscale Funnel; el servicio devuelve 401 sin token) y código en [`icf-service/`](icf-service/README.md): esquema PostgreSQL/pgvector, cargador del catálogo (1.593 códigos, carga repetible verificada en un contenedor pgvector), mapeo D1–D6 → capítulo → dominio oficial, escala de calificador, y diagnóstico `GET /icf/health` en el backend (solo admin, 8 pruebas). Variables `ICF_LLM_*` declaradas en `render.yaml` y cargadas en QA. **Pendiente para cerrar 07a:** descargar `bge-m3` y ejecutar `embed_catalog.py` en el servidor, verificar `/icf/health` en QA tras el deploy, y transcribir del Anexo el resto de la tabla de candidatos por dominio (hoy solo los 12 códigos confirmados de Movilidad y Cognición; requiere releer el PDF del Anexo contra el original).

**Riesgos y supuestos de HU-07:**
- Los niveles de HAB son por capítulo y la CIF califica por categoría; el calificador de cada categoría se toma del capítulo (aproximación). Por eso el médico puede editarlo.
- Funciones (b) y estructuras (s) se identifican oficialmente desde la historia clínica; sin diagnóstico CIE ni notas, las sugerencias de b y s serán genéricas.
- El set de referencia requiere validación médica; sin ella no se puede medir la calidad del motor.
- Un paciente sin predicción puede generar sugerencias igual (se omite el perfil de barreras del prompt).
- Si el servidor local o el túnel caen, solo esta función queda afectada.

**DoD:** Servidor local operativo con RAG sobre el catálogo CIF, sugerencias funcionando de punta a punta (frontend, backend, servicio local) con aceptar/editar/rechazar, set de referencia validado por un médico, pruebas en verde en CI y documentación de instalación y mantenimiento.  
**Estimación:** **25 puntos** (07a 5 + 07b 8 + 07c 5 + 07d 5 + 07e 2). Reestimada desde 21 puntos el 05-oct-2026 tras revisar el Anexo Técnico de la Resolución 1239 del 21 de julio de 2022 (+4: estructuras s, 3 códigos por componente, mapeo de dominios y campos clínicos). Con esto el Momento 3 pasa de 47 a **51 pts** (HU-07 25 + HU-08 13 + HU-09 8 + HU-10 5) y el total del proyecto de 134 a **138 pts** (87 completados, 63.0 %).
**Decisión de alcance confirmada (23-sep-2026, refinada el 05-oct-2026):** se usará **Ollama** sobre un servidor físico ya disponible (no se comprará hardware nuevo), con un modelo open-weight gratuito (Qwen o Gemma, a elegir en HU-07b según la evaluación) usando **RAG sobre el estándar CIF-Colombia, sin fine-tuning**. Esta decisión reduce el riesgo de presupuesto de hardware señalado en `docs/reports/INSIGHTS_REPORT3.md` §11 (punto 5) y desacopla el cómputo del LLM del Web Service de Render (ver nota de DEUDA-01 arriba).

---

### Sprint 10 & 11: Dashboards y Cierre (Semanas 23-26)

#### HU-08: Dashboard de Análisis y Exportación
- **Como** Administrador / Médico
- **Deseo** visualizar estadísticas globales y exportar reportes
- **Para** análisis y toma de decisiones a nivel poblacional.

**Tareas:**
- Crear dashboards con gráficos interactivos (Chart.js, D3.js).
- Funcionalidad de exportar a Excel y PDF.
- Despliegue final en Render.

**DoD:** Dashboard funcional, exportación sin errores, documentación.  
**Estimación:** 13 puntos.

---

### Sprint 11: Pruebas Funcionales y Usabilidad

#### HU-09: Pruebas completas y feedback de usuarios
- **Como** QA y usuarios finales
- **Deseo** validar funcionalidad, usabilidad y accesibilidad
- **Para** entregar un producto estable y usable.

**Criterios de Aceptación:**
- Pruebas manuales y automatizadas completadas.
- Feedback documentado y corregido.

**DoD:** Reporte final de pruebas, correcciones aplicadas.  
**Estimación:** 8 puntos.

---

### Sprint 12: Entrega Final y Documentación (Semana 27)

#### HU-10: Despliegue final y generación de manuales
- **Como** Equipo de proyecto
- **Deseo** desplegar la versión estable en la nube y entregar documentación completa
- **Para** cerrar el proyecto con calidad y soporte.

**Tareas:**
- Despliegue en Render.
- Documentación técnica y manuales de usuario.
- Reportes finales.

**DoD:** Aplicación en producción, documentación entregada.  
**Estimación:** 5 puntos.
