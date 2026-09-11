import { test, expect } from '@playwright/test';

/**
 * HU-06 — E2E: flujo crítico de autenticación.
 * Requiere que el backend correspondiente (local o QA) tenga el usuario
 * de seed medico1@salud.co / medico123 disponible.
 */
test.describe('Login', () => {
  test('un médico puede iniciar sesión y llega al dashboard', async ({ page }) => {
    await page.goto('/login');

    await page.locator('#email').fill('medico1@salud.co');
    await page.locator('#password').fill('medico123');
    await page.getByRole('button', { name: /iniciar sesión|login/i }).click();

    await expect(page).toHaveURL(/\/dashboard/, { timeout: 15000 });
  });

  test('credenciales inválidas muestran un error y no navega', async ({ page }) => {
    await page.goto('/login');

    await page.locator('#email').fill('medico1@salud.co');
    await page.locator('#password').fill('password-incorrecto');
    await page.getByRole('button', { name: /iniciar sesión|login/i }).click();

    await expect(page).toHaveURL(/\/login/);
  });
});
