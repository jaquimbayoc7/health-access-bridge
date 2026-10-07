# Brief para Kimi: presentación del Momento 3 (Trabajo Integrador III) de Health Access Bridge

**Escrito para:** Kimi (IA que generará la presentación en PowerPoint) y, a través de ella, el jurado académico que evalúa el Momento 3.
**Corte de los datos:** 7 de octubre de 2026. Todas las cifras salen del repositorio (`jaquimbayoc7/health-access-bridge`), de GitHub y de mediciones propias; ninguna es inventada.
**Idioma:** español (Colombia). Tono: técnico, claro, honesto sobre lo pendiente.

---

## 0. Instrucciones para Kimi

1. **Crea una presentación de unas 25 diapositivas** (16:9) siguiendo el guion de la sección 4, con **notas del orador** en cada una (2 a 4 frases).
2. **Usa gráficas de apoyo en casi todas las diapositivas**, sobre todo en agilismo, sprints, reportes, insights, decisiones, pruebas y métricas de IA. Los datos de cada gráfica están en bloques `DATOS` dentro de este documento: úsalos tal cual y **no inventes valores**. Si una gráfica necesita un dato que no está, dilo en vez de estimarlo.
3. **Estilo visual: el del frontend de Health Access Bridge** (sección 1): fondo gris muy claro, tarjetas blancas con borde fino y esquinas redondeadas, azul primario, tipografía Inter, íconos de línea, insignias de estado verde/ámbar/rojo.
4. **Honestidad por encima de todo.** La confiabilidad clínica del módulo de IA **aún no está validada por un profesional** (pendiente de la reunión de la próxima semana). Dilo con claridad donde corresponda; no presentes las cifras de precisión como confiabilidad clínica.
5. **No uses datos personales** en ninguna imagen. Todos los casos de prueba son sintéticos.
6. Donde el guion pide **captura de pantalla**, deja un marcador visible con el texto «[CAPTURA: …]» para que el autor la inserte (la sección 9 lista las capturas).
7. Cada diapositiva de evidencia debe terminar con una línea pequeña **«Fuente»** con el archivo o la URL del repositorio.
8. Máximo 6 líneas de texto por diapositiva; el detalle va a las notas del orador.

---

## 1. Estilo visual (tomado del frontend)

| Elemento | Valor |
|---|---|
| Tipografía | **Inter** (300 a 800). Títulos 700, texto 400/500 |
| Fondo de diapositiva | `#F6F7F9` (gris muy claro); portada y cierre: degradado azul `#3C83F6` → `#1D4ED8` con texto blanco |
| Tarjetas | blanco `#FFFFFF`, borde `#E5E7EB` de 1 px, radio 12 px, sombra muy suave |
| Texto principal / secundario | `#2B303B` / `#676F7E` |
| Color primario (acentos, botones, líneas) | `#3C83F6` (hover `#2563EB`) |
| Éxito / completado | `#21C45D` |
| Advertencia / en curso / pendiente | `#F59F0A` |
| Error / riesgo | `#EF4343` |
| Paleta de gráficas, en este orden | `#3C83F6`, `#21C45D`, `#F59F0A`, `#AF57DB`, `#E23670` |
| Color del Momento 3 / HU-07 | cian `#06B6D4` (como en la página oficial) |
| Colores por momento | M1 verde `#21C45D` · M2 azul `#3C83F6` · M3 cian `#06B6D4` |
| Íconos | estilo línea (Lucide): clipboard-list (Perfil Funcional), shield (privacidad), gauge (latencia), zap (energía), git-branch, check-circle |
| Estados | ✅ verde · 🟡 ámbar · 📋 gris |
| Gráficas | líneas de 3 px, barras con esquina redondeada, cuadrícula `#F1F5F9`, sin 3D; el valor sobre cada barra; **un mensaje por gráfica como título** |

La página oficial del proyecto (`docs/presentation/index.html`, publicada en `health-access-bridge.onrender.com/presentation`) usa este mismo estilo y sirve de referencia visual.

---

## 2. Mapa de la rúbrica a las diapositivas

| Criterio de la rúbrica | Diapositivas |
|---|---|
| Aplicación eficiente y eficaz de prácticas ágiles (avance vs. resultados esperados) | 3, 4, 5, 6 |
| Prácticas ágiles de **planeación y diseño** (solo sprints de esta entrega; qué se modificó) | 7, 8, 9 |
| Prácticas ágiles de **desarrollo** | 10, 11 |
| Prácticas ágiles de **control y seguimiento** | 12, 13 |
| Prácticas ágiles de **aseguramiento de calidad** | 14, 15, 16 |
| **CI/CD** (opcional) | 17 |
| **Avance en la integración de servicios** | 18 |
| **Evidencia de servicios funcionando** (inteligentes integrados; avance entre 65 % y 100 %) | 19, 20 |
| **Métricas, políticas y consideraciones de la IA** (ética, costo, eficiencia, latencia, precisión, energía) | 21, 22, 23, 24 |
| **Optimización y ajustes** a los servicios inteligentes | 25 |
| Decisiones importantes, riesgos, pendientes y cierre | 26, 27, 28, 29 |

**Avance del proyecto: 80,1 % (117 de 146 pts)**, dentro del rango de 65 % a 100 % que pide la rúbrica.

---

## 3. Datos maestros (referencia para todas las gráficas)

### 3.1 Proyecto en una vista

| Dato | Valor |
|---|---|
| Producto | Plataforma web para médicos: registran pacientes con discapacidad (zonas rurales de Colombia), predicen su perfil de barreras de acceso (modelo híbrido K-Means + Gradient Boosting sobre las dimensiones D1 a D6) y, desde el Momento 3, **sugieren códigos CIF** para el perfil de funcionamiento (Resolución 1239 de 2022, Anexo Técnico) con IA local |
| Metodología | SCRUM, 27 semanas, 3 Momentos, 146 story points |
| Equipo | Un desarrollador (Product Owner y Dev Team) + médicos entrevistados como stakeholders; una profesional de salud como revisora clínica del Momento 3 |
| Ambientes | DEV (`develop`), QA (`staging`), PROD (`master`) en Render; el servicio de IA corre en un PC propio |
| Repositorio | 249 commits en `master` (rama oficial; 56 son merges de promoción), 22 días activos, 26 feb a 7 oct 2026; 55 PRs mergeados; 74 issues y PRs cerrados |

### 3.2 Avance por Momento

```
DATOS avance_por_momento (barras apiladas)
momento,        completados, pendientes, total
M1 (sem 1-9),   63,          0,          63
M2 (sem 10-18), 24,          0,          24
M3 (sem 19-27), 30,          29,         59
TOTAL,          117,         29,         146   -> 80,1 %
```

### 3.3 Release Plan (línea de tiempo)

```
DATOS release_plan (diagrama de Gantt por semanas)
release,                       semanas, puntos, estado,          epica,  milestone
R1 MVP Clínico,                1-9,     63,     entregado,       #11,    1 (cerrado)
R2 Usabilidad y Calidad,       10-18,   24,     entregado,       #12,    2 (cerrado)
R3 IA Generativa y Cierre,     19-27,   59,     en progreso 51 %,#13,    3 (abierto)
```

Contenido de cada release:
- **R1 (63 pts):** HU-01 autenticación y roles (8), HU-02 pacientes (13), HU-03 integración y despliegue (5), HU-04 modelo predictivo (21, adelantada), HU-11 smoke tests (3), HU-12 pruebas de backend (5), HU-13 pruebas de UI (8).
- **R2 (24 pts):** HU-05 mejoras de usabilidad HCI (13), HU-05b ayuda traducida (3), HU-06 pruebas de integración y rendimiento (8). Hallazgo: prueba de carga con p95 = 54,6 s (200 usuarios) → DEUDA-01 cerrada con riesgo aceptado.
- **R3 (59 pts):** HU-07 Perfil Funcional ICF (33), HU-08 dashboard y exportación (13), HU-09 pruebas completas y feedback (8), HU-10 despliegue final y manuales (5).
- **Criterios de salida de R3:** servidor de IA operativo y accesible solo por túnel autenticado; confiabilidad clínica medida con un profesional; el médico acepta, edita o rechaza cada código y el reporte es un borrador de apoyo; dashboard exportable; UAT documentada; despliegue final con manuales.
- **Estrategia de ambientes:** `develop` → `staging` → `master`; DEV y QA se despliegan automáticamente, PROD con aprobación manual y pruebas smoke posteriores.

### 3.4 Sprints reales y velocity

```
DATOS velocity (barras: completados vs planificados)
sprint,                semanas_plan, completados, planificados
Sprint 1,              4-5,          8,           8
Sprint 2,              6-7,          13,          13
Sprint 3,              8-9,          26,          26      (HU-03 5 + HU-04 21, esta adelantada)
Sprint 3.5,            9,            16,          16
Sprint 4-5 (adelant.), 10-13,        21,          21      (HU-04 ya entregada en Sprint 3; NO suma dos veces)
Sprint 6-7,            14-17,        16,          16
Sprint 7,              16-17,        8,           8
Sprint 8 (deuda),      -,            0,           0       (DEUDA-01: deuda técnica, sin puntos de producto)
Sprint 8-9 (en curso), 19-22,        30,          33      (HU-07; falta 07g = 3 pts)
```
Velocidad promedio de los sprints cerrados de M1 y M2: 14,5 SP por sprint (87 pts en 6 sprints).

```
DATOS burndown_proyecto_completo (146 pts; línea real, plan restante e ideal)
punto,             real, plan, ideal
Inicio,            146,  ,     146,0
Fin S1,            138,  ,     134,8
Fin S2,            125,  ,     123,5
Fin S3,            99,   ,     112,3
Fin S3.5,          83,   ,     101,1
Fin S4-5 (meseta), 83,   ,     89,8
Fin S6-7,          67,   ,     78,6
Fin S7,            59,   ,     67,4
Fin S8 (deuda),    59,   ,     56,2
S8-9 (hoy),        29,   29,   44,9
Fin S8-9,          ,     26,   33,7
Fin S10-11,        ,     13,   22,5
Fin S11,           ,     5,    11,2
Fin S12,           ,     0,    0
```
Lectura: el burndown real baja por debajo de la línea ideal desde el Sprint 3 y el Sprint 8-9 es el mayor tramo de avance (30 pts). Las mesetas (S4-5 y S8) se explican: HU-04 se entregó antes y DEUDA-01 no suma puntos. El plan restante (línea punteada) es una proyección, no un dato real.

### 3.5 Commits (de `git log develop`)

```
DATOS commits_por_dia (barras, días con actividad)
2026-09-11: 12   2026-09-18: 17   2026-09-23: 12   2026-09-24: 1
2026-10-05: 35   2026-10-06: 35   2026-10-07: 23
(Antes de septiembre: feb-jun, 114 commits en 15 días activos; total 249 en 22 días. El 6 y 7 de octubre incluyen los merges de promoción.)

DATOS commits_por_tipo (dona; total 249)
docs 62 · fix 58 · merge 56 · feat 52 · chore 10 · ci 5 · otros 6 (test 2, perf 2, sin prefijo 2)

DATOS comparativo_reportes_insights (líneas o barras; R6 = 7 oct)
metrica,                     R1(20 mar), R2(16 abr), R3(18 sep), R4(23 sep), R5(6 oct), hoy(7 oct)
Commits totales,             43,         65,         128,        146,        221,       249
Issues + PRs numerados,      13,         16,         16,         19,         59,        80
Story points completados,    47,         63,         87,         87,         100,       117
Avance del proyecto (%),     40,9,       48,1,       64,9,       64,9,       68,5,      80,1
Tests (backend+front+ICF),   32,         53,         60,         60,         136,       218
PRs mergeados (acumulado),   0,          0,          0,          3,          42,        55
Servicios desplegables,      2,          2,          2,          2,          3,         3
```
Nota: el total del proyecto subió de 134 a 146 pts por la reestimación de HU-07 (21 → 25 → 33), no por trabajo nuevo fuera de ella; el avance de R4 sobre 146 pts sería 59,6 %.

### 3.6 Pruebas

```
DATOS pruebas (barras por capa)
capa,                        pruebas, en_CI
Backend (pytest),            105,     105
Frontend (Vitest + RTL),     38,      38
Servicio ICF (pytest),       75,      67   (8 necesitan el catálogo local, con derechos de la OMS)
E2E (Playwright),            12,      12   (5 son del Perfil Funcional ICF; login real, servicio ICF simulado)
Smoke (CI/CD),               7,       7
TOTAL,                       237,     229
```
Cobertura del backend: 89 %. Casos documentados en estándar Gherkin: 53 del Momento 1 y las suites 8 a 11 de HU-07 (`docs/reports/TEST_CASES.md`).

```
DATOS pruebas_nuevas_en_M3 (barras)
backend +53 (52 → 105) · frontend +22 (16 → 38) · servicio ICF +75 (nuevo) · E2E +5 (7 → 12)
```

### 3.7 Defectos encontrados (por las pruebas y revisiones)

| # | Defecto | Cómo se detectó | Corrección |
|---|---|---|---|
| 1 | El filtro por categoría se aplicaba después de buscar: el caso solo psicosocial no devolvía funciones | Revisión de salidas reales | Filtro dentro de la búsqueda |
| 2 | Códigos «otros» y «no especificados» entre los candidatos | Revisión de salidas | Se excluyen los códigos terminados en 8 y 9 |
| 3 | Una ruta nueva de Caddy podía quedar sin pedir el token (servicio expuesto) | Prueba de comportamiento del túnel | Bloque `route`; probado con Caddy real |
| 4 | Un token del túnel quedó expuesto y el túnel apuntaba directo a Ollama sin autenticación | La prueba «el token viejo aún funciona» | `tailscale funnel reset`, token rotado, prueba fija sin token / token falso / token correcto |
| 5 | Tiempo de espera de 20 s cortaba sugerencias de 40 a 55 s | Medición de latencia | Espera de 90 s en el backend |
| 6 | Gemma 4 devolvía el JSON en bloque de código y «razonaba» antes de responder: 21 de 21 casos caían al respaldo **sin avisar** | El script advirtió; se leyó antes de comparar tablas | Parser de bloques de código y `think=false` (resultado: 100 % de JSON válido) |
| 7 | El archivo de secretos se creó dentro de una carpeta sincronizada con la nube | Revisión antes de usarlo | Se borró, se movió fuera de OneDrive y se regeneraron las claves |
| 8 | Ollama rechazaba (403) por la vía pública porque exige un `Host` local | `check.ps1` pública | `header_up Host` en Caddy |
| 9 | E2E intermitente por el modal de onboarding (Sprint 8, deuda) | CI | Corregido; 7/7 en dos corridas limpias |
| 10 | Cifras de la presentación desalineadas del repositorio (sprints, commits, HU) | Auditoría pedida por el propietario | Corregidas y verificadas |

### 3.8 Decisiones importantes (línea de tiempo)

| Fecha | Decisión | Por qué |
|---|---|---|
| 23-sep | Cerrar DEUDA-01 aceptando el riesgo de rendimiento; activar flujo de PR y protección de rama | La causa raíz era CPU fraccional y bcrypt; escalar tenía costo recurrente |
| 23-sep | IA con Ollama y un modelo de pesos abiertos, sin APIs de pago | Costo cero y datos de salud sensibles |
| 05-oct | HU-07 pasa a **RAG sin fine-tuning** y se ajusta al Anexo de la Resolución 1239 (21 → 25 pts) | No hay datos etiquetados; el Anexo exige máximo 3 códigos por componente, estructuras con 3 calificadores y calificador por reglas |
| 06-oct | **Se descarta Qwen 3B** (peor que la similitud y 24 a 46 s) | Medición en el servidor físico |
| 06-oct | **Se descarta un modelo externo por API** (se evaluó Claude) y se prueban Gemma 4 y MedGemma locales; HU-07 sube a 33 pts | Privacidad (Ley 1581 de 2012): ningún dato clínico sale de la infraestructura propia |
| 07-oct | **`gemma4:e4b` como modelo mínimo viable** | Única opción que supera claramente a la similitud |
| 07-oct | **Producción en el PC propio** (RTX 5050 de 8 GB), sin comprar hardware | Cumple el mínimo medido; no hay presupuesto |
| 07-oct | **MedGemma no se usa**; Gemma 4 sí (Apache 2.0) | Verificación de licencias: MedGemma prohíbe el uso clínico |
| 07-oct | **Umbrales de validación clínica aprobados** y revisión con a ciegas | Evitar sesgo de anclaje de la revisora |

---

## 4. Guion de diapositivas

> Formato: **Título** · Mensaje · Contenido · Gráfica · Evidencia/Fuente. Las notas del orador las redacta Kimi a partir de este contenido.

### 1. Portada
Health Access Bridge · Momento 3: Trabajo Integrador III · «Perfil Funcional ICF con IA local, privada y trazable». Autor: @jaquimbayoc7 · Octubre 2026. Insignias: M1 ✅ · M2 ✅ · M3 🟡 · 80,1 %.

### 2. Qué se entrega hoy (agenda y rúbrica)
Mapa de la sección 2 en forma de tabla de 10 criterios con íconos. Gráfica: ninguna (tabla).

### 3. Resumen ejecutivo
Mensaje: «80,1 % del proyecto, con la IA ya integrada y privada». KPIs en tarjetas: 117/146 pts · 30/59 pts de M3 · 237 pruebas · 229 en CI · ~2,6 s por sugerencia · 0 USD en APIs. Gráfica: **anillo de avance** (117 hechos, 29 pendientes).

### 4. Release Plan (R1, R2, R3)
Mensaje: «Tres releases, dos entregadas y la tercera al 51 %». Gráfica: **Gantt por semanas** con los datos de 3.3, cada barra con su porcentaje. Contenido: puntos y HU por release (viñetas cortas).

### 5. Avance real frente a lo esperado
Gráfica: **barras apiladas** de 3.2 (completados / pendientes por Momento). Mensaje: M1 y M2 cerrados al 100 %; M3 en 30 de 59. Línea: el total del proyecto creció de 134 a 146 pts por la reestimación de HU-07.

### 6. Prácticas ágiles aplicadas
Mensaje: «SCRUM adaptado a un equipo unipersonal, con evidencia verificable». Tabla roles / eventos / artefactos (Product Owner redacta HUs en `BACKLOG.md`; Planning = estimación en SP con Planning Poker informal; Review = HU demostrada desplegada en DEV/QA/PROD; Retro = hallazgos documentados en reportes de insights por cierre; artefactos: Product Backlog, DoR, DoD, Release Plan, burndown, velocity). Gráfica: **rueda o diagrama de ciclo** Planificar → Desarrollar → Probar → Desplegar → Revisar. Fuente: `docs/reports/AGILE_PRACTICES.md`.

### 7. Planeación (1): backlog, DoR y DoD
Mensaje: «Una HU entra a un sprint solo si cumple la Definition of Ready». Viñetas: formato Como/Deseo/Para, criterios de aceptación, estimación acordada, sin dependencias bloqueantes, DoD explícito. Priorización por dependencia técnica, valor clínico y riesgo de usabilidad. Gráfica: **embudo o tablero Kanban** (Done / En progreso / Backlog) con el estado de hoy: 9 HU hechas, HU-07 en curso, HU-08 / 09 / 10 por hacer. Fuente: `BACKLOG.md`.

### 8. Planeación (2): qué se modificó en esta entrega
Mensaje: «El plan cambió porque medimos, no porque improvisamos». Gráfica: **línea de reestimación de HU-07** (21 → 25 → 33 pts) con el total del proyecto (134 → 138 → 146) y del M3 (47 → 51 → 59) como segunda serie. Viñetas: 05-oct revisión del Anexo 1239 (+4); 06-oct pruebas con servidor físico (+2 escalera de modelos, +3 validación clínica, +3 despliegue en PC propio). Se dividió HU-07 en 8 sub-historias (07a a 07h) y se crearon sus issues #65 a #72.

### 9. Diseño de la solución de IA
Mensaje: «RAG con lista cerrada: el modelo solo puede elegir entre códigos del catálogo». Diagrama de flujo (ver sección 6, «Arquitectura»): datos del paciente → reglas (calificador, capítulos, máximo 3) → búsqueda en el catálogo CIF-IA (1.593 códigos, embeddings `bge-m3`, PostgreSQL + pgvector) → modelo local elige entre 12 candidatos → título desde el catálogo → médico acepta, edita o rechaza. Gráfica: **diagrama de bloques** con colores: reglas (azul), búsqueda (verde), modelo (morado), decisión humana (ámbar). Fuente: `docs/diagrams/rag-icf-postgresql.md`.

### 10. Desarrollo (1): sprints de esta entrega
Mensaje: «Dos sprints: uno de deuda técnica y uno de HU-07». Tabla: **Sprint 8 (deuda técnica, 23 a 24 sep):** DEUDA-01 (carga repetida a 30 usuarios, causa raíz CPU/bcrypt), flujo de PR y protección de rama (#18, #19), verificación de `package-lock.json` en CI, sincronización de ramas, corrección de E2E intermitente. **Sprint 8-9 (semanas 19 a 22; desde el 5 de octubre):** HU-07a a 07h. Gráfica: **barras horizontales de las sub-historias de HU-07** (puntos y estado) con las fechas de cierre:
```
DATOS hu07_subhistorias
sub,  pts, estado,                     cierre
07a,  5,   hecha,                      06-oct
07b,  8,   hecha,                      06-oct
07c,  5,   hecha,                      07-oct
07d,  5,   hecha,                      07-oct
07e,  2,   hecha,                      07-oct
07f,  2,   hecha,                      07-oct
07g,  3,   instrumento listo, falta revisión clínica
07h,  3,   hecha,                      07-oct
TOTAL 33 → 30 completados
```

### 11. Desarrollo (2): cómo se trabaja el código
Mensaje: «Commits convencionales, ramas por ambiente y pruebas con cada cambio». Gráficas: **barras de commits por día** y **dona de commits por tipo** (3.5). Viñetas: `develop` → `staging` → `master`; plantilla de PR; commits `feat/fix/docs/test/ci`; el servicio de IA como segundo servicio con su propia base y pruebas (~2.400 líneas de Python al 6-oct). Dato de proceso honesto: gran parte de los commits de `develop` se hicieron directo con el bypass del propietario.

### 12. Control y seguimiento (1): backlog, issues y milestones
Mensaje: «GitHub refleja el avance real». Contenido: milestone 1 (7 issues) y 2 (4) cerrados; milestone 3 con 8 abiertos y 5 cerrados al corte de la auditoría, luego actualizado (07e y 07h cerrados el 7-oct); sub-historias 07a a 07h como issues #65 a #72; épica #13 con el 51 %. Gráfica: **tablero Kanban** o barras de issues cerrados / abiertos por milestone. **Captura:** [CAPTURA: milestones y lista de issues de GitHub]. Hallazgo de seguimiento corregido: el milestone del M3 marcaba 0 % cuando había 13 pts hechos.

### 13. Control y seguimiento (2): burndown, velocity y reportes de insights
Gráficas: **burndown del proyecto completo** y **velocity por sprint** (3.4); al pie, **línea comparativa de los reportes R1 a hoy** (3.5: story points y avance %). Mensaje: «Cinco reportes de insights muestran la trayectoria: de 40,9 % a 80,1 %». Viñetas: los reportes también registran correcciones retrospectivas (el R5 corrige una decisión del R4 tomada antes de medir). Fuente: `docs/reports/INSIGHTS_REPORT*.md`, `PROJECT_STATUS_M3.md`.

### 14. Calidad (1): estrategia y pirámide de pruebas
Gráfica: **pirámide** (base: 105 backend + 75 servicio ICF + 38 frontend; medio: 12 E2E; punta: 7 smoke) con el total 237 y 229 en CI. Viñetas: Gherkin (suites 8 a 11 para HU-07), cobertura del backend 89 %, casos de referencia sintéticos, E2E con el servicio ICF simulado (determinista) más verificación real en QA con `/icf/health`.

### 15. Calidad (2): defectos encontrados y corregidos
Mensaje: «La calidad se mide leyendo las salidas reales». Tabla compacta de la sección 3.7 (elegir los 6 más ilustrativos: 1, 3, 4, 6, 7, 8). Gráfica: **barras de defectos por origen** (revisión de salidas 2; prueba de comportamiento 2; medición 1; script/advertencia 1; revisión previa 1; chequeo público 1; CI 1; auditoría 1). Lección destacada: el defecto 6 parecía «un modelo igual a la similitud» y era un fallo silencioso.

### 16. Calidad (3): validación clínica de la IA (con el profesional de salud)
Mensaje: «Medimos con una profesional, a ciegas, con umbrales definidos de antemano». Contenido: hoja de revisión con 24 casos sintéticos; **Fase A a ciegas** (la revisora escribe los códigos que elegiría sin ver la sugerencia) y **Fase B** (valora cada código: Adecuado / Aceptable / No adecuado, calificador correcto y faltantes). Gráfica: **«medidores» (gauge) de los umbrales aprobados** (precisión estricta ≥ 60 %, flexible ≥ 80 %, cobertura a ciegas ≥ 60 %, calificadores ≥ 80 %, casos revisados ≥ 20 de 24) con la etiqueta **«pendiente: reunión con la revisora la próxima semana»**. Estado: instrumento listo, 5 pruebas automáticas, resultado por llegar. **No presentar cifras clínicas.** Fuente: `docs/reports/PROTOCOLO_VALIDACION_CLINICA_HU07G.md`.

### 17. CI/CD
Mensaje: «Cada push pasa por el pipeline; producción exige aprobación». Gráfica: **diagrama del pipeline**:
`push` → GitHub Actions → `backend-test` (105 pruebas) → `icf-service-test` (67) → `frontend-build` (38 pruebas + build) → (QA) deploy por hook a Render → smoke tests (4) → E2E Playwright → **compuerta de aprobación manual** → PROD: smoke tests (3). Viñetas: 3 workflows (`ci-dev`, `ci-qa`, `ci-prod`), protección de rama con 2 checks requeridos, verificación de sincronía de `package-lock.json`, el job `icf-service-test` se agregó en esta entrega. **Captura:** [CAPTURA: GitHub Actions con las corridas en verde].

### 18. Integración de servicios
Mensaje: «Tres servicios y una IA local conectados por un túnel autenticado». Diagrama de arquitectura (sección 6). Tabla de servicios: frontend (Render), backend (Render), servicio ICF (PC propio), Ollama (modelos), PostgreSQL con pgvector, Caddy (token), Tailscale Funnel (túnel). Endpoints: `POST` y `GET /patients/{id}/icf-suggestions`, `PATCH /icf/suggestions/{id}`, `GET /icf/causes`, `GET /icf/health` (solo administrador); servicio: `POST /suggest`, `GET /health`.

### 19. Evidencia: servicios funcionando
Mensaje: «De la pantalla del médico hasta el modelo local, funcionando». **Capturas** (ver sección 9): [CAPTURA: pantalla Perfil Funcional ICF con códigos b, s y d], [CAPTURA: salida de `check.ps1 -Public -Suggest` con «Todo correcto.»], [CAPTURA: `/icf/health` en QA], [CAPTURA: Render con los tres ambientes en verde]. Dato: E2E 5/5 contra el frontend DEV; verificación en QA hecha por el responsable.

### 20. La pantalla del Perfil Funcional ICF
Contenido: el médico elige paciente, escribe diagnóstico CIE y notas (con enlaces a la CIE-10 y ejemplos sintéticos), genera, y acepta / edita / rechaza cada código; el reporte se copia o se descarga en PDF con la leyenda «borrador de apoyo». Guía de uso en la Guía Predictiva (dos secciones) y avance en Ayuda. **Captura:** [CAPTURA: pantalla con enlaces CIE y ejemplos] y [CAPTURA: Guía Predictiva, pestaña Perfil Funcional ICF].

### 21. IA responsable (1): ética y privacidad
Mensaje: «Ningún dato clínico sale de la infraestructura propia». Lista con íconos (shield): (1) **no viajan** nombre, documento ni orientación sexual (lista blanca; el servicio rechaza campos no previstos; hay prueba automática); (2) **sin APIs externas** (Ley 1581 de 2012); (3) el modelo **solo elige de una lista cerrada** y los **títulos salen del catálogo**; (4) **decisión humana**: cada código queda «sugerido» hasta que el médico lo acepta, edita o rechaza, con el modelo que lo sugirió; (5) **leyenda de borrador de apoyo** y cita de la Resolución 1239; (6) **licencias verificadas**; (7) catálogo de la OMS no se publica; (8) secretos fuera del repositorio; (9) límites declarados: HAB captura 2 de las 7 categorías de discapacidad; menores de 6 años no aplica. Gráfica: **diagrama de flujo de datos** marcando en rojo lo que nunca sale y en verde lo que viaja.

### 22. IA responsable (2): costo y energía
Mensaje: «Costo variable cero y energía medida». Datos:
```
DATOS costo_y_energia
Costo de APIs de IA: 0 USD (modelo local de código abierto, Apache 2.0)
Hardware: el PC existente (i5-13450HX, 32 GB, RTX 5050 de 8 GB); sin compra de hardware
Energía medida (GPU, 14 casos de prueba, 50,9 s en total, incluye carga inicial del modelo):
  potencia en reposo 4,4 W · potencia media 38,4 W · pico 75 W · utilización media de la GPU 45 %
  energía ≈ 0,54 Wh para 13 sugerencias → ≈ 0,042 Wh por sugerencia (solo GPU; cota superior)
  equivalencia: ≈ 24 sugerencias por Wh; 1.000 sugerencias ≈ 42 Wh
```
Gráfica: **barras de potencia** (reposo 4,4 W · media 38,4 W · pico 75 W) y un indicador «0,042 Wh por sugerencia». Aclarar: no incluye CPU ni el resto del equipo. Alternativas de nube no se costearon porque no se verificaron precios, y se descartaron por privacidad.

### 23. IA responsable (3): latencia y eficiencia
Gráfica 1: **barras de latencia por configuración** (log opcional):
```
DATOS latencia_segundos
configuracion,                              segundos
Qwen 3B v1 en servidor i3 (sin GPU),        55,6
Qwen 3B rediseñado (d sin modelo),          22,9
Qwen 3B modo rápido (i3),                   24,0
Qwen 3B modo calidad (i3),                  46,0
Similitud sola (i3, sin modelo),            0,6
Gemma 4 e4b solo CPU, rápido,               9,3
Gemma 4 e4b solo CPU, calidad,              15,3
Gemma 4 e4b GPU, rápido,                    2,5
Gemma 4 e4b GPU, calidad (modo elegido),    3,4
Producción, modelo en memoria,              2,6
Producción, primer pedido tras 30 min,      18,0
```
Gráfica 2: **concurrencia en producción** (línea): 1 médico 2,6 s · 3 a la vez hasta 7,2 s · 5 a la vez hasta 11,6 s. Datos de eficiencia: ~471 tokens de entrada y ~230 de salida por sugerencia; el modelo ocupa ~4,6 GB de VRAM y 6,6 GB en disco; 100 % de JSON válido y 0 códigos fuera del catálogo en la corrida del 7-oct (13 casos): p50 2,5 s, p95 4,8 s, media 3,8 s (incluye un arranque en frío de 18,8 s).

### 24. IA responsable (4): precisión de las respuestas
Mensaje: «Un modelo más grande no bastó: ganó el generalista de tamaño medio». Gráfica: **barras agrupadas** de precisión y cobertura:
```
DATOS precision_modelos (21 casos con pistas orientativas, NO validadas por un médico)
modelo / modo,            funciones_precision, funciones_cobertura, estructuras_precision, estructuras_cobertura, latencia_s
Similitud sola,           29,                  25,                  25,                    67,                    0,1
Qwen 3B calidad,          19,                  16,                  26,                    67,                    8,6
MedGemma 4B calidad,      30,                  26,                  28,                    76,                    4,9
Gemma 4 e2b calidad,      32,                  27,                  28,                    76,                    2,3
Gemma 4 e4b rápido,       33,                  29,                  28,                    76,                    2,5
Gemma 4 e4b calidad,      43,                  37,                  32,                    86,                    3,4
```
Advertencia visible: «Estas cifras comparan modelos entre sí con pistas orientativas; **no son la confiabilidad clínica**, que se mide con la revisora». Ganancia de `gemma4:e4b` frente a la similitud: +14 puntos de precisión en funciones y +19 de cobertura en estructuras.

### 25. Optimización y ajustes a los servicios inteligentes
Mensaje: «Cada ajuste se decidió con una medición». Gráfica: **cascada o barras antes/después**:
```
DATOS optimizaciones
ajuste,                                              antes,                         despues
Actividades (d) sin modelo + prompt corto,           55,6 s y 773 tokens de entrada, 22,9 s y 348 tokens
Buscar solo códigos de 3 dígitos (cobertura @12),    funciones 19 %, estructuras 48 %, funciones 40 %, estructuras 86 %
Filtro por categoría dentro de la búsqueda,          caso psicosocial sin funciones, resuelto
Excluir códigos «otros/no especificados»,            sugerencias sin contenido,      resuelto
Cambio de modelo y equipo (Qwen 3B/i3 → Gemma 4 e4b/GPU), 46 s y 19 % precisión,    3,4 s y 43 % precisión
Interpretar bloque de código y think=false,          0 de 21 respuestas válidas,    100 % de JSON válido
Modelo en memoria 30 min (keep_alive),               arranque en frío ~18 s,        ~2,6 s
Espera de 90 s y 503 con aviso + respaldo por similitud, corte a los 20 s,          sin caídas visibles para el médico
```
Viñetas: modo `rápido` y `calidad` configurables; el modelo se cambia con una variable de entorno sin tocar código.

### 26. Toma de decisiones importantes
Gráfica: **línea de tiempo** con las 9 decisiones de la sección 3.8, cada una con su motivo y el dato que la sustenta (por ejemplo, 06-oct: 24 a 46 s y peor que la similitud → se descarta Qwen). Mensaje: «Las decisiones se corrigieron con datos, y quedaron registradas».

### 27. Riesgos y lecciones aprendidas
Tabla de riesgos (de `RELEASE_PLAN.md`) con semáforo: rendimiento de API (cerrado, riesgo aceptado), latencia del modelo (resuelto), calidad de modelos pequeños (mitigado), privacidad (mitigado por diseño y licencias), producción en PC propio (operando; sin redundancia), cobertura parcial del Anexo (mitigado), confiabilidad clínica (🟡 pendiente de validación), encuadre regulatorio como dispositivo médico (🟡 por consultar). **Lecciones:** (1) leer las salidas reales antes de comparar tablas; (2) verificar licencias antes de elegir un modelo; (3) un modelo mayor o «médico» no garantiza mejor resultado; (4) agrupar las promociones de rama; (5) probar el túnel con y sin token como paso fijo. Gráfica: **matriz de riesgo** (impacto vs. probabilidad) con los puntos coloreados por estado.

### 28. Pendientes y próximos pasos
Mensaje: «Falta la validación clínica y las tres HU finales». Lista: reunión con la revisora la próxima semana (entregar la hoja, presentar los umbrales); promoción `develop` → `staging` → `master`; HU-08 dashboard y exportación (13 pts); HU-09 pruebas completas y feedback (8); HU-10 despliegue final y manuales (5); consulta regulatoria (INVIMA). Gráfica: **barras de los 29 pts pendientes** (07g 3, HU-08 13, HU-09 8, HU-10 5) y proyección del burndown hasta el Sprint 12 (semana 27).

### 29. Conclusiones
Cuatro mensajes: (1) 80,1 % del proyecto y las dos primeras releases cerradas; (2) IA integrada, local y privada, medida en latencia (~2,6 s), costo (0 USD) y energía (~0,042 Wh); (3) calidad respaldada por 237 pruebas, CI/CD y defectos corregidos con evidencia; (4) honestidad: la confiabilidad clínica se mide la próxima semana con una profesional. Cierre con enlaces: repositorio, página oficial, frontend en producción.

---

## 5. Evidencia ágil por categoría (texto de apoyo, solo sprints de esta entrega)

**Planeación y diseño:** reestimación de HU-07 en dos pasos con su motivo (Anexo 1239; pruebas con el servidor físico); división en sub-historias 07a a 07h con issues enlazados, dependencias y estimación; DoR y DoD en cada una; decisión de arquitectura documentada (`docs/diagrams/rag-icf-postgresql.md`, con historial de decisiones corregidas); plan de pruebas de modelos y protocolo de validación clínica definidos antes de ejecutar.

**Desarrollo:** commits convencionales; ramas `develop` / `staging` / `master`; servicio de IA con pruebas unitarias y de integración; backend con endpoints versionados por contrato (Pydantic con `extra=forbid`); frontend con pantalla, guía y ayuda bilingües (español e inglés); scripts de evaluación y comparación de modos reproducibles.

**Control y seguimiento:** `BACKLOG.md` como fuente de verdad; issues #65 a #72 y épica #13 actualizados; milestones 1 y 2 cerrados; burndown, velocity y reportes de insights; estado del Momento 3 (`PROJECT_STATUS_M3.md`); auditoría de coherencia entre GitHub, repositorio y página oficial; documento de pendientes para retomar (`docs/PENDIENTES_PROXIMA_SESION.md`).

**Aseguramiento de calidad:** 237 pruebas; Gherkin; E2E; revisión de salidas reales; pruebas de comportamiento del túnel; validación clínica a ciegas con umbrales aprobados; verificación de licencias; lint, `tsc` y build sin errores en los archivos de HU-07 (5 errores de lint heredados, fuera de esta entrega).

**CI/CD:** 3 workflows; protección de rama; compuerta de aprobación a producción; despliegues automáticos en DEV y QA; smoke tests; job nuevo `icf-service-test`.

---

## 6. Arquitectura (para el diagrama de las diapositivas 9 y 18)

```
Médico (navegador)
  └─▶ Frontend React (Render: DEV / QA / PROD)
        └─▶ Backend FastAPI (Render)  ── guarda sugerencias y decisiones (PostgreSQL)
              └─ HTTPS + token ─▶ Tailscale Funnel ─▶ Caddy (PC propio, exige token; solo /suggest, /health, /api/tags)
                                        ├─▶ Servicio ICF (FastAPI en Docker, sin puerto publicado)
                                        │      ├─ reglas del Anexo 1239 (calificador 0–4, máximo 3 por componente)
                                        │      ├─ PostgreSQL + pgvector (catálogo CIF-IA, 1.593 códigos, embeddings bge-m3)
                                        │      └─ Ollama: bge-m3 (búsqueda) y gemma4:e4b (selección entre 12 candidatos)
                                        └─▶ Ollama /api/tags (diagnóstico)
Respaldo: si el modelo o el equipo no responden, el backend usa la búsqueda por similitud (0,6 s) y el resto de la aplicación sigue funcionando.
```
Qué decide quién: **reglas** (calificador, capítulos, máximo 3, lista cerrada de actividades) · **catálogo** (títulos) · **modelo** (elige funciones y estructuras entre candidatos) · **médico** (acepta, edita o rechaza).

---

## 7. Notas de método para las métricas de IA

- **Latencia:** medida con el motor completo contra Ollama; en producción con 1, 3 y 5 solicitudes simultáneas; la corrida del 7-oct usó 14 casos (13 aplicables).
- **Precisión:** contra 21 casos con «pistas orientativas» (códigos que la lógica de la CIF haría esperar); **no las validó un médico**; los porcentajes absolutos no son confiabilidad clínica. La muestra es pequeña (21 casos, 73 pistas).
- **Energía:** solo GPU, muestreada cada ~0,25 s con `nvidia-smi` durante la corrida de 50,9 s; incluye la carga del modelo y el arranque del contenedor, por eso es una cota superior. No se midió la energía de la CPU ni la del equipo completo (pendiente opcional).
- **Costo:** no se compararon precios de APIs de nube (no se verificaron); el costo variable es la electricidad.
- **Una sola máquina y un solo desarrollador:** las cifras son de este equipo.

## 8. Fuentes en el repositorio

`BACKLOG.md` · `docs/reports/RELEASE_PLAN.md` · `docs/reports/PROJECT_STATUS_M3.md` · `docs/reports/INSIGHTS_REPORT5.md` (con 3 adendas del 7-oct) · `docs/reports/TESTING_REPORT.md` · `docs/reports/TEST_CASES.md` · `docs/reports/PRUEBAS_HU07_SERVIDOR_FISICO.md` · `docs/reports/PRUEBAS_HU07F_MODELOS_ABIERTOS.md` · `docs/reports/PROTOCOLO_VALIDACION_CLINICA_HU07G.md` · `docs/reports/LICENCIAS_COMPONENTES_ICF.md` · `docs/MANUAL_OPERACION_ICF.md` · `docs/diagrams/rag-icf-postgresql.md` · `docs/presentation/index.html` · `docs/presentation/entregable_tecnico_rubrica.html` (entregable análogo del Momento 2) · `.github/workflows/ci-*.yml`.

URLs: repositorio https://github.com/jaquimbayoc7/health-access-bridge · página oficial https://health-access-bridge.onrender.com/presentation · frontend PROD https://hab-frontend.onrender.com · DEV https://hab-frontend-dev.onrender.com · QA https://hab-frontend-qa.onrender.com.

## 9. Capturas que debe reunir el autor (Kimi deja los marcadores)

1. Pantalla **Perfil Funcional ICF** con una sugerencia (b, s, d, calificadores, origen) en DEV o PROD, con un paciente sintético.
2. Pantalla con los **enlaces a la CIE y los ejemplos de notas** desplegados.
3. **Guía Predictiva**, pestaña «Perfil Funcional ICF».
4. Terminal con **`check.ps1 -Public -Suggest`** terminando en «Todo correcto.» (sin mostrar el token).
5. **GitHub Actions** con las corridas en verde de `develop` y `staging` (incluido `icf-service-test`).
6. **GitHub**: milestones, lista de issues #65 a #72 cerrados / abiertos y la épica #13.
7. **Render**: los servicios de los tres ambientes en verde.
8. Gráfica **burndown y velocity** de la página oficial (ya están actualizadas en `docs/presentation/index.html`).
9. Salida de `pytest` (75 del servicio ICF) y de `vitest` (38).
10. `/icf/health` en QA con `configured`, `reachable` y `model_available` en verdadero (sin URL ni token).
11. **Animaciones del proyecto** (opcional, para las diapositivas 9, 18 y 19): videos de 14 s en `docs/presentation/animaciones/video/` (`arquitectura-hab.webm`, `servicio-icf.webm`, `recorrido-medico-pacientes.webm`, `recorrido-medico-icf.webm`, `recorrido-administrador.webm`) y sus versiones interactivas en `docs/presentation/animaciones/index.html`. Muestran la arquitectura completa, el funcionamiento interno del servicio de IA (útil para la diapositiva 9) y los recorridos del médico y del administrador.
