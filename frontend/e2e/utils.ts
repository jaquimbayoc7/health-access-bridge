import { Page } from '@playwright/test';

/**
 * Helper de login reutilizado por los specs E2E de HU-06.
 * Usa el usuario médico de seed disponible en dev/qa/prod.
 */
export async function loginAsMedico(page: Page) {
  // Evita que el OnboardingModal (App.tsx) se abra 600ms después de cada
  // page.goto: compite por role="dialog" con los diálogos que los tests
  // sí esperan (ver OnboardingModal.ONBOARDING_KEY).
  await page.addInitScript(() => {
    window.localStorage.setItem('hab_onboarding_done', 'true');
  });

  await page.goto('/login');
  await page.locator('#email').fill('medico1@salud.co');
  await page.locator('#password').fill('medico123');
  await page.getByRole('button', { name: /iniciar sesión|login/i }).click();
  await page.waitForURL(/\/dashboard/, { timeout: 15000 });
}
