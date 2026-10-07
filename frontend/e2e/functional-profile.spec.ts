import { test, expect, Page } from '@playwright/test';
import { loginAsMedico } from './utils';

/**
 * HU-07e — E2E: pantalla «Perfil Funcional ICF».
 *
 * El login es real (backend QA), pero la lista de pacientes y los endpoints de sugerencia ICF se
 * simulan con page.route: así la prueba no depende del PC con la GPU (servicio ICF) ni de los datos
 * compartidos de QA, y es determinista. Todos los datos son sintéticos.
 */
const PATIENT = {
  id: 9001, nombre_apellidos: 'Paciente Sintetico', numero_documento: '0000000001', fecha_nacimiento: '1990-01-01',
  edad: 34, genero: 'masculino', orientacion_sexual: 'heterosexual', causa_deficiencia: 'Enfermedad general',
  cat_fisica: 'Severa', cat_psicosocial: 'Leve', nivel_d1: 70, nivel_d2: 60, nivel_d3: 80, nivel_d4: 50,
  nivel_d5: 65, nivel_d6: 75, nivel_global: 67, owner_id: 1, prediction_profile: 2,
  prediction_description: 'Perfil de Barreras Altas',
};

const item = (over: Record<string, unknown>) => ({
  id: 1, component: 'b', code: 'b730', title: 'Funciones relacionadas con la fuerza muscular', qualifier: 3,
  qualifier_cn: null, qualifier_cl: null, justification: 'Debilidad en piernas', origin: 'llm', status: 'sugerido',
  original_code: null, ...over,
});

const SET = {
  patient_id: PATIENT.id, batch_id: 'e2e', model: 'gemma4:e4b', llm_used: true, created_at: null, latency_ms: 3000,
  warnings: [],
  functions: [item({ id: 101 })],
  structures: [item({ id: 102, component: 's', code: 's750', title: 'Estructura de la extremidad inferior', qualifier_cn: 8, qualifier_cl: 8, justification: '' })],
  activities: [item({ id: 103, component: 'd', code: 'd450', title: 'Andar', origin: 'rules', justification: '' })],
};
const EMPTY = { ...SET, batch_id: null, model: null, functions: [], structures: [], activities: [] };

const json = (body: unknown, status = 200) => ({ status, contentType: 'application/json', body: JSON.stringify(body) });

/** Simula la lista de pacientes y los endpoints ICF; devuelve lo que recibió el POST de generación. */
async function mockBackend(page: Page, opts: { generateStatus?: number } = {}) {
  const captured: { generateBody?: unknown; decisions: Array<{ id: string; body: unknown }> } = { decisions: [] };
  await page.route(/\/patients\/\?/, (route) => route.fulfill(json([PATIENT])));
  await page.route(/\/patients\/\d+\/icf-suggestions/, async (route) => {
    const req = route.request();
    if (req.method() === 'POST') {
      captured.generateBody = req.postDataJSON();
      if (opts.generateStatus && opts.generateStatus !== 200) {
        return route.fulfill(json({ detail: 'El servicio de sugerencias no está disponible.' }, opts.generateStatus));
      }
      return route.fulfill(json(SET));
    }
    return route.fulfill(json(EMPTY));
  });
  await page.route(/\/icf\/suggestions\/\d+/, async (route) => {
    const req = route.request();
    const body = req.postDataJSON();
    captured.decisions.push({ id: req.url().split('/').pop() ?? '', body });
    const found = [...SET.functions, ...SET.structures, ...SET.activities].find((i) => String(i.id) === req.url().split('/').pop());
    return route.fulfill(json({ ...found, ...body }));
  });
  return captured;
}

async function choosePatient(page: Page) {
  await page.getByRole('combobox', { name: /seleccionar paciente|select patient/i }).click();
  await page.getByRole('option', { name: /Paciente Sintetico/ }).click();
}

test.describe('Perfil Funcional ICF', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsMedico(page);
  });

  test('genera el perfil con el diagnóstico y las notas y muestra b, s y d con su calificador', async ({ page }) => {
    const captured = await mockBackend(page);
    await page.goto('/functional-profile');
    await expect(page.getByText(/borrador de apoyo/i).first()).toBeVisible();

    await choosePatient(page);
    await page.locator('#fp-diag').fill('G80 Parálisis cerebral');
    await page.locator('#fp-notes').fill('Espasticidad en ambas piernas');
    await page.getByRole('button', { name: /generar perfil funcional|generate functional profile/i }).click();

    await expect(page.getByTestId('code-101')).toHaveText('b730.3');
    await expect(page.getByTestId('code-102')).toHaveText('s750.388');
    await expect(page.getByTestId('code-103')).toHaveText('d450.3');
    expect(captured.generateBody).toEqual({ diag_cie: 'G80 Parálisis cerebral', clinical_notes: 'Espasticidad en ambas piernas' });
  });

  test('el enlace de la CIE abre en pestaña nueva y «Usar este ejemplo» rellena los campos', async ({ page }) => {
    await mockBackend(page);
    await page.goto('/functional-profile');

    const link = page.getByRole('link', { name: /CIE-10 en español|ICD-10 in Spanish/i });
    await expect(link).toHaveAttribute('href', 'https://ais.paho.org/classifications/Chapters/');
    await expect(link).toHaveAttribute('target', '_blank');

    await page.getByText(/ejemplos de notas clínicas|clinical note examples/i).click();
    await page.getByRole('button', { name: /usar este ejemplo|use this example/i }).first().click();
    await expect(page.locator('#fp-diag')).toHaveValue(/G80/);
    await expect(page.locator('#fp-notes')).not.toHaveValue('');
  });

  test('acepta un código y rechaza otro guardando la decisión', async ({ page }) => {
    const captured = await mockBackend(page);
    await page.goto('/functional-profile');
    await choosePatient(page);
    await page.getByRole('button', { name: /generar perfil funcional|generate functional profile/i }).click();
    await expect(page.getByTestId('code-101')).toBeVisible();

    await page.getByRole('button', { name: /aceptar b730|accept b730/i }).click();
    await page.getByRole('button', { name: /rechazar d450|reject d450/i }).click();

    await expect.poll(() => captured.decisions.length).toBe(2);
    expect(captured.decisions.map((d) => d.body)).toEqual([{ status: 'aceptado' }, { status: 'rechazado' }]);
  });

  test('si el servicio falla muestra un aviso y el resto de la aplicación sigue funcionando', async ({ page }) => {
    await mockBackend(page, { generateStatus: 503 });
    await page.goto('/functional-profile');
    await choosePatient(page);
    await page.getByRole('button', { name: /generar perfil funcional|generate functional profile/i }).click();

    await expect(page.getByRole('alert').filter({ hasText: /no se pudo generar|could not generate/i })).toBeVisible();
    await page.goto('/patients');
    await expect(page.getByRole('heading', { name: /pacientes|patients/i, level: 1 })).toBeVisible();
  });

  test('la Guía Predictiva abre la sección del Perfil Funcional ICF', async ({ page }) => {
    await page.goto('/predictive-guide?section=icf');
    await expect(page.getByTestId('icf-guide')).toBeVisible();
    await page.getByRole('tab', { name: /niveles de barrera|barrier levels/i }).click();
    await expect(page.getByText(/perfil 0|profile 0/i).first()).toBeVisible();
  });
});
