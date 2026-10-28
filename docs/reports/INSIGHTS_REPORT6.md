# GitHub Insights Report 6 — Health Access Bridge

> **Fuente:** repositorio `jaquimbayoc7/health-access-bridge` (Git y API de GitHub) · **Corte:** 27 de octubre de 2026
> **Período:** 26 de febrero – 27 de octubre de 2026 (acumulado) · **Anterior:** [Insights Report 4](./INSIGHTS_REPORT4.md) (23-sep) y [Insights Report 5](./INSIGHTS_REPORT5.md) (episodio del modelo local, con adendas hasta el cierre de HU-07g)
> **Estado del proyecto en este corte:** **146 de 146 puntos (100 %)**: proyecto cerrado el 28 de octubre de 2026.

## 1. Resumen
| Indicador | Valor |
|---|---|
| Commits en `develop` | 267 (en 25 días con actividad) |
| Fusiones (merges) | 42 |
| Pull requests | 73 (72 integrados) |
| Issues cerradas / abiertas | 22 / 2 (#10 HU-10 y #13 épica 3) |
| Ramas `develop`, `staging` y `master` | Alineadas hasta el PR #96; el trabajo posterior está en `develop` |
| Puntos de historia | 146 de 146 (los tres momentos al 100 %) |

## 2. Tipos de cambio
Clasificados por el prefijo del mensaje del commit (convención de commits):

| Tipo | Commits | Lectura |
|---|---|---|
| `docs` | 80 | El proyecto es muy documental: manuales, reportes, protocolo de validación, presentación |
| `fix` | 61 | Muchas correcciones, varias halladas por pruebas en ambientes reales (ver §4) |
| `feat` | 56 | Funcionalidades: pacientes, predicción, perfil ICF, dashboard |
| `chore` | 11 | Mantenimiento |
| `ci` | 5 | Flujos de CI/CD |
| `test` | 3 | Pruebas aisladas (la mayoría viaja dentro de `feat` y `fix`) |
| `perf` | 1 | Rendimiento |
| sin prefijo | 8 | Mensajes antiguos o de fusión |

La relación `docs` > `fix` > `feat` es coherente con un Momento 3 dominado por validación, medición y documentación del módulo de IA.

## 3. Avance desde el Insights Report 4
| Hito | Fecha | Resultado |
|---|---|---|
| Servidor propio y catálogo CIF-IA (HU-07a/b) | oct-2026 | Servicio RAG con búsqueda por significado |
| Modelo local descartado (`qwen2.5:3b`) | 6-oct | 24–46 s por sugerencia y peor que la similitud (Insights R5) |
| Modelo mínimo viable `gemma4:e4b` en PC con GPU | 7-oct | ~2,6 s por sugerencia (HU-07f/h) |
| Validación clínica en 3 rondas (HU-07g) | 26-oct | 5 de 6 criterios; el calificador (κ 0,312) no cumple; se acreditan los 3 pts por decisión del responsable |
| Dashboard de análisis y exportación (HU-08) | 26-oct | 10 gráficos, filtros, Excel y PDF |
| Pruebas completas y feedback (HU-09) | 27-oct | UAT 18/18, WCAG 2.2 AA sin violaciones, SUS 81,25 con 10 usuarios |
| Manuales de usuario, técnico y del servicio ICF (HU-10) | 27-oct | Escritos y aprobados por el responsable |
| Documentación final (guía de la profesora) y cierre de HU-10 | 28-oct | Documento en Word con formato ICONTEC y citación APA 7; diagramas C4 y Archify al día; **proyecto cerrado: 146 de 146 puntos** |

## 4. Calidad: qué se midió y qué se encontró
**Pruebas automáticas:** backend 123 (cobertura 90,7 %, el CI exige 80 %), frontend 61, servicio ICF 101 (92 en CI, 9 locales por la licencia del catálogo), E2E 20, *smoke* 7, más 18 escenarios de aceptación bajo demanda. Lint y tipos del frontend en cero errores desde el 27-oct.

**Hallazgos de las pruebas en ambientes reales** (lo que una prueba unitaria no habría visto):
- HU-08: el PDF con gráficos pesaba 19 MB (ahora 220 KB) y el género aparecía duplicado («femenino» y «Femenino»).
- HU-09: 7 grupos de violaciones de accesibilidad (botones sin nombre, contraste del azul primario, jerarquía de títulos, navegación, gráficos); un color de «destructivo» con contraste insuficiente apareció solo en QA, donde había un usuario inactivo.
- HU-09: el Dashboard coloreaba los perfiles 0, 1 y 2 con umbrales de 1 a 10 (defecto funcional).
- HU-09 (usuarios): dos de diez participantes no entendieron los niveles de severidad del perfil ICF; se agregó una guía.

## 5. Lecciones del cierre (errores propios incluidos)
1. **Verificar la fecha antes de rotular.** Eventos del 26-oct se rotularon como 27-oct y hubo que corregir 17 archivos y 4 issues; ahora se comprueba la fecha del sistema.
2. **No reutilizar los casos de diseño para validar.** La tercera ronda clínica usó 24 casos nuevos y reglas escritas antes de ver los datos (Nosek et al., 2018; Cawley y Talbot, 2010).
3. **Un ajuste puede empeorar otro.** El vínculo mental del motor ICF causó 6 de 7 estructuras rechazadas; se documentó como error propio y se recomienda apagarlo.
4. **Una corrección de accesibilidad puede crear otra violación.** Poner `aria-label` a cada sector de los gráficos generó `aria-prohibited-attr`; se detectó en la siguiente ejecución contra DEV y se revirtió. Por eso la prueba de accesibilidad quedó en el repositorio.
5. **Las pruebas de aceptación dejan huella.** El guion UAT deja un usuario desactivado por ejecución en el ambiente donde corre; hay que limpiarlo o correrlo solo donde se pueda.
6. **Probar en el ambiente desplegado.** Varios hallazgos (CORS, contraste con datos reales, tiempos del servicio de IA) solo aparecieron contra DEV y QA.

## 6. Riesgos abiertos
| Riesgo | Estado |
|---|---|
| Servicio ICF en un solo PC sin redundancia | Mitigado con el respaldo por similitud; persiste |
| Calificador ICF con concordancia baja (κ 0,312) | El médico lo edita; no se aprueba uso clínico autónomo |
| Sin migraciones de base de datos (`create_all`) | Deuda técnica; recomendado Alembic para cambios de esquema |
| Rendimiento con 200 usuarios simultáneos en plan gratuito (DEUDA-01) | Riesgo aceptado (23-sep-2026), sin escalar la infraestructura; producción usa base de pago |
| Revisión de accesibilidad con lector de pantalla | No se hará por tiempo (decisión del responsable, 27-oct); queda solo la verificación con axe-core y teclado |
| Segunda revisora clínica del motor ICF | No se hará por tiempo (decisión del responsable, 27-oct); no se mide el acuerdo entre profesionales |
| Lint y tipos como puerta del CI | No se exigen (decisión del responsable, 27-oct); están en cero errores pero una regresión no frenaría un despliegue |
| Documentación integral del proyecto (guía de la profesora) | Entregada el 28-oct-2026; el autor debe completar el código estudiantil y revisar las referencias ajenas al `.bib` |

## 7. Cierre
El proyecto se cerró el 28 de octubre de 2026 con 146 de 146 puntos. Se cerraron los issues #10 y #13 y el Milestone 3, se actualizaron la presentación, el backlog, el estado y el plan de liberación, y se retiraron los archivos de IA que el sistema no usa (brief de presentación, evidencias de la herramienta de diagramas la configuración de un proveedor externo de modelos y la del servicio externo de predicción que el código no consume, y se alineó el modelo por defecto del servicio ICF con el de producción). Quedan como recomendaciones abiertas, sin bloquear: calificador del perfil CIF con rango 0 a 4, apagar `ICF_MENTAL_LINK`, una cuarta ronda de validación y más pruebas con usuarios.

## Referencias
- Cawley, G. C. y Talbot, N. L. C. (2010). On over-fitting in model selection and subsequent selection bias in performance evaluation. *Journal of Machine Learning Research, 11*, 2079–2107.
- Nosek, B. A. et al. (2018). The preregistration revolution. *PNAS, 115*(11), 2600–2606.
- Convención de commits: https://www.conventionalcommits.org/es/v1.0.0/
