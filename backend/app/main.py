# app/main.py

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
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

# Middleware para logging de requests (debe ir antes de CORS)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware para loggear todas las requests entrantes.
    Útil para debuggear problemas de CORS.
    """
    origin = request.headers.get("origin", "N/A")
    method = request.method
    path = request.url.path
    
    print(f"📨 {method} {path} | Origin: {origin}")
    
    # Llamar al siguiente middleware/handler
    response = await call_next(request)
    
    # Log del status code de la respuesta
    print(f"📤 {method} {path} | Status: {response.status_code}")
    
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# ======================================================================
# Exception handlers para asegurar que los headers de CORS siempre 
# estén presentes, incluso en respuestas de error
# ======================================================================

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Maneja excepciones HTTP y asegura que los headers de CORS estén presentes.
    Esto es crucial para que el frontend reciba errores correctamente.
    """
    origin = request.headers.get("origin")
    
    # Crear la respuesta de error
    response = JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
    
    # Agregar headers de CORS si el origen está permitido
    if origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
    
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Maneja errores de validación de requests y asegura que los headers de CORS estén presentes.
    """
    origin = request.headers.get("origin")
    
    # Crear la respuesta de error de validación
    response = JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body}
    )
    
    # Agregar headers de CORS si el origen está permitido
    if origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
    
    return response

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Maneja cualquier otra excepción no capturada y asegura que los headers de CORS estén presentes.
    """
    origin = request.headers.get("origin")
    
    # Log del error para debugging
    print(f"❌ Error no manejado: {type(exc).__name__}: {str(exc)}")
    
    # Crear la respuesta de error general
    response = JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Error interno del servidor"}
    )
    
    # Agregar headers de CORS si el origen está permitido
    if origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
    
    return response

@app.on_event("startup")
def on_startup():
    """
    Evento de startup que:
    1. Intenta crear las tablas si no existen
    2. Crea el usuario administrador por defecto si no existe
    
    Es tolerante a errores de conexión para que la app siga funcionando
    aunque la BD no esté lista inicialmente.
    """
    # Mostrar configuración de CORS
    print("=" * 60)
    print("🌐 CONFIGURACIÓN DE CORS")
    print("=" * 60)
    print("Orígenes permitidos:")
    for origin in allowed_origins:
        print(f"  ✓ {origin}")
    print("=" * 60)
    
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