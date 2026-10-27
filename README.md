# Health Access Bridge (HAB)

Plataforma web para la gestión clínica de pacientes con discapacidad, el análisis predictivo de perfiles de barreras de acceso a la salud en zonas rurales y el **perfil funcional ICF** asistido por una IA que corre en infraestructura propia.

**Presentación del proyecto (estado, calidad, sprints y métricas):** [`docs/presentation/`](./docs/presentation/index.html)

---

## Estado del Proyecto

> **Corte: 27 de octubre de 2026** · **141 de 146 puntos (96,6 %)** · Momentos 1 y 2 al 100 % · Momento 3: 54 de 59 pts (HU-07, HU-08 y HU-09 completas; queda HU-10)

| Capa | Estado | Detalle |
|------|--------|----------|
| **Backend** | ✅ Desplegado en los 3 ambientes | Autenticación y RBAC, CRUD de pacientes, predicción ML, sugerencias ICF y dashboard de análisis (`/analytics`) |
| **Frontend** | ✅ Desplegado en los 3 ambientes | Login, Dashboard, Pacientes, Predicciones, **Perfil Funcional ICF**, **Dashboard de análisis** (exporta a Excel y PDF), Guía, Ayuda, Admin |
| **Servicio ICF** | ✅ En producción en un PC propio | PostgreSQL/pgvector + Ollama (`gemma4:e4b`, ~2 s por sugerencia) detrás de un túnel con token; ningún dato clínico sale a terceros |
| **CI/CD** | ✅ Configurado | GitHub Actions → Render (auto-deploy y aprobación manual en producción) |
| **Base de datos** | ✅ PostgreSQL en Render | 3 instancias independientes (dev/qa/prod) con seed de datos |
| **Calidad** | ✅ 309 pruebas automáticas | Backend 123 (cobertura 90,7 %) · frontend 61 · servicio ICF 101 · E2E 17 · smoke 7 |

---

## Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| **Backend** | Python 3.11 · FastAPI · SQLAlchemy · PostgreSQL |
| **Frontend** | React 18 · TypeScript · Vite · TailwindCSS · shadcn/ui · Recharts · React Query · jsPDF y xlsx (exportaciones) |
| **Autenticación** | JWT con claims de rol (Admin, Médico) · Bcrypt |
| **IA predictiva** | HybridModelDisability (K-Means + Gradient Boosting, embebido en el backend) |
| **Servicio ICF (HU-07)** | Servicio en un PC propio (PostgreSQL/pgvector + embeddings `bge-m3` + modelo local `gemma4:e4b` con Ollama) que, mediante RAG sobre el catálogo CIF-IA y sin fine-tuning, sugiere códigos CIF según el Anexo Técnico de la Resolución 1239 del 21 de julio de 2022. El médico acepta, edita o rechaza cada código; es un **borrador de apoyo**, no un certificado. Sin APIs externas por privacidad. Validado con una profesional de salud en tres rondas (ver [reporte final](./docs/presentation/reporte-afinamiento-icf.html)) |
| **Dashboard de análisis (HU-08)** | Endpoints `/analytics/*` con conteos y promedios agregados (sin datos identificables); gráficos interactivos con Recharts y exportación a Excel (5 hojas) y PDF |
| **Despliegue** | Render · Web Service · PostgreSQL managed |
| **CI/CD** | GitHub Actions · 3 workflows (dev/qa/prod) |

---

## Arquitectura — C4 Model

Documentación de arquitectura en cuatro niveles siguiendo el [C4 Model](https://c4model.com) de Simon Brown.

| Nivel | Diagrama | Descripción |
|-------|----------|-------------|
| **L1 — Context** | [system-context-diagram.html](./docs/diagrams/system-context-diagram.html) | Actores (Admin, Médico), sistema HAB y sistemas externos (GitHub Actions, Render, servidor de IA propio) |
| **L2 — Container** | [container-diagram.html](./docs/diagrams/container-diagram.html) | Frontend SPA, Backend API, PostgreSQL, servicio ICF en el PC propio, CI/CD y Render |
| **L3 — Component** | [component-diagram.html](./docs/diagrams/component-diagram.html) | Componentes del backend: routers (Users, Admin, Patients, **ICF**, **Analytics**), Auth, RBAC, ML, ICF Client, CRUD y sesión |
| **L4 — Code (Backend)** | [code-diagram.html](./docs/diagrams/code-diagram.html) | Modelos SQLAlchemy y esquemas Pydantic v2 |
| **L4 — Code (Frontend)** | [code-diagram-frontend.html](./docs/diagrams/code-diagram-frontend.html) | Servicios TypeScript, contextos y páginas React |
| **Deployment** | [deployment-diagram.html](./docs/diagrams/deployment-diagram.html) | DEV / QA / PROD en Render, el PC propio del servicio ICF y GitHub Actions |

> Los diagramas son HTML interactivos. Ábrelos directamente en el navegador desde la carpeta `docs/diagrams/`.

---

## Ambientes y URLs

| Ambiente | Rama | Backend | Frontend | API Docs |
|----------|------|---------|----------|----------|
| **Development** | `develop` | https://hab-backend-dev.onrender.com | https://hab-frontend-dev.onrender.com | [/docs](https://hab-backend-dev.onrender.com/docs) |
| **QA / Staging** | `staging` | https://hab-backend-qa.onrender.com | https://hab-frontend-qa.onrender.com | [/docs](https://hab-backend-qa.onrender.com/docs) |
| **Production** | `master` | https://hab-backend-szj1.onrender.com | https://hab-frontend.onrender.com | [/docs](https://hab-backend-szj1.onrender.com/docs) |

La referencia completa de la API (ReDoc) está en [`docs/api/redoc-api.html`](./docs/api/redoc-api.html).

### Credenciales de prueba (seed — disponibles en los 3 ambientes)

| Rol | Email | Contraseña |
|-----|-------|------------|
| **Admin** | `administrador@salud.co` | `adminpassword` |
| **Médico** | `medico1@salud.co` | `medico123` |
| **Médico** | `medico2@salud.co` | `medico123` |

> `medico1@salud.co` tiene 5 pacientes de prueba. `medico2@salud.co` tiene 5 pacientes. `administrador@salud.co` puede ver los 10 (todos).

---

## Endpoints disponibles

### Autenticación y Usuarios
| Método | Endpoint | Acceso | Descripción |
|--------|----------|--------|-------------|
| `POST` | `/users/login` | Público | Login → retorna JWT |
| `GET` | `/users/me` | Autenticado | Perfil del usuario actual |
| `GET` | `/admin/users` | Admin | Lista todos los usuarios |
| `POST` | `/admin/users/register` | Admin | Crear nuevo usuario (médico/admin) |
| `PATCH` | `/admin/users/{id}/status` | Admin | Activar / desactivar usuario |

### Pacientes
| Método | Endpoint | Acceso | Descripción |
|--------|----------|--------|-------------|
| `POST` | `/patients/` | Médico | Crear paciente |
| `GET` | `/patients/?search=&skip=&limit=` | Admin (todos) · Médico (propios) | Listar con búsqueda y paginación |
| `GET` | `/patients/{id}` | Admin (cualquiera) · Médico (dueño) | Detalle de paciente |
| `PUT` | `/patients/{id}` | Admin (cualquiera) · Médico (dueño) | Actualizar historia clínica |
| `DELETE` | `/patients/{id}` | Admin (cualquiera) · Médico (dueño) | Soft delete |
| `POST` | `/patients/{id}/predict` | Admin · Médico | Predicción del perfil de barreras |

### Perfil funcional ICF (HU-07)
| Método | Endpoint | Acceso | Descripción |
|--------|----------|--------|-------------|
| `POST` | `/patients/{id}/icf-suggestions` | Admin · Médico (dueño) | Genera hasta 3 códigos CIF-IA por componente (no aplica a menores de 6 años) |
| `GET` | `/patients/{id}/icf-suggestions` | Admin · Médico (dueño) | Último lote con la decisión del médico |
| `PATCH` | `/icf/suggestions/{id}` | Admin · Médico (dueño) | Aceptar, editar o rechazar un código |
| `GET` | `/icf/causes` | Autenticado | Causas de la deficiencia del Anexo 1239 (21 opciones) |
| `GET` | `/icf/health` | Admin | Diagnóstico de la conexión con el servidor de IA |

### Dashboard de análisis (HU-08)
| Método | Endpoint | Acceso | Descripción |
|--------|----------|--------|-------------|
| `GET` | `/analytics/summary` | Admin (todos, con filtro por médico) · Médico (propios) | Conteos y promedios agregados, con filtros de género, edad, causa y perfil; incluye el bloque ICF. Sin datos identificables |
| `GET` | `/analytics/filters` | Autenticado | Valores disponibles para los filtros |

### Admin — Utilidades
| Método | Endpoint | Acceso | Descripción |
|--------|----------|--------|-------------|
| `POST` | `/admin/reset-seed` | Admin | DROP + recrear tabla patients y re-seedear |

### Sistema
| Método | Endpoint | Descripción |
|--------|----------|--------------|
| `GET` | `/health` | Health check (CI/CD) |
| `GET` | `/` | Bienvenida |

---

## GitHub Environments

| Ambiente | Protección | Secrets |
|----------|-----------|---------|
| `development` | Sin restricciones | `DATABASE_URL`, `SECRET_KEY`, `PYTHON_VERSION` |
| `qa` | Sin restricciones | `DATABASE_URL`, `SECRET_KEY`, `PYTHON_VERSION` |
| `production` | Aprobación manual requerida | `DATABASE_URL`, `SECRET_KEY`, `PYTHON_VERSION` |

[Ver environments en GitHub](https://github.com/jaquimbayoc7/health-access-bridge/settings/environments)

---

## Historias de Usuario

### Momento 1 — Trabajo Integrador I (Semanas 1-9) · [Milestone](https://github.com/jaquimbayoc7/health-access-bridge/milestone/1) · ✅ 63 pts

> Épica: [#11 EPICA-01 Estructuración y Diseño](https://github.com/jaquimbayoc7/health-access-bridge/issues/11)

| Issue | Título | Sprint | Pts | Backend | Frontend | Estado |
|-------|--------|--------|-----|---------|----------|--------|
| [#1](https://github.com/jaquimbayoc7/health-access-bridge/issues/1) | [HU-01] Autenticación y Roles (RBAC) | Sprint 1 (Sem. 4-5) | 8 | ✅ Completo | ✅ Completo | ✅ Done |
| [#2](https://github.com/jaquimbayoc7/health-access-bridge/issues/2) | [HU-02] Registro y Precarga de Pacientes | Sprint 2 (Sem. 6-7) | 13 | ✅ Completo | ✅ Completo | ✅ Done |
| [#3](https://github.com/jaquimbayoc7/health-access-bridge/issues/3) | [HU-03] Integración Frontend-Backend | Sprint 3 (Sem. 8-9) | 5 | ✅ Completo | ✅ Completo | ✅ Done |
| [#4](https://github.com/jaquimbayoc7/health-access-bridge/issues/4) | [HU-04] Integración Modelo Predictivo (HybridModelDisability) | Sprint 3 (adelantada del 4-5) | 21 | ✅ Completo | ✅ Completo | ✅ Done |
| [#14](https://github.com/jaquimbayoc7/health-access-bridge/issues/14) | [HU-11] Pruebas Smoke en Producción | Sprint 3.5 (Sem. 9) | 3 | ✅ CI/CD | — | ✅ Done |
| [#15](https://github.com/jaquimbayoc7/health-access-bridge/issues/15) | [HU-12] Pruebas de Integración Backend | Sprint 3.5 (Sem. 9) | 5 | ✅ pytest | — | ✅ Done |
| [#16](https://github.com/jaquimbayoc7/health-access-bridge/issues/16) | [HU-13] Pruebas de Diseño y UI Frontend | Sprint 3.5 (Sem. 9) | 8 | — | ✅ Vitest | ✅ Done |

### Momento 2 — Trabajo Integrador II (Semanas 10-18) · [Milestone](https://github.com/jaquimbayoc7/health-access-bridge/milestone/2) · ✅ 24 pts

> Épica: [#12 EPICA-02 Funcionalidades Core](https://github.com/jaquimbayoc7/health-access-bridge/issues/12) (HU-04 se entregó antes, en el Momento 1)

| Issue | Título | Sprint | Pts | Estado |
|-------|--------|--------|-----|--------|
| [#5](https://github.com/jaquimbayoc7/health-access-bridge/issues/5) | [HU-05] Mejoras de Usabilidad (Investigación HCI) | Sprint 6-7 (Sem. 14-17) | 13 | ✅ Done |
| [#6](https://github.com/jaquimbayoc7/health-access-bridge/issues/6) | [HU-06] Pruebas de Integración y Rendimiento API | Sprint 7 (Sem. 16-17) | 8 | ✅ Done |
| — | [HU-05b] Ayuda contextual (Help + Tooltips ICF) traducida por idioma | Sprint 6-7 (Sem. 14-17) | 3 | ✅ Done |

### Momento 3 — Trabajo Integrador III (Semanas 19-27) · [Milestone](https://github.com/jaquimbayoc7/health-access-bridge/milestone/3) · 🟡 46 de 59 pts

> Épica: [#13 EPICA-03 IA Generativa, Dashboards y Cierre](https://github.com/jaquimbayoc7/health-access-bridge/issues/13)

| Issue | Título | Sprint | Pts | Estado |
|-------|--------|--------|-----|--------|
| [#7](https://github.com/jaquimbayoc7/health-access-bridge/issues/7) | [HU-07] Perfil Funcional ICF con RAG y LLM local para sugerencia de códigos CIF (Colombia) — 07a a 07h, con la validación clínica 07g ([#71](https://github.com/jaquimbayoc7/health-access-bridge/issues/71)) | Sprint 8-9 (Sem. 19-22) | 33 | ✅ Done |
| [#8](https://github.com/jaquimbayoc7/health-access-bridge/issues/8) | [HU-08] Dashboard de Análisis y Exportación | Sprint 8-9 (adelantada del 10-11) | 13 | ✅ Done |
| [#9](https://github.com/jaquimbayoc7/health-access-bridge/issues/9) | [HU-09] Pruebas Completas y Feedback de Usuarios | Sprint 11 (Sem. 25-26) | 8 | ✅ Completada |
| [#10](https://github.com/jaquimbayoc7/health-access-bridge/issues/10) | [HU-10] Despliegue Final y Generación de Manuales | Sprint 12 (Sem. 27) | 5 | 📋 Backlog |

🔗 [Ver todas las issues](https://github.com/jaquimbayoc7/health-access-bridge/issues) · [Ver SCRUM Board](https://github.com/users/jaquimbayoc7/projects/1)

---

## Épicas

| Issue | Épica | Momento | HUs | Pts | Estado |
|-------|-------|---------|-----|-----|--------|
| [#11](https://github.com/jaquimbayoc7/health-access-bridge/issues/11) | EPICA-01 Estructuración, Diseño e Implementación M1 | 1 · Sem. 1-9 | HU-01, 02, 03, 04, 11, 12, 13 | 63 | ✅ Done |
| [#12](https://github.com/jaquimbayoc7/health-access-bridge/issues/12) | EPICA-02 Funcionalidades Core y Capacidades Avanzadas | 2 · Sem. 10-18 | HU-05, 05b, 06 | 24 | ✅ Done |
| [#13](https://github.com/jaquimbayoc7/health-access-bridge/issues/13) | EPICA-03 IA Generativa, Dashboards y Cierre | 3 · Sem. 19-27 | HU-07 al 10 | 59 | 🟡 En progreso (46 de 59) |

---

## Calidad

| Capa | Pruebas | Herramienta |
|------|---------|-------------|
| Backend | 123 (cobertura 90,7 %; el CI exige 80 %) | pytest · TestClient · SQLite |
| Frontend | 61 | Vitest · Testing Library · jsdom |
| Servicio ICF | 101 (92 en CI; 9 necesitan el catálogo de la OMS y corren en el PC propio) | pytest |
| E2E | 17 | Playwright |
| Smoke | 7 (QA 4 · PROD 3) | GitHub Actions |

Detalle en [`docs/reports/TESTING_REPORT.md`](./docs/reports/TESTING_REPORT.md) y [`docs/reports/TEST_CASES.md`](./docs/reports/TEST_CASES.md). La validación clínica del perfil funcional ICF está en [`docs/reports/PROTOCOLO_VALIDACION_CLINICA_HU07G.md`](./docs/reports/PROTOCOLO_VALIDACION_CLINICA_HU07G.md).

---

## Setup local

```bash
# 1. Clonar el repositorio
git clone https://github.com/jaquimbayoc7/health-access-bridge.git
cd health-access-bridge

# 2. Configurar variables de entorno
cp .env.dev.example .env

# 3. Instalar dependencias backend
cd backend
pip install -r requirements.txt

# 4. Iniciar el servidor de desarrollo
uvicorn app.main:app --reload --port 8000

# 5. Frontend (otra terminal)
cd frontend && npm ci && npm run dev
```

> La app crea las tablas y ejecuta el seed automáticamente en el primer startup.
> Documentación interactiva disponible en: http://localhost:8000/docs
> Las sugerencias ICF necesitan el servicio ICF (`icf-service/`, ver su [manual de operación](./docs/MANUAL_OPERACION_ICF.md)); sin él, el resto de la aplicación funciona y la pantalla muestra un aviso.

---

## Estructura del proyecto

```
health-access-bridge/
├── backend/
│   ├── app/
│   │   ├── main.py          # Entrypoint FastAPI + startup + CORS
│   │   ├── models.py        # Modelos SQLAlchemy (User, Patient, IcfSuggestion)
│   │   ├── schemas.py       # Esquemas Pydantic
│   │   ├── crud.py          # Operaciones de base de datos
│   │   ├── auth.py          # JWT + Bcrypt
│   │   ├── dependencies.py  # Inyección de dependencias y RBAC
│   │   ├── database.py      # Configuración SQLAlchemy
│   │   ├── seed.py          # Seed de datos de prueba (idempotente)
│   │   ├── routers/         # users · patients · admin · icf · analytics
│   │   ├── services/        # icf_client (servicio de IA) · analytics (agregados del dashboard)
│   │   └── tests/           # 123 pruebas pytest
│   ├── requirements.txt · requirements-test.txt · build.sh · runtime.txt
├── frontend/
│   ├── src/
│   │   ├── pages/           # Login, Dashboard, Patients, Predictions, FunctionalProfile, Analytics, Admin…
│   │   ├── components/      # Layout, UI (shadcn), Dashboard widgets
│   │   ├── services/        # api.ts, patients.ts, icf.ts, analytics.ts
│   │   ├── lib/             # analyticsExport (Excel/PDF), analyticsLabels, icfReport…
│   │   ├── contexts/        # AuthContext (JWT), LanguageContext (ES/EN)
│   │   └── __tests__/       # 61 pruebas Vitest + Testing Library
│   ├── e2e/                 # 17 pruebas Playwright
│   └── package.json · vite.config.ts
├── icf-service/             # Servicio de IA local (RAG sobre CIF-IA, Ollama, pgvector) · 101 pruebas
├── docs/
│   ├── presentation/        # Página de presentación del proyecto y reporte del afinamiento ICF
│   ├── reports/             # Estado, pruebas, validación clínica, insights, release plan
│   ├── diagrams/            # C4 (6 diagramas) y diseño del RAG
│   └── api/                 # Referencia ReDoc de la API y documentación del frontend
├── render.yaml              # Blueprint Render (3 backends + 3 frontends + 3 DBs)
└── .github/workflows/       # ci-dev.yml · ci-qa.yml · ci-prod.yml (aprobación manual y smoke tests en producción)
```

---

## Documentación

- [Presentación del proyecto](./docs/presentation/index.html) (resumen, producto, proceso y sprints, calidad, IA y validación ICF, usuarios, documentos)
- [Backlog](./BACKLOG.md) · [Pendientes](./docs/PENDIENTES_PROXIMA_SESION.md)
- Estado: [Momento 1](./docs/reports/PROJECT_STATUS.md) · [Momento 2](./docs/reports/PROJECT_STATUS_M2.md) · [Momento 3](./docs/reports/PROJECT_STATUS_M3.md) · [Release Plan](./docs/reports/RELEASE_PLAN.md)
- Pruebas: [Casos de prueba](./docs/reports/TEST_CASES.md) · [Reporte de testing](./docs/reports/TESTING_REPORT.md) · [Reporte de HU-06](./docs/test-report.md)
- IA e ICF: [Protocolo de validación clínica](./docs/reports/PROTOCOLO_VALIDACION_CLINICA_HU07G.md) · [Reporte final del afinamiento](./docs/presentation/reporte-afinamiento-icf.html) · [Licencias](./docs/reports/LICENCIAS_COMPONENTES_ICF.md) · [Manual de operación](./docs/MANUAL_OPERACION_ICF.md)
- Reportes de insights: [R5 (con adendas hasta el cierre de HU-07g)](./docs/reports/INSIGHTS_REPORT5.md) y [R1 a R4](./docs/reports)
- [GitHub Project SCRUM Board](https://github.com/users/jaquimbayoc7/projects/1) · [Environments](https://github.com/jaquimbayoc7/health-access-bridge/settings/environments) · [Deployments](https://github.com/jaquimbayoc7/health-access-bridge/deployments)
- [🎨 Mockups de Diseño](./frontend/design/images/) — 8 pantallas: Login, Dashboard, Pacientes, Predicciones, Admin Panel, Análisis, Guía Predictiva, Perfil Funcional ICF

### Referencias técnicas

| Archivo | Contenido |
|---------|-----------|
| [docs/api/redoc-api.html](./docs/api/redoc-api.html) | Referencia de la API (OpenAPI/ReDoc) con ICF y analytics |
| [docs/api/frontend-docs.html](./docs/api/frontend-docs.html) | Arquitectura de la SPA: rutas, servicios, páginas y pruebas |
| [docs/diagrams/](./docs/diagrams) | Diagramas C4 y diseño del RAG |
