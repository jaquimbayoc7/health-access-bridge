# Pruebas de Carga — HU-06

> ⚠️ **PENDIENTE:** esta prueba aún no se ha ejecutado contra un ambiente real
> desplegado. Sigue pendiente de agendar y ejecutar, y de documentar los
> resultados en `docs/test-report.md`.

Prueba de carga con [k6](https://k6.io) para validar el criterio de aceptación:
**"API responde en menos de 200ms bajo carga simulada (200 usuarios concurrentes)"**.

## Instalación de k6

```bash
# macOS
brew install k6

# Windows (winget)
winget install k6

# Linux (ver https://k6.io/docs/get-started/installation/)
```

## Ejecución local

1. Levanta el backend localmente:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
2. Asegúrate de que exista el usuario médico de seed (`medico1@salud.co` / `medico123`)
   o pasa credenciales propias por variable de entorno.
3. Corre la prueba de carga:
   ```bash
   k6 run backend/tests/load/k6_load_test.js
   ```

## Ejecución contra un ambiente desplegado (QA)

> ⚠️ No ejecutar contra **producción** sin autorización explícita: 200 VUs generan
> carga real sobre la base de datos y el servicio de Render.

```bash
BASE_URL=https://hab-backend-qa.onrender.com \
MEDICO_EMAIL=medico1@salud.co \
MEDICO_PASSWORD=medico123 \
k6 run backend/tests/load/k6_load_test.js
```

## Qué mide

El script simula una rampa de 0 → 200 usuarios virtuales concurrentes (30s → 30s → 30s
sostenidos 1 min en el pico → bajada), ejecutando en cada iteración:

1. `GET /health` — health check público
2. `POST /users/login` — autenticación
3. `GET /patients/` — listado autenticado (endpoint más usado en la app)

### Thresholds (criterios de aceptación configurados en el script)

| Métrica | Umbral |
|---|---|
| `http_req_duration` (p95) | < 200ms |
| `http_req_failed` (tasa de error) | < 1% |

Si algún threshold falla, `k6` termina con código de salida distinto de 0 — apto para
integrarlo como gate en CI/CD contra un ambiente de staging dedicado.

## Resultados

Ver `docs/test-report.md` para el resumen de la última ejecución documentada.
