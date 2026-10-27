import { test, expect, Page } from '@playwright/test';
import { mkdirSync } from 'node:fs';

/**
 * HU-09 — Guion de aceptación (UAT) ejecutado de punta a punta contra un ambiente real, sin simulaciones.
 *
 * NO corre en el CI: crea y borra un paciente de prueba y genera sugerencias con el servicio de IA. Se ejecuta a pedido:
 *   UAT=1 UAT_EVIDENCE_DIR=docs/uat/evidencia PLAYWRIGHT_BASE_URL=https://hab-frontend-dev.onrender.com \
 *     npx playwright test e2e/uat-aceptacion.spec.ts --reporter=list
 * Cada caso corresponde a un escenario de docs/uat/PLAN_PRUEBAS_UAT_HU09.md. Es una ejecución guiada por script del
 * mismo recorrido que haría un usuario; NO sustituye la sesión con usuarios reales (ver el plan, sección 6).
 */
test.skip(!process.env.UAT, 'Guion UAT: se ejecuta solo con UAT=1');
test.describe.configure({ mode: 'serial' });
test.setTimeout(180000);

const EVIDENCE = process.env.UAT_EVIDENCE_DIR;
const STAMP = Date.now();
const PATIENT = { name: `UAT Paciente ${STAMP}`, doc: `UAT${STAMP}` };

async function shot(page: Page, id: string) {
  if (!EVIDENCE) return;
  mkdirSync(EVIDENCE, { recursive: true });
  await page.screenshot({ path: `${EVIDENCE}/${id}.jpg`, type: 'jpeg', quality: 55 });
}

async function login(page: Page, email: string, password: string, landing: RegExp = /\/dashboard/) {
  await page.addInitScript(() => {
    window.localStorage.setItem('hab_onboarding_done', 'true');
    window.localStorage.setItem('language', 'es');
  });
  await page.goto('/login');
  await page.locator('#email').fill(email);
  await page.locator('#password').fill(password);
  await page.getByRole('button', { name: /iniciar sesión|login/i }).click();
  await page.waitForURL(landing, { timeout: 60000 });
}

const MEDICO = { email: 'medico1@salud.co', password: 'medico123' };
const MEDICO2 = { email: 'medico2@salud.co', password: 'medico123' };
const ADMIN = { email: 'administrador@salud.co', password: 'adminpassword' };

test.describe('Médico', () => {
  let page: Page;
  test.beforeAll(async ({ browser }) => {
    page = await (await browser.newContext({ viewport: { width: 1280, height: 800 } })).newPage();
  });
  test.afterAll(async () => { await page.context().close(); });

  test('UAT-M01 inicia sesión con credenciales válidas y ve su panel', async () => {
    await login(page, MEDICO.email, MEDICO.password);
    await expect(page.getByRole('heading', { level: 1 }).first()).toBeVisible();
    await expect(page.getByRole('navigation', { name: /menú principal|main menu/i })).toBeVisible();
    await shot(page, 'UAT-M01-panel');
  });

  test('UAT-M03 registra un paciente y lo encuentra con el buscador', async () => {
    await page.goto('/patients');
    await page.getByRole('button', { name: /agregar paciente|add patient/i }).first().click();
    await page.locator('#nombre_apellidos').fill(PATIENT.name);
    await page.locator('#numero_documento').fill(PATIENT.doc);
    await page.locator('#fecha_nacimiento').fill('1985-03-12');
    await page.locator('#orientacion_sexual').fill('No informa');
    await shot(page, 'UAT-M03a-formulario');
    const created = page.waitForResponse((r) => r.url().includes('/patients/') && r.request().method() === 'POST', { timeout: 60000 });
    await page.getByRole('button', { name: /guardar|save/i }).click();
    expect((await created).status()).toBe(201);
    await expect(page.getByRole('dialog')).not.toBeVisible({ timeout: 20000 });
    await page.getByPlaceholder(/buscar|search/i).fill(PATIENT.name);
    await expect(page.getByRole('cell', { name: PATIENT.name }).first()).toBeVisible({ timeout: 20000 });
    await shot(page, 'UAT-M03b-lista');
  });

  test('UAT-M04 edita el paciente y el cambio queda guardado', async () => {
    await page.goto('/patients');
    await page.getByPlaceholder(/buscar|search/i).fill(PATIENT.name);
    await page.getByRole('button', { name: new RegExp(`(editar|edit): ${PATIENT.name}`, 'i') }).first().click();
    await page.locator('#orientacion_sexual').fill('Heterosexual');
    const updated = page.waitForResponse((r) => r.url().includes('/patients/') && r.request().method() === 'PUT', { timeout: 60000 });
    await page.getByRole('button', { name: /guardar|save/i }).click();
    expect((await updated).status()).toBe(200);
    await expect(page.getByRole('dialog')).not.toBeVisible({ timeout: 20000 });
  });

  test('UAT-M05 ejecuta la predicción de barreras sobre el paciente', async () => {
    await page.goto('/predictions');
    await page.locator('#patient').click();
    await page.getByRole('option', { name: new RegExp(PATIENT.name) }).click();
    await shot(page, 'UAT-M05a-seleccion');
    await page.getByRole('button', { name: /ejecutar predicción|run prediction/i }).click();
    await expect(page.getByText(/predicción completada|prediction completed/i)).toBeVisible({ timeout: 30000 });
    await shot(page, 'UAT-M05b-resultado');
  });

  test('UAT-M06 genera el perfil funcional ICF, acepta un código, rechaza otro y descarga el reporte', async () => {
    await page.goto('/functional-profile');
    await expect(page.getByText(/borrador de apoyo/i).first()).toBeVisible();
    await page.getByRole('combobox', { name: /seleccionar paciente|select patient/i }).click();
    await page.getByRole('option', { name: new RegExp(PATIENT.name) }).click();
    await page.locator('#fp-diag').fill('G80 Parálisis cerebral');
    await page.locator('#fp-notes').fill('Espasticidad en ambas piernas; usa silla de ruedas.');
    await page.getByRole('button', { name: /generar perfil funcional|generate functional profile/i }).click();
    await expect(page.locator('[data-testid^="code-"]').first()).toBeVisible({ timeout: 150000 });
    expect(await page.locator('[data-testid^="code-"]').count()).toBeGreaterThanOrEqual(3);
    await shot(page, 'UAT-M06a-perfil');
    const accepted = page.waitForResponse((r) => /\/icf\/suggestions\/\d+/.test(r.url()) && r.request().method() === 'PATCH');
    await page.getByRole('button', { name: /^(aceptar|accept) /i }).first().click();
    expect((await accepted).status()).toBe(200);
    const rejected = page.waitForResponse((r) => /\/icf\/suggestions\/\d+/.test(r.url()) && r.request().method() === 'PATCH');
    await page.getByRole('button', { name: /^(rechazar|reject) /i }).nth(1).click();
    expect((await rejected).status()).toBe(200);
    await shot(page, 'UAT-M06b-decisiones');
    const [pdf] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: /descargar pdf|download pdf/i }).click()]);
    expect(pdf.suggestedFilename()).toMatch(/\.pdf$/i);
  });

  test('UAT-M07 exporta la lista de pacientes a Excel y a PDF', async () => {
    await page.goto('/patients');
    const [xlsx] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Excel' }).click()]);
    expect(xlsx.suggestedFilename()).toMatch(/\.xlsx$/);
    const [pdf] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'PDF' }).click()]);
    expect(pdf.suggestedFilename()).toMatch(/\.pdf$/);
  });

  test('UAT-M08 consulta el dashboard de análisis, lo filtra y lo exporta', async () => {
    await page.goto('/analytics');
    await expect(page.getByTestId('kpi-patients')).toBeVisible({ timeout: 60000 });
    const total = Number(await page.getByTestId('kpi-patients').textContent());
    expect(total).toBeGreaterThanOrEqual(1);
    await shot(page, 'UAT-M08a-dashboard');
    const options = await page.locator('#f-genero option').allTextContents();
    const gender = options.find((o) => o && !/^(todos|all)$/i.test(o.trim()));
    if (gender) {
      await page.locator('#f-genero').selectOption({ label: gender });
      await expect.poll(async () => Number(await page.getByTestId('kpi-patients').textContent())).toBeLessThanOrEqual(total);
    }
    await page.getByRole('tab', { name: /perfil funcional icf|icf functional profile/i }).click();
    await expect(page.getByTestId('kpi-suggestions')).toBeVisible();
    await shot(page, 'UAT-M08b-icf');
    const [xlsx] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: /exportar excel|export excel/i }).click()]);
    expect(xlsx.suggestedFilename()).toMatch(/^analisis_hab_.*\.xlsx$/);
    const [pdf] = await Promise.all([page.waitForEvent('download', { timeout: 60000 }), page.getByRole('button', { name: /exportar pdf|export pdf/i }).click()]);
    expect(pdf.suggestedFilename()).toMatch(/^analisis_hab_.*\.pdf$/);
  });

  test('UAT-M09 cambia el idioma de la interfaz a inglés y vuelve a español', async () => {
    await page.goto('/patients');
    await page.getByRole('button', { name: /cambiar idioma|change language/i }).click();
    await page.getByRole('menuitem', { name: 'English' }).click();
    await expect(page.getByRole('heading', { name: /^patients$/i, level: 1 })).toBeVisible();
    await shot(page, 'UAT-M09-ingles');
    await page.getByRole('button', { name: /change language/i }).click();
    await page.getByRole('menuitem', { name: 'Español' }).click();
    await expect(page.getByRole('heading', { name: /^pacientes$/i, level: 1 })).toBeVisible();
  });

  test('UAT-M10 el centro de ayuda y la guía predictiva abren', async () => {
    await page.goto('/help');
    await expect(page.getByRole('heading', { level: 1 }).first()).toBeVisible();
    await shot(page, 'UAT-M10a-ayuda');
    await page.goto('/predictive-guide');
    await expect(page.getByRole('heading', { level: 1 }).first()).toBeVisible();
  });

  test('UAT-M11 elimina el paciente de prueba y ya no aparece', async () => {
    await page.goto('/patients');
    await page.getByPlaceholder(/buscar|search/i).fill(PATIENT.name);
    await page.getByRole('button', { name: new RegExp(`(eliminar|delete): ${PATIENT.name}`, 'i') }).first().click();
    await shot(page, 'UAT-M11a-confirmacion');
    const deleted = page.waitForResponse((r) => r.url().includes('/patients/') && r.request().method() === 'DELETE', { timeout: 60000 });
    await page.getByRole('alertdialog').getByRole('button', { name: /eliminar|delete/i }).click();
    expect((await deleted).status()).toBe(204);
    await expect(page.getByRole('cell', { name: PATIENT.name })).toHaveCount(0, { timeout: 20000 });
  });
});

test.describe('Aislamiento entre médicos', () => {
  test('UAT-M12 otro médico no ve a los pacientes del primero', async ({ page }) => {
    await login(page, MEDICO2.email, MEDICO2.password);
    await page.goto('/patients');
    await page.waitForLoadState('networkidle');
    const names = await page.locator('table tbody tr td:first-child').allTextContents();
    expect(names.filter((n) => /^UAT Paciente/.test(n))).toEqual([]);
    expect((await page.locator('table tbody tr').count())).toBeLessThanOrEqual(50);
  });

  test('UAT-M13 credenciales inválidas no dan acceso y avisan en español', async ({ page }) => {
    await page.addInitScript(() => window.localStorage.setItem('language', 'es'));
    await page.goto('/login');
    await page.locator('#email').fill('medico1@salud.co');
    await page.locator('#password').fill('contraseña-incorrecta');
    await page.getByRole('button', { name: /iniciar sesión|login/i }).click();
    await expect(page.getByText(/credenciales|incorrect|inválid/i).first()).toBeVisible({ timeout: 30000 });
    await expect(page).toHaveURL(/\/login/);
    await shot(page, 'UAT-M13-error-login');
  });
});

test.describe('Administrador', () => {
  test('UAT-A01 inicia sesión y ve la administración de usuarios', async ({ page }) => {
    await login(page, ADMIN.email, ADMIN.password, /\/(dashboard|admin)/);
    await page.goto('/admin');
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
    await expect(page.locator('#register-email')).toBeVisible();
    await shot(page, 'UAT-A01-admin');
  });

  test('UAT-A02 el administrador no ve los menús de pacientes ni de predicciones', async ({ page }) => {
    await login(page, ADMIN.email, ADMIN.password, /\/(dashboard|admin)/);
    const nav = page.getByRole('navigation', { name: /menú principal|main menu/i });
    await expect(nav.getByRole('link', { name: /^pacientes$|^patients$/i })).toHaveCount(0);
    await expect(nav.getByRole('link', { name: /análisis|analytics/i })).toBeVisible();
  });

  test('UAT-A03 el administrador ve el análisis de todos los pacientes y puede filtrar por médico', async ({ page }) => {
    await login(page, ADMIN.email, ADMIN.password, /\/(dashboard|admin)/);
    await page.goto('/analytics');
    await expect(page.getByTestId('kpi-patients')).toBeVisible({ timeout: 60000 });
    await expect(page.getByText(/todos los pacientes|all patients/i).first()).toBeVisible();
    const listarMedicos = async () => (await page.locator('#f-owner option').allTextContents()).filter((o) => o && !/^(todos|all)$/i.test(o.trim()));
    // los médicos del filtro llegan de /analytics/filters: se espera a que carguen
    await expect.poll(async () => (await listarMedicos()).length, { timeout: 30000 }).toBeGreaterThanOrEqual(2);
    const medicos = await listarMedicos();
    await page.locator('#f-owner').selectOption({ label: medicos[0] });
    await expect(page.getByText(/mis pacientes|my patients/i).first()).toBeVisible({ timeout: 30000 });
    await shot(page, 'UAT-A03-admin-analisis');
  });

  test('UAT-A04 crea un usuario médico y lo desactiva', async ({ page }) => {
    await login(page, ADMIN.email, ADMIN.password, /\/(dashboard|admin)/);
    await page.goto('/admin');
    const email = `uat.${STAMP}@salud.co`;
    await page.locator('#register-name').fill('Médico UAT');
    await page.locator('#register-email').fill(email);
    await page.locator('#register-password').fill('Uat-Prueba-2026!');
    await page.locator('#register-role').click();
    await page.getByRole('option', { name: /médico|doctor/i }).first().click();
    const created = page.waitForResponse((r) => r.url().includes('/admin/users/register') && r.request().method() === 'POST', { timeout: 60000 });
    await page.getByRole('button', { name: /crear|create|registrar|register/i }).first().click();
    expect((await created).status()).toBe(201);
    await shot(page, 'UAT-A04a-usuario-creado');
    await page.getByRole('button', { name: /cerrar|close|entendido|ok/i }).first().click().catch(() => undefined);
    await page.getByPlaceholder(/buscar por nombre|search by name/i).fill('Médico UAT');
    const toggle = page.getByRole('switch').first();
    const patched = page.waitForResponse((r) => /\/admin\/users\/\d+\/status/.test(r.url()) && r.request().method() === 'PATCH', { timeout: 60000 });
    await toggle.click();
    expect((await patched).status()).toBe(200);
  });
});

test.describe('Transversales', () => {
  test('UAT-X01 en un teléfono (390 px) no hay desplazamiento horizontal y el menú se abre', async ({ browser }) => {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 800 } });
    const page = await ctx.newPage();
    await login(page, MEDICO.email, MEDICO.password);
    for (const route of ['/dashboard', '/patients', '/analytics']) {
      await page.goto(route);
      await page.waitForLoadState('networkidle');
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      expect(overflow, `desplazamiento horizontal en ${route}`).toBeLessThanOrEqual(1);
    }
    await shot(page, 'UAT-X01-movil');
    await ctx.close();
  });

  test('UAT-X02 el inicio de sesión se completa solo con el teclado', async ({ page }) => {
    await page.addInitScript(() => {
      window.localStorage.setItem('hab_onboarding_done', 'true');
      window.localStorage.setItem('language', 'es');
    });
    await page.goto('/login');
    await page.locator('#email').focus();
    await page.keyboard.type(MEDICO.email);
    await page.keyboard.press('Tab');
    await page.keyboard.type(MEDICO.password);
    await page.keyboard.press('Enter');
    await page.waitForURL(/\/dashboard/, { timeout: 60000 });
  });
});
