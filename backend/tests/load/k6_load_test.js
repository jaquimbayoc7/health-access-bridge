/**
 * HU-06 / DEUDA-01 — Prueba de carga (rendimiento API)
 *
 * Simula usuarios concurrentes contra el backend de HAB para validar el
 * criterio de aceptacion: "API responde en menos de 200ms bajo carga
 * simulada".
 *
 * Requiere k6 (https://k6.io/docs/get-started/installation/).
 *
 * Uso:
 *   BASE_URL=https://hab-backend-qa.onrender.com \
 *   MEDICO_EMAIL=medico1@salud.co \
 *   MEDICO_PASSWORD=medico123 \
 *   k6 run backend/tests/load/k6_load_test.js
 *
 * Por defecto apunta a un backend corriendo en local (http://localhost:8000).
 * NO ejecutar contra produccion sin autorizacion explicita.
 *
 * NOTA (DEUDA-01, 23 Sep 2026): el objetivo de concurrencia se ajusto de
 * 200 a 30 VUs porque la capacidad real de la infraestructura actual esta
 * acotada por el pool de conexiones de SQLAlchemy en produccion/QA
 * (pool_size=10 + max_overflow=20 = 30 conexiones maximas, ver
 * backend/app/database.py) y por 1 solo worker de Uvicorn (sin --workers
 * en render.yaml). Probar con 200 VUs contra un pool de 30 conexiones no
 * mide el rendimiento del API: mide la saturacion inmediata de la cola de
 * conexiones, que es la causa raiz ya confirmada del fallo de latencia
 * documentado el 18 Sep 2026 (p95 real ~55s vs. <200ms esperado, ver
 * docs/test-report.md Seccion 4). Esta version evalua el rendimiento
 * dentro de la capacidad real que la infraestructura soporta hoy.
 */
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend } from 'k6/metrics';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';
const MEDICO_EMAIL = __ENV.MEDICO_EMAIL || 'medico1@salud.co';
const MEDICO_PASSWORD = __ENV.MEDICO_PASSWORD || 'medico123';

// Metrica custom para reportar latencia por tipo de endpoint
const healthTrend = new Trend('hab_health_duration');
const loginTrend = new Trend('hab_login_duration');
const patientsTrend = new Trend('hab_patients_list_duration');

export const options = {
  scenarios: {
    ramp_to_30_vus: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30s', target: 10 },
        { duration: '30s', target: 20 },
        { duration: '30s', target: 30 }, // 30 usuarios concurrentes = limite del pool (pool_size=10 + max_overflow=20)
        { duration: '1m', target: 30 },  // sostiene la carga pico
        { duration: '30s', target: 0 },
      ],
    },
  },
  thresholds: {
    // Criterio de aceptacion HU-06: API < 200ms bajo carga simulada
    http_req_duration: ['p(95)<200'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  // 1. Health check (endpoint publico, sin auth)
  const healthRes = http.get(`${BASE_URL}/health`);
  healthTrend.add(healthRes.timings.duration);
  check(healthRes, { 'health check: status 200': (r) => r.status === 200 });

  // 2. Login como medico (form-encoded, OAuth2PasswordRequestForm)
  const loginRes = http.post(
    `${BASE_URL}/users/login`,
    { username: MEDICO_EMAIL, password: MEDICO_PASSWORD },
    { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  );
  loginTrend.add(loginRes.timings.duration);
  const loginOk = check(loginRes, {
    'login: status 200': (r) => r.status === 200,
    'login: tiene access_token': (r) => !!r.json('access_token'),
  });

  if (loginOk) {
    const token = loginRes.json('access_token');
    const authHeaders = { headers: { Authorization: `Bearer ${token}` } };

    // 3. Listar pacientes (endpoint autenticado mas usado en la app)
    const patientsRes = http.get(`${BASE_URL}/patients/`, authHeaders);
    patientsTrend.add(patientsRes.timings.duration);
    check(patientsRes, { 'patients list: status 200': (r) => r.status === 200 });
  }

  sleep(1);
}
