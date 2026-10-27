import { test, expect, Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

/**
 * HU-09 — Accesibilidad automatizada (WCAG 2.2 AA) con axe-core sobre las pantallas de cada rol.
 *
 * El login es real (backend del ambiente). Verifica los criterios que una herramienta automática puede comprobar
 * (nombres accesibles, contraste, jerarquía de títulos, puntos de referencia, texto alternativo); no sustituye una
 * evaluación con usuarios ni con lectores de pantalla. La puerta es cero violaciones en estas reglas.
 */
const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];

const ROLES = {
  medico: { email: 'medico1@salud.co', password: 'medico123', routes: ['/dashboard', '/patients', '/predictions', '/functional-profile', '/analytics', '/predictive-guide', '/help', '/settings'] },
  admin: { email: 'administrador@salud.co', password: 'adminpassword', routes: ['/dashboard', '/analytics', '/admin', '/help', '/settings'] },
} as const;

async function login(page: Page, email: string, password: string) {
  await page.addInitScript(() => {
    window.localStorage.setItem('hab_onboarding_done', 'true');
    window.localStorage.setItem('language', 'es');
  });
  await page.goto('/login');
  await page.locator('#email').fill(email);
  await page.locator('#password').fill(password);
  await page.getByRole('button', { name: /iniciar sesión|login/i }).click();
  await page.waitForURL(/\/(dashboard|admin)/, { timeout: 60000 });
}

async function audit(page: Page) {
  const results = await new AxeBuilder({ page }).withTags(TAGS).analyze();
  return results.violations.map((v) => `${v.impact} ${v.id} (${v.nodes.length}): ${v.help} → ${v.nodes[0].target.join(' ').slice(0, 90)}`);
}

test.describe('Accesibilidad (WCAG 2.2 AA, axe-core)', () => {
  test.setTimeout(120000);

  test('pantalla de inicio de sesión (con la guía de bienvenida que se abre sola)', async ({ page }) => {
    await page.goto('/login');
    await page.waitForLoadState('networkidle');
    expect(await audit(page)).toEqual([]);
  });

  for (const [role, cfg] of Object.entries(ROLES)) {
    test(`pantallas del rol ${role}`, async ({ page }) => {
      await login(page, cfg.email, cfg.password);
      const found: Record<string, string[]> = {};
      for (const route of cfg.routes) {
        await page.goto(route);
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(800); // los gráficos de recharts terminan de montarse
        const violations = await audit(page);
        if (violations.length) found[route] = violations;
      }
      expect(found).toEqual({});
    });
  }
});
