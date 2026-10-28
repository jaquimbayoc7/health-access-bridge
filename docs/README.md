# Documentación del Proyecto — Health Access Bridge (HAB)

> **Última actualización:** 28 de octubre de 2026 · **proyecto cerrado: 146 de 146 pts (100 %)** · Momentos 1, 2 y 3 completos

**Punto de entrada:** [`presentation/index.html`](./presentation/index.html), una página por vistas (Resumen, Producto, Proceso y sprints, Calidad, IA y validación ICF, Usuarios y Documentos) con buscador de documentos.

---

## Estado, planeación y pruebas

| Documento | Descripción |
|-----------|-------------|
| [../BACKLOG.md](../BACKLOG.md) | Backlog maestro SCRUM: historias, épicas, estimaciones y estado |
| [reports/PROJECT_STATUS_M3.md](./reports/PROJECT_STATUS_M3.md) | Estado del Momento 3 (corte al 26-oct-2026) |
| [reports/PROJECT_STATUS_M2.md](./reports/PROJECT_STATUS_M2.md) · [reports/PROJECT_STATUS.md](./reports/PROJECT_STATUS.md) | Cierre de los Momentos 2 y 1 |
| [reports/RELEASE_PLAN.md](./reports/RELEASE_PLAN.md) | Plan de releases por Momento: alcance, fechas, riesgos y ambientes |
| [reports/AGILE_PRACTICES.md](./reports/AGILE_PRACTICES.md) | Roles, eventos y artefactos SCRUM con su evidencia en el repo |
| [PENDIENTES_PROXIMA_SESION.md](./PENDIENTES_PROXIMA_SESION.md) | Punto de partida, pendientes y cuidados recurrentes |
| [reports/TEST_CASES.md](./reports/TEST_CASES.md) | Casos de prueba y trazabilidad (suites 1 a 12) |
| [reports/TESTING_REPORT.md](./reports/TESTING_REPORT.md) | Reporte de pruebas: 123 backend (90,7 % de cobertura), 61 frontend, 101 del servicio ICF, 17 E2E y 7 smoke |
| [test-report.md](./test-report.md) | Reporte de HU-06: integración de ML, E2E y prueba de carga con k6 |
| [reports/INSIGHTS_REPORT5.md](./reports/INSIGHTS_REPORT5.md) | Insights R5 con adendas hasta el cierre de la validación clínica (R1 a R4 en la misma carpeta) |

## IA y perfil funcional ICF (HU-07)

| Documento | Descripción |
|-----------|-------------|
| [presentation/reporte-afinamiento-icf.html](./presentation/reporte-afinamiento-icf.html) | Reporte final del afinamiento: tres rondas de validación clínica, método, sustento de los umbrales y fuentes |
| [reports/PROTOCOLO_VALIDACION_CLINICA_HU07G.md](./reports/PROTOCOLO_VALIDACION_CLINICA_HU07G.md) | Protocolo, guía de la revisora, métricas, umbrales con su sustento científico y resultados |
| [reports/referencias_validacion_clinica.bib](./reports/referencias_validacion_clinica.bib) | Bibliografía (51 entradas) |
| [reports/PRUEBAS_HU07_SERVIDOR_FISICO.md](./reports/PRUEBAS_HU07_SERVIDOR_FISICO.md) · [reports/PRUEBAS_HU07F_MODELOS_ABIERTOS.md](./reports/PRUEBAS_HU07F_MODELOS_ABIERTOS.md) | Pruebas en el servidor físico y escalera de modelos abiertos |
| [reports/LICENCIAS_COMPONENTES_ICF.md](./reports/LICENCIAS_COMPONENTES_ICF.md) | Licencias de los componentes (Gemma 4, MedGemma, catálogo de la OMS) |
| [manuals/MANUAL_ICF.md](./manuals/MANUAL_ICF.md) | Manual del servicio ICF: arquitectura, instalación, operación, mantenimiento y fallas |
| [manuals/MANUAL_USUARIO.md](./manuals/MANUAL_USUARIO.md) · [manuals/MANUAL_TECNICO.md](./manuals/MANUAL_TECNICO.md) | Manual de usuario (con capturas) y manual técnico (también en PDF) |
| [diagrams/rag-icf-postgresql.md](./diagrams/rag-icf-postgresql.md) | Diseño del RAG sobre PostgreSQL/pgvector |
| [presentation/animaciones/](./presentation/animaciones/index.html) | Animaciones: arquitectura, servicio de IA, recorridos y proceso de validación |

---

## Documentación de API y Frontend

| Documento | Descripción |
|-----------|-------------|
| [api/redoc-api.html](./api/redoc-api.html) | **API Reference** (ReDoc): usuarios, pacientes, admin, **ICF** y **analytics**, con esquemas, ejemplos y ambientes |
| [api/frontend-docs.html](./api/frontend-docs.html) | **Frontend Docs**: rutas, contextos, servicios (incluye `icf.ts` y `analytics.ts`), páginas, dashboard de análisis y pruebas |

> Ambos son HTML estáticos: ábrelos directamente en el navegador (el de ReDoc necesita internet para cargar la librería).

---

## Diagramas de Arquitectura C4

| Archivo | Nivel C4 | Descripción |
|---------|----------|-------------|
| [diagrams/system-context-diagram.html](./diagrams/system-context-diagram.html) | L1 — System Context | Actores, sistema HAB e integraciones externas |
| [diagrams/container-diagram.html](./diagrams/container-diagram.html) | L2 — Container | Frontend SPA, Backend API, PostgreSQL, servicio ICF, CI/CD |
| [diagrams/component-diagram.html](./diagrams/component-diagram.html) | L3 — Component | Routers (incluye ICF y Analytics), Auth, RBAC, ML, ICF Client y CRUD |
| [diagrams/code-diagram.html](./diagrams/code-diagram.html) | L4 — Code (Backend) | Modelos SQLAlchemy y esquemas Pydantic v2 |
| [diagrams/code-diagram-frontend.html](./diagrams/code-diagram-frontend.html) | L4 — Code (Frontend) | Servicios TypeScript, AuthContext, páginas React |
| [diagrams/deployment-diagram.html](./diagrams/deployment-diagram.html) | Deployment | DEV / QA / PROD en Render, PC propio del servicio ICF y GitHub Actions |

---

## Diseño UI/UX y usuarios

**🎨 [Ver mockups en el repositorio](../frontend/design/images/)** — 8 pantallas: Login, Dashboard, Pacientes, Predicciones, Admin, Análisis, Guía Predictiva y Perfil Funcional ICF.

Investigación HCI: [presentation/hci_report.html](./presentation/hci_report.html) · [presentation/hci_heuristic_report.html](./presentation/hci_heuristic_report.html) · [00_portal_hci.html](./00_portal_hci.html).

---

## Documentos de planificación

| Documento | Estado |
|-----------|--------|
| **Mockups de diseño** (8 pantallas) | ✅ Completado |
| **Arquitectura C4** (6 diagramas HTML) | ✅ Completado y al día con HU-07 y HU-08 |
| **Release Plan** | ✅ [`reports/RELEASE_PLAN.md`](./reports/RELEASE_PLAN.md) |
| **Manual de operación del servicio ICF** | ✅ [`MANUAL_ICF.md`](./manuals/MANUAL_ICF.md) |
| **Manuales de usuario y técnico finales** | 📋 Pendiente (HU-10) |
| **BPM — Business Process Model** | 📋 Pendiente |

---

## Referencia de Issues

- [EPICA-01 — Estructuración y Diseño](https://github.com/jaquimbayoc7/health-access-bridge/issues/11) ✅
- [EPICA-02 — Funcionalidades Core](https://github.com/jaquimbayoc7/health-access-bridge/issues/12) ✅
- [EPICA-03 — IA Generativa, Dashboards y Cierre](https://github.com/jaquimbayoc7/health-access-bridge/issues/13) ✅ 59 de 59 pts (HU-07 a HU-10 hechas)
- [Milestone 1 — Trabajo Integrador I](https://github.com/jaquimbayoc7/health-access-bridge/milestone/1) ✅
- [Milestone 2 — Trabajo Integrador II](https://github.com/jaquimbayoc7/health-access-bridge/milestone/2) ✅
- [Milestone 3 — Trabajo Integrador III](https://github.com/jaquimbayoc7/health-access-bridge/milestone/3) 🟡
