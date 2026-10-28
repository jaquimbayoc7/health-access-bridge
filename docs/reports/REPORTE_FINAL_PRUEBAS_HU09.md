# Reporte final de pruebas — HU-09

**Fecha:** 27 de octubre de 2026 · **Ambiente probado:** DEV (Render) · **Commit:** `5ba9c3c` · **Plan:** [`PLAN_PRUEBAS_UAT_HU09.md`](../uat/PLAN_PRUEBAS_UAT_HU09.md)

## 1. Resultado
| Verificación | Resultado |
|---|---|
| Guion de aceptación (UAT) automatizado: 18 escenarios (médico, administrador y transversales) | **18/18 aprobados** (50 s) |
| Accesibilidad WCAG 2.2 AA con axe-core: inicio de sesión + 8 pantallas del médico + 5 del administrador | **0 violaciones** (3/3 pruebas) |
| Pruebas unitarias de frontend (Vitest) | 61/61 |
| CI de `develop` | en verde en cada commit |
| Sesión de usabilidad con 10 participantes (5 médicos y 5 administradores), SUS | **Media 81,25** (mediana 81,25; rango 72,5–90); 10/10 por encima de 68; ver sección 2 |

Evidencia: capturas en [`docs/uat/evidencia/`](../uat/evidencia/).

## 2. Sesión de usabilidad (SUS)
Datos registrados por el equipo en [`FORMATO_REGISTRO_UAT_SUS_HU09.xlsx`](../uat/FORMATO_REGISTRO_UAT_SUS_HU09.xlsx) (27-oct-2026, DEV). Los puntajes los calcula el propio libro con la fórmula de Brooke (1996).

| Indicador | Valor |
|---|---|
| Participantes con cuestionario completo | 10 (5 médicos, 5 administradores) |
| Media / mediana | 81,25 / 81,25 |
| Mínimo – máximo | 72,5 – 90,0 |
| Con SUS ≥ 68 (por encima del promedio) | 10 de 10 |
| Con SUS ≥ 80,3 (excelente) | 5 de 10 |
| Media por rol | Médico 84,0 · Administrador 78,5 |

Lectura: todos los puntajes superan el promedio de referencia de 68 y la media cae en el rango «bueno–excelente» (Bangor et al., 2008; Sauro y Lewis, 2016). Con n = 10 la media es una estimación gruesa (se recomiendan 12 a 14 para precisión, Tullis y Stetson, 2004), y la diferencia entre roles (5 + 5) no es concluyente.

**Tareas observadas.** Solo se registraron intentos de la tarea M06 (perfil funcional ICF): P01 y P10 la completaron **con ayuda** (3 y 5 min, 0 errores). Las demás tareas del guion no se registraron en el libro, por lo que no hay tiempos ni tasas de éxito para ellas.

**Hallazgos (2, ambos de severidad media).** P01 y P10 coincidieron: no entendían los niveles de severidad (calificador) de los códigos ICF sugeridos ni que podían ajustarlos.

| Hallazgo | Decisión | Atención |
|---|---|---|
| Sin ayudas para entender los niveles de severidad del perfil ICF y poder agregarlos/ajustarlos | Registrada como «pasar al backlog» por el equipo; se atendió de inmediato por ser de bajo costo y coincidir en 2 de 2 hallazgos | La pantalla del perfil funcional ahora trae una guía desplegable con la escala 0–4 (con sus rangos en %, escala genérica de la CIF de la OMS, 2001), y el diálogo de edición repite la escala. La edición del calificador ya existía (lápiz de cada fila) |

## 3. Defectos hallados y corregidos (accesibilidad)
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

## 4. Limitaciones y riesgos
1. **Tamaño y alcance de la muestra.** n = 10 permite detectar los problemas frecuentes pero no estima el SUS con precisión; solo se observó una tarea (M06) y los participantes fueron evaluados en un solo día. Es un primer corte, no una validación clínica de usabilidad.
2. axe-core **no sustituye** la revisión manual con lectores de pantalla (NVDA, VoiceOver). **No se realizará por tiempo** (decisión del responsable, 27-oct-2026): la accesibilidad queda verificada con axe-core y con el uso por teclado, y esta limitación se acepta.
3. El guion UAT usa cuentas semilla de DEV y deja un usuario médico `uat.<marca>@salud.co` desactivado por cada ejecución.
4. Los errores de tipos (`tsc --noEmit`) y de lint preexistentes se corrigieron el 27-oct-2026 (cero errores); el CI no los exige como puerta (decisión del responsable).

## 5. Verificación tras la promoción (27-oct-2026)
Tras los PR a `staging` y `master` (hasta el #100; las tres ramas quedaron alineadas) se repitieron las pruebas en los ambientes promovidos:

| Ambiente | Aceptación (UAT) | Accesibilidad WCAG 2.2 AA |
|---|---|---|
| DEV | 18/18 | 3/3, 0 violaciones |
| QA | 18/18 | 3/3, 0 violaciones |
| Producción | No se ejecuta (crea y borra datos de prueba) | 3/3, 0 violaciones |

Hallazgos de esta verificación: (1) en QA, la insignia de usuario inactivo del panel de administración tenía contraste insuficiente (3,76:1) y se corrigió (`--destructive` a 4,83:1); (2) el escenario UAT-A03 leía la lista de médicos antes de que el filtro terminara de cargarla (intermitente) y ahora espera a que cargue. Los `/health` de QA y producción responden `ok` y el CI de producción está en verde.

## 6. Cierre
Criterios de salida del plan cumplidos para DEV y QA (aceptación y accesibilidad) y para producción (accesibilidad y salud); el UAT no se corre en producción por diseño.
