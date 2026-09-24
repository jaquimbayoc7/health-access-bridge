import { test, expect } from '@playwright/test';
import { loginAsMedico } from './utils';

/**
 * HU-06 — E2E: flujo crítico de gestión de pacientes.
 */
test.describe('Pacientes', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsMedico(page);
  });

  test('la lista de pacientes carga correctamente', async ({ page }) => {
    await page.goto('/patients');
    // Nivel 1 para no matchear tambien el heading "No patients yet" del estado vacio,
    // que tambien contiene la palabra "patients" (bug reproducido en QA con lista vacia).
    await expect(page.getByRole('heading', { name: /pacientes|patients/i, level: 1 })).toBeVisible();
  });

  test('el diálogo de creación de paciente abre y cierra', async ({ page }) => {
    await page.goto('/patients');

    // .first(): con la lista vacia existen 2 botones "Add Patient" (header + estado vacio),
    // ambos abren el mismo dialogo.
    await page.getByRole('button', { name: /agregar paciente|add patient/i }).first().click();
    await expect(page.getByRole('dialog')).toBeVisible();
    await expect(page.locator('#nombre_apellidos')).toBeVisible();
    await expect(page.locator('#numero_documento')).toBeVisible();

    await page.getByRole('button', { name: /cancelar|cancel/i }).click();
    await expect(page.getByRole('dialog')).not.toBeVisible();
  });

  test('crear un paciente con datos ICF completos', async ({ page }) => {
    await page.goto('/patients');
    const documentNumber = `E2E${Date.now()}`;

    await page.getByRole('button', { name: /agregar paciente|add patient/i }).first().click();

    await page.locator('#nombre_apellidos').fill('Paciente Prueba E2E');
    await page.locator('#numero_documento').fill(documentNumber);
    await page.locator('#fecha_nacimiento').fill('1990-01-01');
    await page.locator('#orientacion_sexual').fill('Heterosexual');

    // El backend QA es una instancia real compartida (Render free tier) y puede
    // tardar en responder (cold start); se espera explícitamente la respuesta
    // de creación antes de verificar que el diálogo se cierre.
    const createResponse = page.waitForResponse(
      (res) => res.url().includes('/patients/') && res.request().method() === 'POST',
      { timeout: 30000 }
    );
    await page.getByRole('button', { name: /guardar|save/i }).click();
    await createResponse;

    // El toast de éxito confirma que la creación se completó del lado del backend
    // antes que el cierre del diálogo, que puede demorar por el re-render de la
    // lista (el backend QA compartido acumula muchos pacientes de corridas previas).
    await expect(page.getByText(/paciente creado|patient created/i)).toBeVisible({ timeout: 15000 });
    await expect(page.getByRole('dialog')).not.toBeVisible({ timeout: 15000 });
    await expect(page.getByText(documentNumber)).toBeVisible({ timeout: 15000 });
  });
});
