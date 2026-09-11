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
    await expect(page.getByRole('heading', { name: /pacientes|patients/i })).toBeVisible();
  });

  test('el diálogo de creación de paciente abre y cierra', async ({ page }) => {
    await page.goto('/patients');

    await page.getByRole('button', { name: /agregar paciente|add patient/i }).click();
    await expect(page.getByRole('dialog')).toBeVisible();
    await expect(page.locator('#nombre_apellidos')).toBeVisible();
    await expect(page.locator('#numero_documento')).toBeVisible();

    await page.getByRole('button', { name: /cancelar|cancel/i }).click();
    await expect(page.getByRole('dialog')).not.toBeVisible();
  });

  test('crear un paciente con datos ICF completos', async ({ page }) => {
    await page.goto('/patients');
    const documentNumber = `E2E${Date.now()}`;

    await page.getByRole('button', { name: /agregar paciente|add patient/i }).click();

    await page.locator('#nombre_apellidos').fill('Paciente Prueba E2E');
    await page.locator('#numero_documento').fill(documentNumber);
    await page.locator('#fecha_nacimiento').fill('1990-01-01');
    await page.locator('#orientacion_sexual').fill('Heterosexual');

    await page.getByRole('button', { name: /guardar|save/i }).click();

    await expect(page.getByRole('dialog')).not.toBeVisible({ timeout: 10000 });
    await expect(page.getByText(documentNumber)).toBeVisible({ timeout: 10000 });
  });
});
