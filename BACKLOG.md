# Backlog Maestro: Health Access Bridge (HAB)

**Proyecto:** Health Access Bridge  
**Metodología:** SCRUM  
**Duración Total:** 27 Semanas  
**Última actualización:** 7 de octubre de 2026 · HU-07e completada (E2E, tests del servicio ICF en CI, manual de operación y reportes) · HU-07h completada (producción operativa en el PC propio, con Render, QA, reinicio y tapa verificados) · HU-07d completada (pantalla «Perfil Funcional ICF»; 12 pruebas nuevas de frontend) · HU-07c completada (backend con generar, consultar y decidir sugerencias; 38 pruebas nuevas) · HU-07f completada: `gemma4:e4b` propuesto como modelo mínimo viable (`docs/reports/PRUEBAS_HU07F_MODELOS_ABIERTOS.md`) · 6 de octubre de 2026 · HU-07a y HU-07b completadas; pruebas con el servidor físico y Qwen documentadas (`docs/reports/PRUEBAS_HU07_SERVIDOR_FISICO.md`); HU-07 sigue con modelo local de pesos abiertos (sin APIs externas por privacidad; Gemma/MedGemma se prueban en un PC de pruebas), se agregan 07f, 07g y 07h y el total del proyecto queda en 146 pts (06-oct-2026) · Historial: Septiembre 2026 · Momento 1 y Momento 2 completados (HU-06 cerrada) · DEUDA-01 cerrada con riesgo aceptado (23-sep-2026) · Protección de rama y flujo de PR activados (23-sep-2026) · Hallazgo post-cierre de flakiness E2E corregido y validado en CI (24-sep-2026) · HU-07 redefinida con RAG y dividida en 07a–07e para iniciar Momento 3 (05-oct-2026) · HU-07 ajustada al Anexo Técnico de la Resolución 1239 de 2022 (05-oct-2026) · HU-07 reestimada a 25 pts y total del proyecto en 138 pts (05-oct-2026) · Ver [`docs/reports/INSIGHTS_REPORT4.md`](docs/reports/INSIGHTS_REPORT4.md) para el detalle completo de esta sesión.

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
| HU-02 Registro y Precarga de Pacientes (13 pts) | HU-07 Perfil Funcional ICF con RAG y LLM local (33 pts; 07a, 07b, 07c, 07d, 07e, 07f y 07h ✅; solo 07g pendiente) | — |
| HU-03 Integración Frontend-Backend y Despliegue Cloud (5 pts) | — | — |
| HU-04 Modelo Predictivo ML (21 pts) *(adelantada en M1)* | — | — |
| — | — | HU-08 Dashboard de Análisis y Exportación (13 pts) |
| [#14 HU-11](https://github.com/jaquimbayoc7/health-access-bridge/issues/14) Pruebas Smoke en Producción (3 pts) | — | HU-09 Pruebas Completas y Feedback (8 pts) |
| [#15 HU-12](https://github.com/jaquimbayoc7/health-access-bridge/issues/15) Pruebas de Integración Backend (5 pts) | — | HU-10 Despliegue Final y Manuales (5 pts) |
| [#16 HU-13](https://github.com/jaquimbayoc7/health-access-bridge/issues/16) Pruebas de Diseño y UI Frontend (8 pts) | — | — |
| HU-05 Mejoras de Usabilidad (HCI) (13 pts) | — | — |
| HU-05b Ayuda contextual traducida (3 pts) | — | — |
| [#6 HU-06](https://github.com/jaquimbayoc7/health-access-bridge/issues/6) Pruebas de Integración y Rendimiento (8 pts) | — | — |

**Puntos completados: 117 pts · Puntos pendientes: 29 pts · Total: 146 pts** *(HU-07 reestimada de 21 a 25 pts el 05-oct-2026 y de 25 a 33 pts el 06-oct-2026 por los hallazgos de las pruebas en el servidor físico; HU-07a y HU-07b completadas el 06-oct-2026 y HU-07c, HU-07d, HU-07e, HU-07f y HU-07h el 07-oct-2026: +30 pts)*  
**Avance general: 77% · Momento 1 100% completado (Sprint 3.5 incluido) · Momento 2 100% completado**

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
- **Para** documentar el perfil de funcionamiento según el Anexo Técnico de la Resolución 1239 del 21 de julio de 2022, aplicable a toda la población con discapacidad de Colombia (certificación de discapacidad, CIF-IA) con razonamiento en lenguaje natural, manteniendo el criterio clínico del médico como decisión final. El catálogo, la búsqueda y el modelo de lenguaje (de pesos abiertos, ejecutado con Ollama) corren en infraestructura propia: ningún dato clínico sale hacia terceros. El reporte es un **borrador de apoyo**: el certificado oficial lo emite el equipo multidisciplinario en el aplicativo RLCPD.

**Diseño:** [`docs/diagrams/rag-icf-postgresql.md`](docs/diagrams/rag-icf-postgresql.md) — RAG sobre PostgreSQL/pgvector, sin entrenar el modelo. Resultados de las pruebas con el servidor físico y Qwen (06-oct-2026): [`docs/reports/PRUEBAS_HU07_SERVIDOR_FISICO.md`](docs/reports/PRUEBAS_HU07_SERVIDOR_FISICO.md).

**Detalles:**
- **Enfoque (decisión 05-oct-2026, ajustada el 06-oct-2026):** **RAG sin fine-tuning.** No hay datos etiquetados para entrenar. En cada consulta se buscan en PostgreSQL los códigos CIF candidatos y se entregan al LLM, que solo puede elegir entre ellos. **Ajuste del 06-oct-2026:** las pruebas en el servidor físico mostraron que un modelo local de ~3B (`qwen2.5:3b`) no mejora la selección sobre la búsqueda por similitud sola (con el modelo bajaron la precisión y la cobertura de las pistas) y tarda de 24 a 46 s por sugerencia en un i3 sin GPU. Se evaluó usar un modelo externo por API y **se descartó (06-oct-2026) por privacidad**: los datos de salud son sensibles (Ley 1581 de 2012) y no deben salir de la infraestructura propia. Se decide **seguir con modelos locales de pesos abiertos y buscar el modelo mínimo viable**: la escalera Gemma 4 / MedGemma se prueba en un PC de pruebas con GPU (HU-07f) y, con esas medidas, se recomienda la máquina de producción (HU-07h). **Resultado (07-oct-2026): el mínimo viable provisional es `gemma4:e4b`** (ver `docs/reports/PRUEBAS_HU07F_MODELOS_ABIERTOS.md`). El servidor actual (i3, 12 GB, sin GPU) queda para el catálogo, los embeddings, la búsqueda y la similitud como respaldo.
- **Reglas fijas (sin LLM):** los niveles D1–D6 de HAB corresponden a los capítulos d1–d6 de la CIF (Aprendizaje, Tareas generales, Comunicación, Movilidad, Autocuidado, Vida doméstica). **No son los 6 dominios oficiales del Anexo** (Cognición, Movilidad, Cuidado personal, Relaciones, Actividades cotidianas, Participación); decisión del 05-oct-2026: se mantienen los niveles de HAB (los usan el modelo predictivo, el formulario y los datos) con una **tabla de mapeo explícita** HAB → capítulo CIF-IA → dominio oficial, y el reporte los rotula como "niveles internos de HAB", no como el "nivel de dificultad en el desempeño" oficial. El código decide qué capítulos revisar (nivel ≥ 5) y calcula el calificador 0–4 con la escala genérica de la CIF (0–4 → 0, 5–24 → 1, 25–49 → 2, 50–95 → 3, 96–100 → 4). Es una aproximación: oficialmente el calificador sale de cada pregunta del instrumento, por lo que queda marcado como sugerido y editable. El LLM no decide la gravedad.
- **Salida oficial del perfil:** máximo **3 códigos por componente** — funciones corporales (b), estructuras corporales (s) y actividades y participación (d) — ordenados por relevancia, hasta el tercer nivel de la CIF-IA, cada uno con su calificador (un código sin calificador está incompleto). En funciones y estructuras solo cuentan calificadores ≥ 1.
- **Estructuras corporales (s) (decisión 05-oct-2026):** se incluyen con tres calificadores (magnitud, naturaleza del cambio, localización). HAB solo permite sugerir la magnitud; naturaleza y localización quedan en **8 (no especificada)** por defecto y el médico las edita.
- **Campos clínicos opcionales (decisión 05-oct-2026):** en la pantalla Perfil Funcional, "Diagnóstico CIE" y "Notas clínicas", porque el Anexo identifica funciones y estructuras desde la historia clínica (CIE, soportes, causa) y HAB solo tiene causa y 2 categorías. Se envían al servicio y se guardan como instantánea de entrada junto a la sugerencia en `icf_suggestions`; **no se agregan columnas a `patients`** (no hay migraciones y `build.sh` solo revisa un conjunto fijo de columnas).
- **Candidatos por reglas:** las tablas 7–9 y 11 del Anexo ligan cada dominio con códigos CIF-IA concretos (ej. Movilidad: d4154, d4104, d4600, d4602, d4501). Se transcriben a una tabla de candidatos como pre-filtro antes de pgvector; el PDF escaneado se lee mal en varios códigos, por lo que se transcriben revisando el original.
- **Causa de la deficiencia:** el Anexo define una lista oficial de 21 opciones en 3 grupos (selección única; "Enfermedad laboral" y "Accidente de trabajo" exigen dictamen de pérdida de capacidad laboral). El formulario de HAB ofrece 5 opciones válidas, pero los datos semilla de QA traen valores no oficiales; se normalizan.
- **Limitaciones conocidas:** HAB captura 2 de las 7 categorías de discapacidad del Anexo (física y psicosocial), por lo que la sugerencia cubrirá mejor lo físico y psicosocial que lo visual, auditivo o intelectual; y para pacientes **menores de 6 años** no hay niveles por dominio, por lo que se avisa y no se genera la sugerencia basada en D1–D6.
- **Servicio ICF (`icf-service/`):** FastAPI + PostgreSQL con pgvector y la tabla `icf_codes` (catálogo CIF oficial) + Ollama para los embeddings (`bge-m3`) y para el modelo de selección, en infraestructura propia. La selección de funciones y estructuras la hace un **modelo local configurable** (`ICF_LLM_MODEL`): un modelo abierto de la escalera Gemma/MedGemma (en prueba, 07f), Qwen (evaluado y descartado como selector en el servidor i3) o ninguno (solo similitud, que es también el respaldo si el modelo falla). Salida del LLM en JSON con lista cerrada de códigos; el título de cada código sale del catálogo, nunca del LLM, y el calificador de las reglas.
- **Backend en Render:** nueva tabla `icf_suggestions` (columnas simples, compatible con SQLite de los tests), cliente HTTP hacia el servicio local y endpoints para generar, consultar y decidir (aceptar/editar/rechazar) cada sugerencia, con la misma regla de acceso que pacientes (médico solo los suyos, admin supervisa).
- **Conexión (decisión 05-oct-2026, implementada el 06-oct-2026):** túnel autenticado (Tailscale Funnel + Caddy con token) entre Render y el servidor local. No hay llamadas a APIs externas ni claves de terceros: el modelo corre en Ollama dentro de la infraestructura propia.
- **Privacidad:** los datos identificables (nombre, documento) permanecen en Render. Al servicio local solo viajan edad, género, causa, categorías física/psicosocial, niveles D1–D6, perfil de barreras y los campos clínicos opcionales; **no se envía la orientación sexual** (no aporta a la codificación). Como las notas clínicas son texto libre, la pantalla advierte no incluir datos identificables. **Decisión del 06-oct-2026:** no se usan APIs externas; el modelo de lenguaje corre en infraestructura propia, de modo que el diagnóstico, las notas y los datos clínicos mínimos **no salen** del entorno controlado por el proyecto (Ley 1581 de 2012, datos sensibles). Las pruebas se hacen con casos sintéticos en un PC de pruebas propio. Pendiente: verificar las licencias de uso de los modelos abiertos (Gemma, MedGemma) antes de producción.
- **Frontend:** nueva página `FunctionalProfile` (ruta `/functional-profile`) según el mockup: selector de paciente, datos, niveles, predicción, campos opcionales de diagnóstico CIE y notas, y botón "Generar Perfil Funcional"; panel de reporte con 3 códigos por componente (b, s, d), calificador y justificación, acciones aceptar/editar/rechazar por fila, y Copiar/Descargar con encabezado "Resolución 1239 del 21 de julio de 2022" y la leyenda de borrador de apoyo.
- **Fuente del catálogo:** **CIF-IA** (versión infancia y adolescencia, OMS 2011), referencia que exige el Anexo, en PDF/Excel disponible; se carga hasta el tercer nivel con un script único.
- **Estado del catálogo (05-oct-2026):** confirmado que el archivo es la **CIF-IA** (OMS 2011, ISBN 978-92-4-354732-9, 371 páginas). Unas 175 páginas del cuerpo son imagen escaneada, por lo que se extrajeron con OCR y se revisaron contra el índice alfabético del libro y las páginas renderizadas. Resultado: **1.593 códigos con título** (b, s, d, e), sin códigos huérfanos y con los 68 códigos evaluados del Anexo 1239 presentes. Hay 3 códigos solo citados en el índice (b1125, b239, d341) sin definición en el cuerpo: no se les inventa título y **quedan fuera del catálogo, pendientes de resolver** (se agregan cuando se confirme su definición). El catálogo se guarda solo en local, en `data/private/icf/catalog_cifia.tsv` (ruta ignorada por git). Los hijos de e5750 están impresos con «d» en el libro (errata) y se normalizan a e57501–e57509. El PDF, el texto extraído y el catálogo derivado **no se publican en el repositorio** (copyright de la OMS). Detalle visual del uso de los códigos: [`docs/diagrams/cif-ia-codigos.svg`](docs/diagrams/cif-ia-codigos.svg) y apartado «Códigos CIF» de la página de presentación.
- **Aclaraciones del Anexo 1239:** el perfil lleva un **único calificador** en actividades y participación (la CIF base usa dos); los factores ambientales (e) quedan fuera del perfil del certificado (solo b, s, d); las estructuras (s) no traen definición en el cuerpo de la CIF-IA, solo título, por lo que el diagnóstico CIE y las notas pesan más en su sugerencia.
- **Fuera de alcance:** fine-tuning, y usar casos aceptados como ejemplos en el prompt (mejora posterior).

**Criterios de Aceptación:**
- El servidor local queda operativo con el catálogo y los embeddings cargados, y es accesible desde el backend de Render solo mediante el túnel autenticado (token inválido → 401).
- Dado un paciente con niveles D1–D6, el sistema sugiere códigos CIF con calificador y una justificación breve; **100 % de las respuestas con JSON válido y 0 códigos que no existan en el catálogo** sobre el set de referencia validado por un médico.
- El título de cada código proviene del catálogo oficial y el calificador del cálculo por reglas (ej. d450 se muestra siempre como "Andar").
- El reporte presenta como máximo 3 códigos por componente (b, s, d); las estructuras (s) muestran los tres calificadores, con naturaleza y localización en 8 por defecto.
- El reporte indica que es un borrador de apoyo que no sustituye el certificado del RLCPD y cita la Resolución 1239 del 21 de julio de 2022.
- Para un paciente menor de 6 años, la pantalla avisa que no aplica la sugerencia basada en D1–D6.
- Ninguna petición al servicio ICF ni al modelo **incluye nombre, documento ni orientación sexual** del paciente, y ningún dato sale de la infraestructura propia.
- El médico puede aceptar, editar o rechazar cada código y la decisión queda guardada con el modelo que la sugirió.
- Si el servicio ICF o el modelo no responden, la pantalla muestra un aviso claro (o se entrega la sugerencia por similitud, marcada como tal) y el resto de la aplicación sigue funcionando.
- Latencia de la sugerencia dentro de un umbral aceptable para uso clínico. Medido: 24 a 46 s con Qwen en el i3 (no aceptable); `gemma4:e4b` tarda ~3,4 s con una GPU de 8 GB y ~15 s solo con CPU de 10 núcleos (07f); el umbral definitivo se fija con el médico.
- Queda documentado el **modelo mínimo viable** y la **máquina recomendada** para producción (calidad, latencia y memoria medidas en el PC de pruebas); no hay presupuesto aprobado, por lo que la compra es una decisión posterior (07h).
- La confiabilidad clínica del motor está medida con la revisión de un médico sobre el set de referencia y el umbral de uso queda definido con él (07g).
- Documentación de instalación y mantenimiento del servidor.

**Sub-historias (división de HU-07, Sprint 8 & 9):**

| ID | Alcance | Pts | Depende de |
|----|---------|-----|-----------|
| **HU-07a** | **Servidor local y catálogo:** directorio `icf-service/` con docker-compose (Ollama + PostgreSQL/pgvector), modelos Qwen (`qwen2.5:3b`) y de embeddings (`bge-m3`), tabla `icf_codes` y script de carga del catálogo **CIF-IA hasta el tercer nivel** (mínimo capítulos d1–d6, funciones corporales b y estructuras s de las causas del seed), tabla de mapeo HAB D1–D6 → capítulo CIF-IA → dominio oficial y tabla de candidatos por dominio transcrita del Anexo, túnel autenticado con token — ✅ **Completada 06-oct-2026** | 5 | — |
| **HU-07b** | **Motor de sugerencia y evaluación:** reglas de capítulo/calificador, salida de máx. 3 códigos por componente (b, s, d) con estructuras de 3 calificadores (naturaleza/localización en 8), actividades (d) desde la lista cerrada del Anexo ordenadas por calificador y similitud, funciones y estructuras (b, s) por búsqueda semántica entre códigos de 3 dígitos con selección del LLM, diagnóstico CIE y notas como contexto, validación contra el catálogo, respaldo por similitud, `POST /suggest`, modos calidad y rápido, set de referencia de 25 casos sintéticos y herramientas de evaluación (`evaluate`, `probe_retrieval`, `compare_modes`, `benchmark_llm`); evaluación de `qwen2.5:3b` en el servidor físico (ver informe de pruebas) — ✅ **Completada 06-oct-2026** (la validación médica del set pasa a 07g y la prueba de modelos abiertos a 07f) | 8 | 07a |
| **HU-07c** | **Backend en Render:** modelo y esquemas `IcfSuggestion` (incluye instantánea de diagnóstico CIE y notas), CRUD, `services/icf_client.py` (túnel, token, timeout, sin nombre/documento/orientación sexual), router `icf` con generar/consultar/decidir, rechazo de pacientes menores de 6 años, normalización de la causa de la deficiencia a la lista oficial (incluidos los datos semilla), variables de entorno por ambiente en `render.yaml`, respuesta 503 si el servicio ICF no responde (timeout de 90 s: con Qwen en el i3 una sugerencia llegó a tardar 55 s; el valor final se ajusta con el modelo elegido en 07f), pruebas pytest con cliente mockeado — ✅ **Completada 07-oct-2026**: endpoints, cliente, tabla y 38 pruebas nuevas; la lista oficial de causas del Anexo (21 opciones) y su normalización se incorporaron el 07-oct-2026 | 5 | 07b |
| **HU-07d** | **Frontend "Perfil Funcional ICF":** página `FunctionalProfile.tsx` con campos opcionales de diagnóstico CIE y notas, tabla de 3 códigos por componente con aceptar/editar/rechazar (incluye edición de los 3 calificadores de estructuras), Copiar/Descargar (jsPDF) con encabezado Resolución 1239 del 21 de julio de 2022 y leyenda de borrador de apoyo, lista oficial de causa de deficiencia en el formulario de pacientes (la lista oficial ya la expone el backend en `GET /icf/causes`; el formulario debe consumirla), ruta, menú lateral, breadcrumb, claves es/en, servicio de API, estados de carga/error/sin predicción/menor de 6 años — ✅ **Completada 07-oct-2026**: `FunctionalProfile.tsx`, servicio `icf.ts`, ruta `/functional-profile`, menú, edición de los tres calificadores de estructuras, copiar y descargar PDF, 21 causas oficiales en el formulario y 12 pruebas Vitest; queda fuera de la interfaz cambiar el código en sí (el backend ya lo permite) y la spec E2E pasa a 07e | 5 | contrato de 07c |
| **HU-07e** | **Pruebas y documentación:** pruebas Vitest de la pantalla, spec E2E con respuesta del servicio mockeada (`page.route`, porque el servicio local no existe en QA/CI), documentación de instalación/mantenimiento (incluye la instalación de Ollama y de los modelos, y la máquina recomendada), ejecución de las pruebas de `icf-service` en el pipeline de CI, actualización de reportes y página principal — ✅ **Completada 07-oct-2026**: ver «Cierre de HU-07e» | 2 | 07c, 07d |
| **HU-07f** | **Escalera de modelos abiertos locales (Gemma 4 / MedGemma) y modelo mínimo viable:** en un PC de pruebas propio (i5-13450HX, 32 GB de RAM, RTX 5050 de 8 GB) instalar Ollama, PostgreSQL con pgvector y el catálogo, y medir con las 21 pistas orientativas y los scripts existentes (`compare_modes`) la calidad, la latencia y la memoria de `qwen2.5:3b` (referencia), `medgemma:4b`, `gemma4:e2b`, `gemma4:e4b`, `gemma4:12b`, `gemma4:26b`, `medgemma:27b` y `gemma4:31b` frente a la similitud; ajustar el modelo configurable (`ICF_LLM_MODEL`) y, si hace falta, el diseño de candidatos (por ejemplo, la lista completa de las 154 categorías de nivel 2); decidir y documentar el modelo mínimo viable. Todo local con datos sintéticos: ningún dato sale del equipo — ✅ **Completada 07-oct-2026** con una escalera parcial (`qwen2.5:3b`, `medgemma:4b`, `gemma4:e2b`, `gemma4:e4b`): `gemma4:e4b` es el mínimo viable provisional. Los modelos de 12B a 31B no se descargaron ni midieron (en estructuras `e4b` ya alcanza el techo de cobertura de los candidatos); se miden solo si la validación clínica (07g) muestra que `e4b` no alcanza el umbral | 2 | 07b |
| **HU-07g** | **Validación clínica y umbral de confiabilidad:** hoja de revisión para el médico (casos, códigos sugeridos con título, calificador y justificación, y una columna correcto / parcial / incorrecto), cálculo de la confiabilidad clínica por componente (b, s, d) sobre los 25 casos del set de referencia, definición con el médico del umbral de uso, `expected` completado en `reference/cases.json` e informe de resultados. El tiempo de la revisora no cuenta como esfuerzo de desarrollo. **Revisora designada (07-oct-2026): Emilly Maria Celis, profesional en salud** | 3 | 07f |
| **HU-07h** | **Despliegue y operación en el PC de producción:** decisión del 07-oct-2026: la producción corre en el PC propio (Intel i5-13450HX, 32 GB de RAM, NVIDIA RTX 5050 de 8 GB), que cumple el mínimo medido en 07f (`gemma4:e4b`, ~3,4 s por sugerencia); **no se compra hardware**. Alcance: instalar y dejar como servicios Ollama, PostgreSQL con pgvector, el servicio ICF y el túnel autenticado en ese equipo; evitar la suspensión y definir la energía; procedimiento para reconstruir la base (no guarda datos de pacientes); arranque automático tras reiniciar; medición de concurrencia con uno y pocos médicos a la vez; y manual de operación. Al ser un equipo personal, queda documentado el respaldo por similitud para cuando no responda | 3 | 07f |

**Avance de HU-07a (06-oct-2026):** servidor operativo (Ollama con `qwen2.5:3b`, Caddy con token y Tailscale Funnel; el servicio devuelve 401 sin token) y código en [`icf-service/`](icf-service/README.md): esquema PostgreSQL/pgvector, cargador del catálogo (1.593 códigos, carga repetible verificada en un contenedor pgvector), mapeo D1–D6 → capítulo → dominio oficial, escala de calificador, y diagnóstico `GET /icf/health` en el backend (solo admin, 8 pruebas). Variables `ICF_LLM_*` declaradas en `render.yaml` y cargadas en QA. **Servidor preparado (06-oct-2026):** `bge-m3` descargado, PostgreSQL con pgvector en contenedor local, catálogo cargado y **1.593 de 1.593 códigos con embedding**; la búsqueda de prueba «dificultad para caminar distancias largas» devuelve d4501, d4556, d4500, d4503 y d455 (todos del capítulo de movilidad, con d4501 primero). **Tabla de candidatos del Anexo (06-oct-2026):** transcrita de las tablas 9 (6–17 años) y 11 (WHODAS, 18 años o más): **32 códigos** repartidos en los 6 dominios oficiales, cada uno marcado como de ambos grupos de edad, solo 6–17 (d520, d740) o solo 18+ (d7702, d850, d570, d879, d940). Se excluyen los factores ambientales (e150, e155, e4) porque el perfil lleva solo b, s y d, y las tablas 7 y 8 (0–5 años) porque para menores de 6 años no se calculan niveles por dominio. Como el Anexo liga cada pregunta del instrumento con estos códigos, los candidatos del componente **d** son una lista cerrada y pequeña; la búsqueda con pgvector pesa sobre todo en **b** y **s**. **HU-07a completada (06-oct-2026):** `GET /icf/health` verificado en QA con un administrador: `configured: true`, `reachable: true`, `model_available: true` y 943 ms de latencia (Render QA → Tailscale Funnel → Caddy → Ollama). Servidor, catálogo con embeddings y tabla de candidatos listos para 07b. **Orden de promoción:** `develop` → `staging` → `master`; los cambios no deben ir directo de `develop` a `master`.

**Avance de HU-07b (06-oct-2026):** el motor está implementado en `icf-service/` (reglas, candidatos, llamada a `qwen2.5:3b` con JSON Schema donde los códigos candidatos son un `enum`, validación contra el catálogo y respaldo por reglas y similitud si el modelo falla), con `POST /suggest`, imagen Docker, 25 casos sintéticos de referencia (`reference/cases.json`) y el script `scripts/evaluate.py` (JSON válido, códigos fuera del catálogo, latencia p50/p95 y precisión). La configuración de Caddy con la ruta nueva se probó con Caddy real (el token se exige en todas las rutas). Para las actividades (d) los candidatos son la lista cerrada del Anexo, que HAB cubre solo en los capítulos d1–d6 (D2 usa el capítulo como respaldo).

**Medición de latencia y rediseño (06-oct-2026):** la primera versión, con el servidor real (i3 sin GPU), tardó **~55 s** por sugerencia (media 55,6 s, p95 60,5 s): leer el prompt de 760 tokens costó ~35 s (21 tok/s), escribir 167 tokens ~16 s (10 tok/s); el embedding 0,6 s y la búsqueda 4 ms. El JSON Schema no influye en la velocidad. Resultado válido en 4/4 casos y 0 códigos fuera del catálogo. Ajuste: las actividades (d) dejan de pasar por el modelo (se ordenan por calificador y similitud con el embedding ya calculado), el modelo solo elige funciones (b) y estructuras (s) entre 6 candidatos y devuelve solo códigos, y la parte fija del prompt va primero para que Ollama la reutilice. Con `ICF_USE_LLM=false` el servicio responde sin el modelo de generación. **Medido tras el ajuste:** media 22,9 s, p95 25 s (prompt de 348 tokens leído en ~14,5 s y 65 tokens escritos en ~6 s), con JSON válido en 4/4 casos y 0 códigos fuera del catálogo.

**Calidad de la búsqueda de funciones y estructuras (06-oct-2026):** la revisión de las salidas mostró candidatos pobres (para parálisis cerebral salían códigos de dolor en lugar de fuerza o tono muscular), porque el modelo solo puede elegir lo que la búsqueda le ofrece. Se midió la cobertura de 21 casos con pistas orientativas (códigos esperables por la lógica de la CIF, **no validados por un médico**; sirven para comparar variantes, no como precisión clínica). Resultados de funciones/estructuras: búsqueda inicial 4 % / 10 % con 6 candidatos; solo texto clínico (diagnóstico sin código CIE + notas) 11 % / 43 %; **solo códigos de 3 dígitos 23 % / 71 % con 6 candidatos y 40 % / 86 % con 12**; enriquecer el texto con los títulos de los hijos no mejoró; pedirle al modelo que describa el diagnóstico empeoró (inventaba estructuras). Se corrigió además un defecto: filtrar por categoría después de buscar dejaba vacío el caso solo psicosocial (esquizofrenia). Decisión: buscar entre códigos de 3 dígitos (sin los terminados en 8 y 9, «otros/no especificados») y dos modos configurables con `ICF_MODE`: **calidad** (predeterminado; 12 candidatos y justificación corta del modelo, ~40 s esperados) y **rápido** (6 candidatos y solo códigos, ~20 s). El perfil llega con un nivel menos de detalle en b y s (por ejemplo `b730`); el médico puede afinarlo. El backend de Render debe esperar 90 s mientras se use un modelo con latencia de decenas de segundos (medido después: el modo calidad con Qwen llegó a 55 s). 68 pruebas pasan, incluida una contra PostgreSQL con pgvector real.

**Resultados de las pruebas con Qwen en el servidor físico y decisión (06-oct-2026):** el modo calidad (12 candidatos y justificación del modelo) tardó 39 s de media (p95 55 s). Los tres modos se compararon con las pistas orientativas de 21 casos (no validadas por un médico; sirven para comparar modos, no como precisión clínica): **similitud sola** 29 % de precisión y 25 % de cobertura en funciones, 25 % y 67 % en estructuras, 0,6 s; **rápido** (Qwen, 6 candidatos) 23 % / 19 % y 24 % / 57 %, 24 s; **calidad** (Qwen, 12 candidatos) 20 % / 15 % y 24 % / 48 %, 46 s. El modelo local empeora la selección y cuesta de 40 a 80 veces más tiempo; las diferencias son pequeñas (21 casos, 73 pistas) pero consistentes. **Decisión (revisada el 06-oct-2026):** se evaluó pasar a un modelo externo (Claude Sonnet 5.5) y se descartó por privacidad y por no querer depender de APIs. Se prueban **modelos abiertos de Google (Gemma 4 y MedGemma) en un PC de pruebas** para hallar el modelo mínimo viable (HU-07f) y se dimensiona la máquina de producción (HU-07h); la similitud queda como respaldo. Informe completo: [`docs/reports/PRUEBAS_HU07_SERVIDOR_FISICO.md`](docs/reports/PRUEBAS_HU07_SERVIDOR_FISICO.md). **HU-07b se da por completada** con el motor y las herramientas de evaluación; la validación médica pasa a 07g.

**Resultados de HU-07f, modelos abiertos en el PC de pruebas (07-oct-2026):** en un PC con Intel i5-13450HX, 32 GB de RAM y una RTX 5050 de 8 GB se instaló Ollama, se levantó PostgreSQL con pgvector local, se cargó el catálogo con sus 1.593 embeddings y se repitió la comparación de modos con los mismos 21 casos. Al medir Gemma 4 se encontraron y corrigieron **dos defectos del motor**: Gemma 4 devuelve el JSON dentro de un bloque de código y razona antes de responder (se agregaron el análisis de bloques de código y la variable `ICF_LLM_THINK=false`; la primera corrida era inválida porque todo caía a similitud sin que se notara). Resultados en modo calidad contra las pistas orientativas (no validadas por un médico): similitud sola 29 % de precisión en funciones y 67 % de cobertura en estructuras; `qwen2.5:3b` 19 % / 67 % (peor); `medgemma:4b` 30 % / 76 %; `gemma4:e2b` 32 % / 76 %; **`gemma4:e4b` 43 % / 86 %** en 3,4 s de media. `gemma4:e4b` ocupa ~4,6 GB de VRAM y tarda ~15 s solo con CPU de 10 núcleos. **Mínimo viable provisional: `gemma4:e4b`**; máquina mínima con GPU de 8 GB, 16 GB de RAM y 6 núcleos, o solo CPU de 8 núcleos o más con 16 GB de RAM; el servidor i3 de 12 GB no alcanza (estimación). Los modelos de 12B a 31B no se midieron. Pendientes: licencias de Gemma y validación clínica. Informe completo: [`docs/reports/PRUEBAS_HU07F_MODELOS_ABIERTOS.md`](docs/reports/PRUEBAS_HU07F_MODELOS_ABIERTOS.md).

**Avance de HU-07c (07-oct-2026), backend:** nueva tabla `icf_suggestions` (un código por fila, agrupados por `batch_id`; regenerar crea un lote nuevo y conserva los anteriores), cliente `services/icf_client.py` hacia `POST /suggest` del servicio ICF (token Bearer, tiempo de espera propio `ICF_SUGGEST_TIMEOUT_S` de 90 s por defecto, errores genéricos que no revelan la URL ni el token) y tres endpoints: `POST /patients/{id}/icf-suggestions` (genera; acepta `diag_cie` y `clinical_notes` opcionales y rechaza cualquier otro campo), `GET /patients/{id}/icf-suggestions` (último lote) y `PATCH /icf/suggestions/{id}` (aceptar, editar o rechazar; al editar se pueden ajustar los calificadores o cambiar el código con su título y queda guardado el código original). Reglas: menores de 6 años → 422 sin llamar al servicio; servicio caído, sin configurar o con token rechazado → 503; el médico solo accede a sus pacientes y el admin a todos. La petición al servicio se arma campo por campo (lista blanca): edad, género, causa, categorías, niveles D1–D6, descripción de la predicción y los campos clínicos opcionales; una prueba verifica que nunca viajan el nombre, el documento ni la orientación sexual. `render.yaml` pasa `ICF_LLM_MODEL` a `gemma4:e4b`. **Pruebas:** 38 nuevas (105 en el backend con las causas oficiales, cobertura 89 %). **Causa de la deficiencia (07-oct-2026):** con el Anexo técnico en mano se agregó `app/causes.py` con las 21 opciones oficiales en 3 grupos (4 de nacimiento, 16 adquiridas y «no se identifica causa»), `GET /icf/causes` para el formulario y `normalize_cause`, que ajusta a la lista oficial los valores no oficiales con correspondencia clara (por ejemplo «Accidente laboral» → «Accidente de trabajo» o «Enfermedad degenerativa» → «Enfermedad general») y deja sin tocar los ambiguos («Enfermedad congénita», «Parálisis cerebral», «Trauma craneoencefálico»). Se aplica solo a lo que viaja al servicio ICF; los datos de los pacientes no se modifican. «Enfermedad laboral» y «Accidente de trabajo» exigen dictamen de origen de pérdida de capacidad laboral, que verifica el equipo clínico. Pruebas: 105 en el backend (cobertura 89 %). 

**Avance de HU-07d (07-oct-2026), frontend:** nueva página «Perfil Funcional ICF» (`/functional-profile`, para médicos): selección de paciente con resumen de datos y niveles D1–D6, campos opcionales de diagnóstico CIE y notas con la advertencia de no incluir datos identificables, aviso para menores de 6 años (sin llamar al servicio), estado de carga con aviso de espera, aviso claro si el servicio no responde y tres tablas (funciones, estructuras y actividades) con código, título del catálogo, calificador, justificación, origen (modelo, similitud o reglas) y estado. Acciones por fila: aceptar, editar y rechazar (en estructuras se editan magnitud, naturaleza y localización). Copiar y descargar PDF con el encabezado «Resolución 1239 del 21 de julio de 2022» y la leyenda de borrador de apoyo; los rechazados se omiten y el PDF incluye el nombre del paciente. El formulario de pacientes ofrece las 21 causas oficiales por grupo y conserva un valor anterior no oficial hasta que se edite. **Pruebas:** 28 de frontend (12 nuevas), lint sin errores y build correcto. **Datos semilla de QA:** las causas pasaron a la lista oficial; las tres ambiguas se asignaron así: «Enfermedad congénita» → Alteración genética o hereditaria, «Parálisis cerebral» → No se identifica causa y «Trauma craneoencefálico» → Otra (propuesta aprobada, no equivalencia del Anexo). **Pendiente en 07e:** spec E2E y documentación.

**Ajustes de uso tras las pruebas en DEV (07-oct-2026), dentro de HU-07d:** la pantalla «Perfil Funcional ICF» ahora trae enlaces a la CIE-10 (navegador de la OMS y CIE-10 en español de la OPS, en pestaña nueva), siete códigos CIE frecuentes para rellenar el diagnóstico y un panel «Ejemplos de notas clínicas» con seis casos sintéticos, consejos de redacción y el botón «Usar este ejemplo». La Guía Predictiva quedó en dos secciones (pestañas): «Niveles de barrera» y «Perfil Funcional ICF» (pasos de uso, origen de cada dato, escala del calificador, límites y privacidad; se abre directo con `?section=icf`). La Ayuda tiene una tarjeta con el avance del Perfil Funcional ICF (hecho y pendiente). Contenido bilingüe en `frontend/src/lib/icfGuideContent.ts`. Frontend: 38 pruebas pasan, tsc y build sin errores.

**Avance de HU-07h (07-oct-2026), despliegue en el PC de producción:** el servicio quedó operativo en el PC propio con `icf-service/deploy/windows/` (Docker Compose con la base pgvector, el servicio ICF y Caddy; Ollama nativo con la GPU). Caddy exige el token en todas las rutas y solo deja pasar `/suggest`, `/health` y `/api/tags`; el servicio ICF no publica puertos. Los secretos viven en `%USERPROFILE%\.hab-icf\.env`, fuera del repositorio y de OneDrive, y la clave de la base se cambió por una aleatoria. Tailscale Funnel publica el puerto de Caddy; verificado por la URL pública: sin token 401, token falso 401, token correcto 200, y `/api/generate` de Ollama bloqueado (404). Con el modelo en memoria una sugerencia tarda ~2,6 s; el primer pedido tras 30 min sin uso, ~18 s; con 3 médicos a la vez 2,7 a 7,2 s y con 5, 2,7 a 11,6 s. Energía: suspensión e hibernación con corriente alterna en «nunca». Hallazgo: este PC no guarda datos de pacientes (la base solo tiene el catálogo y los embeddings, que se reconstruyen), así que no hace falta copia de seguridad de datos clínicos. **Cierre de HU-07h (07-oct-2026):** el responsable configuró las variables en Render (`ICF_LLM_URL`, `ICF_LLM_TOKEN`, `ICF_LLM_MODEL=gemma4:e4b`), hizo la prueba de extremo a extremo en QA, comprobó la acción de la tapa del portátil y probó un reinicio del equipo. **HU-07h queda completada (3 pts).**

**Cierre de HU-07e (07-oct-2026), pruebas y documentación:** `frontend/e2e/functional-profile.spec.ts` tiene 5 casos de Playwright (generar con diagnóstico y notas, enlaces de la CIE y ejemplos, aceptar y rechazar, falla 503 del servicio y la guía); el login es real y la lista de pacientes y los endpoints ICF se simulan con `page.route`, porque el servicio ICF corre en un PC propio y los pacientes de QA son compartidos. Se verificó 5/5 contra el frontend DEV en un contenedor de Playwright 1.63 (el primer intento falló por asumir el idioma de la interfaz y se corrigió). Las pruebas de `icf-service` (62 pasan y 8 se omiten porque necesitan el catálogo local, que tiene derechos de la OMS) corren ahora en el CI de los tres ambientes con el job `icf-service-test`, del que dependen los despliegues y la compuerta de QA. Se escribió el manual de operación (`docs/MANUAL_OPERACION_ICF.md`: requisitos de la máquina, Ollama y modelos, variables, operación diaria, fallas, seguridad) y se actualizaron `TEST_CASES.md` (suites 8 a 11), `TESTING_REPORT.md`, `PROJECT_STATUS_M3.md`, `INSIGHTS_REPORT5.md` (segunda adenda) y la presentación. Cifras: backend 105, frontend 38, servicio ICF 70, E2E 12. **HU-07e queda completada (2 pts).** **Pendiente de HU-07:** solo 07g (validación clínica con Emilly Maria Celis, 3 pts).

**Riesgos y supuestos de HU-07:**
- Los niveles de HAB son por capítulo y la CIF califica por categoría; el calificador de cada categoría se toma del capítulo (aproximación). Por eso el médico puede editarlo.
- Funciones (b) y estructuras (s) se identifican oficialmente desde la historia clínica; sin diagnóstico CIE ni notas, las sugerencias de b y s serán genéricas.
- El set de referencia requiere validación médica; sin ella no se puede medir la calidad del motor.
- Un paciente sin predicción puede generar sugerencias igual (se omite el perfil de barreras del prompt).
- Si el servicio ICF, el túnel o el modelo local caen, solo esta función queda afectada (respaldo por similitud).
- **Privacidad y marco legal:** con modelo local los datos no salen de la infraestructura propia (Ley 1581 de 2012); el riesgo restante es la copia de datos en el PC de pruebas, que solo usa casos sintéticos. Pendiente: verificar las licencias de uso de Gemma y MedGemma antes de producción.
- **Calidad del modelo local:** un modelo pequeño (Qwen 3B) no superó a la similitud; `gemma4:e4b` sí, pero con pistas no validadas por un médico. Mitigación: similitud como respaldo y validación clínica (07g).
- **Producción en un PC propio:** el equipo puede suspenderse, apagarse o quedar sin internet, y no tiene redundancia. Mitigación: respaldo por similitud en el backend, arranque automático, energía sin suspensión y procedimiento para reconstruir la base (07h, completada).
- **Confiabilidad clínica aún no medida:** las cifras actuales usan pistas orientativas no validadas por un médico; solo la revisión clínica (07g) mide la confiabilidad real.
- **Equipo de pruebas:** el PC de pruebas se usa solo con datos sintéticos y el catálogo (con derechos de la OMS) no se publica.

**DoD:** Servidor local operativo con RAG sobre el catálogo CIF, sugerencias funcionando de punta a punta (frontend, backend, servicio local) con aceptar/editar/rechazar, set de referencia validado por un médico, pruebas en verde en CI y documentación de instalación y mantenimiento.  
**Estimación:** **33 puntos** (07a 5 + 07b 8 + 07c 5 + 07d 5 + 07e 2 + 07f 2 + 07g 3 + 07h 3). Reestimada desde 25 puntos el 06-oct-2026 por los hallazgos de las pruebas en el servidor físico (+8: escalera de modelos abiertos 2, validación clínica 3 y dimensionamiento de la máquina 3): el Momento 3 pasa de 51 a **59 pts** y el total del proyecto de 138 a **146 pts** (117 completados al 07-oct-2026, 80,1 %). Historial: la estimación de 25 puntos se reestimó desde 21 puntos el 05-oct-2026 tras revisar el Anexo Técnico de la Resolución 1239 del 21 de julio de 2022 (+4: estructuras s, 3 códigos por componente, mapeo de dominios y campos clínicos). Con esto el Momento 3 pasa de 47 a **51 pts** (HU-07 25 + HU-08 13 + HU-09 8 + HU-10 5) y el total del proyecto de 134 a **138 pts** (87 completados, 63.0 %).
**Decisión de alcance confirmada (23-sep-2026, refinada el 05-oct-2026):** se usará **Ollama** sobre un servidor físico ya disponible (no hay presupuesto aprobado para hardware nuevo), con un modelo open-weight gratuito (inicialmente **Qwen `qwen2.5:3b`**; el 06-oct-2026 se decide probar Gemma 4 y MedGemma en un PC de pruebas) usando **RAG sobre el estándar CIF-Colombia, sin fine-tuning**. Esta decisión reduce el riesgo de presupuesto de hardware señalado en `docs/reports/INSIGHTS_REPORT3.md` §11 (punto 5) y desacopla el cómputo del LLM del Web Service de Render (ver nota de DEUDA-01 arriba). **Actualización 06-oct-2026:** Qwen 3B no sirvió como selector en el i3 (peor que la similitud y 24–46 s). Se descarta usar APIs externas (privacidad). Se prueban Gemma 4 y MedGemma en un PC de pruebas para hallar el modelo mínimo viable y dimensionar la máquina de producción (sin presupuesto aprobado); mientras tanto el servidor actual sirve catálogo, embeddings, búsqueda y similitud. **Decisión 07-oct-2026:** la producción corre en el PC propio (Intel i5-13450HX, 32 GB de RAM, NVIDIA RTX 5050 de 8 GB), que cumple el mínimo medido en 07f; no se compra hardware.

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
- Documentación técnica y manuales de usuario (incluye el manual de operación del servicio ICF: servidor propio, túnel, instalación de Ollama y de los modelos, y requisitos de la máquina).
- Reportes finales.

**DoD:** Aplicación en producción, documentación entregada.  
**Estimación:** 5 puntos.
