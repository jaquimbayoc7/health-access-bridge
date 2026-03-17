## Historia de Usuario

**Como** Administrador del sistema
**Deseo** gestionar el acceso mediante roles (Admin, Médico)
**Para** asegurar que solo personal autorizado acceda a la información clínica.

---

## Detalles Técnicos

| Campo | Detalle |
|-------|---------|
| **Entradas** | Email, password, selección de rol |
| **Proceso** | Encriptación de claves (Bcrypt), generación de JWT |
| **Salida** | Token de sesión con claims de rol |
| **Stack** | Python/FastAPI + React/TypeScript |
| **Estimación** | 8 puntos |
| **Sprint** | Sprint 1 (Semanas 4-5) |
| **Momento** | Momento 1 - Trabajo Integrador I |

---

## Criterios de Aceptación

- [x] El Admin puede crear cuentas para Médicos mediante `POST /admin/users/register`
- [x] El Médico no puede acceder a funciones de configuración global (403 Forbidden)
- [x] Login falla con credenciales erróneas (401 Unauthorized)
- [x] Token JWT contiene claims de rol (admin/medico)
- [x] Contraseñas almacenadas con Bcrypt (nunca en texto plano)

---

## Tareas

### Backend ✅
- [x] Configurar boilerplate Python/FastAPI con estructura de carpetas
- [x] Diseñar modelo `User` (id, email, hashed_password, role, full_name, is_active)
- [x] Implementar `POST /users/login` → retorna JWT con claims de rol
- [x] Implementar `POST /admin/users/register` → solo Admin (403 si no es admin)
- [x] Implementar `GET /users/me` → retorna usuario autenticado actual
- [x] Implementar `GET /admin/users` → lista todos los usuarios (solo Admin)
- [x] Implementar `PATCH /admin/users/{id}/status` → activar/desactivar usuario
- [x] Implementar middleware `get_current_user` + `get_current_active_admin` + `get_current_active_medico`
- [x] Tablas creadas automáticamente en startup (`create_all`)
- [x] Seed script idempotente: Admin + 2 Médicos + 10 Pacientes de prueba
- [x] Desplegado en Render DEV, QA y PROD

### Frontend ⏳ (pendiente — siguiente sprint)
- [ ] Crear vista Login en React con TailwindCSS + shadcn/ui
- [ ] Implementar Auth Context con JWT + rutas protegidas
- [ ] Crear panel Admin para crear cuentas de Médicos

---

## Definition of Done (DoD)

- [x] Código mergeado en `master`, `develop` y `staging`
- [x] Seed valida login con credenciales correctas e incorrectas
- [x] Documentación de endpoints en `/docs` (Swagger auto-generado por FastAPI)
- [x] Variables de entorno en `.env.dev.example`, `.env.qa.example`, `.env.prod.example`

---

## Credenciales de prueba (seed — disponibles en DEV, QA y PROD)

| Rol | Nombre | Email | Contraseña |
|-----|--------|-------|------------|
| **Admin** | Administrador del Sistema | `administrador@salud.co` | `adminpassword` |
| **Médico** | Dr. Carlos Martínez | `medico1@salud.co` | `medico123` |
| **Médico** | Dra. Ana Lucía Gómez | `medico2@salud.co` | `medico123` |

> `medico1@salud.co` tiene **10 pacientes de prueba** asignados con perfiles variados (barreras bajas, moderadas y severas).
> `medico2@salud.co` está vacío — para probar el flujo de creación de pacientes desde cero.

---

## URLs por ambiente

| Ambiente | API Base | Docs |
|----------|----------|------|
| **DEV** | https://hab-backend-dev.onrender.com | https://hab-backend-dev.onrender.com/docs |
| **QA** | https://hab-backend-qa.onrender.com | https://hab-backend-qa.onrender.com/docs |
| **PROD** | https://hab-backend.onrender.com | https://hab-backend.onrender.com/docs |

---

## Rama Git

`feature/hu-01-auth-rbac` → mergeado en `master`
