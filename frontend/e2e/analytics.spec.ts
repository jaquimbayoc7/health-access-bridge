import { test, expect, Page } from '@playwright/test';

/**
 * HU-08 — E2E: dashboard de análisis y exportación.
 *
 * La sesión se siembra en localStorage y /analytics/* se simula con page.route: la prueba no depende del backend ni de
 * los pacientes compartidos del ambiente y es determinista. Los datos son sintéticos y agregados (no hay datos de personas).
 */
const SUMMARY = {
  generated_at: '2026-10-27T15:00:00Z',
  scope: 'propio',
  filters: {},
  totals: { patients: 12, with_prediction: 10, prediction_rate: 0.8333, mean_age: 41.5, mean_global_level: 52.3, with_icf_profile: 4 },
  distributions: {
    profile: [{ key: 'Perfil 0', count: 6 }, { key: 'Perfil 1', count: 4 }],
    cat_fisica: [{ key: 'Leve', count: 5 }, { key: 'Moderada', count: 7 }],
    cat_psicosocial: [{ key: 'Leve', count: 12 }],
    genero: [{ key: 'Femenino', count: 7 }, { key: 'Masculino', count: 5 }],
    age_group: [{ key: '18-29', count: 3 }, { key: '30-44', count: 9 }],
    cause: [{ key: 'Enfermedad general', count: 8 }, { key: 'Accidente', count: 4 }],
  },
  domains: ['D1', 'D2', 'D3', 'D4', 'D5', 'D6'].map((d, i) => ({ domain: d, name: `Dominio ${d}`, mean: 20 + i * 10, n: 12 })),
  icf: {
    patients_with_profile: 4, suggestions: 20,
    by_status: { sugerido: 5, aceptado: 8, editado: 3, rechazado: 4 }, decided: 15, acceptance_rate: 0.7333,
    by_component: {
      b: { total: 8, aceptado: 4, editado: 1, rechazado: 1, sugerido: 2, acceptance_rate: 0.8333 },
      s: { total: 4, aceptado: 1, editado: 1, rechazado: 2, sugerido: 0, acceptance_rate: 0.5 },
      d: { total: 8, aceptado: 3, editado: 1, rechazado: 1, sugerido: 3, acceptance_rate: 0.8 },
    },
    by_origin: [{ key: 'llm', count: 12 }, { key: 'rules', count: 8 }],
    by_model: [{ key: 'gemma4:e4b', count: 20 }],
    top_codes: [{ code: 'b730', title: 'Fuerza muscular', component: 'b', count: 6, accepted: 5, rejected: 1 }],
  },
};

/** Sesión de médico sin pasar por el backend: JWT de forma válida y con vencimiento lejano (useJWTExpiry lo lee). */
async function seedSession(page: Page, role: 'médico' | 'admin' = 'médico') {
  await page.addInitScript((r) => {
    const b64 = (o: object) => btoa(JSON.stringify(o)).replace(/=+$/, '');
    const token = `${b64({ alg: 'HS256', typ: 'JWT' })}.${b64({ sub: 'medico@e2e.test', exp: Math.floor(Date.now() / 1000) + 86400 })}.firma`;
    window.localStorage.setItem('authToken', token);
    window.localStorage.setItem('user', JSON.stringify({ id: 1, email: 'medico@e2e.test', name: 'Médico E2E', role: r }));
    window.localStorage.setItem('hab_onboarding_done', 'true');
    window.localStorage.setItem('language', 'es'); // los textos de la prueba están en español
  }, role);
}

const json = (body: unknown, status = 200) => ({ status, contentType: 'application/json', body: JSON.stringify(body) });

async function mockAnalytics(page: Page) {
  const queries: string[] = [];
  await page.route(/\/analytics\/filters/, (route) =>
    route.fulfill(json({ genero: ['Femenino', 'Masculino'], cause: ['Enfermedad general', 'Accidente'], profile: [0, 1] })));
  await page.route(/\/analytics\/summary/, (route) => {
    const url = new URL(route.request().url());
    queries.push(url.search);
    const genero = url.searchParams.get('genero');
    // con un filtro, el backend devuelve menos pacientes
    return route.fulfill(json(genero ? { ...SUMMARY, filters: { genero }, totals: { ...SUMMARY.totals, patients: 7 } } : SUMMARY));
  });
  return queries;
}

test.describe('Dashboard de análisis (HU-08)', () => {
  test('muestra los indicadores y los gráficos, y permite filtrar', async ({ page }) => {
    const queries = await mockAnalytics(page);
    await seedSession(page);
    await page.goto('/analytics');

    await expect(page.getByTestId('kpi-patients')).toHaveText('12');
    await expect(page.getByTestId('kpi-prediction-rate')).toHaveText('83.3 %');
    await expect(page.getByText(/no incluyen nombres, documentos/i)).toBeVisible();
    await expect(page.locator('svg.recharts-surface').first()).toBeVisible();

    await page.getByRole('combobox', { name: 'Género' }).selectOption('Femenino');
    await expect(page.getByTestId('kpi-patients')).toHaveText('7');
    expect(queries.some((q) => q.includes('genero=Femenino'))).toBe(true);

    await page.getByRole('button', { name: 'Quitar filtros' }).click();
    await expect(page.getByTestId('kpi-patients')).toHaveText('12');
  });

  test('la pestaña ICF muestra la tasa de aceptación y los códigos frecuentes', async ({ page }) => {
    await mockAnalytics(page);
    await seedSession(page);
    await page.goto('/analytics');
    await page.getByRole('tab', { name: 'Perfil funcional ICF' }).click();
    await expect(page.getByTestId('kpi-acceptance')).toHaveText('73.3 %');
    await expect(page.getByRole('cell', { name: 'b730' })).toBeVisible();
  });

  test('exporta a Excel sin errores', async ({ page }) => {
    await mockAnalytics(page);
    await seedSession(page);
    await page.goto('/analytics');
    await expect(page.getByTestId('kpi-patients')).toBeVisible();
    const [download] = await Promise.all([
      page.waitForEvent('download'),
      page.getByRole('button', { name: /Exportar Excel/ }).click(),
    ]);
    expect(download.suggestedFilename()).toMatch(/^analisis_hab_\d{4}-\d{2}-\d{2}\.xlsx$/);
  });

  test('exporta a PDF con los gráficos', async ({ page }) => {
    await mockAnalytics(page);
    await seedSession(page);
    await page.goto('/analytics');
    await expect(page.getByTestId('kpi-patients')).toBeVisible();
    const [download] = await Promise.all([
      page.waitForEvent('download', { timeout: 20000 }),
      page.getByRole('button', { name: /Exportar PDF/ }).click(),
    ]);
    expect(download.suggestedFilename()).toMatch(/^analisis_hab_\d{4}-\d{2}-\d{2}\.pdf$/);
    if (process.env.E2E_SAVE_DIR) await download.saveAs(`${process.env.E2E_SAVE_DIR}/${download.suggestedFilename()}`); // inspección manual
    const path = await download.path();
    const { statSync } = await import('node:fs');
    // con 10 gráficos rasterizados el PDF pesa mucho más que uno solo de tablas (~10 KB)
    expect(statSync(path!).size).toBeGreaterThan(40_000);
    await expect(page.getByText('Archivo PDF descargado')).toBeVisible();
  });

  test('muestra el error y permite reintentar', async ({ page }) => {
    let calls = 0;
    await page.route(/\/analytics\/filters/, (route) => route.fulfill(json({ genero: [], cause: [], profile: [] })));
    await page.route(/\/analytics\/summary/, (route) =>
      ++calls === 1 ? route.fulfill(json({ detail: 'Error temporal' }, 500)) : route.fulfill(json(SUMMARY)));
    await seedSession(page);
    await page.goto('/analytics');
    await expect(page.getByRole('alert')).toBeVisible();
    await page.getByRole('button', { name: /Reintentar/ }).click();
    await expect(page.getByTestId('kpi-patients')).toHaveText('12');
  });
});
