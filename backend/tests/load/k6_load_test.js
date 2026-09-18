/**
 * HU-06 — Prueba de carga (rendimiento API)
 *
 * Simula hasta 200 usuarios concurrentes contra el backend de HAB para
 * validar el criterio de aceptacion: "API responde en menos de 200ms bajo
 * carga simulada (200 usuarios concurrentes)".
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
 * NO ejecutar contra produccion sin autorizacion explicita: 200 VUs pueden
 * generar carga significativa sobre la base de datos y el dyno de Render.
 *
 * PENDIENTE (ver docs/test-report.md y BACKLOG.md HU-06): esta prueba aun
 * no se ha ejecutado contra un ambiente real desplegado. Sigue pendiente
 * de agendar y ejecutar, y de documentar sus resultados.
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
    ramp_to_200_vus: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30s', target: 50 },
        { duration: '30s', target: 100 },
        { duration: '30s', target: 200 }, // 200 usuarios concurrentes
        { duration: '1m', target: 200 },  // sostiene la carga pico
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
