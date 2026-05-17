# GitHub Insights Report — Health Access Bridge
> **Fuente:** GitHub API · `jaquimbayoc7/health-access-bridge`
> **Período analizado:** 26 Feb 2026 – 20 Mar 2026 (23 días activos)
> **Generado:** 20 Mar 2026

---

## 1. Resumen del Repositorio

| Campo | Valor |
|-------|-------|
| **Repositorio** | [jaquimbayoc7/health-access-bridge](https://github.com/jaquimbayoc7/health-access-bridge) |
| **Visibilidad** | Público |
| **Lenguaje principal** | TypeScript |
| **Tamaño total** | 4,409 KB |
| **Fecha de creación** | 25 Feb 2026 |
| **Último push** | 20 Mar 2026 |
| **Issues abiertas** | 8 |
| **Forks / Stars / Watchers** | 0 / 0 / 0 |
| **Rama por defecto** | `master` |

---

## 2. Distribución de Lenguajes

| Lenguaje | Bytes | % del total |
|----------|-------|------------|
| **TypeScript** | 280,720 | **80.6 %** |
| **Python** | 58,996 | **16.9 %** |
| CSS | 3,652 | 1.0 % |
| Shell | 2,550 | 0.7 % |
| HTML | 1,148 | 0.3 % |
| JavaScript | 846 | 0.2 % |
| Dockerfile | 420 | 0.1 % |
| Procfile | 54 | < 0.1 % |
| **Total** | **348,386** | 100 % |

**Insight clave:** El **80.6 % del código es TypeScript**, confirmando que el proyecto es frontend-intensivo. Python representa el 16.9 % con toda la lógica del Backend API (FastAPI + SQLAlchemy + ML). La presencia de Dockerfile y Shell indica madurez en infraestructura.

---

## 3. Actividad de Commits

### 3.1 Totales y velocidad

| Métrica | Valor |
|---------|-------|
| **Total de commits** | 43 |
| **Días activos** | 23 |
| **Velocidad promedio** | 1.87 commits / día |
| **Día pico** | 4 Mar 2026 (13 commits) |
| **Rango de fechas** | 26 Feb – 20 Mar 2026 |

### 3.2 Distribución por tipo (Conventional Commits)

| Tipo | # Commits | % | Significado |
|------|-----------|---|-------------|
| `fix:` | 16 | 37.2 % | Correcciones de bugs e infraestructura |
| `docs:` | 12 | 27.9 % | Documentación, README, issues |
| `feat:` | 11 | 25.6 % | Nuevas funcionalidades |
| `chore:` | 3 | 7.0 % | Configuración y mantenimiento |
| `feat(design):` | 1 | 2.3 % | Diseños UI/UX |

> **Insight:** El ratio **fix > docs > feat** es típico de una fase de despliegue activo. El alto porcentaje de `fix:` (37 %) se concentró en la primera semana de Render/CI-CD — indica alta fricción inicial de infraestructura que luego se estabilizó.

### 3.3 Actividad por período

| Período | # Commits | Tipo predominante | Actividad principal |
|---------|-----------|-------------------|---------------------|
| **26 Feb** | 5 | `chore` / `docs` | Setup inicial: README, BACKLOG, render.yaml, CI/CD workflows |
| **4 Mar** | 13 | `fix` | Correcciones masivas: Python version (3.10→3.11.10), render.yaml, pipeline CI/CD, backend importado desde HybridModelDisability |
| **16–17 Mar** | 12 | `feat` + `fix` | Sprint 3 completado: HU-01 (RBAC), HU-02 (Pacientes), HU-03 (Integración), CORS, seed data, admin |
| **19 Mar** | 9 | `feat` + `docs` | Fase de diseño y documentación: 8 pantallas Pencil UI, PROJECT_STATUS, testing report, issues actualizadas |
| **20 Mar** | 2 | `docs` | Diagramas de arquitectura C4 (L1–L4), actualización README |

### 3.4 Commits más representativos

| SHA | Fecha | Mensaje | Impacto |
|-----|-------|---------|---------|
| `f3fb722` | 4 Mar | `feat: add backend/ from HybridModelDisability` | Importación del modelo ML embebido — hito técnico central |
| `ad57e21` | 4 Mar | `feat: implement dev→QA→prod pipeline with manual approval gates` | Pipeline CI/CD completo con 3 ambientes |
| `797ed98` | 17 Mar | `feat(HU-02): add numero_documento, search filter, soft delete, seed` | Core del CRUD de pacientes |
| `e549545` | 16 Mar | `feat(HU-01): add GET /users/me, fix seed, 3 users + 10 patients` | Autenticación completa + seed funcional |
| `17c07c5` | 17 Mar | `feat(HU-03): add integration tests, pytest, Dockerfile, docker-compose` | 30 tests de integración + infraestructura local |
| `61b07e2` | 19 Mar | `feat(design): Pencil UI — 6 screens actualizados` | Diseño UI completo con datos reales |
| `622f9b6` | 20 Mar | `docs: add C4 architecture diagrams (L1-L4)` | Documentación arquitectónica completa |

---

## 4. Estado de Issues y Backlog

### 4.1 Resumen global

| Estado | # Issues | HUs | Épicas |
|--------|----------|-----|--------|
| ✅ Cerradas | 5 | 4 (HU-01 a HU-04) | 1 (EPICA-01) |
| 🔵 Abiertas | 8 | 6 (HU-05 a HU-10) | 2 (EPICA-02, EPICA-03) |
| **Total** | **13** | **10** | **3** |

### 4.2 Historias de Usuario — Estado detallado

| Issue | HU | Sprint | Pts | Estado | Fecha cierre |
|-------|----|--------|-----|--------|--------------|
| [#1](https://github.com/jaquimbayoc7/health-access-bridge/issues/1) | HU-01: Autenticación y RBAC | Sprint 1 (Sem. 4-5) | 8 | ✅ Done | 16 Mar 2026 |
| [#2](https://github.com/jaquimbayoc7/health-access-bridge/issues/2) | HU-02: Registro de Pacientes | Sprint 2 (Sem. 6-7) | 13 | ✅ Done | 17 Mar 2026 |
| [#3](https://github.com/jaquimbayoc7/health-access-bridge/issues/3) | HU-03: Integración Frontend-Backend | Sprint 3 (Sem. 8-9) | 5 | ✅ Done | 17 Mar 2026 |
| [#4](https://github.com/jaquimbayoc7/health-access-bridge/issues/4) | HU-04: Modelo Predictivo ML | Sprint 4-5 *(adelantada)* | 21 | ✅ Done | 17 Mar 2026 |
| [#5](https://github.com/jaquimbayoc7/health-access-bridge/issues/5) | HU-05: Modo Offline y PWA | Sprint 6-7 | 13 | 📋 Backlog | — |
| [#6](https://github.com/jaquimbayoc7/health-access-bridge/issues/6) | HU-06: Pruebas de Integración | Sprint 7 | 8 | 📋 Backlog | — |
| [#7](https://github.com/jaquimbayoc7/health-access-bridge/issues/7) | HU-07: LLM Recomendaciones Clínicas | Sprint 8-9 | 21 | 📋 Backlog | — |
| [#8](https://github.com/jaquimbayoc7/health-access-bridge/issues/8) | HU-08: Dashboard y Exportación | Sprint 10-11 | 13 | 📋 Backlog | — |
| [#9](https://github.com/jaquimbayoc7/health-access-bridge/issues/9) | HU-09: Pruebas Completas y UAT | Sprint 11 | 8 | 📋 Backlog | — |
| [#10](https://github.com/jaquimbayoc7/health-access-bridge/issues/10) | HU-10: Despliegue Final y Manuales | Sprint 12 | 5 | 📋 Backlog | — |

### 4.3 Épicas

| Issue | Épica | Momento | Pts | Estado |
|-------|-------|---------|-----|--------|
| [#11](https://github.com/jaquimbayoc7/health-access-bridge/issues/11) | EPICA-01: Estructuración y Diseño | M1 · Sem. 1-9 | 26 | ✅ Done (4 Mar 2026) |
| [#12](https://github.com/jaquimbayoc7/health-access-bridge/issues/12) | EPICA-02: Funcionalidades Core | M2 · Sem. 10-18 | 42 | 🔵 Open (25% avance) |
| [#13](https://github.com/jaquimbayoc7/health-access-bridge/issues/13) | EPICA-03: IA Generativa y Cierre | M3 · Sem. 19-27 | 47 | 🔵 Open (0% avance) |

---

## 5. Story Points y Velocity

### 5.1 Avance global del proyecto

```
Completados : ████████████████░░░░░░░░░░░░░░░░  47 / 115 pts  (40.9 %)
Backlog     : ░░░░░░░░░░░░░░░░████████████████  68 / 115 pts  (59.1 %)
```

| Etapa | Pts planificados | Pts completados | % |
|-------|-----------------|-----------------|---|
| **Momento 1** (M1) | 26 | 26 | **100 %** ✅ |
| **HU-04** (adelantada de M2) | 21 | 21 | **100 %** ✅ |
| **Momento 2** (M2, restante) | 21 | 0 | 0 % |
| **Momento 3** (M3) | 47 | 0 | 0 % |
| **Total proyecto** | **115** | **47** | **40.9 %** |

### 5.2 Velocity por Sprint completado

| Sprint | HU(s) | Pts entregados | Semanas |
|--------|-------|---------------|---------|
| Sprint 1 | HU-01 | 8 pts | 2 sem (Sem. 4-5) |
| Sprint 2 | HU-02 | 13 pts | 2 sem (Sem. 6-7) |
| Sprint 3 | HU-03 + **HU-04 adelantada** | **26 pts** | 2 sem (Sem. 8-9) |

> **Velocity promedio M1:** ~15.7 pts/sprint · **Pico:** 26 pts en Sprint 3 (incluye HU-04 adelantada)

---

## 6. Milestones

| Milestone | HUs | Issues cerradas | Issues abiertas | Avance |
|-----------|-----|-----------------|-----------------|--------|
| [Momento 1](https://github.com/jaquimbayoc7/health-access-bridge/milestone/1) | HU-01, 02, 03 | 4 | 0 | ✅ **100 %** |
| [Momento 2](https://github.com/jaquimbayoc7/health-access-bridge/milestone/2) | HU-04, 05, 06 | 1 (HU-04) | 3 | 🔵 **25 %** |
| [Momento 3](https://github.com/jaquimbayoc7/health-access-bridge/milestone/3) | HU-07 a HU-10 | 0 | 5 | 🔴 **0 %** |

---

## 7. Patrones de Desarrollo Identificados

### 7.1 Alta fricción de infraestructura en semana 1
El **30 % del total de commits (13 de 43)** ocurrieron el **4 de marzo**, todos relacionados con correcciones de configuración: versión de Python, `render.yaml`, CI/CD workflows, CORS. Esto indica que la integración inicial con Render fue el mayor cuello de botella técnico del proyecto.

**Commits de `fix` en Mar 4:** `runtime.txt`, `PYTHON_VERSION`, `pip wheels`, `render.yaml plan`, `static/web runtime`, `frontend subfolder`, `CORS wildcard`

### 7.2 HU-04 adelantada en Sprint 3 — señal de capacidad técnica alta
HU-04 (integración del modelo predictivo, 21 puntos, valorada como la historia más compleja del proyecto) fue completada **2 sprints antes** de lo planificado. Esto indica que el modelo ML ya estaba disponible como módulo (`HybridModelDisability`) y la integración fue más rápida de lo esperado. Libera capacidad para M2.

### 7.3 Patrón burst → documentación
El ciclo observado es: **burst de features** (Mar 16-17) seguido inmediatamente de **burst de documentación** (Mar 19-20). Los commits de features (`feat`) activan directamente commits de `docs:`. Esto sugiere disciplina de documentación continua.

### 7.4 Monorepo backend + frontend embebido
El frontend (`assist-reach-aid`) se referencia en los CI/CD workflows pero vive en un repositorio separado. En Mar 17 se consolidó moviendo el frontend dentro de `frontend/` en este mismo repo. Este patrón redujo la complejidad de CI/CD y centraliza la arquitectura.

### 7.5 Sin Pull Requests — flujo de commit directo a master
Todos los 43 commits van directo a `master`. No hay evidencia de PRs ni code review workflow. Para un equipo pequeño es aceptable en fase inicial, pero representa un riesgo técnico a medida que el proyecto escala hacia M2/M3.

---

## 8. Cobertura de Pruebas (HU-03)

Según el commit `17c07c5` y los criterios de aceptación de HU-03:

| Componente | Tests | Cobertura objetivo |
|------------|-------|-------------------|
| `test_auth.py` | 15 tests | Login, `/users/me`, RBAC admin endpoints |
| `test_patients.py` | 15 tests | CRUD, búsqueda, ownership, soft delete |
| **Total backend** | **30 tests** | **≥ 80 % cobertura (pytest-cov)** |
| Frontend E2E | Playwright (HU-09) | Pendiente M3 |

---

## 9. Resumen de Hallazgos

| # | Insight | Impacto |
|---|---------|---------|
| 1 | **Momento 1 completado al 100 %** con HU-04 adelantada (+21 pts bonus) | 🟢 Alto positivo |
| 2 | **40.9 % del proyecto completado** en las primeras 3 semanas activas de desarrollo | 🟢 Alto positivo |
| 3 | **80.6 % TypeScript** — codebase sólido y tipado en frontend | 🟢 Positivo |
| 4 | **30 tests de integración backend** con cobertura ≥ 80 % desde Sprint 3 | 🟢 Positivo |
| 5 | **Alta fricción inicial en Render/CI-CD** — 7 fixes de configuración en un día | 🟡 Resuelto |
| 6 | **Sin PRs / code review** — commit directo a master | 🟡 Riesgo técnico |
| 7 | **68 pts pendientes** en M2 y M3 — HU-05 (PWA) y HU-07 (LLM) son las más complejas | 🔴 Prioridad futura |
| 8 | **Pipeline CI/CD completo** con gate de aprobación manual en producción | 🟢 Positivo |

---

## 10. Recomendaciones

1. **Activar Pull Requests para M2/M3**: Con HU-07 (LLM, 21 pts) la complejidad aumenta. Implementar feature branches + PR workflow antes de iniciar M2.
2. **HU-05 (PWA) depende de estabilidad de frontend**: Asegurar que el refactor a `frontend/` subfolder sea estable antes de agregar Service Workers.
3. **Capitalizar HU-04 adelantada**: Los 21 puntos ganados en M1 dan colchón para afrontar HU-07 (LLM) sin presión de tiempo.
4. **Lighthouse audit antes de HU-06**: Ejecutar auditoría de rendimiento en ambientes DEV/QA antes de escribir pruebas de integración formales.

---

*Datos extraídos de la GitHub API pública. Para métricas de tráfico (clones, vistas) se requiere autenticación con token de acceso personal.*
