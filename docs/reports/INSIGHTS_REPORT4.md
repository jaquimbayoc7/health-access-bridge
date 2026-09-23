# GitHub Insights Report 4 — Health Access Bridge
> **Fuente:** GitHub API · `jaquimbayoc7/health-access-bridge`
> **Período analizado:** 26 Feb 2026 – 23 Sep 2026 (acumulado total del proyecto)
> **Δ Desde último reporte:** 18 Sep 2026 – 23 Sep 2026 (cierre de deuda técnica de rendimiento + proceso)
> **Generado:** 23 Sep 2026

---

## 1. Resumen del Repositorio

| Campo | Valor | Δ vs. Reporte 3 (18 Sep) |
|-------|-------|--------------------------|
| **Repositorio** | [jaquimbayoc7/health-access-bridge](https://github.com/jaquimbayoc7/health-access-bridge) | — |
| **Visibilidad** | Público | — |
| **Lenguaje principal** | TypeScript | — |
| **Tamaño total** | 7,759 KB | +142 KB |
| **Fecha de creación** | 25 Feb 2026 | — |
| **Último push** | 23 Sep 2026 | +5 días |
| **Issues totales** (incl. PRs) | 19 | +3 (#17, #18, #19) |
| **Issues abiertas** | 5 | = sin cambio (HU-07, 08, 09, 10, EPICA-03) |
| **Issues cerradas** | 14 | +3 |
| **Forks / Stars / Watchers** | 0 / 0 / 0 | — |
| **Rama por defecto** | `master` | — |
| **Ramas activas** | `master`, `develop`, `staging` — **las 3 sincronizadas al mismo commit** (ver §8) | ✨ Corregido |
| **Assignee único** | `@jaquimbayoc7` | Todos los issues |

---

## 2. Distribución de Lenguajes

| Lenguaje | Bytes | % del total | Δ vs. R3 |
|----------|-------|------------|----------|
| **TypeScript** | 337,130 | **79.4 %** | −0.1 pp |
| **Python** | 75,041 | **17.7 %** | = |
| JavaScript | 4,555 | 1.1 % | +0.1 pp (ajuste de `k6_load_test.js`) |
| CSS | 3,652 | 0.9 % | = |
| Shell | 2,550 | 0.6 % | = |
| HTML | 1,148 | 0.3 % | = |
| Dockerfile | 420 | 0.1 % | = |
| Procfile | 54 | < 0.1 % | = |
| **Total** | **424,550** | 100 % | +703 bytes |

---

## 3. Actividad de Commits

### 3.1 Totales y velocidad

| Métrica | Reporte 3 (18 Sep) | Reporte 4 (23 Sep) | Δ |
|---------|-------------------|-------------------|---|
| **Total de commits** | 128 | 146 | +18 |
| **Días activos** | 17 | 18 | +1 |
| **Período total** | 26 Feb – 18 Sep (204 días) | 26 Feb – 23 Sep (209 días) | +5 días |
| **Velocidad global** | 0.63 commits/día | 0.70 commits/día | +0.07 |

### 3.2 Distribución total por tipo (Conventional Commits)

| Tipo | # Commits | % | Δ vs. R3 |
|------|-----------|---|-----------|
| `fix:` (todas variantes) | 51 | 34.9 % | +9 |
| `docs:` | 42 | 28.8 % | +5 |
| `feat:` (todas variantes) | 37 | 25.3 % | +4 |
| `chore:` | 10 | 6.8 % | +1 |
| `ci:` | 1 | 0.7 % | ✨ nuevo tipo (esta sesión) |
| Otros (merges, sin prefijo) | 5 | 3.4 % | — |
| **Total** | **146** | 100 % | +18 |

### 3.3 Timeline de actividad — Δ desde Reporte 3

| Fecha | # Commits | Tipo predominante | Actividad principal |
|-------|-----------|-------------------|---------------------|
| **18 Sep 2026** (posterior al cierre de R3) | 11 | `docs` + `fix` | Entregable técnico M2 (rúbrica, release plan, prácticas ágiles), fix de redirección por rol, merge de PR #17 (`develop`→`master`) |
| **23 Sep 2026** (esta sesión) | 3 (+ 2 merges de PR) | `docs` + `chore` + `ci` | Prueba de carga refinada a 30 VUs (DEUDA-01), activación de flujo de PR + protección de rama (#18), check de CI de lockfile (#19), sincronización de `develop`/`staging`/`master` |

> **Insight:** el PR #17 ("Develop", merged 18-sep) fue el primer PR real del proyecto — coincide justo con el cierre de R3, que señalaba "Sin PRs / code review" como riesgo pendiente. Sin embargo, el hábito no se sostuvo inmediatamente: los primeros commits de esta sesión (documentación del hallazgo de carga) volvieron a ir directo a `master` antes de que se formalizara la protección de rama en el PR #18.

---

## 4. Estado de Issues y Backlog

### 4.1 Resumen global

| Estado | R3 (18 Sep) | R4 (23 Sep) | Δ |
|--------|-------------|-------------|---|
| ✅ Cerradas | 11 | **14** | +3 |
| 🔵 Abiertas | 5 | **5** | = |
| **Total (issues + PRs)** | **16** | **19** | +3 |

> Los 3 nuevos elementos cerrados son Pull Requests (#17 `develop→master`, #18 flujo de PR/protección de rama, #19 check de lockfile), no nuevas Historias de Usuario — el conteo de HUs/épicas no cambia respecto a R3.

### 4.2 Historias de Usuario — sin cambio de estado desde R3

Las 10 HUs + 2 épicas completadas en R3 (HU-01 a HU-06, HU-11 a HU-13, EPICA-01, EPICA-02) permanecen `✅ Done`. Las 4 HUs + 1 épica de Momento 3 (HU-07 a HU-10, EPICA-03) permanecen `📋 Backlog` — **sin avance de puntos**, pero con dos decisiones de alcance/infraestructura tomadas esta sesión que las desbloquean para el siguiente sprint (ver §6).

### 4.3 Milestones

| Milestone | Issues cerradas | Issues abiertas | Estado |
|-----------|-----------------|-----------------|--------|
| Momento 1: Trabajo Integrador I | 7 | 0 | ✅ 100 % |
| Momento 2: Trabajo Integrador II | 4 | 0 | ✅ 100 % |
| Momento 3: Trabajo Integrador III | 0 | 5 | 🔴 0 % (sin cambio — HU-07/08/09/10 + EPICA-03) |

---

## 5. Story Points y Velocity

Sin cambio respecto a R3 — **87 / 134 pts (64.9 %)**. Esta sesión no agregó ni cerró Historias de Usuario nuevas; el trabajo fue **deuda técnica y de proceso** (DEUDA-01, riesgos de CI/CD), que no suma story points de producto pero elimina bloqueos para Momento 3.

```
R3 (18 Sep): █████████████████████████████░░░  87 / 134 pts  (64.9 %)
R4 (23 Sep): █████████████████████████████░░░  87 / 134 pts  (64.9 %)  — sin cambio de alcance de producto
```

---

## 6. Deuda técnica y de proceso — cerrada esta sesión (23 Sep 2026)

Esta es la actividad central del período y el motivo de este reporte.

### 6.1 DEUDA-01 — Rendimiento de la API bajo carga: hallazgo refinado y cerrado

| | 200 VUs (18-sep) | 30 VUs (23-sep, límite real del pool) |
|---|---|---|
| `http_req_duration` p95 | 54.6 s | **17.04 s** |
| `http_req_failed` | 0.98 % | **0.00 %** |
| Iteraciones interrumpidas | 140 | **0** |

**Hallazgo nuevo:** incluso sin saturar el pool de conexiones (30 VUs = exactamente `pool_size=10 + max_overflow=20`), el sistema sigue sin cumplir `<200ms`. Esto descarta al pool como única causa raíz. El limitante dominante es la **CPU fraccional del tier Starter (0.5 CPU)** de Render, agravado por el costo computacional de `bcrypt` (12 rounds) en `POST /users/login` — que compite por esa misma CPU con todo el resto de tráfico, incluyendo `GET /health` (sin BD, p95=592ms bajo la misma carga). Detalle completo en `docs/test-report.md` §4.1.

**Decisión de negocio (23-sep-2026):** no se escalará la infraestructura de Render (Web Service ni PostgreSQL) por ahora. Se acepta el riesgo de latencia degradada bajo alta concurrencia (>30 usuarios simultáneos) como limitación conocida y documentada. Esta decisión se apoya en que **HU-07 se reorienta a un servidor local propio con Ollama** (ver 6.3), lo que reduce la urgencia de escalar la API en la nube: el cómputo pesado del LLM no correrá sobre el mismo Web Service.

**Estado:** DEUDA-01 pasa de `📋 Backlog` a **`✅ Cerrado (riesgo aceptado)`**.

### 6.2 Riesgo de proceso — "Sin PRs / code review" (señalado en R3 §9, ítem 10)

- Se activó **protección de rama** en GitHub para `develop`, `staging` y `master`: requiere Pull Request + checks de CI en verde (`Backend Tests` y `Frontend Build` del ambiente correspondiente) antes de mergear. `required_approving_review_count=0` (único desarrollador). `enforce_admins=false` (el admin puede saltarse la regla en una emergencia).
- Se agregó plantilla de PR (`.github/PULL_REQUEST_TEMPLATE.md`).
- Validado end-to-end: [PR #18](https://github.com/jaquimbayoc7/health-access-bridge/pull/18) y [PR #19](https://github.com/jaquimbayoc7/health-access-bridge/pull/19) pasaron por el flujo completo (rama → checks en verde → merge), confirmando que la protección funciona como se espera.
- Configuración reproducible vía API en `.github/scripts/branch-protection-*.json`.

### 6.3 Riesgo de proceso — `package-lock.json` desincronizado (bug #4 de HU-06, R3 §8)

- Se agregó un paso explícito **"Verificar sincronía package.json / package-lock.json"** (`npm ci --dry-run`) al inicio de `frontend-build` en `ci-dev.yml`, `ci-qa.yml` y `ci-prod.yml`, que falla rápido con un mensaje claro.
- Combinado con la protección de rama (§6.2), un desync del lockfile ya no puede llegar a `master` sin bloquear el merge — cierra el escenario que causó 6+ deploys de frontend rotos silenciosamente durante ~1 semana (hallazgo de R3).

### 6.4 Decisión de alcance — HU-07 confirmada

Se confirma que HU-07 (servidor local + LLM para códigos ICF-Colombia) se implementará con **Ollama sobre un servidor físico ya disponible** (sin compra de hardware nuevo) y un **modelo open-weight gratuito** ajustado vía RAG/fine-tuning con el estándar CIF-Colombia. Esto resuelve la recomendación abierta en R3 §11 (punto 5: "validar el alcance de HU-07 con el equipo/stakeholders antes de Sprint 8-9").

### 6.5 Hallazgo adicional — divergencia de ramas `develop`/`staging` vs. `master`

Durante la verificación del flujo de PR se detectó que `develop` y `staging` llevaban **meses sin sincronizarse con `master`** (~24,000 líneas de diferencia — prácticamente todo el trabajo desde HU-04 en adelante nunca llegó a esas ramas; todo el desarrollo real ocurría directo en `master`). Se verificó que los commits únicos de `develop`/`staging` eran duplicados de contenido (mismo cambio, distinto hash) ya presentes en `master`, y se sincronizaron las 3 ramas al mismo commit (`341c779`) sin pérdida de trabajo.

---

## 7. Cobertura de Pruebas — sin cambio desde R3

| Capa | R3 (18 Sep) | R4 (23 Sep) | Δ |
|------|------------|------------|---|
| Backend (pytest) | 44 tests, 83% cobertura | 44 tests, 83% cobertura | = |
| Frontend (Vitest+RTL) | 16 tests | 16 tests | = |
| E2E (Playwright) | 7 specs | 7 specs | = |
| Carga (k6) | 1 script (200 VUs, ejecutado) | 1 script (**ajustado a 30 VUs**, ejecutado 23-sep) | Metodología refinada |
| Smoke (CI/CD) | 2 tests | 2 tests | = |

No se agregaron pruebas nuevas esta sesión — el trabajo fue de infraestructura de CI/CD y proceso, no de cobertura funcional.

---

## 8. Estado de branch protection (nuevo en R4)

| Rama | PR requerido | Checks requeridos | Force-push | Enforce admins |
|------|:---:|---|:---:|:---:|
| `develop` | ✅ | Backend Tests (Dev), Frontend Build (Dev) | ❌ | ❌ |
| `staging` | ✅ | Backend Tests (QA), Frontend Build (QA) | ❌ | ❌ |
| `master` | ✅ | Backend Tests (Prod), Frontend Build (Prod) | ❌ | ❌ |

Las 3 ramas apuntan actualmente al mismo commit (`341c779`), eliminando la divergencia de meses descrita en §6.5.

---

## 9. Resumen de Hallazgos

| # | Insight | Impacto | Δ vs. R3 |
|---|---------|---------|----------|
| 1 | **DEUDA-01 cerrada** — causa raíz refinada (CPU/bcrypt, no solo el pool) y decisión explícita de aceptar el riesgo sin escalar infraestructura | 🟢 Desbloquea Momento 3 | ✨ Nuevo |
| 2 | **Riesgo "sin PRs/code review" resuelto** — protección de rama activa y validada en las 3 ramas | 🟢 Alto positivo | ✨ Resuelto (era riesgo abierto desde R1) |
| 3 | **Riesgo del lockfile mitigado** — check de CI dedicado + protección de rama como doble barrera | 🟢 Positivo | ✨ Resuelto |
| 4 | **`develop`/`staging` estaban desincronizadas por meses** — descubierto y corregido en esta sesión | 🟡 Hallazgo de proceso (ya corregido) | ✨ Nuevo |
| 5 | **HU-07 confirma alcance** (Ollama + servidor propio + modelo gratuito) — responde a la recomendación abierta de R3 | 🟢 Positivo, reduce riesgo de presupuesto | ✨ Resuelto |
| 6 | **Sin avance de story points de producto** — el período fue 100% deuda técnica/proceso | 🟡 Neutral (esperado, no es Momento 3 aún) | ✨ Nuevo |
| 7 | **Persiste el patrón de corrección retrospectiva de reportes** — cada Insights Report corrige datos del anterior (R2 corrigió R1, R3 corrigió milestones, R4 corrige la causa raíz de rendimiento de R3) | 🟡 Observación de proceso | = Patrón recurrente |

---

## 10. Comparativo R1 vs. R2 vs. R3 vs. R4

| Métrica | R1 (20 Mar) | R2 (16 Abr) | R3 (18 Sep) | R4 (23 Sep) | Δ R3→R4 |
|---------|------------|------------|------------|------------|---------|
| Total commits | 43 | 65 | 128 | 146 | +18 |
| Issues totales (incl. PRs) | 13 | 16 | 16 | 19 | +3 |
| Issues cerradas | 5 | 8 | 11 | 14 | +3 |
| HUs + épicas completadas | 4 | 7 | 10 + 2 épicas | 10 + 2 épicas | = |
| Story Points completados | 47 | 63 | 87 | 87 | = |
| Avance del proyecto | 40.9 % | 48.1 % | 64.9 % | 64.9 % | = |
| Tests totales (backend+frontend+smoke) | 32 | 53 | 60 | 60 | = |
| Bugs críticos corregidos (acumulado) | 0 | 0 | 4 | 4 (+1 mitigado con CI) | = |
| PRs mergeados (acumulado) | 0 | 0 | 0 | 3 (#17, #18, #19) | +3 |
| Ramas protegidas | 0 | 0 | 0 | 3 (`develop`, `staging`, `master`) | +3 |
| Tamaño repo (KB) | — | 4,521 | 7,617 | 7,759 | +142 |

---

## 11. Recomendaciones para Momento 3

1. **Iniciar HU-07 (Sprint 8-9) con el alcance ya confirmado:** Ollama sobre servidor propio + modelo open-weight gratuito, sin bloqueo de infraestructura en la nube (DEUDA-01 cerrada, decisión de no escalar tomada).
2. **Usar el flujo de PR ya activo para todo el trabajo de HU-07 en adelante:** crear rama, abrir PR, esperar checks en verde, mergear — el flujo se validó dos veces esta sesión (PR #18, #19) y las 3 ramas están sincronizadas como línea base limpia.
3. **Vigilar la latencia real una vez el servidor local del LLM esté operativo:** aunque se decidió no escalar la API en la nube, conviene confirmar que el tráfico adicional del servicio de sugerencia de códigos ICF (si se integra con el backend de Render) no reintroduce el cuello de botella de CPU documentado en §6.1.
4. **Mantener la disciplina de PR sin excepción** — el hallazgo de §6.5 (meses de divergencia entre ramas) ocurrió precisamente por la ausencia de este flujo; la protección de rama activa ahora debería prevenir que se repita.
5. **Continuar con HU-08, HU-09 y HU-10** según el orden ya definido en `BACKLOG.md`, sin deuda técnica pendiente que las bloquee.

---

*Datos extraídos de GitHub API pública (`gh api`), `git log` local, y la ejecución real de `backend/tests/load/k6_load_test.js` (30 VUs) contra QA el 23 Sep 2026.*
