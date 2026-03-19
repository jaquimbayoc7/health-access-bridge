## Épica 1: Estructuración y Diseño

**Momento:** Momento 1 - Trabajo Integrador I  
**Semanas:** 1-3  
**Tipo:** Épica

---

## Descripción

Fase inicial del proyecto en la que se definen todos los artefactos de arquitectura, diseño y planificación antes de comenzar el desarrollo. Esta épica es prerequisito de todos los Sprints del Momento 1.

---

## Artefactos a Entregar

- [ ] **BPM (Business Process Model):** Modelado de procesos de negocio del flujo de atención médica
- [ ] **Release Plan:** Plan de releases para las 27 semanas del proyecto
- [ ] **Arquitectura:** Diagrama de arquitectura del sistema (frontend, backend, base de datos, modelo predictivo, LLM)
- [x] **Mockups de Diseño:** Prototipos de alta fidelidad de las pantallas principales
  - Ver mockups en: [`frontend/design/images/`](../../frontend/design/images/)
  - Pantallas: Login, Dashboard, Pacientes, Predicciones, Admin Panel, Análisis, Guía Predictiva, Perfil Funcional ICF

---

## Criterios de Aceptación

- [ ] BPM aprobado por el equipo y docente
- [ ] Release Plan publicado en el repositorio
- [ ] Diagrama de arquitectura documenta stack completo (FastAPI + React + PostgreSQL + HybridModelDisability + LLM)
- [x] Mockups de diseño cubren flujos de Admin y Médico (8 pantallas completadas)

---

## Issues dependientes

Los siguientes Sprints dependen de esta épica:
- #1 - HU-01: Sistema de Autenticación y Roles (RBAC)
- #2 - HU-02: Registro y Precarga de Datos de Pacientes
- #3 - HU-03: Integración Frontend-Backend y Despliegue Local

---

## Definition of Done (DoD)

- [ ] Todos los artefactos documentados y en el repositorio (`/docs/`)
- [ ] Prototipo Figma con enlace compartido en el README
- [ ] Revisión y aprobación del equipo

---

## Rama Git

`docs/epica-01-design`
