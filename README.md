# Health Access Bridge (HAB)

Aplicación web para facilitar el acceso a servicios de salud para personas con discapacidad en zonas rurales.

## Stack

- **Backend:** Python 3.11 + FastAPI + SQLAlchemy + Alembic + PostgreSQL
- **Frontend:** React 18 + TypeScript + Vite + TailwindCSS + shadcn/ui
- **Auth:** JWT con claims de rol (Admin, Médico)
- **IA Predictiva:** HybridModelDisability
- **IA Generativa:** LLM (OpenAI GPT-4)
- **Despliegue:** Render (Web Service + Static Site + PostgreSQL managed)

## Ambientes

| Ambiente | Rama | Backend URL | Frontend URL |
|----------|------|-------------|--------------|
| Development | `develop` | https://hab-backend-dev.onrender.com | https://hab-frontend-dev.onrender.com |
| QA / Staging | `staging` | https://hab-backend-qa.onrender.com | https://hab-frontend-qa.onrender.com |
| Production | `master` | https://hab-backend.onrender.com | https://hab-frontend.onrender.com |

> Las URLs de Render se activan automáticamente tras el primer deploy exitoso del scaffold de código.

## GitHub Environments

| Ambiente | Protección | Secrets configurados |
|----------|-----------|----------------------|
| `development` | Sin restricciones | `JWT_SECRET`, `VITE_API_BASE_URL` |
| `qa` | Sin restricciones | `JWT_SECRET`, `VITE_API_BASE_URL` |
| `production` | 🔒 Aprobación manual requerida | `JWT_SECRET`, `VITE_API_BASE_URL` |

🔗 [Ver environments en GitHub](https://github.com/jaquimbayoc7/health-access-bridge/settings/environments)

## Épicas

| Issue | Épica | Momento | Semanas | HUs | Pts |
|-------|-------|---------|---------|-----|-----|
| [#11](https://github.com/jaquimbayoc7/health-access-bridge/issues/11) | [EPICA-01] Estructuración y Diseño | Momento 1 | 1-3 | — | — |
| [#12](https://github.com/jaquimbayoc7/health-access-bridge/issues/12) | [EPICA-02] Funcionalidades Core y Capacidades Avanzadas | Momento 2 | 10-18 | HU-04, HU-05, HU-06 | 42 |
| [#13](https://github.com/jaquimbayoc7/health-access-bridge/issues/13) | [EPICA-03] IA Generativa, Dashboards y Cierre | Momento 3 | 19-27 | HU-07, HU-08, HU-09, HU-10 | 47 |

## Issues / Historias de Usuario

### Momento 1 — Trabajo Integrador I (Semanas 1-9) · [Milestone](https://github.com/jaquimbayoc7/health-access-bridge/milestone/1)

> Épica: [#11 EPICA-01 Estructuración y Diseño](https://github.com/jaquimbayoc7/health-access-bridge/issues/11)

| Issue | Título | Sprint | Pts | Estado |
|-------|--------|--------|-----|--------|
| [#1](https://github.com/jaquimbayoc7/health-access-bridge/issues/1) | [HU-01] Sistema de Autenticación y Roles (RBAC) | Sprint 1 (Sem. 4-5) | 13 | 📋 Backlog |
| [#2](https://github.com/jaquimbayoc7/health-access-bridge/issues/2) | [HU-02] Registro y Precarga de Datos de Pacientes | Sprint 2 (Sem. 6-7) | 8 | 📋 Backlog |
| [#3](https://github.com/jaquimbayoc7/health-access-bridge/issues/3) | [HU-03] Integración Frontend-Backend y Despliegue Local | Sprint 3 (Sem. 8-9) | 5 | 📋 Backlog |

### Momento 2 — Trabajo Integrador II (Semanas 10-18) · [Milestone](https://github.com/jaquimbayoc7/health-access-bridge/milestone/2)

> Épica: [#12 EPICA-02 Funcionalidades Core y Capacidades Avanzadas](https://github.com/jaquimbayoc7/health-access-bridge/issues/12)

| Issue | Título | Sprint | Pts | Estado |
|-------|--------|--------|-----|--------|
| [#4](https://github.com/jaquimbayoc7/health-access-bridge/issues/4) | [HU-04] Integración del Modelo Predictivo (HybridModelDisability) | Sprint 4-5 (Sem. 10-13) | 21 | 📋 Backlog |
| [#5](https://github.com/jaquimbayoc7/health-access-bridge/issues/5) | [HU-05] Modo Offline y PWA | Sprint 6-7 (Sem. 14-17) | 13 | 📋 Backlog |
| [#6](https://github.com/jaquimbayoc7/health-access-bridge/issues/6) | [HU-06] Pruebas de Integración Backend-Frontend y Rendimiento API | Sprint 7 (Sem. 16-17) | 8 | 📋 Backlog |

### Momento 3 — Trabajo Integrador III (Semanas 19-27) · [Milestone](https://github.com/jaquimbayoc7/health-access-bridge/milestone/3)

> Épica: [#13 EPICA-03 IA Generativa, Dashboards y Cierre](https://github.com/jaquimbayoc7/health-access-bridge/issues/13)

| Issue | Título | Sprint | Pts | Estado |
|-------|--------|--------|-----|--------|
| [#7](https://github.com/jaquimbayoc7/health-access-bridge/issues/7) | [HU-07] Orquestación con LLM para Recomendaciones Clínicas | Sprint 8-9 (Sem. 19-22) | 21 | 📋 Backlog |
| [#8](https://github.com/jaquimbayoc7/health-access-bridge/issues/8) | [HU-08] Dashboard de Análisis y Exportación | Sprint 10-11 (Sem. 23-26) | 13 | 📋 Backlog |
| [#9](https://github.com/jaquimbayoc7/health-access-bridge/issues/9) | [HU-09] Pruebas Completas y Feedback de Usuarios | Sprint 11 (Sem. 25-26) | 8 | 📋 Backlog |
| [#10](https://github.com/jaquimbayoc7/health-access-bridge/issues/10) | [HU-10] Despliegue Final y Generación de Manuales | Sprint 12 (Sem. 27) | 5 | 📋 Backlog |

🔗 [Ver todas las issues](https://github.com/jaquimbayoc7/health-access-bridge/issues) · [Ver SCRUM Board](https://github.com/users/jaquimbayoc7/projects/1)

## Milestones

| Milestone | Periodo | Épica | Issues | Avance |
|-----------|---------|-------|--------|--------|
| [Momento 1: Trabajo Integrador I](https://github.com/jaquimbayoc7/health-access-bridge/milestone/1) | Semanas 1-9 | EPICA-01 | HU-01, HU-02, HU-03 | 24% |
| [Momento 2: Trabajo Integrador II](https://github.com/jaquimbayoc7/health-access-bridge/milestone/2) | Semanas 10-18 | EPICA-02 | HU-04, HU-05, HU-06 | 60% |
| [Momento 3: Trabajo Integrador III](https://github.com/jaquimbayoc7/health-access-bridge/milestone/3) | Semanas 19-27 | EPICA-03 | HU-07, HU-08, HU-09, HU-10 | 100% |

## Setup local

```bash
cp .env.dev.example .env
docker-compose up --build
```

## Documentación

- [Backlog](./BACKLOG.md)
- [Arquitectura](./docs/architecture.md)
- [GitHub Project SCRUM Board](https://github.com/users/jaquimbayoc7/projects/1)
- [GitHub Environments](https://github.com/jaquimbayoc7/health-access-bridge/settings/environments)
- [Historial de Deployments](https://github.com/jaquimbayoc7/health-access-bridge/deployments)
