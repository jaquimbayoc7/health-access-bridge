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

## Estado actual

> 🟡 **En Progreso** — Backend completo ✅ | Frontend pendiente ⏳

---

## Criterios de Aceptación

- [x] Al iniciar la app, existen al menos 10 pacientes de prueba (seed)
- [x] El Médico puede ver listado de pacientes con búsqueda por nombre/documento (`?search=`)
- [x] El Médico puede editar la historia clínica de un paciente existente
- [x] Validación de campos obligatorios (nombre, numero_documento, fecha_nacimiento, género)
- [x] Solo usuarios autenticados pueden acceder a los datos de pacientes
- [ ] Componente visual con tabla y buscador funcional (frontend)

---

## Tareas

### Backend ✅ Completo
- [x] Diseñar esquema SQL tabla `patients` (normalizado, 3FN)
- [x] Tablas creadas automáticamente en startup (`create_all`)
- [x] Seed idempotente con 10+ pacientes de prueba y `numero_documento` único
- [x] Implementar `GET /patients/` con paginación (`skip`, `limit`) y búsqueda (`?search=`)
- [x] Implementar `GET /patients/{id}` con verificación de propiedad (403 si no es dueño)
- [x] Implementar `POST /patients/` para crear paciente (solo médico autenticado)
- [x] Implementar `PUT /patients/{id}` para actualizar historia clínica
- [x] Implementar `DELETE /patients/{id}` — soft delete (`is_active=False`)
- [x] Campo `numero_documento` único e indexado en modelo `Patient`
- [x] Campo `is_active` para soft delete en modelo `Patient`
- [x] Desplegado en Render DEV, QA y PROD

### Frontend ⏳ Pendiente
- [ ] Desarrollar componente `PatientsTable` con búsqueda y paginación
- [ ] Desarrollar formulario de edición de historia clínica

---

## Definition of Done (DoD)

- [x] CRUD funcional al 100% — verificable vía `/docs` Swagger
- [x] Base de datos normalizada (3FN) — tabla `patients` con FK `owner_id → users`
- [x] Validación de campos obligatorios en backend (Pydantic + Field validators)
- [x] Seed script ejecuta sin errores (idempotente en startup)
- [x] Código mergeado en `master`, `develop` y `staging`
- [ ] Validación de campos obligatorios en frontend
- [ ] Pruebas E2E del flujo de gestión de pacientes

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

## Datos de prueba (seed — 10 pacientes asignados a medico1@salud.co)

| # | Nombre | Documento |
|---|--------|-----------|
| 1 | Juan Pérez García | 1001234567 |
| 2 | María Fernanda López | 1002345678 |
| 3 | Carlos Eduardo Ramírez | 1003456789 |
| 4 | Lucía Valentina Torres | 1004567890 |
| 5 | Andrés Felipe Morales | 1005678901 |
| 6 | Diana Patricia Herrera | 1006789012 |
| 7 | Santiago Alejandro Ruiz | 1007890123 |
| 8 | Valentina Sofía Castillo | 1008901234 |
| 9 | Miguel Ángel Ortiz | 1009012345 |
| 10 | Laura Camila Mendoza | 1010123456 |

---

## URLs por ambiente

| Ambiente | API Base | Docs |
|----------|----------|------|
| **DEV** | https://hab-backend-dev.onrender.com | https://hab-backend-dev.onrender.com/docs |
| **QA** | https://hab-backend-qa.onrender.com | https://hab-backend-qa.onrender.com/docs |
| **PROD** | https://hab-backend.onrender.com | https://hab-backend.onrender.com/docs |

---

## Rama Git

`feature/hu-02-patients-crud` → mergeado en `master`
