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

## Issues / Historias de Usuario

| Issue | Título | Sprint | Momento | Estado |
|-------|--------|--------|---------|--------|
| [#1](https://github.com/jaquimbayoc7/health-access-bridge/issues/1) | [HU-01] Sistema de Autenticación y Roles (RBAC) | Sprint 1 | Momento 1 | 📋 Backlog |
| [#2](https://github.com/jaquimbayoc7/health-access-bridge/issues/2) | [HU-02] Registro y Precarga de Datos de Pacientes | Sprint 2 | Momento 1 | 📋 Backlog |
| [#3](https://github.com/jaquimbayoc7/health-access-bridge/issues/3) | [HU-03] Integración Frontend-Backend y Despliegue Local | Sprint 3 | Momento 1 | 📋 Backlog |
| [#4](https://github.com/jaquimbayoc7/health-access-bridge/issues/4) | [HU-04] Integración del Modelo Predictivo (HybridModelDisability) | Sprint 4-5 | Momento 2 | 📋 Backlog |
| [HU-05] | Modo Offline y PWA | Sprint 6-7 | Momento 2 | 📋 Backlog |
| [HU-06] | Pruebas de Integración Backend-Frontend | Sprint 7 | Momento 2 | 📋 Backlog |
| [HU-07] | Orquestación con LLM para Recomendaciones Clínicas | Sprint 8-9 | Momento 3 | 📋 Backlog |
| [HU-08] | Dashboard de Análisis y Exportación | Sprint 10-11 | Momento 3 | 📋 Backlog |
| [HU-09] | Pruebas Completas y Feedback de Usuarios | Sprint 11 | Momento 3 | 📋 Backlog |
| [HU-10] | Despliegue Final y Generación de Manuales | Sprint 12 | Momento 3 | 📋 Backlog |

🔗 [Ver todas las issues](https://github.com/jaquimbayoc7/health-access-bridge/issues) · [Ver SCRUM Board](https://github.com/users/jaquimbayoc7/projects/1)

## Milestones

| Milestone | Periodo | Issues | Avance |
|-----------|---------|--------|--------|
| [Momento 1: Trabajo Integrador I](https://github.com/jaquimbayoc7/health-access-bridge/milestone/1) | Semanas 1-9 | HU-01, HU-02, HU-03 | 24% |
| [Momento 2: Trabajo Integrador II](https://github.com/jaquimbayoc7/health-access-bridge/milestone/2) | Semanas 10-18 | HU-04, HU-05, HU-06 | 60% |
| Momento 3: Trabajo Integrador III | Semanas 19-27 | HU-07, HU-08, HU-09, HU-10 | 100% |

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
