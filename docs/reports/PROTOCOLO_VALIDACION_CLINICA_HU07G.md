# Protocolo de validación clínica del Perfil Funcional ICF (HU-07g)

**Fecha:** 7 de octubre de 2026
**Estado:** revisión **devuelta por la profesional de salud (Emilly Maria Celis) el 26 de octubre de 2026** y segunda ronda sobre las sugerencias nuevas del motor corregido el mismo día. Veredicto del `score`: **NO CUMPLE**, antes por tres criterios y ahora por uno (cobertura 0,582 frente a 0,60; secciones 8 a 11). HU-07g no se acredita; falta decidir los puntos y medir con casos nuevos. **27-oct: reglas de la tercera ronda con casos nuevos fijadas antes de ver las sugerencias (sección 12).**
**Para quién:** la revisora y el responsable del proyecto.

## 1. Qué se mide y por qué

Hasta ahora las cifras de calidad del sistema (por ejemplo, `gemma4:e4b` con 43 % de precisión en funciones frente a 29 % de la búsqueda sola) se calcularon con **pistas orientativas que no validó ningún profesional**: sirven para comparar modelos, no para decir si los códigos son clínicamente adecuados. Esta validación mide eso: **si los códigos de la CIF-IA que sugiere el sistema son los que elegiría una profesional de la salud**, y si el calificador de gravedad es razonable.

El resultado no certifica a nadie. El Perfil Funcional ICF es un borrador de apoyo; el certificado lo emite el equipo multidisciplinario en el RLCPD (Resolución 1239 de 2022).

## 2. Material

| Pieza | Dónde |
|---|---|
| 24 casos sintéticos aplicables (el caso C10, menor de 6 años, no aplica) | `icf-service/reference/cases.json` |
| Hoja de revisión en Excel con la sugerencia actual del sistema (`gemma4:e4b`) | `data/private/icf/review/hoja_revision_v2.xlsx` (la que se entrega: pide la gravedad a ciegas; se obtuvo de `hoja_revision.xlsx` del 9 de octubre con `review_sheet.py upgrade`, con las mismas sugerencias) |
| Generador y calculadora de métricas | `icf-service/scripts/review_sheet.py`, `icf-service/icf/review.py` |
| Repetibilidad del sistema (no requiere a la revisora) | `icf-service/scripts/repeatability.py`, `icf-service/icf/stability.py` |
| Análisis de potencia y agrupamiento (reproduce las tablas de 4.3 y 4.4) | `icf-service/scripts/design_simulation.py` (requiere numpy) |
| Diagrama interactivo del proceso completo con la médica (Archify) | `docs/presentation/animaciones/proceso-validacion-clinica.html` (fuente en `fuentes/proceso-validacion-clinica.json`) |
| Contraste de las funciones estadísticas con scikit-learn y statsmodels | `icf-service/tests/test_review_reference.py` (se omite si no están instaladas; para correrlo: `pip install numpy scikit-learn statsmodels`) |
| Bibliografía (40 entradas; los DOI citados en este protocolo se verificaron contra Crossref y Europe PMC) | `docs/reports/referencias_validacion_clinica.bib` |
| Pruebas automáticas de la lógica y del Excel | `icf-service/tests/test_review.py` |

La hoja **no está en el repositorio**: trae títulos del catálogo CIF-IA, que tiene derechos de la OMS. Se entrega a la revisora por un canal privado y no se publica. Los casos son inventados: no hay datos de personas reales.

## 3. Guía para la revisora (unos 60 a 90 minutos)

1. **Fase A, a ciegas.** En la hoja «Fase A (a ciegas)», para cada caso lea los datos y escriba los códigos de **funciones (b)** y **estructuras (s)** que usted elegiría (máximo 3 por componente, separados por coma) y, tras un punto, la **gravedad de 0 a 4** que les asignaría: por ejemplo `b730.3, b735.2` (0 = sin deficiencia, 1 = leve, 2 = moderada, 3 = grave, 4 = completa). No abra la hoja «Fase B» hasta terminar: ver la sugerencia antes sesgaría su criterio. Si el caso no tiene deficiencia en funciones o estructuras, déjelo vacío.
2. **Fase B, valorar la sugerencia.** En «Fase B (sugerencias)», para cada código elija en las columnas amarillas:
   - *Valoración:* **Adecuado** (lo habría elegido), **Aceptable** (razonable, pero no es el más preciso) o **No adecuado**.
   - *¿Calificador correcto?:* **Sí**, **Parcial** o **No** (la gravedad 0 a 4 asignada). Es un dato secundario: la comparación principal es la gravedad que escribió en la Fase A.
3. **Faltantes.** En la hoja «Faltantes», por caso, escriba los códigos que a su juicio faltan.
4. Guarde con otro nombre (por ejemplo `hoja_revision_llena.xlsx`) y devuélvala.

Qué tener en cuenta: el calificador sale de los niveles D1–D6 del paciente por capítulo (aproximación); en estructuras, naturaleza y localización quedan «sin especificar» (8) y no se evalúan; las actividades (d) salen de una lista cerrada del Anexo y se valoran aparte. El caso C19 (sin dificultad en ningún dominio) debe quedar **sin códigos**: si el sistema sugiere alguno, es un error.

## 4. Métricas y umbrales

| Métrica | Cómo se calcula | Umbral aprobado |
|---|---|---|
| Casos revisados | casos con al menos una valoración | ≥ 20 de 24 |
| Precisión estricta b+s | «Adecuado» / códigos b y s valorados | ≥ 60 % |
| Precisión flexible b+s | («Adecuado» + «Aceptable») / valorados | ≥ 80 % |
| Cobertura a ciegas b+s | de lo que la revisora eligió en la Fase A, cuánto estaba en la sugerencia | ≥ 60 % |
| Calificador b+s | κ ponderado (pesos lineales) entre la gravedad 0–4 que la revisora escribió a ciegas y la del sistema, en los códigos que ambos eligieron; mínimo 30 códigos coincidentes | κ ≥ 0,50 |
| Precisión flexible d | igual que b+s, solo actividades | ≥ 80 % |

Los códigos se comparan por su forma de 3 dígitos (`b730`); si la revisora escribe uno más específico (`b7301`), cuenta para `b730`.

**Umbrales aprobados por el responsable del proyecto el 7 de octubre de 2026** (el del calificador se reformuló el 21 de octubre; ver 4.1). Se presentan a la revisora en la reunión de la próxima semana; si ella plantea un ajuste clínico, se cambia en `THRESHOLDS` de `icf-service/icf/review.py` y se documenta aquí.

**Piso del intervalo de confianza.** Un criterio con proporción cumple solo si el valor observado alcanza la meta **y** el límite inferior del IC 95 % (Wilson) alcanza un piso: precisión estricta ≥ 40 %, precisión flexible (b+s y d) ≥ 60 %, cobertura a ciegas ≥ 40 %. Los pisos (`CI_FLOORS`) están **pendientes de aprobación del responsable**; su sustento está en 4.3.

**Veredicto:** `CUMPLE` si se alcanzan todos los criterios; `NO CUMPLE` si alguno falla (el informe indica si fue por la meta o por el piso del IC); `INCOMPLETO` si falta algún dato, incluidos menos de 30 códigos coincidentes para el calificador (con menos pares el IC del κ es demasiado ancho; ver 4.4, punto 6).

**IC por bootstrap de casos (informativo).** Cada criterio del informe trae además un IC 95 % calculado remuestreando los casos y no los códigos (2 000 remuestras, semilla fija), que corrige la correlación entre códigos de un mismo caso (ver 4.4). No decide el veredicto: la simulación muestra que, con el tamaño de muestra previsto, da la misma decisión que el IC de Wilson. Aparece como `ic95_casos` en el informe JSON.

**Métricas informativas (no entran al veredicto):** precisión y F1 frente a la elección a ciegas, recall por capítulo, κ de Cohen por capítulo (b1–b8, s1–s8, presencia/ausencia) y acuerdo exacto y dentro de ±1 nivel del calificador. El κ por capítulo se calcula con la misma hoja, sin trabajo extra de la revisora.

### 4.1 Sustento científico de los umbrales y cómo se mide la concordancia

**Cómo se mide la concordancia en la práctica clínica.** La literatura de codificación CIF usa tres piezas: (1) un estándar de referencia elaborado por profesionales que codifican de forma independiente, con el acuerdo entre anotadores medido y las discrepancias resueltas por consenso ([Newman-Griffis et al. 2021](https://doi.org/10.3389/fresc.2021.742702): acuerdo con F1 y consenso en reuniones; [Cieza et al. 2002](https://doi.org/10.1080/165019702760279189): porcentaje de acuerdo entre dos profesionales al vincular instrumentos con la CIF); (2) una medida de acuerdo según el tipo de dato: κ de Cohen para decisiones categóricas ([Cohen 1960](https://doi.org/10.1177/001316446002000104)), κ ponderado para escalas ordinales como el calificador 0–4 ([Cohen 1968](https://doi.org/10.1037/h0026256)) y F1 (acuerdo positivo específico) cuando no hay «negativos» definidos, como al elegir códigos de un catálogo grande ([Hripcsak y Rothschild 2005](https://doi.org/10.1197/jamia.M1733), que lo proponen para medir la fiabilidad del estándar de referencia entre expertos); (3) la fiabilidad entre expertos como referencia con la cual leer el desempeño del sistema. El acuerdo entre expertos al codificar con la CIF es bajo ([Roitero et al. 2023](https://doi.org/10.3233/SHTI230262), que lo afirma en su resumen), por eso un umbral absoluto cercano al 100 % no es realista.

**Qué respalda cada umbral** (estado verificado contra las fuentes del `.bib`):

| Criterio | Umbral | Sustento | Juicio |
|---|---|---|---|
| Precisión flexible b+s y d | ≥ 80 % | **Dos referentes numéricos de codificación clínica humana.** (1) El estándar mínimo de auditoría de codificación del NHS ([DHCW](https://dhcw.nhs.wales/data/information-standards/clinical-classifications-and-terminology-standards/clinical-coding-audit-programme/clinical-coding-audit-methodology/), página oficial): 90 % de códigos correctos en diagnóstico principal y **80 % en diagnósticos secundarios**; la sobrecodificación no cuenta como error. (2) [Burns et al. 2012](https://doi.org/10.1093/pubmed/fdr054), revisión sistemática de 32 estudios: exactitud mediana de la codificación hospitalaria frente a las historias clínicas de 83,2 %, y de 80,3 % en diagnósticos (RIC 63,3–94,1 %; rango 50,5–97,8 %). Es decir, 80 % equivale al desempeño de la codificación humana rutinaria. Límites: son ICD-10 en hospitales y no CIF-IA, y el auditor aplica un manual de reglas. McHugh 2012 (80 % de acuerdo como mínimo habitual) queda como apoyo adicional | Respaldado por referentes numéricos; mantener y reportar el IC |
| Precisión estricta b+s | ≥ 60 % | Referente indirecto: 60 % está cerca del **cuartil inferior (63,3 %)** de la exactitud humana de Burns 2012, es decir, un sistema por debajo estaría en el peor cuarto de la codificación humana. Pero «Adecuado» estricto es más exigente que «código correcto» de una auditoría, así que no hay un referente directo. El bajo acuerdo entre expertos en CIF (Roitero 2023; ver el calificador) explica que no se exija más | Referente indirecto; mantener como meta y declararlo |
| Cobertura a ciegas b+s | ≥ 60 % | Los F1 de la literatura (84 % en Newman-Griffis y Fosler-Lussier 2021; más de 80 % en Newman-Griffis et al. 2021, con 13 a 16 categorías de movilidad y autocuidado) son de clasificadores supervisados sobre conjuntos reducidos de códigos: **no son comparables** con recuperación abierta sobre un catálogo amplio. El recall se complementa con F1 y κ por capítulo. Los estándares de auditoría de codificación (NHS, Burns 2012) miden códigos correctos sobre los asignados, es decir precisión: **no hay referente externo de cobertura** | Sin referente externo; mantener como meta del proyecto y declararlo |
| Calificador b+s | κ ≥ 0,50 (antes: ≥ 80 % de «Sí/Parcial») | El criterio anterior no tenía sustento: escala propia y la revisora ya había visto la sugerencia (anclaje). El κ ponderado ([Cohen 1968](https://doi.org/10.1037/h0026256)) es la medida estándar para una escala ordinal como 0–4 y se compara contra una gravedad asignada a ciegas. **Referentes humanos en CIF:** [Okochi et al. 2005](https://doi.org/10.1186/1477-7525-3-46) (test-retest de códigos y calificadores CIF en 742 adultos mayores): κ ponderado mediano de 0,46 en funciones corporales y 0,55 en actividades y participación, que los autores califican de «relativamente bajo» y que mejora con evaluadores experimentados; [Chen et al. 2016](https://doi.org/10.2340/16501977-2063) (Brief ICF Core Set de ictus): parejas de evaluadores expertos κ 0,50–0,85 y novatos 0,18–0,69. Por eso se fijó **0,50** (decisión del 21 de octubre de 2026): es el límite inferior del rango de expertos de Chen y queda cerca de la mediana humana de Okochi. El piso general de McHugh 2012 (0,60) sería más exigente que lo que logran las personas en esta tarea | Ajustado a 0,50; criterio del proyecto anclado a la fiabilidad humana (ver 4.6) |
| Casos revisados | ≥ 20 de 24 | Es un criterio de completitud, no de validez | Mantener |

El diseño de revisión por profesionales de lo que genera un LLM tiene antecedentes en rehabilitación: [Zhang et al. 2023](https://doi.org/10.2340/jrm.v55.13373) hicieron revisar por 2 fisiatras las respuestas de ChatGPT-4 para **un solo caso** de ictus (sin ocultar el origen), y [Cao et al. 2026](https://doi.org/10.1186/s12984-026-01903-0) hicieron una evaluación **a ciegas** con 6 fisiatras y 48 casos reales. Ninguno **fija umbrales de aceptación**: el diseño a ciegas con casos múltiples de nuestra Fase A se parece más al de Cao. Ningún artículo del `.bib` define un umbral de concordancia para este tipo de sistema: los valores de la tabla se justifican como criterios razonables, no como normas.

**Interpretación del κ por capítulo** (informativo, McHugh 2012): < 0,60 inadecuado; 0,60–0,79 moderado; ≥ 0,80 fuerte.

### 4.2 Reformulaciones adoptadas (21 de octubre de 2026) y descartadas

Se cuenta con una sola revisora, por lo que se adoptaron las que no dependen de una segunda:

1. **Calificador a ciegas** (adoptada): la revisora escribe la gravedad 0–4 junto a cada código de la Fase A y se mide κ ponderado sobre los códigos en los que coincide con el sistema. Con pocos códigos coincidentes (menos de 30) el κ no es concluyente y el veredicto queda `INCOMPLETO`.
2. **Piso del límite inferior del IC** (adoptada): ver la sección 4. Los pisos son propuestos y pendientes de aprobación.
3. **Repetibilidad del sistema** (adoptada, no requiere a la revisora): `python scripts/repeatability.py --runs 5` corre cada caso varias veces con la configuración de producción y reporta κ de Fleiss por capítulo y por código, Jaccard medio entre corridas y proporción de códigos estables, como en [Liu et al. 2026](https://doi.org/10.64898/2026.04.03.26350117). Se interpreta con McHugh 2012 (< 0,60 inadecuado). Es informativa: no entra al veredicto clínico, pero un κ bajo indica que la validación de la revisora describe una sola corrida de un sistema inestable. El κ por código se calcula solo sobre los códigos que salieron en alguna corrida y queda sin dato si todos fueron estables; en ese caso mandan el Jaccard y la proporción de códigos estables.
4. **Segunda revisora** (descartada por ahora): permitiría medir el acuerdo entre expertos y expresar el resultado como proporción de ese techo. Sin ella, la interpretación se apoya en la literatura (Roitero 2023) y no en una medida propia.

### 4.3 Sustento del piso del IC (qué está respaldado y qué es criterio del proyecto)

**Respaldado por la literatura (la regla):**
- Decidir con el **límite inferior del IC** y no con la estimación puntual es la práctica en estudios de exactitud diagnóstica y de fiabilidad. [Flahault et al. 2005](https://doi.org/10.1016/j.jclinepi.2004.12.009) diseñan el estudio a partir de una sensibilidad esperada y un **límite inferior aceptable** del IC 95 %, con una probabilidad máxima del 5 % de que el límite estimado caiga bajo ese nivel; es la fuente más cercana a nuestro diseño de «meta esperada + mínimo aceptable». [Koo y Li 2016](https://doi.org/10.1016/j.jcm.2016.02.012) indican que el nivel de fiabilidad debe juzgarse por el IC 95 % «y no por la estimación» (peor escenario). [Jones et al. 1996](https://doi.org/10.1136/bmj.313.7048.36) establecen que, al probar equivalencia, el análisis debe basarse en intervalos de confianza. La guía de la [FDA 2007](https://www.fda.gov/media/71147/download) pide reportar los IC porque las estimaciones puntuales no expresan la incertidumbre del muestreo. [Obuchowski 1998](https://doi.org/10.1177/096228029800700405) presenta las fórmulas de tamaño de muestra para sensibilidad y especificidad de una prueba.
- **Con pocos casos las estimaciones son imprecisas y pueden engañar** (es lo que el piso protege): [Riley et al. 2021](https://doi.org/10.1002/sim.9025) señalan que los estudios de validación suelen tener muestras pequeñas y, por tanto, estimaciones de desempeño imprecisas, y proponen fijar el tamaño de muestra por el ancho del IC deseado (también [Riley et al. 2024](https://doi.org/10.1136/bmj-2023-074821), solo verificado el título); [Jones et al. 1996](https://doi.org/10.1136/bmj.313.7048.36) advierten que los ensayos de equivalencia con muy pocos pacientes tienden a concluir «sin diferencia» y que el análisis debe basarse en IC; [Hripcsak y Heitjan 2002](https://doi.org/10.1016/S1532-0464(02)00500-2) muestran que, con baja frecuencia de una categoría, el acuerdo observado puede sobrestimar el acuerdo real.
- El **IC de Wilson**: [Newcombe 1998](https://doi.org/10.1002/(SICI)1097-0258(19980430)17:8%3C857::AID-SIM777%3E3.0.CO;2-E) compara siete métodos en 96 000 puntos del espacio de parámetros, concluye que los intervalos simples (Wald) tienen mala cobertura y recomienda los métodos de áreas de cola y los de puntuación (Wilson es el de puntuación). [Brown, Cai y DasGupta 2001](https://doi.org/10.1214/ss/1009213286) llegan a una conclusión similar (según un resumen de búsqueda; el resumen oficial está bloqueado por la editorial).
- Equivale a **exigir que no se pueda rechazar** que el desempeño real sea tan bajo como el piso (prueba de puntuación unilateral al 2,5 %). Esta equivalencia se **comprueba numéricamente** en las pruebas del repositorio (4.5). Por eso la meta es el desempeño esperado y el piso el nivel mínimo aceptable, igual que en el diseño de Flahault.

**Criterio del proyecto (los valores):** ninguna de esas fuentes fija cifras para este tipo de sistema, y ninguna aborda la codificación CIF con LLM; son referencias metodológicas de estudios diagnósticos y de fiabilidad, aplicadas por analogía.
- Flexible ≥ 60 %: McHugh 2012 señala que alrededor de 61 % de acuerdo ya es problemático (casi 40 % de datos erróneos) y que κ < 0,60 es acuerdo inadecuado. Es el único piso con referente numérico, y es por analogía.
- Estricta y cobertura ≥ 40 %: se eligieron 20 puntos bajo su meta, igual que en la flexible. El referente es débil (la escala de Cohen llama «regular» a κ 0,21–0,40 y McHugh dice que 0,40 no es acuerdo adecuado).

**Lo que hacen realmente los pisos** (cálculo propio con el IC de Wilson; k ~ Binomial(n, p)):

| Con n códigos valorados | Estricta (meta 60 %, piso 40 %) | Flexible (meta 80 %, piso 60 %) |
|---|---|---|
| Probabilidad de aprobar si el desempeño real es 10 puntos sobre la meta (n = 30 / 60) | 92 % / 96 % | 97 % / 99 % |
| Probabilidad de aprobar si el desempeño real es el de la meta (n = 30 / 60) | 58 % / 56 % | 61 % / 58 % |
| Probabilidad de aprobar si el desempeño real es el del piso (n = 30 / 60) | 2 % / 0,1 % | 1,7 % / 0,1 % |

Observado mínimo para que el límite inferior alcance un nivel X:

| Límite inferior ≥ | n = 30 | n = 45 | n = 60 | n = 90 |
|---|---|---|---|---|
| 40 % | 60 % | 56 % | 53 % | 51 % |
| 60 % | 80 % | 76 % | 73 % | 71 % |
| 70 % | 87 % | 84 % | 82 % | 80 % |
| 80 % | 97 % | 93 % | 92 % | 89 % |

**Conclusión honesta:** con 30 o más códigos valorados, alcanzar la meta ya implica un límite inferior sobre el piso (con 60 códigos, un 80 % observado tiene límite inferior de 68 %). Los pisos actuales son entonces una **protección contra muestras muy pequeñas** (5 de 5 adecuados da límite inferior de 57 %), no una exigencia adicional. Exigir que el límite inferior alcance la propia meta, como hace Flahault con el nivel aceptable, pediría observar 92 % en la precisión flexible con 60 códigos, algo poco realista cuando el acuerdo entre expertos ya es bajo (Roitero 2023). Un piso intermedio (flexible ≥ 70 %) pide 82 % con 60 códigos y casi no cambia la meta de 80 %.

### 4.4 Sustento estadístico de la prueba

**1. Qué hipótesis se contrasta.** Cada criterio de proporción (precisión estricta y flexible, cobertura a ciegas) es una prueba de una proporción binomial. Para un piso p₀: H₀: p ≤ p₀ frente a H₁: p > p₀. «El límite inferior del IC 95 % de Wilson ≥ p₀» equivale a rechazar H₀ con la prueba de puntuación y α unilateral de 2,5 % ([Wilson 1927](https://doi.org/10.1080/01621459.1927.10502953) define el intervalo a partir de esa prueba; la equivalencia se verifica numéricamente en `tests/test_review_reference.py`). La regla completa es conjuntiva: se aprueba si el valor observado alcanza la **meta** (desempeño esperado) y se rechaza H₀ para el **piso** (desempeño mínimo aceptable). Con eso se controlan los dos errores: el de aprobar un sistema realmente deficiente (α) y el de rechazar uno bueno (potencia).

**2. Tamaño de muestra.** Con la fórmula normal de una proporción (α unilateral 2,5 %, potencia 80 %; es la fórmula estándar de una prueba binomial, aplicada a sensibilidad y especificidad en [Obuchowski 1998](https://doi.org/10.1177/096228029800700405) y a un límite inferior aceptable en [Flahault et al. 2005](https://doi.org/10.1016/j.jclinepi.2004.12.009)), los códigos necesarios para detectar que el desempeño real es la meta frente al piso son:

| Criterio (piso → meta) | Códigos independientes | Con efecto de diseño 1,4 / 1,8 / 2,2 | Equivalente en casos de 5 códigos |
|---|---|---|---|
| Flexible (60 % → 80 %) | 36 | 51 / 65 / 80 | 11 / 13 / 16 |
| Estricta y cobertura (40 % → 60 %) | 48 | 68 / 87 / 106 | 14 / 18 / 22 |

Nuestro diseño aporta 24 casos y hasta 6 códigos b+s por caso (máximo de 3 por componente): como máximo 144, y se supone del orden de 100 códigos. Alcanza para la precisión flexible incluso con correlación alta dentro del caso; en estricta y cobertura queda justo con ρ ≥ 0,2.

**3. Correlación dentro del caso (efecto de diseño).** Los códigos de un mismo caso no son independientes: comparten paciente y criterio. El tamaño efectivo es n/DEFF con DEFF = 1 + (m − 1)ρ, donde m son los códigos por caso y ρ la correlación intraclase (fórmula estándar del efecto de diseño; [Killip et al. 2004](https://doi.org/10.1370/afm.141) la explican con el tamaño efectivo, y que aumentar el número de clusters rinde más que aumentar los sujetos por cluster; [Rao y Scott 1992](https://doi.org/10.2307/2532311) proponen analizar datos binarios agrupados con el efecto de diseño y el tamaño de muestra efectivo). Con m = 5, ρ = 0,2 el DEFF es 1,8: 120 códigos valen como 67. **El rango de ρ (0 a 0,3) es un supuesto**: no encontré un valor publicado para acuerdo en codificación CIF; se podrá estimar con la hoja llena.

**4. Simulación del diseño real** (`scripts/design_simulation.py`, semilla fija; 24 casos × 5 códigos; códigos beta-binomiales con ρ de 0 a 0,3; 1 500 simulaciones por escenario y bootstrap por caso con 400 remuestras):

| ρ | Cobertura real del límite inferior de Wilson (nominal 97,5 %) p = 0,6 / 0,8 | Aprobación si el real = piso (flexible / estricta) | Aprobación si el real = meta (flexible / estricta) | Aprobación si el real = meta + 10 puntos (flexible / estricta) |
|---|---|---|---|---|
| 0 | 97,5 % / 97,7 % | 0 % / 0 % | 53,5 % / 56,7 % | 99,9 % / 98,9 % |
| 0,1 | 95,1 % / 95,5 % | 0 % / 0,1 % | 54,2 % / 53,3 % | 99,6 % / 97,7 % |
| 0,2 | 92,8 % / 92,9 % | 0 % / 0 % | 55,7 % / 51,7 % | 99,5 % / 96,1 % |
| 0,3 | 91,3 % / 90,0 % | 0 % / 0,1 % | 55,7 % / 51,5 % | 98,8 % / 94,3 % |

Lectura: (a) la correlación dentro del caso hace que el IC de Wilson **cubra menos de lo nominal** (90–91 % en lugar de 97,5 % con ρ = 0,3), así que el IC que se reporta es optimista; (b) esto **no cambia la decisión**, porque con n ≈ 120 el criterio que manda es alcanzar la meta y el piso casi nunca es el que decide; la aprobación con bootstrap por caso es igual que con Wilson (≤ 0,1 % si el desempeño real es el del piso, en ambos); (c) quien tenga un desempeño real en la meta aprueba cerca del 52–57 %, como es esperable de un umbral puesto en el valor esperado; con 10 puntos de ventaja aprueba el 94 % o más.

**Consecuencia para el reporte (implementada):** además del IC de Wilson, el informe incluye un IC con **bootstrap por casos** (remuestrear los 24 casos, no los códigos; técnica de [Field y Welsh 2007](https://doi.org/10.1111/j.1467-9868.2007.00593.x), de la que solo pude verificar título y DOI) en `icf/review.py`, función `cluster_bootstrap_ci`, también para el κ ponderado del calificador. Es una mejora de reporte, no de decisión. Con solo 24 casos el bootstrap tampoco es exacto (es una limitación general de remuestrear pocos clusters; no la verifiqué en las fuentes), por lo que se lee como una indicación de la incertidumbre y no como un valor exacto.

**5. Estadígrafos de acuerdo.** Para el calificador 0–4 se usa κ ponderado con pesos lineales ([Cohen 1968](https://doi.org/10.1037/h0026256)), porque es una escala ordinal en la que errar por un nivel pesa menos que por tres. La repetibilidad usa κ de Fleiss ([Fleiss 1971](https://doi.org/10.1037/h0031619)) al haber más de dos corridas por caso. El F1 como acuerdo positivo específico se justifica cuando no hay «negativos» bien definidos ([Hripcsak y Rothschild 2005](https://doi.org/10.1197/jamia.M1733)), y el κ por capítulo sí tiene universo fijo de decisiones. El κ depende de la prevalencia y de las categorías del experimento: con muy baja frecuencia de una categoría puede subestimar el acuerdo real y el acuerdo observado sobrestimarlo ([Hripcsak y Heitjan 2002](https://doi.org/10.1016/S1532-0464(02)00500-2)), por lo que siempre se reporta junto con el acuerdo exacto y ±1. Las tres implementaciones (κ de Cohen, κ ponderado lineal y κ de Fleiss) se contrastan con scikit-learn y statsmodels en `tests/test_review_reference.py`.

**6. Precisión del κ ponderado con pocos pares** (simulación en `scripts/design_simulation.py`; escenario supuesto: la gravedad del sistema coincide exacta con la de la revisora el 55 % de las veces y dentro de ±1 el 90 %, lo que da κ ponderado verdadero = 0,67; IC por bootstrap de los pares):

| Pares (códigos coincidentes) | Ancho medio del IC 95 % | Límite inferior medio |
|---|---|---|
| 10 | 0,62 | 0,25 |
| 20 | 0,42 | 0,42 |
| 30 | 0,33 | 0,50 |
| 40 | 0,29 | 0,50 |
| 60 | 0,24 | 0,53 |

Con 10 pares el IC abarca más de la mitad de la escala del κ, así que el criterio «κ ≥ 0,50» sería prácticamente una moneda al aire. Por eso el mínimo de pares se fijó en **30** (decisión del 21 de octubre de 2026): con 30 pares el ancho baja a 0,33; con 60, a 0,24. Los códigos coincidentes dependen de la cobertura a ciegas: con ~100 códigos elegidos y cobertura del 60 % se esperan unos 60 pares (supuesto); si la doctora coincide poco y no se llega a 30, el calificador queda `INCOMPLETO` en lugar de decidir con un κ poco fiable.

**Brecha conocida (decisión pendiente):** el criterio del calificador compara el κ **observado** con 0,50 y no su límite inferior, que es justo lo que [Koo y Li 2016](https://doi.org/10.1016/j.jcm.2016.02.012) desaconsejan (juzgar por la estimación y no por el IC). Con 60 pares y κ verdadero de 0,67 el límite inferior medio es 0,53, sobre la meta de 0,50; con 30 pares es 0,50, justo en la meta. Si se quiere la misma exigencia que en las proporciones, habría que añadir un piso al límite inferior del κ por bootstrap de casos (por ejemplo, 0,40, el inicio de la zona «moderada» de la escala de Cohen según [McHugh 2012](https://doi.org/10.11613/BM.2012.031), que ella misma considera insuficiente como acuerdo adecuado). Con el mínimo de 30 pares el límite inferior medio es 0,50, así que ese piso rara vez decidiría. El IC por bootstrap ya se informa; falta decidir si pasa a ser criterio.

### 4.5 Nivel de verificación de las fuentes y de las técnicas

| Nivel | Qué significa | Fuentes / técnicas |
|---|---|---|
| A. Texto o resumen leído y contrastado con lo que se afirma | La afirmación del protocolo coincide con el texto o el resumen del propio artículo | McHugh 2012 (texto); Newman-Griffis et al. 2021 en *Frontiers in Digital Health* y *Frontiers in Rehabilitation Sciences* (resumen y métodos); Koo y Li 2016 (texto); Liu et al. 2026, Roitero 2023, Cieza 2002, Zhang 2023, Cao 2026, Hripcsak y Rothschild 2005, Hripcsak y Heitjan 2002, Flahault 2005, Newcombe 1998, Jones 1996, Riley 2021, Rao y Scott 1992, Killip 2004 y Obuchowski 1998 (resumen); guía FDA 2007 (transcripción); Burns 2012, Okochi 2005, Chen 2016, Abràmoff 2018, Liu 2019 y Artstein y Poesio 2008 (resumen); estándar de auditoría de codificación de la DHCW (página oficial, texto) |
| B. Técnica comprobada con una implementación de referencia | La función propia se contrasta numéricamente con una librería estándar | Wilson (statsmodels), equivalencia Wilson–prueba de puntuación (statsmodels), κ de Cohen y κ ponderado lineal (scikit-learn), κ de Fleiss (statsmodels): `tests/test_review_reference.py` |
| C. Solo título y DOI verificados; el contenido se cita como técnica estándar | La editorial bloquea el resumen; no se atribuye al artículo nada más que su tema | Cohen 1960 y 1968, Landis y Koch 1977, Fleiss 1971, Wilson 1927, Brown et al. 2001, Field y Welsh 2007, Riley 2024 |
| D. Cálculo o supuesto propio | No proviene de una fuente | Pisos del IC (40/60/40), mínimo de 30 pares del calificador (elegido por el ancho del IC en la simulación), rango de ρ, número de códigos por caso, distribución del calificador en la simulación; todo reproducible con `scripts/design_simulation.py` |

Ningún nivel A o B respalda por sí mismo las **cifras** de los umbrales: solo respaldan el método y su comportamiento estadístico. La excepción parcial es el 80 % de precisión flexible, que sí tiene referentes numéricos de codificación humana (ver 4.6).

### 4.6 Cómo se acepta la tecnología en medicina y qué dice eso de los umbrales

Revisé estudios donde una tecnología se aceptó o se evaluó frente a profesionales, para ver cómo se fijan los criterios.

**1. Se compara con el desempeño humano sobre la misma muestra.** [Liu et al. 2019](https://doi.org/10.1016/S2589-7500(19)30123-2) (revisión sistemática; 82 estudios, 14 con comparación en la misma muestra y validación externa): sensibilidad conjunta de 87,0 % para el aprendizaje profundo frente a 86,4 % de los profesionales, y especificidad de 92,5 % frente a 90,5 %; concluyen «equivalente», pero advierten que pocos estudios tienen validación externa o comparan en la misma muestra y que el reporte suele ser pobre. Nuestra Fase A y B es una comparación de ese tipo, con las limitaciones de una sola revisora y casos sintéticos.

**2. Se fijan metas numéricas antes del estudio.** [Abràmoff et al. 2018](https://doi.org/10.1038/s41746-018-0040-6) (primer sistema de IA autónomo autorizado por la FDA): metas prefijadas de sensibilidad > 85 % y especificidad > 82,5 %; resultados de 87,2 % (IC 95 % 81,8–91,2) y 90,7 % (IC 95 % 88,3–92,7). Observaciones: (a) el resumen no dice cómo se eligieron esas cifras; (b) el límite inferior del IC de la sensibilidad (81,8 %) queda **por debajo** de la meta de 85 %, así que no se exigió «límite inferior ≥ meta»; (c) el resumen no indica la prueba estadística usada. Es un precedente de «valor observado sobre una meta prefijada, con IC informado», que se parece a nuestra regla: meta sobre el valor observado y un piso más bajo sobre el límite inferior del IC.

**3. La referencia humana es modesta y se reconoce.** En codificación hospitalaria con ICD-10 la exactitud mediana humana ronda el 80 % (Burns 2012) y los servicios de salud fijan 80 % como mínimo en diagnósticos secundarios (NHS). En CIF la fiabilidad humana de los calificadores es baja (Okochi 2005, Chen 2016). Por eso exigir cercano al 100 % no tiene sentido y los umbrales se anclan a lo que logran las personas.

**4. No hay un umbral universal de κ.** [Artstein y Poesio 2008](https://doi.org/10.1162/coli.07-034-R2) plantean que los coeficientes ponderados pueden ser más apropiados para muchas tareas de anotación, pero que su interpretación se vuelve aún más difícil. Por eso el κ no se interpreta solo con una escala genérica (McHugh) sino junto con la fiabilidad humana de la misma tarea.

**Resumen de lo que la evidencia sostiene**

| Criterio | Umbral | Evidencia | Estado |
|---|---|---|---|
| Precisión flexible b+s y d | ≥ 80 % | Estándar NHS (80 % en secundarios) y mediana humana de Burns (80,3 % en diagnósticos) | **Sustentado** |
| Piso del IC de la flexible | ≥ 60 % | Cuartil inferior de Burns (63,3 %); precedente de IDx-DR de piso inferior a la meta | Sustentado de forma indirecta |
| Precisión estricta b+s | ≥ 60 % | Solo cuartil inferior de Burns, como referente indirecto | Indirecto |
| Cobertura a ciegas | ≥ 60 % | Ninguno: los estándares miden precisión y no cobertura | Sin referente externo |
| Calificador (κ ponderado) | ≥ 0,50 (antes 0,60) | Rango de expertos 0,50–0,85 (Chen) y mediana humana rutinaria 0,46–0,55 (Okochi) | **Ajustado** a la fiabilidad humana |

**Sobre el calificador (decidido el 21 de octubre de 2026).** El 0,60 inicial caía dentro del rango de expertos humanos (0,50–0,85) pero por encima de la mediana humana en la práctica rutinaria (0,46–0,55), de modo que un sistema al nivel de un evaluador humano podía quedar como NO CUMPLE. Se fijó **0,50**: el límite inferior del rango de expertos de Chen y cercano a la mediana de Okochi. Es un criterio del proyecto anclado a la fiabilidad humana, no una norma; el piso general de McHugh (0,60) se conserva solo como referencia. Un κ de 0,50–0,59 se lee entonces como «dentro del rango humano», no como un desempeño excelente.

**Aviso de alcance:** estos referentes son de ICD-10 hospitalaria, de CIF en geriatría e ictus y de imagen diagnóstica; no son la misma tarea que sugerir códigos CIF-IA con una IA local. Sirven para anclar el orden de magnitud, no para certificar los valores. Además, el sistema es un borrador que revisa un médico; un sistema autónomo exigiría umbrales más estrictos (esto último es criterio mío, no proviene de una fuente).

## 5. Qué se hace con el resultado

```powershell
# con la hoja llena, en un equipo con Python y openpyxl (o en un contenedor python:3.11-slim)
python scripts/review_sheet.py upgrade ..\data\private\icf\review\hoja_revision.xlsx --output ..\data\private\icf\review\hoja_revision_v2.xlsx   # pone al día una hoja vieja sin la base de datos ni Ollama
python scripts/review_sheet.py score ..\data\private\icf\review\hoja_revision_llena.xlsx --output informe_validacion.json
python scripts/review_sheet.py score hoja_revision_llena.xlsx --apply-expected   # copia la Fase A a reference/cases.json
```

- `--apply-expected` deja la elección a ciegas de la revisora como `expected` en `cases.json` y marca los casos como `validated`. A partir de ahí `evaluate.py` mide **precisión real** y se pueden comparar modelos con un criterio clínico.
- **Si CUMPLE:** el perfil se puede usar como borrador de apoyo en un piloto con médicos, con la leyenda de borrador que ya muestra la pantalla.
- **Si NO CUMPLE:** se revisan los errores por componente (la hoja trae los comentarios) y se decide entre ajustar la búsqueda o las reglas, probar un modelo mayor (de 12B a 31B, aún sin medir) o limitar el alcance (por ejemplo, solo actividades y funciones). No se aprueba el uso clínico.

## 6. Límites de esta validación

- **Una sola revisora**: no se mide el acuerdo entre profesionales; el resultado refleja el criterio de una persona y se interpreta con el techo que da la literatura, no con uno propio. Con una segunda revisora sobre los mismos casos se podría medir.
- **24 casos sintéticos**: dan una idea de la calidad, no una garantía en pacientes reales. Los casos de audición, visión y discapacidad intelectual son pocos porque el sistema captura sobre todo discapacidad física y psicosocial.
- **Sesgo de anclaje**: por eso existe la Fase A a ciegas.
- **El caso C10 (menor de 6 años)** se omite: el sistema responde «no aplica» por diseño.
- Los umbrales los fijó el responsable del proyecto; no son una norma clínica y la revisora puede proponer ajustes. Ningún artículo revisado define un umbral de concordancia para este tipo de sistema (ver 4.1). Los únicos referentes numéricos son de codificación humana (ICD-10 hospitalaria; CIF en geriatría e ictus), una tarea parecida pero no igual (ver 4.6).
- **Intervalos optimistas:** los IC de Wilson tratan cada código como independiente, pero los de un mismo caso se parecen entre sí; con ρ = 0,2 a 0,3 la cobertura real del límite inferior baja de 97,5 % a cerca de 90–93 % (ver 4.4). No cambia la decisión con el tamaño de muestra previsto, pero el IC reportado es algo más estrecho de lo que debería. El valor real de ρ se desconoce y se estimará con la hoja llena.
- **Los escenarios de la simulación son supuestos** (códigos por caso, ρ, distribución de la gravedad); dimensionan la prueba pero no sustituyen los datos reales (ver 4.5, nivel D).
- **Recall y precisión a ciegas dependen del tope de 3 códigos y del largo de la sugerencia:** una sugerencia larga sube el recall y baja la precisión. Por eso se reportan juntos (F1) y la precisión a ciegas no entra al veredicto.

## 7. Pendientes (estado al 21 de octubre; los puntos 2 a 6 se retoman en las secciones 8 y 9)

1. ~~Regenerar la hoja~~ **Hecho el 21 de octubre de 2026:** la hoja del 9 de octubre no pedía la gravedad a ciegas, así que se actualizó con `review_sheet.py upgrade` y quedó en `data/private/icf/review/hoja_revision_v2.xlsx` (24 casos y las mismas 201 sugerencias; la original no se tocó). Solo hace falta volver a correr `generate` (base de datos y Ollama) si se quiere una sugerencia nueva del modelo.
2. Correr `python scripts/repeatability.py --runs 5 --output ...` y anotar el resultado (no necesita a la revisora).
3. Que el responsable apruebe los pisos del IC (`CI_FLOORS`) y el κ ≥ 0,50 del calificador (decidido el 21 de octubre, anclado a la fiabilidad humana según 4.6), y decida si el límite inferior del κ (por bootstrap de casos) pasa a ser criterio con un piso (ver 4.4, «Brecha conocida»).
4. Presentar los umbrales y la sección 4.1 a la revisora en la reunión de la próxima semana.
5. Entregar la hoja regenerada a la revisora por un canal privado.
6. Recibir la hoja llena, correr `score` y documentar el resultado en este archivo y en `BACKLOG.md`. Con eso se completa HU-07g.

## 8. Resultado de la revisión (26 de octubre de 2026)

La revisora (Emilly Maria Celis) devolvió `hoja_revision_v2.xlsx` llena: Fase A a ciegas en los 24 casos aplicables y Fase B con sus valoraciones (el C10 no aplica por edad; el C19, sin deficiencia, no tiene sugerencias que valorar y quedaron 23 casos con valoración). Se corrió `review_sheet.py score` sin modificar `reference/cases.json`. La hoja es privada y no está en el repositorio.

### 8.1 Métricas frente a los umbrales

| Criterio | Valor | IC 95 % | Meta | Piso del IC | Resultado |
|---|---|---|---|---|---|
| Casos revisados | 23 | | ≥ 20 | | Cumple |
| Precisión estricta b+s | 0,591 | Wilson 0,506–0,671 · por casos 0,508–0,674 | ≥ 0,60 | 0,40 | No cumple (bajo la meta; supera el piso) |
| Precisión flexible b+s | 0,788 | Wilson 0,711–0,849 · por casos 0,726–0,848 | ≥ 0,80 | 0,60 | No cumple (bajo la meta; supera el piso) |
| Cobertura a ciegas b+s | 0,552 (37/67) | Wilson 0,434–0,665 · por casos 0,424–0,677 | ≥ 0,60 | 0,40 | No cumple (bajo la meta; supera el piso) |
| Calificador b+s (κ ponderado, 37 pares en 22 casos) | 0,576 | por casos 0,366–0,731 | ≥ 0,50 | | Cumple |
| Precisión flexible d | 1,000 | Wilson 0,947–1,0 | ≥ 0,80 | 0,60 | Cumple |

**Veredicto del `score`: NO CUMPLE.** Tres criterios fallan por su valor puntual (ninguno por el piso del IC): precisión estricta, precisión flexible y cobertura.

Lectura estadística, con la prueba definida en 4.4 (se cumple solo si el límite inferior alcanza la meta): la precisión flexible (0,788) queda 1,2 puntos bajo el 0,80 y su IC (0,711–0,849) **contiene** la meta, de modo que el resultado no demuestra estar por debajo ni por encima del estándar de auditoría de codificación humana (80 %, Digital Health and Care Wales; mediana de 80,3 % en diagnósticos, Burns et al. 2012). Lo mismo ocurre con la estricta y la cobertura. Con 23 casos la prueba no distingue diferencias de unos pocos puntos (4.4, tamaño de muestra); NO CUMPLE significa «no se pudo demostrar el cumplimiento», no «el sistema sea inservible» (decidir con el límite del IC y no con la estimación puntual: Jones et al. 1996; Flahault et al. 2005).

El κ ponderado del calificador (0,576) está dentro del rango humano de 4.6 (mediana 0,46–0,55 en test-retest, Okochi et al. 2005; 0,50–0,85 entre expertos, Chen et al. 2016), pero su IC (0,366–0,731) es amplio con 37 pares: cumple por la estimación puntual, sin certeza sobre el límite inferior (brecha ya declarada en 4.4).

### 8.2 Resultado por componente

| Componente | Sugerencias valoradas | Adecuado / Aceptable / No adecuado | Precisión estricta | Precisión flexible | Cobertura a ciegas | Calificador correcto (Fase B) |
|---|---|---|---|---|---|---|
| Funciones (b) | 69 | 50 / 14 / 5 | 0,725 | 0,928 | 17/39 (0,436) | 0,79 |
| Estructuras (s) | 63 | 28 / 12 / 23 | **0,444** | **0,635** | 20/24 (0,833) | 0,53 |
| Actividades (d) | 69 | 58 / 11 / 0 | 0,841 | 1,000 | no aplica (lista cerrada del Anexo) | 0,92 |

Fase A a ciegas, además: precisión de lo sugerido frente a lo que ella eligió 0,28 y F1 0,37 (informativas: el sistema da hasta 3 códigos por componente y ella escribió en promedio 1,1 estructuras y 1,7 funciones por caso, de modo que la precisión a ciegas tiene un techo cercano a 0,38 en estructuras; por eso no entra al veredicto, ver sección 6); acuerdo por capítulo κ 0,67 y cobertura por capítulo 0,857; calificador a ciegas: coincidencia exacta 0,595 y a ±1 nivel 0,946.

**Lo que dice el resultado:** las actividades (d) cumplen con holgura; las funciones (b) son precisas pero el sistema no encuentra todo lo que ella elegiría; las estructuras (s) se encuentran bien (83 % de cobertura) pero van acompañadas de códigos que ella rechaza. Son dos problemas distintos, con causas distintas (sección 9).

## 9. Análisis de los errores

**Método.** Se leyeron las valoraciones de la Fase B, sus comentarios y la hoja «Faltantes»; se compararon los códigos sugeridos con los que ella eligió a ciegas; y se midió en el servicio local (`icf-service`, PostgreSQL con pgvector, `bge-m3` y `gemma4:e4b`) en qué posición de la búsqueda aparecen los códigos de la médica. **Todo lo de 9.2 a 9.4 es exploratorio y post hoc**: se hizo sobre los mismos 24 casos que miden el sistema, de modo que cualquier ajuste elegido con ellos queda optimista y debe confirmarse con casos nuevos (Cawley y Talbot 2010: seleccionar sobre los datos de evaluación sesga a favor la medida; Kapoor y Narayanan 2023: la fuga entre selección y evaluación produce resultados que no se reproducen). Las tablas de 9.2 y 9.3 son diagnósticos, no una validación de las correcciones.

### 9.1 Dónde se pierde cada criterio

| Criterio | Dónde se pierde | Evidencia |
|---|---|---|
| Precisión de estructuras (s) | **Relleno de la cuota de 3**: el modelo devolvió 3 estructuras en 21 de 21 casos con estructuras; la médica eligió 1 en 20 casos y 2 en tres (C07, C17 y C22). Las posiciones 2 y 3 son las que ella rechaza | 9.2 |
| Cobertura de funciones (b) | **La búsqueda no trae sus códigos**: solo 18 de los 39 códigos b que ella eligió están entre los 12 candidatos; el modelo final recupera 17. El cuello de botella está antes del modelo | 9.3 |
| Cobertura (efecto de la referencia única) | Una sola médica a ciegas es una referencia incompleta: valoró «Adecuado» códigos que no había elegido (`b147`, 4 de 5; `b710`, 6 de 7) | 9.4 |
| Definición de «lo esperado» | Códigos con gravedad 0 («sin deficiencia») cuentan como esperados | 9.4 |

### 9.2 Estructuras (s): relleno de la cuota y caída por posición

Valoración de las estructuras según la posición en que el sistema las puso:

| Posición | Adecuado | Aceptable | No adecuado | Estricta | Flexible |
|---|---|---|---|---|---|
| 1.ª (21 casos) | 17 | 3 | 1 | 0,81 | 0,95 |
| 2.ª (21 casos) | 7 | 5 | 9 | 0,33 | 0,57 |
| 3.ª (21 casos) | 4 | 4 | 13 | 0,19 | 0,38 |

En funciones (b) la caída es mucho menor: 1.ª 20/2/1, 2.ª 15/7/1, 3.ª 15/5/3 (flexible 0,96, 0,96 y 0,87). La estructura principal casi siempre es correcta; lo que sobra son las dos siguientes. Los errores se repiten y son de «relleno»:

- **`s710` (cabeza y cuello) apareció en 9 casos: 0 «Adecuado», 3 «Aceptable», 6 «No adecuado»** («no existe lesión directa cabeza-cuello»), incluso en casos de columna o de amputación.
- **`s120` (médula espinal)**: 3 de 7 «No adecuado» (parálisis cerebral, distrofia muscular, estrés postraumático), por confundir lesión cerebral o muscular con medular.
- **`s140` y `s150` (sistemas nerviosos simpático y parasimpático)**: 3 de 3 y 1 de 1 «No adecuado» («la activación simpática no implica alteración estructural»).
- Aislados: `s830` uñas en lesión de ligamento, `s420` sistema inmunológico en asma, `s240` y `s250` en una hipoacusia neurosensorial.

Los comentarios de la médica a los códigos «No adecuado» de estructuras repiten la misma razón: **«no hay evidencia»** de ese problema en el caso. El prompt pide «hasta 3» y el modelo lo cumple como «3», completando con códigos cercanos semánticamente pero sin respaldo clínico. En la CIF se codifica lo que el caso evidencia, no se completa un cupo (OMS 2001; reglas de vinculación de Cieza et al. 2005, que exigen que el concepto esté en el texto fuente).

El marco clásico cuando un código falso cuesta más que omitir uno es la clasificación con opción de rechazo (Chow 1970): se emite el código solo si la confianza supera un umbral y, si no, el sistema se abstiene. Aquí la abstención equivale a dejar la lista en 1 o 2 estructuras.

Sensibilidad con las valoraciones ya hechas (recortar la lista de estructuras sin volver a ejecutar el modelo; criterios b+s del `score`):

| Estructuras por caso | Estricta | Flexible | Cobertura a ciegas | κ calificador | Veredicto |
|---|---|---|---|---|---|
| Hasta 3 (actual) | 0,591 | 0,788 | 0,552 | 0,576 | NO CUMPLE |
| Hasta 2 | 0,667 | 0,865 | 0,537 | 0,570 | NO CUMPLE (cobertura) |
| Solo 1 | 0,744 | 0,933 | 0,493 | 0,549 | NO CUMPLE (cobertura) |

Recortar lleva la precisión por encima de las metas pero **baja la cobertura**, que ya estaba bajo la suya: es la compensación habitual entre precisión y exhaustividad que resume el F1 (Hripcsak y Rothschild 2005). Recortar por sí solo no cierra la brecha; hay que mejorar la cobertura de funciones (9.3).

### 9.3 Funciones (b): la búsqueda no trae los códigos que ella elige

Posición de los códigos elegidos a ciegas en la búsqueda del motor (distancia coseno, solo códigos de 3 dígitos, mismo texto de contexto que usa el motor; 39 funciones y 24 estructuras, sin `b000` ni `s000` de C19 ni las `s110` de C05 y C13, donde el motor no busca estructuras, ver 9.4):

| | En los 3 primeros | En los 6 | **En los 12 (lo que ve el modelo)** | En los 20 | En los 40 |
|---|---|---|---|---|---|
| Funciones (b) | 12 / 39 | 14 | **18 (46 %)** | 22 | 30 |
| Estructuras (s) | 15 / 24 | 19 | **22 (92 %)** | 22 | 24 |

El modelo final recupera 17 de 39 funciones y 20 de 24 estructuras: casi todo lo que está entre los candidatos se recupera. **El techo de la cobertura de funciones es la búsqueda, no la selección del modelo.**

Qué falta: 12 de las 30 omisiones (40 %) son funciones neuromusculoesqueléticas del capítulo 7: `b730` fuerza muscular (6), `b760` control del movimiento voluntario (3) y `b770` marcha (3), en tetraparesia, parálisis cerebral, ACV, Parkinson, espina bífida y amputación. Para esos casos el sistema devolvió funciones mentales: `b147` (psicomotoras), `b163` y `b164`. Otras omisiones: `b167` lenguaje (2), `b144` memoria (2), `b125`, `b765`, `b620`, `b440`, `b710`.

Es coherente con dos hechos de la literatura. (i) En espacios de embeddings de alta dimensión unos pocos vectores («hubs») aparecen entre los vecinos más cercanos de muchas consultas y desplazan a otros relevantes (Radovanović et al. 2010); `b147`, `b163` y `s110` se repiten en casos muy distintos. (ii) La CIF cuenta con listas de las funciones y estructuras que acompañan a cada condición (ICF Core Sets, Ewert et al. 2004) y con reglas de vinculación (Cieza et al. 2005) porque el vocabulario del diagnóstico no basta para elegir el código.

Variantes de generación de candidatos probadas **solo para la cobertura de funciones** (no se midió precisión: los códigos nuevos no tienen valoración de la médica):

| Variante | Candidatos medios | Funciones de la médica entre los candidatos |
|---|---|---|
| Actual: 12 más cercanos | 12,0 | 18 / 39 (0,46) |
| 16 más cercanos | 16,0 | 19 / 39 (0,49) |
| 20 más cercanos | 20,0 | 22 / 39 (0,56) |
| 24 más cercanos | 23,7 | 24 / 39 (0,62) |
| 12 + los 3 más cercanos del capítulo 7 si hay dificultad de movilidad (D4) | 13,4 | 21 / 39 (0,54) |
| Los 3 más cercanos de cada capítulo | 21,7 | 17 / 39 (0,44) |
| 8 más cercanos + 1 por capítulo | 11,8 | 15 / 39 (0,38) |

Más candidatos sube el techo con un costo: las listas largas hacen que el modelo use peor la información (Liu et al. 2024, «Lost in the Middle») y suben la latencia; garantizar un cupo por capítulo **no ayuda** (empeora). La variante barata y con lógica clínica es añadir candidatos del capítulo 7 cuando el dominio D4 (movilidad) tiene dificultad: 21/39 con solo 1,4 candidatos más. Es una hipótesis generada con estos mismos casos, no un resultado confirmado.

### 9.4 Efectos de la referencia y de la definición de «esperado»

1. **Una sola referencia a ciegas subestima la cobertura.** La médica valoró «Adecuado» o «Aceptable» códigos que no había elegido: `b147` (4 de 5 «Adecuado»), `b710` (6 de 7), `b122` (4 de 5), `b320` (2 de 3). Hay más de una codificación aceptable por caso, y la literatura de codificación muestra variabilidad entre codificadores humanos (exactitud con rango intercuartil de 63,3–94,1 %, Burns et al. 2012; κ ponderado mediano 0,46–0,55, Okochi et al. 2005). Por eso la cobertura es la métrica más sensible a la referencia y la de sustento más débil (4.1: «criterio del proyecto»). Una segunda revisora permitiría medirlo (Artstein y Poesio 2008).
2. **La gravedad 0 no es un código esperado.** En la CIF el calificador 0 significa «no hay problema» (OMS 2001). La médica escribió `s110.0` en C13 y C21 y `b000.0` y `s000.0` en C19; esos 4 códigos cuentan hoy como esperados (3 no encontrados y 1 «encontrado»). Sensibilidad: sin ellos la cobertura es 36/63 = **0,571**, aún bajo 0,60, y el veredicto no cambia. No se modificó el `score`; si se adopta la corrección debe aprobarla el responsable. Se registra aquí como análisis de sensibilidad.
3. **Casos sin deficiencia física** (C05 y C13, psicosociales): el motor no busca estructuras cuando la categoría física es «Ninguna» (`rules.body_chapters`) y la médica espera `s110` (cerebro) en esquizofrenia (C05) y depresión (C13), aunque en C13 anota gravedad 0. Es una decisión de diseño de HU-07b; no hay acuerdo claro ni con ella, así que se deja como pregunta para la revisión con casos nuevos.

### 9.5 Conclusiones y qué se haría

El análisis no apunta a un modelo mayor como solución principal: la parte débil de funciones está en la búsqueda (46 % de techo) y la de estructuras en que el modelo completa la cuota. Orden propuesto, de menor a mayor costo, **cada paso medido con casos nuevos**:

| # | Acción | Efecto esperado | Riesgo | Sustento |
|---|---|---|---|---|
| 1 | **Estructuras: no completar la cuota.** Pedir solo las estructuras con evidencia en el diagnóstico o las notas, conservar siempre la primera y filtrar las posiciones 2 y 3 por similitud mínima | Estricta y flexible de s suben (la 1.ª posición ya es 0,81/0,95) | Baja la cobertura si se corta de más (9.2) | Chow 1970; Hripcsak y Rothschild 2005; Cieza et al. 2005 |
| 2 | **Funciones: ampliar y enriquecer candidatos.** De 12 a 16–20 candidatos y añadir los del capítulo 7 si D4 tiene dificultad | Techo de cobertura de b de 0,46 a unos 0,54–0,56 | Latencia y ruido por listas largas | Radovanović et al. 2010; Liu et al. 2024; Ewert et al. 2004 |
| 3 | **Prueba con casos nuevos** (20 a 25 casos sintéticos nuevos, incluidos visión, audición y discapacidad intelectual), revisados por la médica en Fase A y B, y comparación con el motor actual sobre los mismos casos | Medición confirmatoria sin sesgo de selección | Tiempo de la revisora | Cawley y Talbot 2010; Kapoor y Narayanan 2023; 4.4 |
| 4 | **Segunda revisora**, para medir el acuerdo y tener más de una referencia por caso | Cobertura menos dependiente de una persona | Disponibilidad | Artstein y Poesio 2008; Burns et al. 2012 |
| 5 | Medir `gemma4:12b` a `31b` solo si 1 y 2 no alcanzan | — | Latencia y memoria de 8 GB | Escalera de HU-07f |
| 6 | Si tras 1 a 4 no se cumple, **limitar el alcance** a actividades (cumplen) y funciones, con estructuras como opcionales | Alcance honesto del borrador de apoyo | — | Sección 5 |

**No se aprueba el uso clínico.** Los umbrales no se tocan para que el resultado «cumpla»: moverlos después de ver el resultado invalidaría la prueba (Kapoor y Narayanan 2023). Si la médica propone un ajuste clínico, se registra como decisión nueva y se vuelve a evaluar. Los pasos 1 y 2 se implementaron y midieron de forma preliminar el mismo día (sección 10); el paso 3 sigue pendiente.

**Reproducibilidad.** `icf-service/scripts/review_ablation.py` repite el recorte de estructuras de 9.2 y la sensibilidad de 9.4 con la hoja llena; `icf-service/scripts/variants_vs_review.py` compara las variantes del motor de la sección 10. Las cifras de 9.3 salen de `PgRepo.search` en el servicio local con el texto de `rules.context_text`; no hay script en el repositorio porque depende del catálogo de la OMS, que es privado.

**Nivel de verificación de las fuentes nuevas (ver 4.5).** Con DOI verificado contra Crossref: Cieza et al. 2005, Ewert et al. 2004, Chow 1970, Liu et al. 2024, Kapoor y Narayanan 2023 (nivel C: título, autores y DOI; el contenido se cita como técnica o hallazgo conocido). Con título, autores y volumen verificados en jmlr.org (sin DOI): Cawley y Talbot 2010, Radovanović et al. 2010. OMS 2001: documento oficial citado sin enlace verificado. Las cifras de 9.1 a 9.4 son cálculo propio (nivel D).

## 10. Corrección del motor y medición preliminar (26 de octubre de 2026)

Se implementaron tres cambios, apagados por defecto en `suggest()` (parámetros nuevos) para compararlos con el motor anterior, y se midieron con `icf-service/scripts/variants_vs_review.py` en el PC de producción (`gemma4:e4b`, mismo modelo; no se probó ningún modelo mayor). Las pruebas del servicio pasan (100 pasan y 7 se omiten; `test_app.py` necesita `psycopg`, que el CI sí instala).

| Cambio | Qué hace | Parámetro | Sustento |
|---|---|---|---|
| A. Estructuras con evidencia | El prompt pide solo las estructuras que el diagnóstico o las notas describen, sin completar la lista; el esquema exige al menos una (la 1.ª se conserva) | `s_evidence` | Chow 1970 (rechazo cuando el código falso cuesta más que omitir); Cieza et al. 2005 (se vincula lo que el texto contiene) |
| B. Vínculo de movilidad | Si el dominio D4 tiene dificultad, entran como candidatos las funciones `b710`, `b730`, `b735`, `b760` y `b770`, y el resumen del paciente lo menciona | `motor_link` | Reglas de vinculación (Cieza et al. 2005) y listas de funciones por condición (ICF Core Sets, Ewert et al. 2004); la regla es mía y los códigos concretos no se verificaron ítem por ítem contra los Core Sets |
| C. Más candidatos de funciones | `b_candidates` (16 o 20) y `motor_candidates` (los 3 más cercanos del capítulo 7) | `b_candidates`, `motor_candidates` | Lo contrario a lo que predice Liu et al. 2024 (listas largas empeoran la selección); se midió para descartarlo |

### 10.1 Resultados (24 casos, mismos de la revisión; **preliminar y optimista**)

Cobertura a ciegas = códigos b y s que la médica eligió sin ver la sugerencia y que el motor devuelve (67 en total). «Valoradas» = sugerencias que ella ya había valorado en la Fase B; las sugerencias nuevas **no tienen valoración**, así que su precisión se desconoce.

| Variante | Cobertura b+s | b | s | Sugeridas b / s | Precisión estricta / flexible entre las ya valoradas | Sugerencias nuevas sin valorar |
|---|---|---|---|---|---|---|
| V0 motor actual | 37/67 = 0,552 | 17/40 | 20/27 | 69 / 63 | 0,606 / 0,795 | 5 |
| V1 estructuras con evidencia (A) | 34/67 = 0,507 | 16/40 | 18/27 | 69 / 26 | 0,739 / 0,932 | 7 |
| V2 12 + 3 del capítulo 7 (C) | 37/67 = 0,552 | 17/40 | 20/27 | 69 / 63 | 0,620 / 0,802 | 11 |
| V3 16 + 3 del capítulo 7 (C) | 36/67 = 0,537 | 16/40 | 20/27 | 69 / 63 | 0,625 / 0,817 | 28 |
| V4 20 candidatos (C) | 35/67 = 0,522 | 16/40 | 19/27 | 69 / 63 | 0,643 / 0,837 | 34 |
| V5 A + V2 | 36/67 = 0,537 | 17/40 | 19/27 | 69 / 25 | 0,726 / 0,929 | 10 |
| V6 A + V3 | 35/67 = 0,522 | 16/40 | 19/27 | 69 / 25 | 0,760 / 0,947 | 19 |
| **V7 vínculo de movilidad (B)** | **44/67 = 0,657** | **26/40** | 18/27 | 69 / 63 | 0,709 / 0,848 | 53 |
| V8 A + B | 39/67 = 0,582 | 24/40 | 15/27 | 69 / 24 | 0,923 / 1,000 | 41 |

Lecturas:

1. **Ampliar candidatos (C) no sirve** (V2 a V6): el techo de la búsqueda sube de 18 a 21–24 de 39, pero el modelo no elige los códigos nuevos y la cobertura no mejora o empeora (16 a 17 de 40). Es lo que predice Liu et al. 2024 para listas largas, y los códigos `b760` y `b770` ni siquiera entran entre los 3 más cercanos del capítulo 7: la búsqueda por el texto del diagnóstico no los alcanza («tetraparesia» no se parece, en el espacio de embeddings, a «control del movimiento voluntario»; Radovanović et al. 2010).
2. **El vínculo de movilidad (B) es el cambio que más mueve la cobertura de funciones**: de 17 a 26 de 40 y, en total, de 0,552 a 0,657, sin cambiar el número de sugerencias ni la latencia (≈ 2,5 s). Es una regla clínica explícita y trazable, no un modelo más grande.
3. **Estructuras con evidencia (A) cumple su objetivo de precisión**: de 63 a 24–26 estructuras sugeridas (1,1 por caso, igual que la médica) y la precisión entre las ya valoradas sube de 0,61 a 0,74 estricta y de 0,80 a 0,93 flexible. Cuesta cobertura de estructuras (de 20 a 15–18 de 27): es la compensación precisión–exhaustividad de 9.2.
4. **Hay variabilidad del modelo entre corridas.** Segunda corrida de cuatro variantes: V0 35/67 (antes 37), V1 34/67 (igual), V7 43/67 (antes 44) y V8 40/67 (antes 39). La variación es de 1 a 2 códigos, así que esas diferencias no se interpretan; la ganancia de V7 sobre V0 (+7 a +9) es mayor que ese ruido. En la segunda corrida la precisión entre las ya valoradas fue V0 0,594/0,789, V1 0,739/0,932, V7 0,688/0,838 y V8 0,923/1,000.

### 10.2 Lo que NO se puede concluir todavía

- **El vínculo B se diseñó mirando los códigos que la médica eligió** (`b730`, `b760`, `b770` eran las omisiones), de modo que su mejora de cobertura **está inflada**: es el escenario de fuga entre diseño y evaluación que describen Cawley y Talbot 2010 y Kapoor y Narayanan 2023. La mejora real solo se conoce con casos nuevos.
- **Las sugerencias nuevas no tienen valoración** (53 en V7, 41 en V8). Si el vínculo añade `b735` o `b760` a pacientes donde no corresponden, la precisión baja y hoy no se ve. La «precisión entre las ya valoradas» excluye justo esos códigos y por eso sube (sesgo de selección).
- Las cifras de V8 (0,923 de precisión) se calculan sobre 52 códigos, la mayoría de la 1.ª posición, la más fácil de acertar.
- Dos corridas como máximo por variante, con un modelo no determinista.

### 10.3 Decisión y estado

- **Quedan activos por defecto A y B** (`ICF_S_EVIDENCE=true`, `ICF_MOTOR_LINK=true`, variante V8) en `icf-service`; con `false` se vuelve al motor anterior. **No se adoptó C** (más candidatos) por no aportar. No se probó ningún modelo mayor: se sigue con `gemma4:e4b`, como se decidió.
- **Por qué V8 y no solo V7:** V7 tiene más cobertura (0,64–0,66) pero deja las estructuras con 63 sugerencias y la precisión de s en 0,44; V8 (cobertura 0,58–0,60) deja 1,1 estructuras por caso como la médica. La elección entre ambas se hace con la valoración de las sugerencias nuevas, no con estas cifras (10.2).
- **Pruebas:** 5 pruebas nuevas en `tests/test_engine.py` (prompt y esquema con evidencia, vínculo de movilidad con y sin dificultad en D4, y los dos interruptores); el servicio pasa 105 pruebas con 7 omitidas.
- **Costo:** sin cambio medible de latencia (≈ 1,9 a 2,5 s por sugerencia).
- **Producción actualizada (26-oct-2026):** se reconstruyó la imagen de `icf-service` en el PC de producción (`docker compose up -d --build --no-deps icf-service`; la base y Caddy no se tocaron) y `check.ps1 -Public -Suggest` terminó en «Todo correcto» (local y por el túnel público, token verificado, `/api/generate` bloqueado). La sugerencia sintética ahora devuelve `b735 b760 b770` y una sola estructura, en 2,1 s. Los tres ambientes de Render usan este servicio; no hizo falta tocar Render porque los ajustes están activos por defecto en el servicio.
- **Hoja corta para la médica (preparada el 26-oct-2026):** `data/private/icf/review/hoja_codigos_nuevos.xlsx` (privada, trae títulos de la OMS) con las **41 sugerencias nuevas** de la configuración activa sobre los mismos casos, con descripción, diagnóstico y notas, y las mismas columnas de valoración de la Fase B. No incluye Fase A porque ella ya conoce los casos. Al devolverla, `variants_vs_review.py score-new` calcula la precisión real de la configuración activa uniendo sus valoraciones viejas y las nuevas, con IC de Wilson (la cobertura no cambia: sale de la Fase A).
- **Qué falta:** (1) que la médica valore las 41 sugerencias; (2) revisión de casos nuevos (20 a 25) con Fase A y Fase B, única forma de medir sin la fuga de 10.2 (Cawley y Talbot 2010; Kapoor y Narayanan 2023). Los umbrales no se modifican.

## 11. Segunda ronda: la médica valora las sugerencias nuevas (26 de octubre de 2026)

La revisora valoró las **41 sugerencias nuevas** de la configuración activa (37 funciones y 4 estructuras; `hoja_codigos_nuevos.xlsx`, privada). Con sus valoraciones anteriores se tiene la **precisión real de la configuración activa en los 24 casos** (93 sugerencias, todas valoradas), y con la Fase A, la cobertura. Se calculó con el mismo evaluador del `score` (`compute_metrics` y `evaluate_thresholds`), sin cambiar umbrales.

### 11.1 Resultado frente a los umbrales

| Criterio | Antes (motor anterior) | **Ahora (configuración activa)** | IC 95 % (Wilson) | Meta | Piso del IC | Estado |
|---|---|---|---|---|---|---|
| Casos revisados | 23 | 23 | | ≥ 20 | | Cumple |
| Precisión estricta b+s | 0,591 | **0,710** (66/93) | 0,611–0,792 | ≥ 0,60 | 0,40 | **Cumple** |
| Precisión flexible b+s | 0,788 | **0,871** (81/93) | 0,788–0,925 | ≥ 0,80 | 0,60 | **Cumple** |
| Cobertura a ciegas b+s | 0,552 (37/67) | **0,582** (39/67) | 0,463–0,693 | ≥ 0,60 | 0,40 | **No cumple** (valor bajo la meta) |
| Calificador b+s (κ ponderado) | 0,576 | **0,540** | por casos 0,294–0,708 | ≥ 0,50 | | Cumple |
| Precisión flexible d | 1,000 | 1,000 | 0,947–1,0 | ≥ 0,80 | 0,60 | Cumple |

**Veredicto: NO CUMPLE, ahora por un solo criterio** (la cobertura queda 1,8 puntos bajo la meta: le faltan 2 códigos de 67). Pasaron de fallar tres criterios a fallar uno. El IC de la cobertura (0,463–0,693) contiene la meta, de modo que, como en 8.1, el resultado no demuestra estar por debajo ni por encima (Jones et al. 1996; Flahault et al. 2005). Las dos precisiones cumplen su meta y el límite inferior de su IC supera el piso; el límite inferior de la flexible (0,788) queda 1,2 puntos bajo la meta de 0,80, un margen comparable a la variabilidad entre codificadores humanos (Burns et al. 2012).

Por componente:

| | Sugerencias | Estricta | Flexible | Antes (estricta / flexible) |
|---|---|---|---|---|
| Estructuras (s) | 24 | **0,792** | 0,833 | 0,444 / 0,635 |
| Funciones (b) | 69 | 0,681 | 0,884 | 0,725 / 0,928 |

Además: calificador correcto (Fase B) 0,753; precisión a ciegas 0,419 y F1 0,487 (antes 0,28 y 0,37); acuerdo por capítulo κ 0,753 y cobertura por capítulo 0,804 (antes 0,666 y 0,857).

### 11.2 Qué funcionó y qué no

1. **Estructuras con evidencia: funcionó.** Pasó de 63 a 24 estructuras sugeridas (1,1 por caso, como la médica) y la precisión estricta de 0,444 a 0,792; la médica solo rechazó 4 estructuras nuevas, todas por «sin evidencia estructural». Es la predicción de la clasificación con rechazo (Chow 1970) y de la regla de vincular solo lo que el texto contiene (Cieza et al. 2005). Costo: la cobertura de estructuras bajó de 20 a 15 de 27 (ver punto 3).
2. **Vínculo de movilidad: ayudó a la cobertura y costó precisión de funciones.** La cobertura de funciones subió de 17 a 24 de 40, pero de las 37 funciones nuevas la médica valoró 18 «Adecuado», 11 «Aceptable» y **8 «No adecuado»**: la precisión de funciones bajó de 0,725/0,928 a 0,681/0,884. Los 8 rechazos son todos del mismo tipo: el vínculo propuso `b770` (marcha), `b730` (fuerza), `b760` o `b710` en casos cuya limitación principal no es motora (hipoacusia, asma leve, TEPT, deterioro cognitivo por alcohol, síndrome de Down, TEA), donde D4 tiene una dificultad leve o moderada (10 a 40). Comentarios como «asma leve no afecta la marcha» o «TEPT no implica déficit muscular» apuntan a que la regla se dispara con cualquier dificultad en D4, sin exigir una limitación motora. Es la misma falta de especificidad que se corrigió en estructuras.
3. **Efecto colateral en estructuras: `s110` (cerebro).** Cinco de las 28 omisiones restantes son `s110` en cuadros mentales o del neurodesarrollo (esquizofrenia, síndrome de Down, TEA, depresión, TEPT); en C05 y C13 el motor no busca estructuras (categoría física «Ninguna») y en C06, C09 y C21 elige una estructura periférica (`s770`, `s750`, `s760`) en vez del cerebro. Con la regla de evidencia el modelo no infiere la estructura implícita del diagnóstico (la médica sí).
4. **Las otras omisiones** son dispersas: `b167` y `b144` (2 cada una), `b730` (2), `s750` y `s760` (2 cada una) y una por código en `b125`, `b156`, `b620`, `b765`, `b770`, `b410`, `b440` y `b152`.

### 11.3 Lectura y sensibilidad

- **El avance es real pero en parte optimista.** El vínculo de movilidad se diseñó viendo las omisiones de la médica (10.2); la cobertura de 0,582 incluye ese efecto. Las precisiones, en cambio, sí son valoraciones de la médica a las sugerencias reales, sin la selección de 10.1: son la mejor medida que existe de la configuración activa, aunque sobre los mismos casos con los que se diagnosticó.
- **Sensibilidad (9.4, punto 2):** si no se cuentan como «esperados» los 4 códigos que la médica calificó con gravedad 0 (`b000` y `s000` en C19, `s110` en C13 y C21), la cobertura sería 39/63 = **0,619** y el criterio se cumpliría. **No se aplica al veredicto oficial**: la definición de «esperado» se fijó antes de ver este resultado y cambiarla ahora, para que el número pase, es el movimiento que se debe evitar (Kapoor y Narayanan 2023); la corrección tiene sustento (calificador 0 = «no hay problema», OMS 2001) y debe decidirla el responsable, con la regla escrita antes de los casos nuevos.
- **Dos usos de los mismos 24 casos** (diagnóstico y ajuste, y ahora medición) hacen que el siguiente ajuste ya no se pueda afinar con ellos sin sesgar (Cawley y Talbot 2010).

### 11.4 Qué sigue

| # | Acción | Sustento |
|---|---|---|
| 1 | **Acotar el vínculo de movilidad** a casos con limitación motora (por ejemplo, categoría física al menos moderada y dificultad de movilidad que supere un nivel mínimo), en lugar de cualquier dificultad en D4; apunta a recuperar la precisión de funciones sin perder cobertura | Cieza et al. 2005 (se vincula lo que el caso evidencia); es una hipótesis formulada con estos casos, no se mide con ellos |
| 2 | **No aplicar la regla de evidencia a la estructura principal de cuadros mentales o del neurodesarrollo**, o permitir `s110` cuando el diagnóstico es neurológico o psiquiátrico | Mismo sustento; igual limitación |
| 3 | **Revisar 20 a 25 casos nuevos** con Fase A y Fase B, definiendo antes de verlos el criterio de «esperado» (incluida la gravedad 0) y las reglas del paso 1 y 2 | Cawley y Talbot 2010; Kapoor y Narayanan 2023; 4.4 |
| 4 | **Segunda revisora** | Artstein y Poesio 2008; Burns et al. 2012 |

Los 3 pts de 07g siguen sin acreditarse hasta que el responsable decida; el uso clínico no se aprueba. Para repetir el cálculo: `variants_vs_review.py score-new` (precisión y cobertura) y el cálculo completo con `compute_metrics` y `evaluate_thresholds` descrito arriba (calificador incluido).

## 12. Tercera ronda con casos nuevos: reglas fijadas antes de ver las sugerencias (27 de octubre de 2026)

Esta sección se escribe y se sube **antes** de generar las sugerencias de los casos nuevos y de dárselos a la médica. Es el equivalente de un registro previo del análisis: fijar por escrito qué se mide y cómo se decide antes de ver los datos evita ajustar la regla al resultado (Nosek et al. 2018; Kapoor y Narayanan 2023). Los 24 casos de las rondas 1 y 2 ya se usaron para diagnosticar los errores y para medir la corrección; con ellos no se puede volver a ajustar sin sesgo (Cawley y Talbot 2010).

### 12.1 Cambios al motor desde la ronda 2

Se hicieron tras el análisis de 11.2, con sustento clínico y sin cambiar de modelo (`gemma4:e4b`). Una comprobación en los casos antiguos solo verifica que no se rompió nada: **no cuenta como validación**.

| Cambio | Qué hace | Por qué | Sustento |
|---|---|---|---|
| Vínculo de movilidad más estricto | Solo si la deficiencia física es al menos moderada y D4 ≥ 50 (limitación de movilidad grave, calificador ≥ 3) | En la ronda 2 la médica rechazó 8 de 37 funciones nuevas en casos sin limitación motora, todos con D4 entre 10 y 40 | Se vincula lo que el caso evidencia (Cieza et al. 2005); umbral de 50 = calificador 3 «grave» de la propia escala (OMS 2001) |
| Vínculo mental | Sin deficiencia física pero con psicosocial, las estructuras se buscan en el capítulo 1 (sistema nervioso) | La médica esperaba `s110` en esquizofrenia y depresión y el motor no buscaba estructuras | Las funciones mentales (b1) se vinculan con estructuras del sistema nervioso (reglas de vinculación, Cieza et al. 2005) |
| Regla de evidencia, con una excepción | Se agrega al prompt: si el diagnóstico es neurológico, del neurodesarrollo o psiquiátrico, la estructura es la cerebral | La regla de evidencia hacía elegir estructuras periféricas en síndrome de Down, TEA y TEPT | Mismo sustento |

Las tres reglas son interruptores (`ICF_MOTOR_LINK`, `ICF_MENTAL_LINK`, `ICF_S_EVIDENCE`) y están cubiertas por pruebas. Comprobación en los 24 casos antiguos (no es validación): cobertura 0,657 (44/67) y 23 estructuras sugeridas.

### 12.2 Casos

24 casos sintéticos nuevos, `icf-service/reference/cases_ronda2.json` (N01 a N24), escritos antes de ver sus sugerencias y distintos de C01 a C25. Cubren lo que el primer set cubría poco: visión (3), audición (2, con sordoceguera), discapacidad intelectual (2), neurológicas (esclerosis lateral, esclerosis múltiple, epilepsia, hemiplejia, paraplejia, lesión de plexo braquial), psiquiátricas y del neurodesarrollo (bipolar, ansiedad, TDAH, tartamudez), crónicas (EPOC, renal, diabetes con neuropatía, lupus) y osteomusculares (artrosis, fractura, amputación, escoliosis). Incluyen menores de edad (8, 9, 14, 15 y 16 años). No hay datos de personas reales.

### 12.3 Reglas de medición (no se cambian después de ver los resultados)

1. **Umbrales: los mismos** de 4.1 (precisión estricta ≥ 0,60, flexible ≥ 0,80, cobertura ≥ 0,60, κ ponderado ≥ 0,50 sobre al menos 30 pares, actividades ≥ 0,80, casos revisados ≥ 20), con los mismos pisos del IC.
2. **Definición de «esperado»:** los códigos que la médica califica con **gravedad 0 en la Fase A no cuentan como esperados**, porque en la CIF el calificador 0 significa «no hay problema» (OMS 2001) y no es algo que el sistema deba sugerir. Se calcula con `review_sheet.py score --exclude-zero-severity` (función `without_zero_severity`, con prueba). Es una definición que se identificó viendo la ronda 1; se fija ahora, antes de los datos nuevos, y **se informa también la medición sin esta exclusión** como sensibilidad.
3. **Motor congelado:** se mide con el código del commit que sube esta sección y la configuración por defecto. Mientras la médica revisa, no se cambia el motor.
4. **Fase A antes de la B:** igual que en la ronda 1, para evitar el sesgo de anclaje (Fase A a ciegas con gravedad 0 a 4).
5. **Veredicto:** CUMPLE solo si los seis criterios se cumplen sobre los 24 casos nuevos. Cualquier resultado se informa completo.
6. **Si no cumple:** no se reajusta con estos casos. Los ajustes se miden en una cuarta ronda con casos nuevos y se vuelve a decidir.
7. **Límites que se mantienen:** una sola revisora; casos sintéticos; con 24 casos, diferencias de unos pocos puntos no se distinguen (4.4); el acuerdo entre profesionales no se mide hasta que haya una segunda revisora (Artstein y Poesio 2008).

### 12.4 Cómo se corre

```powershell
# sugerencias y hoja de revisión de la tercera ronda (contenedor temporal con la imagen del servicio y openpyxl)
python scripts/review_sheet.py generate --cases reference/cases_ronda2.json --output ..\data\private\icf\review\hoja_ronda3.xlsx
# con la hoja devuelta
python scripts/review_sheet.py score ..\data\private\icf\review\hoja_ronda3_llena.xlsx --exclude-zero-severity --output informe_ronda3.json
python scripts/review_sheet.py score ..\data\private\icf\review\hoja_ronda3_llena.xlsx    # sensibilidad, definición anterior
```

### 12.5 Estado (27 de octubre de 2026)

- Reglas y casos publicados en `develop` (commit `30cd5ec`) antes de generar las sugerencias.
- **Producción reconstruida** con ese commit (`check.ps1 -Public -Suggest`: «Todo correcto»; la sugerencia sintética devuelve 3 funciones y 1 estructura en 2,0 s).
- **Hoja generada:** `data/private/icf/review/hoja_ronda3.xlsx` (privada, trae títulos de la OMS), con los 24 casos aplicables, la Fase A a ciegas con gravedad 0 a 4, la Fase B y la hoja de faltantes. Se generó en un contenedor temporal con la imagen del servicio (`icf-service:latest`), la red `hab-icf_default` y el mismo código y la misma configuración que producción. El motor devolvió 3 funciones por caso y **1 estructura en 21 casos y 3 en 3 casos** (N02 baja visión, N14 amputación de miembro superior y N20 sordoceguera).
- **Falta:** que la médica complete la hoja (unos 60 a 90 minutos); luego `score` con y sin `--exclude-zero-severity` y el informe de resultados.
