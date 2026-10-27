# Manual técnico — Health Access Bridge

**Versión:** 1.0 · 27 de octubre de 2026 · **Para:** quien instala, despliega, opera o mantiene el sistema. El servicio de IA (ICF) tiene su propio manual: [`docs/MANUAL_OPERACION_ICF.md`](../MANUAL_OPERACION_ICF.md). La referencia de endpoints está en [`docs/api/redoc-api.html`](../api/redoc-api.html) y los diagramas en [`docs/diagrams/`](../diagrams/).

## 1. Arquitectura
| Pieza | Tecnología | Dónde corre |
|---|---|---|
| Frontend | React 18 + TypeScript + Vite + Tailwind + shadcn/ui + Recharts | Render, sitio estático |
| Backend | Python 3.11 + FastAPI + SQLAlchemy | Render, servicio web |
| Base de datos | PostgreSQL (SQLite en las pruebas) | Render, base administrada |
| Predicción de barreras | HybridModelDisability (K-Means + Gradient Boosting) embebido | Dentro del backend |
| Servicio ICF | Ollama (`gemma4:e4b`, `bge-m3`) + PostgreSQL/pgvector + FastAPI + Caddy | PC propio, expuesto con Tailscale Funnel y token |

Flujo: navegador → frontend → API del backend (JWT) → base de datos; para el perfil funcional el backend llama por HTTPS (con token) al servicio ICF.

Hay **tres ambientes** idénticos en forma: Development (rama `develop`), QA (`staging`) y Producción (`master`).

| Ambiente | Backend | Frontend |
|---|---|---|
| Development | https://hab-backend-dev.onrender.com | https://hab-frontend-dev.onrender.com |
| QA | https://hab-backend-qa.onrender.com | https://hab-frontend-qa.onrender.com |
| Producción | https://hab-backend-szj1.onrender.com | https://hab-frontend.onrender.com |

## 2. Estructura del repositorio
`backend/` (API, modelos, pruebas pytest) · `frontend/` (SPA, pruebas Vitest, E2E Playwright en `e2e/`) · `icf-service/` (servicio de IA y sus pruebas) · `docs/` (manuales, reportes, diagramas, presentación) · `render.yaml` (blueprint de Render) · `.github/workflows/` (CI/CD). Detalle en el README.

## 3. Instalación local
Requisitos: Python 3.11, Node 20, Git. PostgreSQL es opcional (por defecto SQLite local).
```bash
git clone https://github.com/jaquimbayoc7/health-access-bridge.git
cd health-access-bridge
# Backend
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000      # docs en http://localhost:8000/docs
# Frontend (otra terminal)
cd frontend && npm ci && npm run dev
```
Al arrancar, la aplicación crea las tablas y ejecuta un **seed idempotente** (administrador y dos médicos de prueba; credenciales en el README, solo para ambientes de prueba). Sin el servicio ICF todo funciona salvo las sugerencias de perfil funcional.

## 4. Variables de configuración
**Backend** (en Render: *Environment*; los marcados *secreto* no van en el repositorio):
| Variable | Uso |
|---|---|
| `ENVIRONMENT`, `DEBUG` | Modo del ambiente |
| `DATABASE_URL` | Conexión a PostgreSQL (la entrega Render desde la base asociada) |
| `JWT_SECRET` (*secreto*), `JWT_ALGORITHM`, `JWT_EXPIRE_MINUTES` | Firma y vigencia de los tokens (480 min) |
| `ALLOWED_ORIGINS` | CORS: URL exacta del frontend del ambiente |
| `DEFAULT_ADMIN_EMAIL`, `DEFAULT_ADMIN_PASSWORD` (*secreto*) | Administrador inicial |
| `PREDICTION_API_URL`, `PREDICTION_API_KEY` (*secreto*) | Servicio de predicción externo (cuando se usa) |
| `ICF_LLM_URL`, `ICF_LLM_TOKEN` (*secreto*) | URL del túnel y token del servicio ICF |
| `ICF_LLM_MODEL`, `ICF_LLM_TIMEOUT_S`, `ICF_LLM_KEEP_ALIVE` | Modelo (`gemma4:e4b`), tiempo máximo y permanencia en memoria |

**Frontend** (variables de *build*): `VITE_API_BASE_URL` (URL del backend del ambiente) y `VITE_ENVIRONMENT`. Cambiarlas exige reconstruir el sitio.

## 5. Pruebas
| Capa | Comando | Notas |
|---|---|---|
| Backend | `cd backend && pytest app/tests/ -v` | SQLite en memoria; el CI exige cobertura ≥ 80 % |
| Frontend | `cd frontend && npm run test` | Vitest + Testing Library |
| Servicio ICF | `cd icf-service && pytest -v` | 9 pruebas necesitan el catálogo de la OMS y solo corren en el PC propio |
| E2E | `cd frontend && npm run test:e2e` | Playwright; `PLAYWRIGHT_BASE_URL` apunta a un ambiente desplegado |
| Accesibilidad | `npx playwright test e2e/accessibility.spec.ts` | axe-core, WCAG 2.2 AA |
| Aceptación (UAT) | `UAT=1 npx playwright test e2e/uat-aceptacion.spec.ts` | Crea y borra datos de prueba: solo bajo demanda, nunca en producción |

Los E2E y el UAT hacen inicio de sesión real: desde un origen que no esté en `ALLOWED_ORIGINS` el navegador bloquea las llamadas (CORS); use el frontend desplegado del ambiente.

## 6. CI/CD y flujo de despliegue
- **Flujo de ramas:** se trabaja en `develop`; la promoción es por *pull request* `develop` → `staging` → `master` (las ramas están protegidas: exigen PR y revisiones de estado).
- **`ci-dev.yml`:** pruebas de backend, servicio ICF y frontend, lint y *build* en cada *push* a `develop`; Render despliega solo.
- **`ci-qa.yml`:** las mismas verificaciones y *smoke tests* (salud, login, ruta protegida, documentación).
- **`ci-prod.yml`:** verificaciones, **aprobación manual obligatoria** (entorno `production` de GitHub) y *smoke tests* con sondeo de hasta 10 minutos tras el despliegue.
- `npm ci` exige que `package-lock.json` esté sincronizado con `package.json`; el CI lo verifica.

### Procedimiento de liberación
1. Verifique que `develop` esté en verde y desplegado en DEV; ejecute `accessibility.spec.ts` y, si procede, el UAT contra DEV.
2. Abra el PR `develop` → `staging`; con las verificaciones en verde, combínelo; Render despliega QA; repita las pruebas contra QA.
3. Abra el PR `staging` → `master`; apruebe el *gate* de producción en GitHub; revise los *smoke tests*.
4. Confirme `/health` y un inicio de sesión real en producción.

### Reversión (rollback)
En Render, en el servicio afectado, use *Rollback* al despliegue anterior (backend y frontend se revierten por separado). Si el problema es del código, revierta el *merge* con `git revert` en una rama nueva y promuévala por el mismo flujo. No ejecute `/admin/reset-seed` en producción (borra y recrea pacientes).

## 7. Operación y mantenimiento
- **Salud:** `GET /health` en cada backend; el plan gratuito de Render duerme los servicios tras inactividad (la primera petición tarda). Producción usa un plan pago para la base.
- **Servicio ICF:** diagnóstico con `GET /icf/health` (rol administrador) y el procedimiento diario en el manual de operación del ICF (encendido del PC, Docker, Ollama, túnel).
- **Usuarios:** alta y baja lógica desde el panel de administración; al rotar `JWT_SECRET` todas las sesiones se invalidan.
- **Secretos:** nunca en el repositorio; se cargan en Render y en los *environments* de GitHub. Rote el token del ICF si se filtra.
- **Datos:** el borrado de pacientes es lógico. Haga copias de la base de producción con las herramientas de Render antes de cambios grandes.

## 8. Solución de problemas
| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| El frontend carga pero el login falla con error de red | CORS: `ALLOWED_ORIGINS` no incluye la URL del frontend | Corregir la variable en el backend y reiniciar |
| 401 en todas las llamadas tras un despliegue | `JWT_SECRET` cambió | Volver a iniciar sesión |
| El *build* del frontend falla en `npm ci` | `package-lock.json` desincronizado | Ejecutar `npm install` localmente y confirmar el lockfile |
| «No se pudo conectar con el servidor de IA» | PC del ICF apagado, Docker/Ollama detenidos o túnel caído | Seguir el manual de operación del ICF; `GET /icf/health` |
| Primera petición muy lenta | Servicio gratuito dormido | Esperar; los *smoke tests* de producción ya sondean hasta 10 minutos |
| Un E2E local falla en el login | El origen no está permitido por CORS | Apuntar `PLAYWRIGHT_BASE_URL` al frontend desplegado |

## 9. Seguridad y cumplimiento
Autenticación con JWT y contraseñas con Bcrypt; control de acceso por rol en cada endpoint (el médico solo ve a sus pacientes; el administrador no registra pacientes). El tablero usa datos agregados. El servicio ICF corre en equipo propio, con token, sin enviar datos clínicos a terceros. El catálogo CIF-IA tiene derechos de la OMS: no se redistribuye (ver [`LICENCIAS_COMPONENTES_ICF.md`](../reports/LICENCIAS_COMPONENTES_ICF.md)). Las sugerencias de la IA son un borrador de apoyo y su validación clínica está documentada en [`PROTOCOLO_VALIDACION_CLINICA_HU07G.md`](../reports/PROTOCOLO_VALIDACION_CLINICA_HU07G.md).

## 10. Deuda técnica conocida
- `tsc --noEmit` reporta errores de tipos preexistentes en `analyticsExport.test.ts` y `Analytics.tsx:234`; no afectan el *build* de Vite.
- Rendimiento con carga alta (200 usuarios simultáneos, p95 de 54,6 s en el plan gratuito): DEUDA-01, ver el reporte de HU-06.
- Pendientes de la validación clínica del ICF (segunda revisora, apagar `ICF_MENTAL_LINK`): ver `docs/PENDIENTES_PROXIMA_SESION.md`.
