# Protocolo de validación clínica del Perfil Funcional ICF (HU-07g)

**Fecha:** 7 de octubre de 2026
**Estado:** instrumento listo y **umbrales aprobados por el responsable el 7 de octubre de 2026**; **pendiente la revisión de la profesional de salud** (Emilly Maria Celis), con quien se reúne la próxima semana (fecha por definir).
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

## 7. Pendientes

1. ~~Regenerar la hoja~~ **Hecho el 21 de octubre de 2026:** la hoja del 9 de octubre no pedía la gravedad a ciegas, así que se actualizó con `review_sheet.py upgrade` y quedó en `data/private/icf/review/hoja_revision_v2.xlsx` (24 casos y las mismas 201 sugerencias; la original no se tocó). Solo hace falta volver a correr `generate` (base de datos y Ollama) si se quiere una sugerencia nueva del modelo.
2. Correr `python scripts/repeatability.py --runs 5 --output ...` y anotar el resultado (no necesita a la revisora).
3. Que el responsable apruebe los pisos del IC (`CI_FLOORS`) y el κ ≥ 0,50 del calificador (decidido el 21 de octubre, anclado a la fiabilidad humana según 4.6), y decida si el límite inferior del κ (por bootstrap de casos) pasa a ser criterio con un piso (ver 4.4, «Brecha conocida»).
4. Presentar los umbrales y la sección 4.1 a la revisora en la reunión de la próxima semana.
5. Entregar la hoja regenerada a la revisora por un canal privado.
6. Recibir la hoja llena, correr `score` y documentar el resultado en este archivo y en `BACKLOG.md`. Con eso se completa HU-07g.
