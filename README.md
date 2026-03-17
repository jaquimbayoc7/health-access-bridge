# Health Access Bridge (HAB)

Plataforma web para la gestión clínica de pacientes con discapacidad y el análisis predictivo de perfiles de barreras de acceso a la salud en zonas rurales.

---

## Estado del Proyecto — Momento 1

> **Actualizado:** Marzo 2026

| Capa | Estado | Detalle |
|------|--------|---------|
| **Backend** | ✅ Desplegado en los 3 ambientes | Autenticación, CRUD de pacientes, predicción ML |
| **Frontend** | ⏳ En desarrollo | Scaffold React pendiente |
| **CI/CD** | ✅ Configurado | GitHub Actions → Render (auto-deploy) |
| **Base de datos** | ✅ PostgreSQL en Render | 3 instancias independientes (dev/qa/prod) |

---

## Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| **Backend** | Python 3.11.10 · FastAPI · SQLAlchemy · PostgreSQL |
| **Frontend** | React 18 · TypeScript · Vite · TailwindCSS · shadcn/ui *(pendiente)* |
| **Autenticación** | JWT con claims de rol (Admin, Médico) · Bcrypt |
| **IA Predictiva** | HybridModelDisability (modelo ML embebido) |
| **IA Generativa** | LLM OpenAI GPT-4 *(HU-07 — futuro)* |
| **Despliegue** | Render · Web Service · PostgreSQL managed |
| **CI/CD** | GitHub Actions · 3 workflows (dev/qa/prod) |

---

## Ambientes y URLs

| Ambiente | Rama | Backend | API Docs |
|----------|------|---------|----------|
| **Development** | `develop` | https://hab-backend-dev.onrender.com | [/docs](https://hab-backend-dev.onrender.com/docs) |
| **QA / Staging** | `staging` | https://hab-backend-qa.onrender.com | [/docs](https://hab-backend-qa.onrender.com/docs) |
| **Production** | `master` | https://hab-backend.onrender.com | [/docs](https://hab-backend.onrender.com/docs) |

### Credenciales de prueba (seed — disponibles en los 3 ambientes)

| Rol | Email | Contraseña |
|-----|-------|------------|
| **Admin** | `administrador@salud.co` | `adminpassword` |
| **Médico** | `medico1@salud.co` | `medico123` |
| **Médico** | `medico2@salud.co` | `medico123` |

> `medico1@salud.co` tiene 10 pacientes de prueba. `medico2@salud.co` está vacío.

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
| `GET` | `/patients/?search=&skip=&limit=` | Médico | Listar con búsqueda y paginación |
| `GET` | `/patients/{id}` | Médico (dueño) | Detalle de paciente |
| `PUT` | `/patients/{id}` | Médico (dueño) | Actualizar historia clínica |
| `DELETE` | `/patients/{id}` | Médico (dueño) | Soft delete |
| `POST` | `/patients/{id}/predict` | Médico (dueño) | Predicción perfil discapacidad |

### Sistema
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/health` | Health check (CI/CD) |
| `GET` | `/` | Bienvenida |

---

## GitHub Environments

| Ambiente | Protección | Secrets |
|----------|-----------|---------|
| `development` | Sin restricciones | `DATABASE_URL`, `SECRET_KEY`, `PYTHON_VERSION` |
| `qa` | Sin restricciones | `DATABASE_URL`, `SECRET_KEY`, `PYTHON_VERSION` |
| `production` | � Aprobación manual requerida | `DATABASE_URL`, `SECRET_KEY`, `PYTHON_VERSION` |

🔗 [Ver environments en GitHub](https://github.com/jaquimbayoc7/health-access-bridge/settings/environments)

---

## Historias de Usuario

### Momento 1 — Trabajo Integrador I (Semanas 1-9) · [Milestone](https://github.com/jaquimbayoc7/health-access-bridge/milestone/1)

> Épica: [#11 EPICA-01 Estructuración y Diseño](https://github.com/jaquimbayoc7/health-access-bridge/issues/11)

| Issue | Título | Sprint | Pts | Backend | Frontend | Estado |
|-------|--------|--------|-----|---------|----------|--------|
| [#1](https://github.com/jaquimbayoc7/health-access-bridge/issues/1) | [HU-01] Autenticación y Roles (RBAC) | Sprint 1 (Sem. 4-5) | 8 | ✅ Completo | ⏳ Pendiente | 🟡 En Progreso |
| [#2](https://github.com/jaquimbayoc7/health-access-bridge/issues/2) | [HU-02] Registro y Precarga de Pacientes | Sprint 2 (Sem. 6-7) | 13 | ✅ Completo | ⏳ Pendiente | � En Progreso |
| [#3](https://github.com/jaquimbayoc7/health-access-bridge/issues/3) | [HU-03] Integración Frontend-Backend | Sprint 3 (Sem. 8-9) | 5 | — | ⏳ Pendiente | 📋 Backlog |

### Momento 2 — Trabajo Integrador II (Semanas 10-18) · [Milestone](https://github.com/jaquimbayoc7/health-access-bridge/milestone/2)

> Épica: [#12 EPICA-02 Funcionalidades Core](https://github.com/jaquimbayoc7/health-access-bridge/issues/12)

| Issue | Título | Sprint | Pts | Estado |
|-------|--------|--------|-----|--------|
| [#4](https://github.com/jaquimbayoc7/health-access-bridge/issues/4) | [HU-04] Integración Modelo Predictivo (HybridModelDisability) | Sprint 4-5 (Sem. 10-13) | 21 | 📋 Backlog |
| [#5](https://github.com/jaquimbayoc7/health-access-bridge/issues/5) | [HU-05] Modo Offline y PWA | Sprint 6-7 (Sem. 14-17) | 13 | 📋 Backlog |
| [#6](https://github.com/jaquimbayoc7/health-access-bridge/issues/6) | [HU-06] Pruebas de Integración y Rendimiento API | Sprint 7 (Sem. 16-17) | 8 | 📋 Backlog |

### Momento 3 — Trabajo Integrador III (Semanas 19-27) · [Milestone](https://github.com/jaquimbayoc7/health-access-bridge/milestone/3)

> Épica: [#13 EPICA-03 IA Generativa, Dashboards y Cierre](https://github.com/jaquimbayoc7/health-access-bridge/issues/13)

| Issue | Título | Sprint | Pts | Estado |
|-------|--------|--------|-----|--------|
| [#7](https://github.com/jaquimbayoc7/health-access-bridge/issues/7) | [HU-07] Orquestación con LLM para Recomendaciones Clínicas | Sprint 8-9 (Sem. 19-22) | 21 | 📋 Backlog |
| [#8](https://github.com/jaquimbayoc7/health-access-bridge/issues/8) | [HU-08] Dashboard de Análisis y Exportación | Sprint 10-11 (Sem. 23-26) | 13 | 📋 Backlog |
| [#9](https://github.com/jaquimbayoc7/health-access-bridge/issues/9) | [HU-09] Pruebas Completas y Feedback de Usuarios | Sprint 11 (Sem. 25-26) | 8 | 📋 Backlog |
| [#10](https://github.com/jaquimbayoc7/health-access-bridge/issues/10) | [HU-10] Despliegue Final y Generación de Manuales | Sprint 12 (Sem. 27) | 5 | 📋 Backlog |

🔗 [Ver todas las issues](https://github.com/jaquimbayoc7/health-access-bridge/issues) · [Ver SCRUM Board](https://github.com/users/jaquimbayoc7/projects/1)

---

## Épicas

| Issue | Épica | Momento | HUs | Pts | Estado |
|-------|-------|---------|-----|-----|--------|
| [#11](https://github.com/jaquimbayoc7/health-access-bridge/issues/11) | EPICA-01 Estructuración y Diseño | 1 · Sem. 1-3 | — | — | ✅ Done |
| [#12](https://github.com/jaquimbayoc7/health-access-bridge/issues/12) | EPICA-02 Funcionalidades Core y Capacidades Avanzadas | 2 · Sem. 10-18 | HU-04, 05, 06 | 42 | 📋 Backlog |
| [#13](https://github.com/jaquimbayoc7/health-access-bridge/issues/13) | EPICA-03 IA Generativa, Dashboards y Cierre | 3 · Sem. 19-27 | HU-07 al 10 | 47 | 📋 Backlog |

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
```

> La app crea las tablas y ejecuta el seed automáticamente en el primer startup.
> Documentación interactiva disponible en: http://localhost:8000/docs

---

## Estructura del proyecto

```
health-access-bridge/
├── backend/
│   ├── app/
│   │   ├── main.py          # Entrypoint FastAPI + startup + CORS
│   │   ├── models.py        # Modelos SQLAlchemy (User, Patient)
│   │   ├── schemas.py       # Esquemas Pydantic
│   │   ├── crud.py          # Operaciones de base de datos
│   │   ├── auth.py          # JWT + Bcrypt
│   │   ├── dependencies.py  # Inyección de dependencias y RBAC
│   │   ├── database.py      # Configuración SQLAlchemy
│   │   ├── seed.py          # Seed de datos de prueba (idempotente)
│   │   └── routers/
│   │       ├── users.py     # POST /users/login · GET /users/me
│   │       ├── patients.py  # CRUD /patients/ + predicción
│   │       └── admin.py     # Gestión de usuarios (solo Admin)
│   ├── requirements.txt
│   ├── build.sh
│   └── runtime.txt          # python-3.11.10
├── .env.dev.example
├── .env.qa.example
├── .env.prod.example
├── render.yaml              # Blueprint Render (3 servicios + 3 DBs)
├── runtime.txt
└── .github/
    └── workflows/
        ├── ci-dev.yml       # Push a develop → tests + deploy DEV
        ├── ci-qa.yml        # Push a staging → tests + deploy QA
        └── ci-prod.yml      # Push a master → aprobación manual + deploy PROD
```

---

## Documentación

- [Backlog](./BACKLOG.md)
- [GitHub Project SCRUM Board](https://github.com/users/jaquimbayoc7/projects/1)
- [GitHub Environments](https://github.com/jaquimbayoc7/health-access-bridge/settings/environments)
- [Historial de Deployments](https://github.com/jaquimbayoc7/health-access-bridge/deployments)
- [📁 Documentos OneDrive (BPM, Release Plan, Arquitectura, Figma)](https://1drv.ms/f/c/1bb90464e00ae32f/IgClfUapHhO0Qqi0xchUzV7PAe4-x2Mk6pn1ZRdFia8Xz8c?e=w6exQH)
