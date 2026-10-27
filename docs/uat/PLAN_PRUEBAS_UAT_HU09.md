# Plan de pruebas de aceptación (UAT) — HU-09

**Fecha:** 27 de octubre de 2026 · **Ambiente:** DEV (`hab-frontend-dev.onrender.com`) · **Issue:** #9

## 1. Alcance
Validar de punta a punta, en un ambiente desplegado real, la funcionalidad, la usabilidad básica y la accesibilidad del sistema para los dos roles (médico y administrador). Hay tres fuentes de evidencia, de la más a la menos automática:

| Capa | Qué comprueba | Cómo |
|---|---|---|
| Automatizada | Funcionalidad de cada rol y accesibilidad WCAG 2.2 AA | `e2e/uat-aceptacion.spec.ts` (18 escenarios, `UAT=1`) y `e2e/accessibility.spec.ts` (axe-core, 3 pruebas) |
| Revisión experta | Heurísticas de usabilidad | Sección 4 |
| Usuarios reales | Facilidad de uso percibida (SUS) y comentarios | Sección 6 — **pendiente de participantes** |

## 2. Guion de aceptación automatizado
Se ejecuta con: `UAT=1 UAT_EVIDENCE_DIR=docs/uat/evidencia PLAYWRIGHT_BASE_URL=<url> npx playwright test e2e/uat-aceptacion.spec.ts`. Crea y borra un paciente de prueba y un usuario médico que queda desactivado; por eso no corre en el CI. Las capturas quedan en `docs/uat/evidencia/`.

| ID | Rol | Escenario | Criterio de aceptación |
|---|---|---|---|
| M01 | Médico | Inicia sesión y ve su panel | Entra a `/dashboard` y ve el menú principal |
| M03 | Médico | Registra un paciente y lo busca | El API responde 201 y aparece en la lista filtrada |
| M04 | Médico | Edita el paciente | El API responde 200 y el diálogo se cierra |
| M05 | Médico | Ejecuta la predicción de barreras | Aparece «Predicción completada» |
| M06 | Médico | Genera el perfil funcional ICF, acepta y rechaza códigos, descarga el PDF | ≥ 3 códigos sugeridos; decisiones guardadas (200); PDF descargado |
| M07 | Médico | Exporta pacientes a Excel y PDF | Se descargan `.xlsx` y `.pdf` |
| M08 | Médico | Dashboard de análisis: filtra y exporta | KPIs visibles, el filtro no aumenta el total, exporta Excel y PDF |
| M09 | Médico | Cambia el idioma a inglés y vuelve | Los títulos cambian y regresan |
| M10 | Médico | Centro de ayuda y guía predictiva | Ambas abren |
| M11 | Médico | Elimina el paciente | API 204 y ya no aparece |
| M12 | Médico | Aislamiento entre médicos | Otro médico no ve los pacientes del primero |
| M13 | Médico | Credenciales inválidas | No entra y muestra el aviso en español |
| A01 | Admin | Inicia sesión y ve la administración de usuarios | Ve el formulario de registro |
| A02 | Admin | Menú del administrador | No ve Pacientes; sí ve Análisis |
| A03 | Admin | Análisis global y filtro por médico | Ve «todos los pacientes» y, al filtrar, «mis pacientes» |
| A04 | Admin | Crea un médico y lo desactiva | API 201 y luego 200 al cambiar el estado |
| X01 | Ambos | Teléfono de 390 px | Sin desplazamiento horizontal en 3 pantallas |
| X02 | Ambos | Solo teclado | El inicio de sesión se completa sin ratón |

El identificador M02 queda reservado: el alta de usuarios es exclusiva del administrador (A04).

## 3. Accesibilidad automatizada
`e2e/accessibility.spec.ts` ejecuta axe-core con las etiquetas `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa` y `wcag22aa` sobre el inicio de sesión, 8 pantallas del médico y 5 del administrador. La puerta es **cero violaciones**. Límite conocido: las herramientas automáticas detectan solo una parte de los problemas de accesibilidad, por lo que no sustituyen la revisión manual ni el uso con lectores de pantalla.

## 4. Revisión de usabilidad (experta)
Lista de comprobación basada en las 10 heurísticas de Nielsen (1994): estado del sistema (avisos de éxito o error tras cada acción, verificados en M03–M06), correspondencia con el mundo real (vocabulario clínico, idioma ES/EN), control del usuario (confirmación antes de eliminar, M11), consistencia (un único color por perfil de barreras), prevención de errores (campos obligatorios) y ayuda (centro de ayuda y guía predictiva, M10).

## 5. Criterios de salida
- 100 % de los escenarios automatizados en verde en DEV, QA y PROD tras la promoción.
- Cero violaciones axe en los tres ambientes.
- Cero defectos abiertos de severidad alta.

## 6. Sesión con usuarios reales (realizada el 27-oct-2026; resultados en `REPORTE_FINAL_PRUEBAS_HU09.md` y en `FORMATO_REGISTRO_UAT_SUS_HU09.xlsx`)
**Muestra.** Cinco participantes detectan cerca del 85 % de los problemas de usabilidad (Nielsen y Landauer, 1993; Virzi, 1992). Para estimar el SUS con precisión se recomiendan más (Tullis y Stetson, 2004: 12 a 14). Un primer corte razonable: 3 a 5 médicos y 1 a 2 administradores.
**Tareas.** Las de la sección 2 (M03, M05, M06 y M08 para el médico; A04 y A03 para el administrador), medidas en: completada sí/no, tiempo y errores.
**Cuestionario.** Escala de Usabilidad del Sistema, SUS (Brooke, 1996), 10 ítems de 1 a 5, versión en español (Sevilla-Gonzalez et al., 2020); puntaje 0–100. Un puntaje ≥ 68 se considera por encima del promedio (Sauro y Lewis, 2016; Bangor et al., 2008).
**Comentarios.** Preguntas abiertas: «¿qué fue lo más confuso?» y «¿qué agregaría?». Cada comentario se registra con severidad (alta/media/baja), decisión (corregir ahora / backlog) y commit.

| Participante | Rol | Tareas completadas | Tiempo total | SUS | Comentario | Severidad | Decisión / commit |
|---|---|---|---|---|---|---|---|
| P1 | | | | | | | |

## Referencias
- Bangor, A., Kortum, P. y Miller, J. (2008). An empirical evaluation of the System Usability Scale. *International Journal of Human-Computer Interaction, 24*(6), 574–594.
- Brooke, J. (1996). SUS: a “quick and dirty” usability scale. En *Usability Evaluation in Industry* (pp. 189–194). Taylor & Francis.
- Nielsen, J. (1994). Enhancing the explanatory power of usability heuristics. *Proc. ACM CHI’94*, 152–158.
- Nielsen, J. y Landauer, T. K. (1993). A mathematical model of the finding of usability problems. *Proc. INTERCHI’93*, 206–213.
- Sauro, J. y Lewis, J. R. (2016). *Quantifying the User Experience* (2.ª ed.). Morgan Kaufmann.
- Sevilla-Gonzalez, M. R. et al. (2020). Spanish version of the System Usability Scale for the assessment of electronic tools. *JMIR Human Factors, 7*(4), e21161.
- Tullis, T. S. y Stetson, J. N. (2004). A comparison of questionnaires for assessing website usability. *Usability Professionals Association Conference*.
- Virzi, R. A. (1992). Refining the test phase of usability evaluation: how many subjects is enough? *Human Factors, 34*(4), 457–468.
- W3C (2023). *Web Content Accessibility Guidelines (WCAG) 2.2*. https://www.w3.org/TR/WCAG22/
