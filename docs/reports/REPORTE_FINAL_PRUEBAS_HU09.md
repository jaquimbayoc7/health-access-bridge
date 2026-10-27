# Reporte final de pruebas — HU-09

**Fecha:** 27 de octubre de 2026 · **Ambiente probado:** DEV (Render) · **Commit:** `5ba9c3c` · **Plan:** [`PLAN_PRUEBAS_UAT_HU09.md`](../uat/PLAN_PRUEBAS_UAT_HU09.md)

## 1. Resultado
| Verificación | Resultado |
|---|---|
| Guion de aceptación (UAT) automatizado: 18 escenarios (médico, administrador y transversales) | **18/18 aprobados** (50 s) |
| Accesibilidad WCAG 2.2 AA con axe-core: inicio de sesión + 8 pantallas del médico + 5 del administrador | **0 violaciones** (3/3 pruebas) |
| Pruebas unitarias de frontend (Vitest) | 61/61 |
| CI de `develop` | en verde en cada commit |
| Sesión con usuarios reales y SUS | **Pendiente** (no hay participantes confirmados) |

Evidencia: capturas en [`docs/uat/evidencia/`](../uat/evidencia/).

## 2. Defectos hallados y corregidos
La auditoría de accesibilidad encontró violaciones reales, corregidas antes del cierre:

| # | Hallazgo (regla axe / criterio WCAG) | Corrección |
|---|---|---|
| 1 | Botones de icono sin nombre: idioma, notificaciones, menú de usuario, editar/eliminar en cada fila de pacientes, filtro de rol (`button-name`, `select-name`; 4.1.2) | `aria-label` en español e inglés; iconos con `aria-hidden` |
| 2 | Contraste insuficiente del color primario (#3c83f6, 3,63:1; 1.4.3) | #2563eb (5,17:1) |
| 3 | Insignias de perfil con contraste bajo y un defecto funcional: el Dashboard usaba umbrales de 1–10 para perfiles 0/1/2 | Una sola tabla de colores (`lib/profile.ts`), texto blanco ≥ 4,5:1 |
| 4 | Menú lateral sin punto de referencia de navegación (`region`; 1.3.1 / 2.4.1) | `<nav aria-label="Menú principal">` |
| 5 | Saltos en la jerarquía de títulos y página de administración sin h1 (`heading-order`, `page-has-heading-one`) | Títulos de tarjeta h2; h1 en el panel |
| 6 | Barra de progreso de la guía de bienvenida sin nombre (`aria-progressbar-name`) | `aria-label` |
| 7 | Gráficos de recharts: sectores con rol de imagen sin alternativa y elementos enfocables dentro de contenido oculto (`svg-img-alt`, `aria-hidden-focus`) | Cada gráfico se expone como una imagen con nombre, sus sectores se ocultan a lectores de pantalla y se desactiva la capa de foco de la biblioteca |

Nota de proceso: la primera versión de la corrección 7 (un `aria-label` en cada sector) generó una violación nueva (`aria-prohibited-attr`); se detectó en la ejecución siguiente contra DEV y se revirtió. Es el argumento para mantener la prueba de accesibilidad en el repositorio.

## 3. Limitaciones y riesgos
1. **Feedback de usuarios reales no recolectado.** El criterio «feedback documentado y corregido» queda cubierto por la revisión experta, la auditoría automática y las correcciones de la sección 2; el SUS y los comentarios de médicos están planificados (muestra, tareas, instrumento y plantilla en el plan, sección 6). No se inventan resultados.
2. axe-core **no sustituye** la revisión manual con lectores de pantalla (NVDA, VoiceOver); conviene hacerla con la sesión de usuarios.
3. El guion UAT usa cuentas semilla de DEV y deja un usuario médico `uat.<marca>@salud.co` desactivado por cada ejecución.
4. `tsc --noEmit` reporta errores de tipos preexistentes (`analyticsExport.test.ts`, `Analytics.tsx:234`); no afectan el build de Vite ni la CI y quedan para HU-10.

## 4. Siguiente paso
Promover `develop` → `staging` → `master` y repetir el guion UAT (`UAT=1`) y `accessibility.spec.ts` contra QA y PROD (criterio de salida del plan).
