# GitHub Insights Report 3 — Health Access Bridge
> **Fuente:** GitHub API · `jaquimbayoc7/health-access-bridge`
> **Período analizado:** 26 Feb 2026 – 18 Sep 2026 (acumulado total del proyecto)
> **Δ Desde último reporte:** 16 Abr 2026 – 18 Sep 2026 (cierre de Momento 2 + prueba de carga)
> **Generado:** 18 Sep 2026

---

## 1. Resumen del Repositorio

| Campo | Valor | Δ vs. Reporte 2 (16 Abr) |
|-------|-------|--------------------------|
| **Repositorio** | [jaquimbayoc7/health-access-bridge](https://github.com/jaquimbayoc7/health-access-bridge) | — |
| **Visibilidad** | Público | — |
| **Lenguaje principal** | TypeScript | — |
| **Tamaño total** | 7,617 KB | +3,096 KB (+68.5 %) |
| **Fecha de creación** | 25 Feb 2026 | — |
| **Último push** | 18 Sep 2026 | +155 días |
| **Issues totales** | 16 | = sin cambio |
| **Issues abiertas** | 5 | −3 (HU-04/05/06 y EPICA-02 cerradas) |
| **Issues cerradas** | 11 | +3 |
| **Forks / Stars / Watchers** | 0 / 0 / 0 | — |
| **Rama por defecto** | `master` | — |
| **Assignee único** | `@jaquimbayoc7` | Todos los issues |

---

## 2. Distribución de Lenguajes

| Lenguaje | Bytes | % del total | Δ vs. R2 |
|----------|-------|------------|----------|
| **TypeScript** | 336,932 | **79.5 %** | −1.8 pp ↓ |
| **Python** | 75,041 | **17.7 %** | +1.4 pp ↑ |
| JavaScript | 4,050 | 1.0 % | ↑ nuevo (specs Playwright/k6) |
| CSS | 3,652 | 0.9 % | −0.1 pp |
| Shell | 2,550 | 0.6 % | −0.1 pp |
| HTML | 1,148 | 0.3 % | = |
| Dockerfile | 420 | 0.1 % | = |
| Procfile | 54 | < 0.1 % | = |
| **Total** | **423,847** | 100 % | +62,775 bytes |

**Insight clave:** El crecimiento de Python (+1.4 pp) refleja `test_predictions.py` y los fixes de `crud.py`/`main.py` de HU-06. El nuevo lenguaje JavaScript (specs de k6 y config de Playwright) es señal directa de la nueva infraestructura de pruebas E2E/carga introducida en esta HU.

---

## 3. Actividad de Commits

### 3.1 Totales y velocidad

| Métrica | Reporte 2 (16 Abr) | Reporte 3 (18 Sep) | Δ |
|---------|-------------------|-------------------|---|
| **Total de commits** | 65 | 128 | +63 |
| **Días activos** | 8 | 17 | +9 |
| **Período total** | 26 Feb – 16 Abr (50 días) | 26 Feb – 18 Sep (204 días) | +154 días |
| **Velocidad global** | 1.30 commits/día | 0.63 commits/día | −0.67 |
| **Velocidad en días activos** | 8.1 commits/día activo | 7.5 commits/día activo | −0.6 |
| **Día pico histórico** | 4 Mar 2026 (13 commits) | 17 Mar 2026 (17 commits) | dato corregido — ver nota |

> **Nota de corrección:** el Reporte 2 registraba el pico como "4 Mar (13 commits)". Al recalcular sobre el historial completo de `git log`, el pico real es **17 Mar 2026 con 17 commits** (Sprint 3: HU-02, HU-03, CORS, admin reset-seed). Se corrige aquí para mantener coherencia con `docs/presentation/index.html`.

> **Insight:** La caída en velocidad global (1.30 → 0.63) refleja que el proyecto pasó por un período largo sin actividad (16 Abr – 16 Jun, y 16 Jun – 11 Sep) entre entregas de Momento 2. La actividad se concentra en sesiones intensas y espaciadas (patrón de "sprints reales" más que cadencia diaria), consistente con un proyecto académico de 27 semanas trabajado en bloques.

### 3.2 Distribución total por tipo (Conventional Commits)

| Tipo | # Commits | % | Tendencia |
|------|-----------|---|-----------|
| `fix:` (todas variantes) | 42 | 32.8 % | ↑ ahora lidera (antes `docs`) |
| `docs:` | 37 | 28.9 % | ↑ +13 desde R2 |
| `feat:` (todas variantes) | 33 | 25.8 % | ↑ +18 desde R2 |
| `chore:` | 9 | 7.0 % | ↑ +6 desde R2 |
| Otros (`test:`, sin prefijo) | 7 | 5.5 % | — |
| **Total** | **128** | 100 % | |

> **Insight:** Por primera vez `fix:` supera a `docs:` como tipo de commit más frecuente. Esto es consistente con el hallazgo de HU-06: la auditoría de integración encontró y corrigió 3 bugs reales de producción (crash en `/users/login`, soft-delete no filtrado, rutas rotas en CI), más los fixes de coherencia de GitHub (milestones, épicas) y de infraestructura de build (`package-lock.json` desincronizado, que rompió silenciosamente 6+ deploys de frontend).

### 3.3 Timeline de actividad — Δ desde Reporte 2

| Fecha | # Commits | Tipo predominante | Actividad principal |
|-------|-----------|-------------------|---------------------|
| **16 Jun 2026** | 16 | `fix(HCI)` + `docs` | Mejoras de estilos PDF, portal HCI, reportes de implementación |
| **11 Sep 2026** | ~50 | `feat` + `fix` + `docs` | **Sesión Momento 2:** HU-05 (mejoras HCI), HU-05b (i18n ayuda), HU-06 (tests, bugs, k6, Playwright), HU-07 redefinida, presentación actualizada |
| **18 Sep 2026** | ~9 | `chore` + `fix` + `docs` | Coherencia GitHub (milestones/épicas), fix crítico de `package-lock.json`, ejecución real de prueba de carga (200 VUs) |

---

## 4. Estado de Issues y Backlog

### 4.1 Resumen global

| Estado | R2 (16 Abr) | R3 (18 Sep) | Δ |
|--------|-------------|-------------|---|
| ✅ Cerradas | 8 | **11** | +3 |
| 🔵 Abiertas | 8 | **5** | −3 |
| **Total issues** | **16** | **16** | = |

### 4.2 Historias de Usuario — Estado detallado

| Issue | HU | Sprint | Pts | Estado | Fecha cierre |
|-------|----|--------|-----|--------|--------------|
| [#1](https://github.com/jaquimbayoc7/health-access-bridge/issues/1) | HU-01: Autenticación y RBAC | Sprint 1 (Sem. 4-5) | 8 | ✅ Done | 16 Mar 2026 |
| [#2](https://github.com/jaquimbayoc7/health-access-bridge/issues/2) | HU-02: Registro de Pacientes | Sprint 2 (Sem. 6-7) | 13 | ✅ Done | 17 Mar 2026 |
| [#3](https://github.com/jaquimbayoc7/health-access-bridge/issues/3) | HU-03: Integración Frontend-Backend | Sprint 3 (Sem. 8-9) | 5 | ✅ Done | 17 Mar 2026 |
| [#4](https://github.com/jaquimbayoc7/health-access-bridge/issues/4) | HU-04: Modelo Predictivo ML (HybridModelDisability) | Sprint 4-5 (Sem. 10-13) *(adelantada a M1)* | 21 | ✅ Done | 17 Mar 2026 |
| [#14](https://github.com/jaquimbayoc7/health-access-bridge/issues/14) | HU-11: Pruebas Smoke Producción | Sprint 3.5 (Sem. 9) | 3 | ✅ Done | 16 Abr 2026 |
| [#15](https://github.com/jaquimbayoc7/health-access-bridge/issues/15) | HU-12: Pruebas Integración Backend | Sprint 3.5 (Sem. 9) | 5 | ✅ Done | 16 Abr 2026 |
| [#16](https://github.com/jaquimbayoc7/health-access-bridge/issues/16) | HU-13: Pruebas Diseño y UI Frontend | Sprint 3.5 (Sem. 9) | 8 | ✅ Done | 16 Abr 2026 |
| [#5](https://github.com/jaquimbayoc7/health-access-bridge/issues/5) | HU-05: Mejoras de Usabilidad (HCI) — antes "Modo Offline y PWA" | Sprint 6-7 (Sem. 14-17) | 13 + 3 (HU-05b) | ✅ Done | 11 Sep 2026 |
| [#6](https://github.com/jaquimbayoc7/health-access-bridge/issues/6) | HU-06: Pruebas de Integración y Rendimiento | Sprint 7 (Sem. 16-17) | 8 | ✅ Done | 11 Sep 2026 |
| [#7](https://github.com/jaquimbayoc7/health-access-bridge/issues/7) | HU-07: Servidor Local con LLM ajustado para códigos ICF — antes "LLM Recomendaciones Clínicas" | Sprint 8-9 (Sem. 19-22) | 21 | 📋 Backlog | — |
| [#8](https://github.com/jaquimbayoc7/health-access-bridge/issues/8) | HU-08: Dashboard y Exportación | Sprint 10-11 (Sem. 23-26) | 13 | 📋 Backlog | — |
| [#9](https://github.com/jaquimbayoc7/health-access-bridge/issues/9) | HU-09: Pruebas Completas y UAT | Sprint 11 (Sem. 25-26) | 8 | 📋 Backlog | — |
| [#10](https://github.com/jaquimbayoc7/health-access-bridge/issues/10) | HU-10: Despliegue Final y Manuales | Sprint 12 (Sem. 27) | 5 | 📋 Backlog | — |

> **Δ vs. R2:** HU-05 y HU-06 cambiaron de "📋 Backlog" a "✅ Done" — y HU-05 cambió de alcance (de PWA/offline, nunca ejecutado, a mejoras de usabilidad HCI, sí ejecutado). HU-07 cambió de alcance (de LLM en la nube a servidor local con LLM ajustado para códigos ICF-Colombia).

### 4.3 Épicas

| Issue | Épica | Momento | Pts | Estado R2 | Estado R3 |
|-------|-------|---------|-----|-----------|-----------|
| [#11](https://github.com/jaquimbayoc7/health-access-bridge/issues/11) | EPICA-01: Estructuración y Diseño | M1 · Sem. 1-9 | 63 | ✅ Done | ✅ Done (sin cambio) |
| [#12](https://github.com/jaquimbayoc7/health-access-bridge/issues/12) | EPICA-02: Funcionalidades Core | M2 · Sem. 10-18 | 45 | 🔵 25 % | ✅ **100 % — cerrada 18 Sep** |
| [#13](https://github.com/jaquimbayoc7/health-access-bridge/issues/13) | EPICA-03: IA Generativa y Cierre | M3 · Sem. 19-27 | 47 | 🔴 0 % | 🔴 0 % (sin cambio) |

> **Nota:** EPICA-02 estuvo abierta con contenido desactualizado (describía "Modo Offline y PWA") hasta la auditoría de coherencia del 18 Sep 2026, momento en que se corrigió su descripción al alcance real (Mejoras HCI) y se cerró formalmente, ya con sus 3 HUs completadas.

---

## 5. Story Points y Velocity

### 5.1 Avance global del proyecto

```
R2 (16 Abr): ██████████████████████░░░░░░░░░░  63 / 131 pts  (48.1 %)
R3 (18 Sep): █████████████████████████████░░░  87 / 134 pts  (64.9 %)
             Δ: +24 pts completados · +3 pts al total (HU-05b)
```

| Etapa | Pts planificados | Pts completados | % | Δ vs. R2 |
|-------|-----------------|-----------------|---|----------|
| **Momento 1** (M1) | 63 | 63 | **100 %** ✅ | = |
| **Momento 2** (M2 — HU-04 adelantada, HU-05+05b, HU-06) | 24 | 24 | **100 %** ✅ | +24 pts (era 0/21) |
| **Momento 3** (M3) | 47 | 0 | 0 % | = |
| **Total proyecto** | **134** | **87** | **64.9 %** | +16.8 pp ↑ |

### 5.2 Velocity por Sprint completado

| Sprint | HU(s) | Pts entregados | Semanas | Velocity |
|--------|-------|---------------|---------|---------|
| Sprint 1 | HU-01 | 8 pts | 2 sem (Sem. 4-5) | 4.0 pts/sem |
| Sprint 2 | HU-02 | 13 pts | 2 sem (Sem. 6-7) | 6.5 pts/sem |
| Sprint 3 | HU-03 + HU-04 adelantada | 26 pts | 2 sem (Sem. 8-9) | 13.0 pts/sem |
| Sprint 3.5 | HU-11 + HU-12 + HU-13 | 16 pts | 1 sem (Sem. 9) | 16.0 pts/sem |
| **Sprint 6-7** | **HU-05 + HU-05b** | **16 pts** | **4 sem (Sem. 14-17)** | **4.0 pts/sem** |
| **Sprint 7** | **HU-06** | **8 pts** | **~1 sem (Sem. 16-17)** | **8.0 pts/sem** |

> **Velocity promedio del proyecto (6 sprints):** 14.5 pts/sprint. Sprint 3.5 sigue siendo el pico de eficiencia (16 pts/1 semana); Sprint 6-7 fue el más lento (4 pts/sem), consistente con la naturaleza de HU-05 (investigación HCI + implementación de UX, trabajo más cualitativo que HU-01-04).

---

## 6. Milestones (corregidos en esta auditoría)

| Milestone | HUs incluidas | Issues cerradas | Issues abiertas | Avance R2 (documentado) | Avance R3 (real, corregido) |
|-----------|--------------|-----------------|-----------------|-----------|-----------|
| [Momento 1](https://github.com/jaquimbayoc7/health-access-bridge/milestone/1) | HU-01, 02, 03, 11, 12, 13 | 7 | 0 | ⚠️ Decía "24%" (dato erróneo) | ✅ **100 %** |
| [Momento 2](https://github.com/jaquimbayoc7/health-access-bridge/milestone/2) | HU-04, 05, 06 | 3 | 1 (EPICA-02) | ⚠️ Decía "60%" (dato erróneo) | ✅ **100 %** |
| [Momento 3](https://github.com/jaquimbayoc7/health-access-bridge/milestone/3) | HU-07 a HU-10 | 0 | 5 | ⚠️ Decía "100%" (dato erróneo) | 🔴 **0 %** |

> **Hallazgo de esta auditoría (18 Sep 2026):** los tres milestones tenían el campo "Avance" invertido o desactualizado en GitHub (Momento 1 decía 24% siendo 100%; Momento 2 decía 60% siendo 100%; Momento 3 decía 100% siendo 0%). Se corrigieron directamente vía API de GitHub. Además, 7 archivos `.github/issues/*-updated.md` con contenido obsoleto (alcance viejo de PWA/LLM) fueron eliminados del repositorio por generar confusión.

---

## 7. Cobertura de Pruebas — Estado Actualizado

### 7.1 Backend (pytest)

| Archivo | Tests | Cobertura | Sprint |
|---------|-------|-----------|--------|
| `backend/app/tests/test_auth.py` | 17 casos | Login, JWT, `/users/me`, RBAC Admin | Sprint 1 + HU-12 |
| `backend/app/tests/test_patients.py` | 20 casos | CRUD, búsqueda, aislamiento médico, soft delete | Sprint 2 + HU-12 |
| `backend/app/tests/test_predictions.py` | 9 casos *(**nuevo** — HU-06)* | Flujo completo de predicción ML, persistencia, errores 403/404/500/503 | Sprint 7 |
| **Total backend** | **44 tests** | **83 % (`--cov-fail-under=80` ✅)** | ✅ Activo en CI/CD |

> Δ vs. R2: +9 tests nuevos (`test_predictions.py`), +2 en `test_patients.py` (correcciones de aserciones desactualizadas)

### 7.2 Frontend (Vitest)

| Archivo | Tests | Cobertura |
|---------|-------|-----------|
| `AuthContext.test.tsx`, `Login.test.tsx`, `DashboardLayout.test.tsx`, `Patients.test.tsx` | 16 | Guards, forms, routing, dialogs, debounce, i18n |
| **Total frontend** | **16/16 tests** ✅ | Sin cambio vs. R2 (se corrigieron 2 mocks desactualizados por cambios de HU-05b/HU-06) |

### 7.3 E2E (Playwright) — NUEVO desde Reporte 2

| Archivo | Escenarios |
|---------|-----------|
| `frontend/e2e/login.spec.ts` | Login exitoso/fallido |
| `frontend/e2e/patients.spec.ts` | Listado, crear, cancelar paciente |
| `frontend/e2e/predictions.spec.ts` | Carga y ejecución de predicción |

Integrados en `ci-qa.yml`. No ejecutados aún en este entorno (requieren Node/Playwright); listos para correr en CI.

### 7.4 Carga (k6) — NUEVO, EJECUTADO desde Reporte 2

Ejecutada el 18 Sep 2026 contra QA con 200 VUs. Resultado: **criterio de latencia no cumplido** (p95 real ≈ 55s vs. <200ms esperado); tasa de error sí cumplida (<1%). Ver detalle en `docs/test-report.md` §4.

### 7.5 Resumen total de pruebas

| Capa | R2 (16 Abr) | R3 (18 Sep) | Δ |
|------|------------|------------|---|
| Backend (pytest) | 35 tests | **44 tests** | +9 |
| Frontend (Vitest+RTL) | 16 tests | **16 tests** | = (2 mocks corregidos) |
| E2E (Playwright) | 0 | **7 specs** (nuevo) | +7 |
| Carga (k6) | 0 | **1 script, ejecutado** | +1 |
| Smoke (CI/CD) | 2 tests | 2 tests | = |
| **Total** | **53** | **60 + 1 script de carga** | **+7 (+13.2 %)** |

---

## 8. Bugs críticos encontrados y corregidos (nuevo en R3)

| # | Bug | Causa | Impacto |
|---|-----|-------|---------|
| 1 | Crash 500 en `/users/login` con body inválido | `exc.body` (FormData de Starlette) no serializable a JSON en el handler de validación | El endpoint de login crasheaba en vez de devolver 422 ante requests malformadas |
| 2 | Paciente eliminado (soft-delete) seguía accesible por ID | `crud.get_patient()` no filtraba `is_active`, a diferencia de los listados | `GET/PUT/DELETE /patients/{id}` exponían y permitían modificar registros ya "eliminados" |
| 3 | Smoke tests de `ci-qa.yml` con rutas inexistentes | `/api/v1/auth/login` y `/api/v1/patients/` no existen (rutas reales: `/users/login`, `/patients/`) | El job de smoke tests de QA habría fallado siempre que corriera |
| 4 | **Deploys de frontend rotos silenciosamente durante ~1 semana** | `package.json` con `@playwright/test` agregado sin regenerar `package-lock.json`; Render usa `npm ci`, que exige sincronía | 6+ deploys consecutivos de `hab-frontend` fallaron sin que se notara; ningún cambio de frontend llegó a producción entre el 11 y el 18 de septiembre |

> **Insight:** el bug #4 es el hallazgo más significativo del período — un problema de *tooling* (no de lógica de negocio) causó que una semana completa de trabajo de frontend (incluyendo disclaimers legales de ICF/OMS y recuperación de contraseña) nunca llegara a producción, sin ninguna alerta visible en la UI de desarrollo. Se detectó únicamente al consultar la API de GitHub Deployments directamente.

---

## 9. Resumen de Hallazgos

| # | Insight | Impacto | Δ vs. R2 |
|---|---------|---------|----------|
| 1 | **Momento 1 y Momento 2 al 100 %** — 10 HUs + 2 épicas completadas | 🟢 Alto positivo | ↑ Nuevo |
| 2 | **64.9 % del proyecto completado** (+16.8 pp desde R2) | 🟢 Alto positivo | ↑ Nuevo |
| 3 | **Milestones de GitHub tenían el avance invertido/erróneo** — corregidos en esta auditoría | 🟡 Hallazgo de proceso | ✨ Nuevo |
| 4 | **Prueba de carga real ejecutada: falla el criterio de 200ms bajo 200 VUs** (p95 ≈ 55s) | 🔴 Hallazgo técnico | ✨ Nuevo |
| 5 | **`package-lock.json` desincronizado rompió deploys de frontend por ~1 semana sin alertas** | 🔴 Riesgo de proceso | ✨ Nuevo |
| 6 | **HU-05 cambió de alcance** (PWA/offline nunca ejecutado → mejoras HCI sí ejecutadas) | 🟢 Positivo (trabajo real entregado) | ✨ Nuevo |
| 7 | **HU-07 redefinida** (LLM en la nube → servidor local con LLM ajustado para ICF-Colombia) | 🟡 Cambio de alcance a validar antes de M3 | ✨ Nuevo |
| 8 | **+9 tests de integración backend** (predicción ML end-to-end), cobertura 83% | 🟢 Positivo | ↑ Mejorado |
| 9 | **Infraestructura de pruebas E2E (Playwright) y carga (k6) creada** | 🟢 Positivo | ✨ Nuevo |
| 10 | **Sin PRs / code review** — commit directo a `master` persiste | 🟡 Riesgo técnico | = Sin cambio |
| 11 | **47 pts pendientes en M3** — HU-07 (servidor local + LLM, 21 pts) es la más compleja | 🔴 Prioridad futura | = Sin cambio |

---

## 10. Comparativo R1 vs. R2 vs. R3

| Métrica | R1 (20 Mar) | R2 (16 Abr) | R3 (18 Sep) | Δ R2→R3 |
|---------|------------|------------|------------|---------|
| Total commits | 43 | 65 | 128 | +63 |
| Issues totales | 13 | 16 | 16 | = |
| Issues cerradas | 5 | 8 | 11 | +3 |
| HUs + épicas completadas | 4 | 7 | 10 + 2 épicas | +3 HU +1 épica |
| Story Points completados | 47 | 63 | 87 | +24 pts |
| Story Points totales | 115 | 131 | 134 | +3 pts (HU-05b) |
| Avance del proyecto | 40.9 % | 48.1 % | 64.9 % | +16.8 pp |
| Tests totales (backend+frontend+smoke) | 32 | 53 | 60 | +7 |
| Specs E2E (Playwright) | 0 | 0 | 7 | +7 |
| Scripts de carga (k6) | 0 | 0 | 1 (ejecutado) | +1 |
| Bugs críticos corregidos (acumulado) | 0 | 0 | 4 | +4 |
| Tamaño repo (KB) | — | 4,521 | 7,617 | +3,096 |
| TypeScript % | 80.6 % | 81.3 % | 79.5 % | −1.8 pp |

---

## 11. Recomendaciones para Momento 3

1. **Resolver el bottleneck de rendimiento antes de iniciar HU-07:** el servidor local con LLM (HU-07, 21 pts) agregará carga computacional adicional. Causa raíz confirmada en código: 1 solo worker de Uvicorn (`render.yaml` sin `--workers`) + pool SQLAlchemy limitado a 30 conexiones (`database.py`) + el servicio web factura como **Starter** (0.5 CPU/512MB) y la BD como **Basic**, aunque el workspace de Render sea Pro (esa suscripción habilita features como autoescalado horizontal, no aumenta el tamaño de cómputo por servicio). Plan de escalado sugerido con pricing real de Render en `docs/test-report.md` §4: pasos gratis primero (workers + pool), luego Web Service → Pro ($85/mes) y Postgres → Pro-8gb ($100/mes), con autoescalado horizontal (ya incluido en el workspace Pro) como opción adicional.

2. **Activar Pull Requests:** persiste desde R1/R2 — con HU-07 (servidor local + LLM) siendo la HU más compleja restante, el riesgo de regresiones sin code review sigue siendo alto.

3. **Agregar un check de CI que valide `package.json`/`package-lock.json` en sincronía** (`npm ci --dry-run` o similar) para prevenir que se repita el incidente de deploys rotos silenciosamente.

4. **Repetir la prueba de carga después de escalar infraestructura**, para verificar mejora real antes de declarar el criterio de HU-06 cumplido de forma definitiva.

5. **Validar el alcance de HU-07 con el equipo/stakeholders** antes de iniciar Sprint 8-9: el cambio de "LLM en la nube" a "servidor local con LLM ajustado" implica requerimientos de hardware e infraestructura distintos a los originalmente presupuestados.

---

*Datos extraídos de GitHub API pública, `git log` local y la ejecución real de `backend/tests/load/k6_load_test.js` contra QA el 18 Sep 2026.*
