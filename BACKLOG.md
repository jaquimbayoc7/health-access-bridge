# Backlog Maestro: Health Access Bridge (HAB)

**Proyecto:** Health Access Bridge  
**Metodología:** SCRUM  
**Duración Total:** 27 Semanas  
**Última actualización:** Septiembre 2026 · Momento 1 y Momento 2 completados (HU-06 cerrada)

---

## Tablero Kanban — Estado General

| ✅ Done | 🟡 En Progreso | 📋 Backlog |
|---------|---------------|-----------|
| EPICA-01 Estructuración y Diseño | — | EPICA-02 Funcionalidades Core |
| HU-01 Autenticación y Roles (8 pts) | — | EPICA-03 IA Generativa y Cierre |
| HU-02 Registro y Precarga de Pacientes (13 pts) | — | EPICA-03 IA Generativa y Cierre |
| HU-03 Integración Frontend-Backend y Despliegue Cloud (5 pts) | — | HU-07 Servidor Local con LLM Ajustado para Códigos ICF (21 pts) |
| HU-04 Modelo Predictivo ML (21 pts) *(adelantada en M1)* | — | HU-08 Dashboard de Análisis y Exportación (13 pts) |
| [#14 HU-11](https://github.com/jaquimbayoc7/health-access-bridge/issues/14) Pruebas Smoke en Producción (3 pts) | — | HU-09 Pruebas Completas y Feedback (8 pts) |
| [#15 HU-12](https://github.com/jaquimbayoc7/health-access-bridge/issues/15) Pruebas de Integración Backend (5 pts) | — | HU-10 Despliegue Final y Manuales (5 pts) |
| [#16 HU-13](https://github.com/jaquimbayoc7/health-access-bridge/issues/16) Pruebas de Diseño y UI Frontend (8 pts) | — | — |
| HU-05 Mejoras de Usabilidad (HCI) (13 pts) | — | — |
| HU-05b Ayuda contextual traducida (3 pts) | — | — |
| [#6 HU-06](https://github.com/jaquimbayoc7/health-access-bridge/issues/6) Pruebas de Integración y Rendimiento (8 pts) | — | — |

**Puntos completados: 87 pts · Puntos pendientes: 47 pts · Total: 134 pts**  
**Avance general: 65% · Momento 1 100% completado (Sprint 3.5 incluido) · Momento 2 100% completado**

---

## MOMENTO 1: TRABAJO INTEGRADOR I (Semanas 1-9) - Avance 100% ✅

### Épica 1: Estructuración y Diseño (Semanas 1-3) ✅ Done
*Artefactos completados:*
- ✅ **Mockups de Diseño** - 8 pantallas en `frontend/design/images/`: Login, Dashboard, Pacientes, Predicciones, Admin Panel, Análisis, Guía Predictiva, Perfil Funcional ICF
- ✅ **Arquitectura C4** - 6 diagramas HTML en `docs/`: L1 Context, L2 Container, L3 Component, L4 Code (Backend), L4 Code (Frontend), Deployment
- ✅ **Reporte de Insights GitHub** - `docs/INSIGHTS_REPORT.md`
- ✅ **Reporte de Testing** - `docs/TESTING_REPORT.md`
- 📋 BPM (pendiente)
- 📋 Release Plan (pendiente)

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
- ✅ Espera 90 segundos para que Render termine el deploy antes de ejecutar.

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
- ✅ `backend/tests/load/k6_load_test.js` — script de carga con k6: rampa 0→200 usuarios concurrentes, thresholds `p95<200ms` y `error rate<1%`.
- ✅ 3 bugs críticos encontrados y corregidos: crash 500 en `/users/login` con body inválido (`FormData` no serializable), paciente con soft-delete seguía accesible por ID (`crud.get_patient` no filtraba `is_active`), rutas incorrectas en smoke tests de `ci-qa.yml` (`/api/v1/...` inexistente) + `PLAYWRIGHT_BASE_URL` mal configurado.
- ✅ Reporte documentado en `docs/test-report.md`.

**Criterios de Aceptación:**
- ✅ Pruebas automatizadas de integración pasan al 100% (44/44 backend).
- 🟡 API responde en menos de 200ms bajo carga simulada — script de k6 listo; ejecución real contra un ambiente desplegado queda pendiente (no se corrió para no generar carga no autorizada sobre Render).

**⚠️ PENDIENTE (recordatorio explícito):**
1. Ejecutar la prueba de carga real con **200 usuarios concurrentes** contra un ambiente desplegado (QA), usando `backend/tests/load/k6_load_test.js`.
2. Con esos resultados, generar un nuevo **Insight Report 3** (`docs/reports/INSIGHTS_REPORT3.md`) con el estado actual del proyecto.
3. Generar el **Estado del Proyecto para Momento Integrador II** posterior a esa prueba de carga.

**DoD:** Reporte de pruebas (`docs/test-report.md`), corrección de bugs críticos.  
**Estimación:** 8 puntos.  
**Estado:** ✅ Completado — ver detalle completo en `docs/test-report.md`.

---

## MOMENTO 3: TRABAJO INTEGRADOR III (Semanas 19-27) - Avance 0% 🔴

### Sprint 8 & 9: Servidor Local y Codificación ICF (Semanas 19-22)

#### HU-07: Alistamiento de Servidor Local Físico con LLM Ajustado para Sugerencia de Códigos ICF (Colombia)
- **Como** Médico / Administrador de TI en sede clínica
- **Deseo** contar con un servidor físico local, con un modelo LLM instalado y ajustado (fine-tuned) para esta misión, que reciba los datos capturados del paciente y sugiera los códigos de la Clasificación Internacional del Funcionamiento (CIF/ICF) bajo el estándar adoptado en Colombia
- **Para** operar de forma confiable en sedes con conectividad limitada, mantener el procesamiento de datos clínicos sensibles dentro de la infraestructura local, y obtener sugerencias de codificación con razonamiento en lenguaje natural en vez de un simple mapeo de reglas.

**Detalles:**
- **Infraestructura:** Aprovisionar y configurar el servidor físico (SO, GPU/CPU con capacidad de inferencia, dependencias, contenedores) en la sede clínica.
- **Modelo LLM local:** Instalar un LLM open-weight ejecutable on-premise (ej. vía Ollama / vLLM) y ajustarlo (fine-tuning o RAG con el manual oficial CIF-Colombia) para la tarea específica de sugerir códigos/calificadores ICF a partir de los niveles D1–D6 y la nota clínica del paciente.
- **Backend local:** Servicio que recibe los datos ICF capturados en HAB, arma el prompt/contexto para el LLM local y devuelve el código/calificador sugerido con su justificación.
- **Sincronización:** Definir estrategia de sincronización o modo standalone entre el servidor local y el backend en la nube (Render); el LLM y los datos sensibles nunca salen de la red local.
- **Referencia:** Cargar la tabla oficial de codificación ICF/CIF como catálogo/contexto local para el modelo (RAG) y como respaldo de reglas.

**Criterios de Aceptación:**
- El servidor local queda operativo y accesible en la red interna de la sede, con el LLM cargado y sirviendo inferencias.
- Dado un registro de paciente con niveles D1–D6, el LLM local sugiere el código ICF/CIF correspondiente según el estándar colombiano, con una justificación breve.
- Funciona sin depender de conexión a internet (modelo e inferencia 100% on-premise).
- Tiempo de respuesta de la inferencia dentro de un umbral aceptable para uso clínico (a definir en pruebas).
- Documentación de instalación, ajuste del modelo y mantenimiento del servidor.

**Tareas:**
- Aprovisionar y configurar el servidor físico (hardware, SO, dependencias, runtime de inferencia).
- Seleccionar y desplegar el LLM local (ej. Ollama/vLLM con un modelo open-weight adecuado al hardware disponible).
- Ajustar el modelo para la tarea (fine-tuning y/o RAG) usando el estándar oficial CIF-Colombia como base de conocimiento.
- Implementar el servicio/endpoint que arma el prompt con los niveles D1–D6 y consulta al LLM local para sugerir el código ICF/CIF.
- Cargar el catálogo oficial de códigos ICF/CIF-Colombia como contexto/referencia del modelo.
- Definir y probar la estrategia de sincronización con el backend en la nube.
- Pruebas de precisión de las sugerencias, disponibilidad y latencia en red local.
- Documentar instalación, ajuste del modelo y mantenimiento del servidor.

**DoD:** Servidor local operativo con el LLM ajustado, sugerencia de códigos ICF/CIF funcionando con datos reales y justificación del modelo, documentación de instalación y ajuste.  
**Estimación:** 21 puntos.

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
