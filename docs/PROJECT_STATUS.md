# Estado del Proyecto Health Access Bridge

**Última actualización:** Marzo 2026  
**Momento actual:** Momento 1 - Trabajo Integrador I (Completado)

---

## Resumen Ejecutivo

El proyecto Health Access Bridge ha completado exitosamente el **Momento 1** (Semanas 1-9) con un avance del **41%** sobre el total del proyecto, superando el 26% proyectado inicialmente. Adicionalmente, se adelantó la implementación de la **HU-04** (Modelo Predictivo ML), originalmente planificada para el Momento 2.

---

## Estado por Épicas

### ✅ EPICA-01: Estructuración, Diseño e Implementación M1 (COMPLETADA)

**Periodo:** Semanas 1-9  
**Puntos:** 26 pts (HU-01, 02, 03) + 21 pts (HU-04 adelantada) = **47 pts completados**

#### Artefactos de Diseño

| Artefacto | Estado | Ubicación |
|-----------|--------|-----------|
| **Mockups de Diseño** (8 pantallas) | ✅ Completado | [`frontend/design/images/`](../frontend/design/images/) |
| **Arquitectura C4** (6 diagramas HTML) | ✅ Completado | [`docs/`](./) — L1 Context · L2 Container · L3 Component · L4 Code × 2 · Deployment |
| **Reporte de Insights GitHub** | ✅ Completado | [`INSIGHTS_REPORT.md`](./INSIGHTS_REPORT.md) |
| **Reporte de Testing** | ✅ Completado | [`TESTING_REPORT.md`](./TESTING_REPORT.md) |
| BPM | 📋 Pendiente | — |
| Release Plan | 📋 Pendiente | — |

**Mockups completados (8 pantallas):**
1. 01 - Login / Landing (`bi8Au.png`)
2. 02 - Dashboard (`717A2.png`)
3. 03 - Pacientes (`i0uhw.png`)
4. 04 - Predicciones (`YPvRD.png`)
5. 05 - Admin Panel (`UpZqF.png`)
6. 06 - Análisis (`HIxNY.png`)
7. 07 - Guía Predictiva (`Nj6le.png`)
8. 08 - Perfil Funcional ICF (`C45o8.png`)

---

## Estado por Historias de Usuario

### ✅ HU-01: Sistema de Autenticación y Roles (RBAC)
**Sprint:** 1 (Semanas 4-5) | **Puntos:** 8 | **Estado:** ✅ COMPLETADO

**Implementación:**
- Backend: JWT + RBAC + Bcrypt
- Endpoints: `POST /users/login`, `GET /users/me`, `POST /admin/users/register`, `PATCH /admin/users/{id}/status`
- Frontend: Login, Auth Context, rutas protegidas, sidebar diferenciada por rol
- Seed: `administrador@salud.co`, `medico1@salud.co`, `medico2@salud.co`
- Desplegado en 3 ambientes (dev/qa/prod)

---

### ✅ HU-02: Registro y Precarga de Datos de Pacientes
**Sprint:** 2 (Semanas 6-7) | **Puntos:** 13 | **Estado:** ✅ COMPLETADO

**Implementación:**
- Backend: CRUD completo con endpoints `/patients/` (POST, GET, PUT, DELETE)
- Seed: 10 pacientes (5 por médico)
- Frontend: Tabla con búsqueda, paginación, formulario de edición, exportación Excel/PDF
- RBAC: Admin ve todos los pacientes, Médico solo los propios
- Modelo Patient con 15+ campos incluyendo niveles de actividad D1-D6

---

### ✅ HU-03: Integración Frontend-Backend y Despliegue Cloud
**Sprint:** 3 (Semanas 8-9) | **Puntos:** 5 | **Estado:** ✅ COMPLETADO

**Implementación:**
- Frontend consume API real con `VITE_API_BASE_URL` configurado por ambiente
- CORS configurado con orígenes explícitos por ambiente
- Pipeline CI/CD con 3 workflows GitHub Actions (dev/qa/prod)
- Smoke tests automáticos en producción
- Desplegado en Render: 3 backends + 3 frontends + 3 BDs PostgreSQL independientes
- `build.sh` con detección automática de cambios de esquema

**Ambientes:**
- Dev: https://hab-frontend-dev.onrender.com (rama `develop`)
- QA: https://hab-frontend-qa.onrender.com (rama `staging`)
- Prod: https://hab-frontend.onrender.com (rama `master` con aprobación manual)

---

### ✅ HU-04: Integración del Modelo Predictivo (HybridModelDisability)
**Sprint:** 4-5 (Semanas 10-13) | **Puntos:** 21 | **Estado:** ✅ COMPLETADO (Adelantado en M1)

**Implementación:**
- Modelo ML embebido en backend: `model_pipeline.joblib` (K-Means + Gradient Boosting)
- Endpoint: `POST /patients/{id}/predict` serializa datos, ejecuta inferencia y persiste resultado
- Frontend:
  - `Predictions.tsx` - Selector de paciente, ejecución, historial con badges
  - `PredictiveGuide.tsx` - Guía clínica de los 3 perfiles de barreras
  - `Analytics.tsx` - Distribución de perfiles con gráfica de torta, estadísticas
- Perfiles: 0 (Barreras Bajas), 1 (Barreras Moderadas), 2 (Barreras Altas)
- Lazy loading del modelo para optimizar memoria

**Nota:** Esta HU fue adelantada e implementada durante el Momento 1 (Sprint 3).

---

### 📋 EPICA-02: Funcionalidades Core y Capacidades Avanzadas (PENDIENTE)

**Periodo:** Semanas 10-18  
**Puntos:** 21 pts (HU-05, 06) = **21 pts pendientes**

#### HU-05: Modo Offline y PWA
**Sprint:** 6-7 (Semanas 14-17) | **Puntos:** 13 | **Estado:** 📋 BACKLOG

#### HU-06: Pruebas de Integración y Rendimiento API
**Sprint:** 7 (Semanas 16-17) | **Puntos:** 8 | **Estado:** 📋 BACKLOG

---

### 📋 EPICA-03: IA Generativa, Dashboards y Cierre (PENDIENTE)

**Periodo:** Semanas 19-27  
**Puntos:** 47 pts (HU-07, 08, 09, 10) = **47 pts pendientes**

#### HU-07: Orquestación con LLM para Recomendaciones Clínicas
**Sprint:** 8-9 (Semanas 19-22) | **Puntos:** 21 | **Estado:** 📋 BACKLOG

#### HU-08: Dashboard de Análisis y Exportación
**Sprint:** 10-11 (Semanas 23-26) | **Puntos:** 13 | **Estado:** 📋 BACKLOG

#### HU-09: Pruebas Completas y Feedback de Usuarios
**Sprint:** 11 (Semanas 25-26) | **Puntos:** 8 | **Estado:** 📋 BACKLOG

#### HU-10: Despliegue Final y Generación de Manuales
**Sprint:** 12 (Semana 27) | **Puntos:** 5 | **Estado:** 📋 BACKLOG

---

## Métricas del Proyecto

| Métrica | Valor |
|---------|-------|
| **Puntos completados** | 47 pts |
| **Puntos pendientes** | 68 pts |
| **Total del proyecto** | 115 pts |
| **Avance general** | 41% |
| **Avance proyectado M1** | 26% |
| **Superación del plan** | +15% |

---

## Stack Tecnológico Implementado

| Capa | Tecnología | Estado |
|------|-----------|--------|
| **Backend** | Python 3.11.10, FastAPI, SQLAlchemy, PostgreSQL | ✅ Desplegado |
| **Frontend** | React 18, TypeScript, Vite, TailwindCSS, shadcn/ui, Recharts | ✅ Desplegado |
| **Autenticación** | JWT con claims de rol, Bcrypt | ✅ Implementado |
| **IA Predictiva** | HybridModelDisability (K-Means + Gradient Boosting) | ✅ Integrado |
| **IA Generativa** | LLM OpenAI GPT-4 | 📋 Pendiente (HU-07) |
| **Despliegue** | Render (Web Service + PostgreSQL managed) | ✅ Configurado |
| **CI/CD** | GitHub Actions (3 workflows: dev/qa/prod) | ✅ Operativo |

---

## Endpoints Disponibles

### Autenticación y Usuarios
- `POST /users/login` - Login → retorna JWT
- `GET /users/me` - Perfil del usuario actual
- `GET /admin/users` - Lista todos los usuarios (Admin)
- `POST /admin/users/register` - Crear nuevo usuario (Admin)
- `PATCH /admin/users/{id}/status` - Activar/desactivar usuario (Admin)

### Pacientes
- `POST /patients/` - Crear paciente (Médico)
- `GET /patients/?search=&skip=&limit=` - Listar con búsqueda y paginación
- `GET /patients/{id}` - Detalle de paciente
- `PUT /patients/{id}` - Actualizar historia clínica
- `DELETE /patients/{id}` - Soft delete
- `POST /patients/{id}/predict` - Predicción perfil discapacidad

### Admin - Utilidades
- `POST /admin/reset-seed` - DROP + recrear tabla patients y re-seedear (Admin)

### Sistema
- `GET /health` - Health check (CI/CD)
- `GET /` - Bienvenida

---

## Próximos Pasos

### Momento 2 (Semanas 10-18)
1. **HU-05:** Implementar modo offline y PWA para zonas rurales
2. **HU-06:** Ejecutar pruebas de integración y rendimiento API

### Momento 3 (Semanas 19-27)
1. **HU-07:** Integrar LLM (GPT-4) para recomendaciones clínicas
2. **HU-08:** Desarrollar dashboards avanzados y exportación
3. **HU-09:** Realizar pruebas completas y recopilar feedback
4. **HU-10:** Despliegue final y generación de manuales

---

## Credenciales de Prueba

Disponibles en los 3 ambientes (dev/qa/prod):

| Rol | Email | Contraseña |
|-----|-------|------------|
| **Admin** | `administrador@salud.co` | `adminpassword` |
| **Médico** | `medico1@salud.co` | `medico123` |
| **Médico** | `medico2@salud.co` | `medico123` |

> `medico1@salud.co` tiene 5 pacientes de prueba. `medico2@salud.co` tiene 5 pacientes. `administrador@salud.co` puede ver los 10.

---

## Enlaces Importantes

- [Repositorio GitHub](https://github.com/jaquimbayoc7/health-access-bridge)
- [SCRUM Board](https://github.com/users/jaquimbayoc7/projects/1)
- [Backlog](../BACKLOG.md)
- [Mockups de Diseño](../frontend/design/images/)
- [GitHub Environments](https://github.com/jaquimbayoc7/health-access-bridge/settings/environments)
- [Historial de Deployments](https://github.com/jaquimbayoc7/health-access-bridge/deployments)

---

## Documentación de Issues

- [EPICA-01 - Estructuración y Diseño](https://github.com/jaquimbayoc7/health-access-bridge/issues/11) ✅
- [HU-01 - Autenticación y Roles](https://github.com/jaquimbayoc7/health-access-bridge/issues/1) ✅
- [HU-02 - Registro y Precarga de Pacientes](https://github.com/jaquimbayoc7/health-access-bridge/issues/2) ✅
- [HU-03 - Integración Frontend-Backend](https://github.com/jaquimbayoc7/health-access-bridge/issues/3) ✅
- [HU-04 - Modelo Predictivo ML](https://github.com/jaquimbayoc7/health-access-bridge/issues/4) ✅
- [HU-05 - Modo Offline y PWA](https://github.com/jaquimbayoc7/health-access-bridge/issues/5) 📋
- [HU-06 - Pruebas de Integración](https://github.com/jaquimbayoc7/health-access-bridge/issues/6) 📋
- [HU-07 - Orquestación LLM](https://github.com/jaquimbayoc7/health-access-bridge/issues/7) 📋
- [HU-08 - Dashboard de Análisis](https://github.com/jaquimbayoc7/health-access-bridge/issues/8) 📋
- [HU-09 - Pruebas Completas](https://github.com/jaquimbayoc7/health-access-bridge/issues/9) 📋
- [HU-10 - Despliegue Final](https://github.com/jaquimbayoc7/health-access-bridge/issues/10) 📋
