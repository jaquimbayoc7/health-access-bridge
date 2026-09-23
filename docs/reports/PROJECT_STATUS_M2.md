# Estado del Proyecto Health Access Bridge — Momento Integrador II

**Última actualización:** Septiembre 2026
**Momento actual:** Momento 2 - Trabajo Integrador II (Completado) · Momento 3 sin iniciar

> Este documento complementa a [`PROJECT_STATUS.md`](./PROJECT_STATUS.md) (que documenta el cierre de Momento 1, Abril 2026). Aquí se documenta el cierre de **Momento 2**, incluyendo el resultado real de la prueba de carga de 200 usuarios concurrentes ejecutada el 18 de septiembre de 2026.

---

## Resumen Ejecutivo

El proyecto Health Access Bridge completó el **Momento 2** (Semanas 10-18) con un avance del **100%** de las 3 historias de usuario planificadas (HU-04 — adelantada desde M1 —, HU-05 y HU-06), acumulando **87 de 134 puntos** del proyecto total (**64.9%**). Durante este momento se ejecutó una auditoría de coherencia completa sobre GitHub (issues, épicas, milestones) que corrigió datos de avance erróneos y cerró la [EPICA-02](https://github.com/jaquimbayoc7/health-access-bridge/issues/12), y se ejecutó la prueba de carga de 200 usuarios concurrentes pendiente de HU-06, cuyo resultado real **no cumple** el criterio de latencia definido (p95 < 200ms), quedando documentado como hallazgo técnico para Momento 3.

---

## Estado por Épicas

### ✅ EPICA-02: Funcionalidades Core y Capacidades Avanzadas (COMPLETADA — cerrada 18 Sep 2026)

**Periodo:** Semanas 10-18
**Puntos:** 21 pts (HU-04, adelantada a M1) + 24 pts (HU-05 + HU-05b, HU-06) = **45 pts totales, 24 pts propios de M2 completados**

> **Nota de alcance:** el objetivo original de esta épica incluía "capacidades PWA para zonas rurales sin conectividad". Ese trabajo nunca se ejecutó. En su lugar, HU-05 se redefinió a **Mejoras de Usabilidad derivadas de Investigación HCI**, que sí se completó en su totalidad. Ver [HU-05 #5](https://github.com/jaquimbayoc7/health-access-bridge/issues/5) para el detalle del cambio.

---

## Estado por Historias de Usuario

### ✅ HU-04: Integración del Modelo Predictivo (HybridModelDisability)
**Sprint:** 4-5 (Semanas 10-13) | **Puntos:** 21 | **Estado:** ✅ COMPLETADO *(adelantado en Momento 1, ver `PROJECT_STATUS.md`)*

---

### ✅ HU-05: Mejoras de Usabilidad derivadas de Investigación HCI
**Sprint:** 6-7 (Semanas 14-17) | **Puntos:** 13 + 3 (HU-05b) = 16 | **Estado:** ✅ COMPLETADO — cerrado 11 Sep 2026

**Implementación (documentada en `docs/HCI/09_implementacion_hci_b.html`):**
- `ICFTooltip.tsx` (nuevo) — tooltips contextuales reutilizables D1–D6 con nombre oficial, descripción, ejemplos y escala 0–100.
- `AlertDialog` de eliminación de paciente con nombre y documento visibles (reconocimiento en lugar de recuerdo).
- Interceptor centralizado de errores HTTP (401/403/422/500) en `api.ts`, con mensajes en español.
- Toast de sesión expirada + logout automático ante 401.
- `OnboardingModal.tsx` (nuevo) — guía de 4 pasos en el primer login.
- `Help.tsx` (nuevo) — Centro de Ayuda con glosario ICF, guía de roles, perfiles de predicción y FAQ.
- `useJWTExpiry.ts` (nuevo) — alerta 5 minutos antes de que expire la sesión.
- **HU-05b:** Centro de Ayuda y tooltips ICF migrados a `LanguageContext`, ahora responden al idioma seleccionado (antes fijos en español).
- Disclaimers agregados: uno en el Centro de Ayuda (adaptación del modelo CIF/ICF de la OMS, no es aplicación oficial, apoyo a la decisión clínica) y otro en el login (recuperación de contraseña vía administrador).

**4 archivos nuevos, 8 modificados, 702 líneas insertadas, 10 tareas completadas en 3 sprints internos.**

---

### ✅ HU-06: Pruebas de Integración Backend-Frontend y Rendimiento API
**Sprint:** 7 (Semanas 16-17) | **Puntos:** 8 | **Estado:** ✅ COMPLETADO — cerrado 11 Sep 2026

**Implementación:**
- `backend/app/tests/test_predictions.py` (nuevo) — 9 pruebas de integración del flujo completo de predicción ML.
- `frontend/e2e/` (nuevo) — 7 specs E2E con Playwright: login, CRUD de pacientes, ejecución de predicción.
- `backend/tests/load/k6_load_test.js` (nuevo) — script de carga con k6.
- **4 bugs críticos** encontrados y corregidos durante la auditoría de integración (ver sección de Hallazgos abajo).
- Suite backend: **44/44 tests pasando**, cobertura 83%.

#### 🔴 Resultado real de la prueba de carga (200 usuarios concurrentes) — ejecutada 18 Sep 2026

| Métrica | Resultado | Umbral | Cumple |
|---|---|---|---|
| `http_req_duration` p95 | 54.6 s | < 200 ms | ❌ No |
| `http_req_failed` | 0.98% | < 1% | ✅ Sí |

El backend de QA (`hab-backend-qa.onrender.com`) **no soporta 200 usuarios concurrentes** dentro del umbral de latencia definido. La tasa de error se mantuvo baja — el servicio no cayó — pero la latencia se degradó severamente (p95 ≈ 55s) conforme la concurrencia subió. El servicio se recuperó a la normalidad inmediatamente después de la prueba. Ver análisis completo, causa probable y recomendaciones en [`docs/test-report.md`](../test-report.md) §4.

**Este hallazgo se documenta como ítem de backlog técnico para Momento 3, sin bloquear el cierre de HU-06** (cuyo objetivo — construir y ejecutar la suite de pruebas de integración y carga — sí se completó).

---

## Hallazgos de esta auditoría (Septiembre 2026)

### Bugs críticos corregidos

1. **Crash 500 en `/users/login`** con body inválido — `exc.body` (FormData) no serializable en el handler de validación de FastAPI.
2. **Paciente con soft-delete seguía accesible por ID** — `crud.get_patient()` no filtraba `is_active`.
3. **Smoke tests de `ci-qa.yml` con rutas inexistentes** (`/api/v1/...`) y `PLAYWRIGHT_BASE_URL` mal configurado.
4. **Deploys de frontend rotos silenciosamente ~1 semana** — `package-lock.json` desincronizado con `package.json` (dependencia de Playwright agregada sin regenerar el lock file), causando que `npm ci` fallara en Render en 6+ deploys consecutivos sin alerta visible.

### Coherencia de GitHub corregida

- **Milestones con "Avance" invertido/erróneo**: Momento 1 decía 24% (real: 100%), Momento 2 decía 60% (real: 100%), Momento 3 decía 100% (real: 0%). Corregidos vía API.
- **EPICA-02** (#12) seguía abierta y describiendo el alcance viejo de HU-05 ("Modo Offline y PWA"). Reescrita con el alcance real y cerrada.
- **EPICA-03** (#13) describía HU-07 con su alcance viejo ("Orquestación con LLM para Recomendaciones Clínicas"). Actualizada al alcance real (servidor local con LLM ajustado para códigos ICF-Colombia).
- **7 archivos obsoletos** `.github/issues/*-updated.md` (duplicados con contenido desactualizado) eliminados del repositorio.

---

## Métricas del Proyecto (post Momento 2)

| Métrica | Valor |
|---------|-------|
| **Puntos completados** | 87 pts |
| **Puntos pendientes** | 47 pts |
| **Total del proyecto** | 134 pts |
| **Avance general** | 64.9% |
| **Momento 1** | ✅ 100% (63 pts) |
| **Momento 2** | ✅ 100% (24 pts) |
| **Momento 3** | 🔴 0% (47 pts) |
| **HUs + épicas completadas** | HU-01 [#1], HU-02 [#2], HU-03 [#3], HU-04 [#4], HU-05 [#5], HU-06 [#6], HU-11 [#14], HU-12 [#15], HU-13 [#16], EPICA-01 [#11], EPICA-02 [#12] |
| **HUs en backlog (M3)** | HU-07 [#7], HU-08 [#8], HU-09 [#9], HU-10 [#10] |

[#1]: https://github.com/jaquimbayoc7/health-access-bridge/issues/1
[#2]: https://github.com/jaquimbayoc7/health-access-bridge/issues/2
[#3]: https://github.com/jaquimbayoc7/health-access-bridge/issues/3
[#4]: https://github.com/jaquimbayoc7/health-access-bridge/issues/4
[#5]: https://github.com/jaquimbayoc7/health-access-bridge/issues/5
[#6]: https://github.com/jaquimbayoc7/health-access-bridge/issues/6
[#7]: https://github.com/jaquimbayoc7/health-access-bridge/issues/7
[#8]: https://github.com/jaquimbayoc7/health-access-bridge/issues/8
[#9]: https://github.com/jaquimbayoc7/health-access-bridge/issues/9
[#10]: https://github.com/jaquimbayoc7/health-access-bridge/issues/10
[#11]: https://github.com/jaquimbayoc7/health-access-bridge/issues/11
[#12]: https://github.com/jaquimbayoc7/health-access-bridge/issues/12
[#14]: https://github.com/jaquimbayoc7/health-access-bridge/issues/14
[#15]: https://github.com/jaquimbayoc7/health-access-bridge/issues/15
[#16]: https://github.com/jaquimbayoc7/health-access-bridge/issues/16

---

## Próximos Pasos — Momento 3 (Semanas 19-27)

1. **Resolver el bottleneck de rendimiento** antes de sumar la carga del servidor local + LLM de HU-07. Causa raíz confirmada: 1 worker de Uvicorn, pool SQLAlchemy de 30 conexiones, y el servicio real facturado como Starter/Basic (el plan Pro que se paga es del **workspace**, no del tamaño de cómputo del servicio). Plan de escalado con pricing real de Render (ver `docs/test-report.md` §4 para el detalle completo):

   | Paso | Acción | Costo |
   |---|---|---|
   | 1-2 | `--workers` en Uvicorn + ajustar `pool_size`/`max_overflow` | $0 |
   | 3 | Web Service: Starter → **Pro** (2 CPU/4GB) | $85/mes |
   | 4 | Postgres: Basic → **Pro-8gb** (2 CPU, 200 conexiones) | $100/mes |
   | 5 (opcional) | Autoescalado horizontal ×2 (ya incluido en el workspace Pro que se paga) | +$85/mes |

2. **HU-07:** Alistar servidor local físico con LLM ajustado para sugerencia de códigos CIF/ICF-Colombia (redefinida — ver [HU-07 #7](https://github.com/jaquimbayoc7/health-access-bridge/issues/7)).
3. **HU-08:** Desarrollar dashboard de análisis y exportación.
4. **HU-09:** Pruebas completas y feedback de usuarios.
5. **HU-10:** Despliegue final y generación de manuales.
6. Repetir la prueba de carga de 200 usuarios después de escalar infraestructura, para verificar mejora real.

---

## Enlaces Importantes

- [Repositorio GitHub](https://github.com/jaquimbayoc7/health-access-bridge)
- [SCRUM Board](https://github.com/users/jaquimbayoc7/projects/1)
- [Backlog](../../BACKLOG.md)
- [Insight Report 3](./INSIGHTS_REPORT3.md)
- [Insight Report 4](./INSIGHTS_REPORT4.md) — cierre de DEUDA-01, flujo de PR/protección de rama, check de CI de lockfile
- [Reporte de Pruebas HU-06](../test-report.md)
- [Estado del Proyecto — Momento 1](./PROJECT_STATUS.md)
