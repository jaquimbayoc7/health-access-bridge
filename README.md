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

| Ambiente | Rama | URL |
|----------|------|-----|
| Development | `develop` | https://hab-backend-dev.onrender.com |
| QA / Staging | `staging` | https://hab-backend-qa.onrender.com |
| Production | `main` | https://hab-backend.onrender.com |

## Setup local

```bash
cp .env.dev.example .env
docker-compose up --build
```

## Documentación

- [Backlog](./BACKLOG.md)
- [Arquitectura](./docs/architecture.md)
- [GitHub Project SCRUM Board](https://github.com/users/jaquimbayoc7/projects/1)
