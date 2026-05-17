# Documentación del Proyecto — Health Access Bridge (HAB)

> **Última actualización:** Marzo 2026 · Momento 1 completado (41 % del proyecto)

---

## Reportes y Estado

| Documento | Descripción | Estado |
|-----------|-------------|--------|
| [PROJECT_STATUS.md](./PROJECT_STATUS.md) | Estado detallado por HU, épica y sprint | ✅ Actualizado |
| [INSIGHTS_REPORT.md](./INSIGHTS_REPORT.md) | Reporte de GitHub Insights: commits, lenguajes, velocity, SCRUM metrics | ✅ Generado |
| [TESTING_REPORT.md](./TESTING_REPORT.md) | Reporte de pruebas: 30 tests de integración backend (pytest), cobertura | ✅ Generado |
| [../BACKLOG.md](../BACKLOG.md) | Backlog maestro SCRUM con todas las HUs y épicas | ✅ Actualizado |

---

## Documentación de API y Frontend (ReDoc)

| Documento | Descripción |
|-----------|-------------|
| [redoc-api.html](./redoc-api.html) | **API Reference** — Documentación interactiva ReDoc del backend FastAPI (OpenAPI 3.0 completo: todos los endpoints, esquemas, ejemplos, seguridad y ambientes) |
| [frontend-docs.html](./frontend-docs.html) | **Frontend Docs** — Arquitectura de la SPA React: rutas, contextos, servicios, páginas, componentes y pruebas UI |

> Ambos documentos son HTML estáticos. Ábrelos directamente en el navegador (sin servidor requerido).

---

## Diagramas de Arquitectura C4

| Archivo | Nivel C4 | Descripción |
|---------|----------|-------------|
| [system-context-diagram.html](./system-context-diagram.html) | L1 — System Context | Actores, sistema HAB e integraciones externas |
| [container-diagram.html](./container-diagram.html) | L2 — Container | Frontend SPA, Backend API, PostgreSQL, CI/CD |
| [component-diagram.html](./component-diagram.html) | L3 — Component | Routers, Auth, RBAC, ML Engine, CRUD Layer |
| [code-diagram.html](./code-diagram.html) | L4 — Code (Backend) | Modelos SQLAlchemy ORM y esquemas Pydantic v2 |
| [code-diagram-frontend.html](./code-diagram-frontend.html) | L4 — Code (Frontend) | Servicios TypeScript, AuthContext, páginas React |
| [deployment-diagram.html](./deployment-diagram.html) | Deployment | DEV / QA / PROD en Render Cloud + GitHub Actions CI/CD |

> Los diagramas son HTML interactivos. Ábrelos directamente en el navegador.

---

## Diseño UI/UX

**🎨 [Ver mockups en el repositorio](../frontend/design/images/)**

Prototipos de alta fidelidad — 8 pantallas principales:

| # | Pantalla | Archivo |
|---|----------|---------|
| 1 | Login / Landing | `bi8Au.png` |
| 2 | Dashboard | `717A2.png` |
| 3 | Pacientes | `i0uhw.png` |
| 4 | Predicciones | `YPvRD.png` |
| 5 | Admin Panel | `UpZqF.png` |
| 6 | Análisis | `HIxNY.png` |
| 7 | Guía Predictiva | `Nj6le.png` |
| 8 | Perfil Funcional ICF | `C45o8.png` |

---

## Documentos de Planificación

| Documento | Estado |
|-----------|--------|
| **Mockups de Diseño** (8 pantallas) | ✅ Completado |
| **Arquitectura C4** (6 diagramas HTML) | ✅ Completado |
| **BPM** — Business Process Model | 📋 Pendiente |
| **Release Plan** | 📋 Pendiente |

---

## Referencia de Issues

- [EPICA-01 — Estructuración y Diseño](https://github.com/jaquimbayoc7/health-access-bridge/issues/11) ✅
- [EPICA-02 — Funcionalidades Core](https://github.com/jaquimbayoc7/health-access-bridge/issues/12) 📋
- [EPICA-03 — IA Generativa y Cierre](https://github.com/jaquimbayoc7/health-access-bridge/issues/13) 📋
- [Milestone 1 — Trabajo Integrador I](https://github.com/jaquimbayoc7/health-access-bridge/milestone/1) ✅
- [Milestone 2 — Trabajo Integrador II](https://github.com/jaquimbayoc7/health-access-bridge/milestone/2) 🔵 25%
- [Milestone 3 — Trabajo Integrador III](https://github.com/jaquimbayoc7/health-access-bridge/milestone/3) 📋
