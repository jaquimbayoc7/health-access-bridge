import { defineConfig, devices } from '@playwright/test';

/**
 * Configuración de Playwright para las pruebas E2E de HU-06.
 * Ver frontend/e2e/*.spec.ts para los flujos críticos cubiertos.
 *
 * workers=1 en CI: los specs corren contra un backend QA real y
 * compartido (misma cuenta de médico, misma lista de pacientes). Con
 * workers>1 dos tests concurrentes pueden mutar/leer el mismo estado
 * (p.ej. abrir el diálogo de creación mientras otro test crea un
 * paciente), causando fallos intermitentes no relacionados con bugs de
 * la app. Ejecución serial evita esa interferencia.
 */
export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: [['html', { open: 'never' }], ['list']],
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:8080',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
