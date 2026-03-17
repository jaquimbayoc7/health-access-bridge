# app/main.py

from fastapi import FastAPI
from .database import engine, Base, SessionLocal
from .routers import users, patients, admin
from . import crud, schemas
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="Health Access Bridge API",
    description=(
        "## Descripción\n\n"
        "API RESTful para la plataforma **Health Access Bridge (HAB)**, orientada a la gestión clínica "
        "de pacientes con discapacidad y al análisis predictivo de perfiles de barreras de acceso a la salud.\n\n"
        "## Funcionalidades principales\n\n"
        "- 🔐 **Autenticación y control de acceso** basado en roles (Admin, Médico) con JWT\n"
        "- 👤 **Gestión de usuarios** — creación, activación/desactivación y consulta de perfil\n"
        "- 🏥 **Gestión de pacientes** — CRUD completo con búsqueda, paginación y soft delete\n"
        "- 🤖 **Predicción de perfiles de discapacidad** — modelo ML integrado (Hybrid Model)\n\n"
        "## Seguridad\n\n"
        "Todos los endpoints (excepto `/users/login` y `/health`) requieren autenticación mediante "
        "token Bearer. Usa el botón **Authorize** para ingresar tu token JWT.\n\n"
        "## Ambientes\n\n"
        "| Ambiente | URL |\n"
        "|----------|-----|\n"
        "| DEV | https://hab-backend-dev.onrender.com |\n"
        "| QA | https://hab-backend-qa.onrender.com |\n"
        "| PROD | https://hab-backend-szj1.onrender.com |\n"
    ),
    version="1.0.0",
    contact={
        "name": "Health Access Bridge",
        "url": "https://github.com/jaquimbayoc7/health-access-bridge",
    },
    license_info={
        "name": "MIT",
    },
)

# NO crear tablas aquí - se hace en el evento de startup
# Esta línea se comentó para evitar problemas de conexión al iniciar


# Agregar CORS middleware
_raw_origins = os.getenv("ALLOWED_ORIGINS", "")
_default_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080",
    "https://hab-frontend.onrender.com",
    "https://hab-frontend-dev.onrender.com",
    "https://hab-frontend-qa.onrender.com",
    "https://e1bb997f-a232-4850-a558-28c9f9aba95b.lovableproject.com",
]
_env_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]
allowed_origins = list(set(_default_origins + _env_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    """
    Evento de startup que:
    1. Intenta crear las tablas si no existen
    2. Crea el usuario administrador por defecto si no existe
    
    Es tolerante a errores de conexión para que la app siga funcionando
    aunque la BD no esté lista inicialmente.
    """
    try:
        # Intentar crear las tablas
        print("Inicializando esquema de base de datos...")
        Base.metadata.create_all(bind=engine)
        print("✓ Esquema de base de datos listo")
    except Exception as e:
        print(f"⚠ Advertencia durante inicialización de BD: {e}")
        print("Continuando con el startup... Las tablas se crearán cuando se necesiten.")
        return
    
    # Ejecutar seed de datos de prueba (idempotente)
    try:
        from .seed import run_seed
        db = SessionLocal()
        print("Ejecutando seed de datos de prueba...")
        run_seed(db)
        db.close()
    except Exception as e:
        print(f"⚠ No se pudo ejecutar seed: {e}")

# ======================================================================
# CORRECCIÓN CLAVE: Asegurarse de que TODOS los routers están incluidos
# correctamente con sus prefijos. Esta sección es la que resuelve el 404.
# ======================================================================
app.include_router(users.router, prefix="/users", tags=["Users & Authentication"])
app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])


@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raíz de bienvenida."""
    return {"message": "Health Access Bridge API v1.0.0 — docs disponibles en /docs"}

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint para CI/CD smoke tests y monitoreo."""
    return {"status": "ok"}