## Historia de Usuario

**Como** Desarrollador  
**Deseo** integrar las capas de la aplicación y realizar pruebas de estrés  
**Para** garantizar la estabilidad de la versión 1.0.

---

## Detalles Técnicos

| Campo | Detalle |
|-------|---------|
| **Stack** | FastAPI + React + Docker |
| **Estimación** | 5 puntos |
| **Sprint** | Sprint 3 (Semanas 8-9) |
| **Momento** | Momento 1 - Trabajo Integrador I |

---

## Dependencias

> ⚠️ Este issue **no puede comenzar** hasta que estén cerrados:
> - #1 HU-01: Sistema de Autenticación y Roles (RBAC)
> - #2 HU-02: Registro y Precarga de Datos de Pacientes

---

## Criterios de Aceptación

- [ ] El frontend consume datos reales del API (no mocks)
- [ ] Pruebas de integración pasan con >80% de cobertura
- [ ] La aplicación arranca con un solo comando (`docker-compose up`)
- [ ] Variables de entorno documentadas en `.env.example`

---

## Tareas

- [ ] Configurar cliente Axios en frontend con base URL desde env var
- [ ] Conectar Login page al endpoint `POST /api/auth/login`
- [ ] Conectar Admin panel al endpoint `POST /api/auth/register`
- [ ] Escribir pruebas de integración para endpoints de auth
- [ ] Escribir pruebas de integración para endpoints de pacientes
- [ ] Configurar `docker-compose.yml` con servicios backend + frontend + PostgreSQL
- [ ] Documentar proceso de setup en `README.md`
- [ ] Generar reporte de cobertura de pruebas

---

## Definition of Done (DoD)

- [ ] Despliegue local funcional via Docker o script de inicio
- [ ] Reporte de pruebas unitarias generado
- [ ] Cobertura >80% en rutas críticas
- [ ] Código mergeado en `main`

---

## Rama Git

`feature/hu-03-integration-v1`
