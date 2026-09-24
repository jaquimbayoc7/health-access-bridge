import { test, expect } from '@playwright/test';
import { loginAsMedico } from './utils';

/**
 * HU-06 — E2E: flujo crítico de ejecución de predicción ML.
 */
test.describe('Predicciones', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsMedico(page);
  });

  test('la página de predicciones carga con el selector de paciente', async ({ page }) => {
    await page.goto('/predictions');

    await expect(page.getByRole('heading', { name: /predicciones|predictions/i })).toBeVisible();
    await expect(page.getByText(/nueva predicción|new prediction/i)).toBeVisible();
    await expect(page.locator('#patient')).toBeVisible();
  });

  test('ejecutar una predicción sobre el primer paciente disponible', async ({ page }) => {
    await page.goto('/predictions');

    await page.locator('#patient').click();
    const firstOption = page.getByRole('option').first();
    // Si no hay pacientes registrados el flujo no aplica; se omite el test.
    test.skip(!(await firstOption.isVisible().catch(() => false)), 'No hay pacientes disponibles para predecir');

    await firstOption.click();
    await page.getByRole('button', { name: /ejecutar predicción|run prediction/i }).click();

    // Se valida el toast de confirmación en vez de buscar el texto del perfil:
    // el backend QA es real y compartido, y el historial acumula predicciones
    // de otros pacientes con la misma descripción, lo que rompe el modo strict
    // de Playwright si se busca ese texto en toda la página.
    await expect(page.getByText(/predicción completada|prediction completed/i)).toBeVisible({ timeout: 15000 });
  });
});
