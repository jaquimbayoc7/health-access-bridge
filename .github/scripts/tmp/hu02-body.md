## Historia de Usuario

**Como** Médico
**Deseo** visualizar y gestionar pacientes con datos precargados
**Para** agilizar la consulta médica y no empezar desde cero con cada registro.

---

## Detalles Técnicos

| Campo | Detalle |
|-------|---------|
| **Entradas** | Script de migración/seed con datos demográficos base |
| **Proceso** | CRUD completo (Create, Read, Update, Delete) en PostgreSQL |
| **Salida** | Lista de pacientes con buscador y filtros |
| **Stack** | FastAPI + SQLAlchemy + React/TypeScript |
| **Estimación** | 13 puntos |
| **Sprint** | Sprint 2 (Semanas 6-7) |
| **Momento** | Momento 1 - Trabajo Integrador I |

---

## Criterios de Aceptación

- [x] Al iniciar la app, existen al menos 10 pacientes de prueba (seed)
- [x] El Médico puede ver listado de pacientes con búsqueda por nombre/documento (`?search=`)
- [x] El Médico puede editar la historia clínica de un paciente existente
- [x] Validación de campos obligatorios (nombre, numero_documento, fecha_nacimiento, género)
- [x] Solo usuarios autenticados pueden acceder a los datos de pacientes

---

## Tareas

### Backend ✅
- [x] Diseñar esquema SQL tabla `patients` (normalizado, 3FN)
- [x] Tablas creadas automáticamente en startup (`create_all` — sin Alembic)
- [x] Crear seed idempotente con 10+ pacientes de prueba
- [x] Implementar `GET /patients/` con paginación (`skip`, `limit`) y búsqueda (`?search=nombre_o_documento`)
- [x] Implementar `GET /patients/{id}` con verificación de propiedad (403 si no es dueño)
- [x] Implementar `POST /patients/` para crear paciente (solo médico autenticado)
- [x] Implementar `PUT /patients/{id}` para actualizar historia clínica
- [x] Implementar `DELETE /patients/{id}` — soft delete (`is_active=False`, registro no se elimina de BD)
- [x] Campo `numero_documento` único e indexado en modelo `Patient`
- [x] Campo `is_active` para soft delete en modelo `Patient`
- [x] Desplegado en Render DEV, QA y PROD

### Frontend ⏳ (pendiente — siguiente sprint)
- [ ] Desarrollar componente `PatientsTable` con búsqueda
- [ ] Desarrollar formulario de edición de historia clínica

---

## Definition of Done (DoD)

- [x] CRUD funcional al 100% — verificable vía `/docs` Swagger
- [x] Base de datos normalizada (3FN) — tabla `patients` con FK `owner_id → users`
- [x] Validación de campos obligatorios en backend (Pydantic + Field validators)
- [x] Seed script ejecuta sin errores (idempotente en startup)
- [x] Código mergeado en `master`, `develop` y `staging`

---

## Endpoints desplegados

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/patients/` | Crear paciente |
| `GET` | `/patients/?search=&skip=&limit=` | Listar con búsqueda y paginación |
| `GET` | `/patients/{id}` | Detalle con verificación de propiedad |
| `PUT` | `/patients/{id}` | Actualizar historia clínica |
| `DELETE` | `/patients/{id}` | Soft delete (`is_active=False`) |
| `POST` | `/patients/{id}/predict` | Predicción perfil discapacidad |

---

## URLs por ambiente

| Ambiente | API Base | Docs |
|----------|----------|------|
| **DEV** | https://hab-backend-dev.onrender.com | https://hab-backend-dev.onrender.com/docs |
| **QA** | https://hab-backend-qa.onrender.com | https://hab-backend-qa.onrender.com/docs |
| **PROD** | https://hab-backend.onrender.com | https://hab-backend.onrender.com/docs |

---

## Datos de prueba (seed — 10 pacientes asignados a medico1@salud.co)

| # | Nombre | Documento | Perfil |
|---|--------|-----------|--------|
| 1 | Juan Pérez García | 1001234567 | Barreras Moderadas |
| 2 | María Fernanda López | 1002345678 | Barreras Altas |
| 3 | Carlos Eduardo Ramírez | 1003456789 | Barreras Bajas |
| 4 | Lucía Valentina Torres | 1004567890 | Barreras Altas |
| 5 | Andrés Felipe Morales | 1005678901 | Barreras Bajas |
| 6 | Diana Patricia Herrera | 1006789012 | Barreras Altas |
| 7 | Santiago Alejandro Ruiz | 1007890123 | Barreras Altas |
| 8 | Valentina Sofía Castillo | 1008901234 | Barreras Moderadas |
| 9 | Miguel Ángel Ortiz | 1009012345 | Barreras Altas |
| 10 | Laura Camila Mendoza | 1010123456 | Barreras Moderadas |

---

## Rama Git

`feature/hu-02-patients-crud` → mergeado en `master`
