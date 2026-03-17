# Health Access Bridge — Backend API

[![DEV](https://img.shields.io/badge/DEV-Live-blue)](https://hab-backend-dev.onrender.com/docs)
[![QA](https://img.shields.io/badge/QA-Live-yellow)](https://hab-backend-qa.onrender.com/docs)
[![PROD](https://img.shields.io/badge/PROD-Live-brightgreen)](https://hab-backend-szj1.onrender.com/docs)

API REST desarrollada con **FastAPI** para la gestión clínica de pacientes con discapacidad y la predicción de perfiles de barreras de acceso a la salud, usando un modelo híbrido de Machine Learning.

## Descripción

El backend provee una plataforma segura para que profesionales de salud gestionen registros de pacientes con discapacidad. Integra autenticación JWT, control de acceso basado en roles (RBAC), CRUD completo de pacientes y un modelo de Machine Learning embebido para predicción de perfiles.

**Modelo ML (dos etapas):**
1. **Clustering (K-Means):** Genera perfiles de percepción a partir de datos de barreras.
2. **Clasificación (Gradient Boosting):** Predice el perfil de un paciente desde datos demográficos y clínicos.

## Características Principales

- **Autenticación JWT** con Bcrypt y control de expiración de tokens.
- **RBAC (Roles):** `admin` (gestión global) · `médico` (gestión de sus propios pacientes).
- **CRUD Pacientes:** Crear, listar, editar, eliminar (soft delete) con búsqueda y paginación.
- **Predicción ML:** Endpoint dedicado que clasifica al paciente en Perfil 0 (Barreras Bajas), 1 (Moderadas) o 2 (Altas).
- **Seed de datos:** 10 pacientes de prueba precargados (5 por médico) — idempotente.
- **Documentación interactiva:** Swagger UI (`/docs`) y ReDoc (`/redoc`) autogenerados.
- **3 ambientes independientes:** DEV · QA · PROD, cada uno con su propia BD PostgreSQL.

## Stack Tecnológico

| Componente | Tecnología |
|---|---|
| **Framework** | FastAPI 0.111 |
| **ASGI Server** | Uvicorn |
| **ORM** | SQLAlchemy 2.x |
| **Base de datos** | PostgreSQL 15 (Render managed) |
| **Validación** | Pydantic v2 |
| **Autenticación** | python-jose (JWT) · Passlib (Bcrypt) |
| **ML** | scikit-learn · pandas · joblib |
| **Testing** | pytest · pytest-cov · httpx |
| **Python** | 3.11.10 |

## Estructura del proyecto

```
backend/
├── app/
│   ├── main.py             # Entrypoint FastAPI + CORS + startup seed
│   ├── models.py           # Modelos SQLAlchemy (User, Patient)
│   ├── schemas.py          # Esquemas Pydantic v2
│   ├── crud.py             # Operaciones de BD (incluye get_all_patients para admin)
│   ├── auth.py             # JWT + Bcrypt
│   ├── dependencies.py     # RBAC: get_current_active_user/admin/medico
│   ├── database.py         # Engine + SessionLocal + Base
│   ├── seed.py             # Seed idempotente: 3 usuarios + 10 pacientes
│   └── routers/
│       ├── users.py        # POST /users/login · GET /users/me
│       ├── patients.py     # CRUD /patients/ + POST /{id}/predict
│       └── admin.py        # /admin/users · /admin/reset-seed
├── model/
│   ├── train_model.py      # Script de entrenamiento
│   └── model_pipeline.joblib # Modelo entrenado (generado por build.sh)
├── requirements.txt        # Dependencias de producción
├── requirements-test.txt   # Dependencias de CI/testing
├── build.sh                # Script Render: verifica/recrea esquema BD + modelo
└── runtime.txt             # python-3.11.10
```

## Instalación y ejecución local

### Requisitos
- Python 3.11+
- PostgreSQL 15 (o usar SQLite cambiando `DATABASE_URL`)

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/jaquimbayoc7/health-access-bridge.git
cd health-access-bridge/backend

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\Activate.ps1   # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Variables de entorno
# Crear archivo .env con:
# DATABASE_URL=postgresql://user:pass@localhost:5432/hab_dev
# JWT_SECRET=tu_secreto_aqui
# ENVIRONMENT=development

# 5. Entrenar el modelo ML (primera vez)
python model/train_model.py

# 6. Iniciar el servidor
uvicorn app.main:app --reload --port 8000
```

API disponible en `http://localhost:8000` · Docs en `http://localhost:8000/docs`

> El seed se ejecuta automáticamente en el primer startup creando 3 usuarios y 10 pacientes.

## Uso de la API

**Docs interactivos:**
- PROD: https://hab-backend-szj1.onrender.com/docs
- DEV: https://hab-backend-dev.onrender.com/docs
- Local: http://localhost:8000/docs

### Flujo básico

```bash
# 1. Login (obtener token)
curl -X POST https://hab-backend-szj1.onrender.com/users/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=medico1@salud.co&password=medico123"

# 2. Listar pacientes
TOKEN="tu_token_aqui"
curl https://hab-backend-szj1.onrender.com/patients/ \
  -H "Authorization: Bearer $TOKEN"

# 3. Ejecutar predicción
curl -X POST https://hab-backend-szj1.onrender.com/patients/1/predict \
  -H "Authorization: Bearer $TOKEN"

# 4. Resetear seed (solo admin)
curl -X POST https://hab-backend-szj1.onrender.com/admin/reset-seed \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

## Despliegue en Render

| Parámetro | Valor |
|---|---|
| **Build Command** | `pip install -r requirements.txt && bash build.sh` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Runtime** | Python 3.11 |

### Variables de entorno requeridas

| Variable | Descripción |
|---|---|
| `DATABASE_URL` | URL interna PostgreSQL de Render (`.internal`) |
| `JWT_SECRET` | Secreto para firmar tokens JWT |
| `ENVIRONMENT` | `development` / `qa` / `production` |
| `ALLOWED_ORIGINS` | URLs del frontend separadas por coma (CORS) |

### `build.sh` — qué hace
1. Verifica / entrena el modelo ML si no existe.
2. Inspecciona el esquema de la tabla `patients`; si está desactualizado la recrea.
3. Ejecuta `create_all` para crear las tablas faltantes.

### Credenciales de prueba (seed)

| Rol | Email | Contraseña | Pacientes |
|-----|-------|------------|-----------|
| Admin | `administrador@salud.co` | `adminpassword` | Ve los 10 |
| Médico 1 | `medico1@salud.co` | `medico123` | 5 |
| Médico 2 | `medico2@salud.co` | `medico123` | 5 |

---

## Autores

- **Julián Andrés Quimbayo Castro** — [julian.quimbayo@corhuila.edu.co](mailto:julian.quimbayo@corhuila.edu.co)
- **Willians Aguilar Rodríguez** — [waguilar-2021a@corhuila.edu.co](mailto:waguilar-2021a@corhuila.edu.co)
- **Jose Miguel Llanos Mosquera** — [jmllanosm@corhuila.edu.co](mailto:jmllanosm@corhuila.edu.co)
- **Cindy Vargas Duque** — [sistemas@corhuila.edu.co](mailto:sistemas@corhuila.edu.co)
