# Guía de Entrevista Semiestructurada — HAB (Perfil No Clínico)

> **Uso:** Guía adaptada para entrevistar personas **fuera del gremio de la salud** con conocimiento leve o contextual de la discapacidad (ej. profesionales de SST, funcionarios de alcaldías, personal de ICBF, trabajadores sociales, ONG).  
> **Duración estimada:** 30–40 minutos  
> **Aplicación a evaluar:** Health Access Bridge (HAB) — `https://hab-frontend-qa.onrender.com`

---

## Perfiles objetivo de esta guía

| ID | Perfil tipo | Ejemplo |
|----|-------------|---------|
| E-NC1 | Profesional SST / bienestar laboral | ICBF, ARL, empresa privada |
| E-NC2 | Funcionario de gobierno local | Alcaldía, secretaría de planeación |
| E-NC3 | Trabajador social / ONG | Fundaciones, entidades sin ánimo de lucro |
| E-NC4 | Coordinador de programas sociales | SENA, UARIV, Prosperidad Social |

> **Nota:** Estos participantes conocen el **contexto** de la discapacidad (ley 1618/2012, PABS, ICF) pero no tienen formación clínica ni gestionan pacientes directamente. Sus respuestas informan la usabilidad institucional y la comunicación inter-sectorial del sistema.

---

## Instrucciones para el entrevistador

- Presentarse y aclarar que la sesión busca **entender cómo su institución se relaciona con el tema de discapacidad**, no evaluar al participante.
- **No usar términos clínicos** (diagnóstico diferencial, HIS, RIPS) a menos que el participante los mencione primero.
- Adaptar la terminología al contexto institucional del participante (SST → "riesgo laboral y discapacidad", Alcaldía → "políticas de inclusión", ICBF → "protección y bienestar familiar").
- Usar **sondas de profundización**: *"¿Cómo impacta eso en su trabajo cotidiano?"* / *"¿Podría darme un ejemplo concreto?"*
- Registrar: nivel de familiaridad con plataformas digitales, vocabulario espontáneo sobre discapacidad, reacciones a la demo.

---

## BLOQUE 0 — Presentación y contexto (5 min)

> Leer textualmente al inicio:

*"Buenos días/tardes. Mi nombre es [NOMBRE]. Estoy realizando una investigación para mejorar una plataforma digital llamada Health Access Bridge, que apoya la gestión de información sobre personas con discapacidad en zonas rurales. Me interesa mucho entender cómo instituciones como la suya se involucran con este tema, qué información manejan y qué dificultades encuentran. No hay respuestas correctas ni incorrectas. ¿Tiene alguna pregunta antes de comenzar?"*

---

## BLOQUE A — Contexto institucional y rol (8 min)

**A1.** ¿Podría contarme brevemente cuál es su cargo y cuál es el rol de su institución en relación con las personas con discapacidad?

**A2.** ¿Con qué frecuencia su trabajo le exige interactuar con o tomar decisiones relacionadas con personas con discapacidad? ¿En qué tipo de situaciones?

**A3.** ¿Qué herramientas digitales o sistemas usa actualmente para gestionar, consultar o reportar información relacionada con discapacidad? *(ej. Excel, plataformas del Ministerio, SISPRO, RLCPD, correo electrónico)*

**A4.** ¿Desde qué dispositivo accede principalmente a estas herramientas? *(computador de oficina, celular, tablet)*

**A5.** En una escala del 1 al 5, ¿qué tan cómodo/a se siente usando aplicaciones web para consultar o reportar información? *(1 = poco cómodo, 5 = muy cómodo)*

---

## BLOQUE B — Flujo de trabajo y puntos de dolor institucional (12 min)

**B1.** Cuando en su institución necesitan conocer el estado de una persona con discapacidad (para una decisión, un reporte, un beneficio), ¿cómo obtienen esa información? ¿Quién se la proporciona?

**B2.** ¿Ha tenido dificultades para acceder a información sobre el historial o el estado de salud/funcionalidad de personas con discapacidad? ¿Qué pasa cuando esa información no está disponible a tiempo?

**B3.** ¿Cómo coordina su institución con los servicios de salud para el seguimiento de personas con discapacidad? ¿Existe algún canal formal o es informal?

**B4.** ¿Cuánto tiempo demoran en su institución en generar un informe o reporte sobre población con discapacidad para una entidad externa?

**B5.** ¿Qué es lo que más dificulta o frustra a su equipo cuando trabaja con información de personas con discapacidad?

**B6.** ¿Ha tenido casos en los que la falta de información oportuna afectó una decisión o la atención a una persona con discapacidad? *(Sin pedir datos sensibles, solo el impacto general)*

> *Para perfil SST / ICBF (E-NC1): agregar*

**B7-SST.** ¿Su institución genera registros de incapacidad o valoración funcional de sus trabajadores o beneficiarios? ¿Cómo los gestionan?

> *Para perfil gobierno local / Alcaldía (E-NC2): agregar*

**B7-GOV.** ¿Cómo recibe la alcaldía la información del PABS o del Registro para la Localización y Caracterización de Personas con Discapacidad (RLCPD)? ¿Qué hacen con esos datos?

---

## BLOQUE C — Demo de HAB y expectativas (10 min)

> *Mostrar brevemente las pantallas del ambiente QA (5 min). Secuencia sugerida: Login → Dashboard (métricas) → Listado de Pacientes → Módulo de Análisis.*  
> *Enmarcar la demo así:* *"Esta aplicación es usada por profesionales de salud para registrar y hacer seguimiento a pacientes con discapacidad, y tiene un módulo que predice el perfil de barreras de acceso de cada persona."*

**C1.** Después de ver esta aplicación, ¿qué información de la que muestra el sistema podría serle útil a su institución?

**C2.** ¿Hay algún módulo o función que le resultó especialmente relevante para el trabajo de su área?

**C3.** ¿Hay algo que le resultó confuso, intimidante o que no está seguro/a de entender desde su perspectiva no clínica?

**C4.** El sistema clasifica automáticamente a los pacientes según su perfil de barreras de acceso (Perfil 1: bajas, 2: moderadas, 3: altas). Como funcionario/a de su institución, ¿qué haría con esa información si la tuviera disponible?

**C5.** Si su institución pudiera usar una herramienta así para coordinar acciones con el sector salud, ¿qué información sería indispensable que tuviera?

**C6.** ¿Qué tan probable es que recomendara una plataforma como esta a otras instituciones que trabajan con discapacidad? *(Escala 0–10, tipo NPS)*

---

## BLOQUE D — Escala SUS Simplificada (5 min)

> *Instrucción: "A continuación voy a leerle 5 afirmaciones sobre la aplicación que acaba de ver. Por favor responda qué tan de acuerdo está con cada una, en una escala de 1 (totalmente en desacuerdo) a 5 (totalmente de acuerdo)."*

| # | Afirmación | 1 | 2 | 3 | 4 | 5 |
|---|-----------|---|---|---|---|---|
| SUS1 | Me sentiría cómodo/a consultando información de esta aplicación con frecuencia | ☐ | ☐ | ☐ | ☐ | ☐ |
| SUS2 | Encontré la aplicación innecesariamente compleja para alguien fuera del sector salud | ☐ | ☐ | ☐ | ☐ | ☐ |
| SUS3 | Creo que un funcionario de mi área podría aprender a consultar esta aplicación sin mucha dificultad | ☐ | ☐ | ☐ | ☐ | ☐ |
| SUS4 | Me sentí seguro/a con respecto a la privacidad de los datos al ver esta aplicación | ☐ | ☐ | ☐ | ☐ | ☐ |
| SUS5 | Necesitaría una capacitación específica antes de poder usar esta aplicación con confianza | ☐ | ☐ | ☐ | ☐ | ☐ |

> **Puntuación SUS:** (SUS1+SUS3+SUS4−3) × 12.5 + (15 − SUS2×2.5 − SUS5×2.5)  
> Puntaje ≥ 68 → Aceptable | ≥ 80 → Buena | ≥ 90 → Excelente  
> **Referencia:** En perfiles no clínicos se espera un puntaje entre 50–75; el foco está en identificar barreras de comprensión, no solo de usabilidad.

---

## Cierre (2 min)

*"Hemos llegado al final. ¿Tiene algún comentario adicional o algo que no hayamos preguntado y que considere importante? Muchas gracias por su tiempo. Sus respuestas ayudarán a que esta herramienta sea útil no solo para el sector salud sino para instituciones como la suya."*

---

## Notas del entrevistador

| Campo | Observación |
|-------|-------------|
| Fecha y hora | |
| Institución y cargo del participante | |
| Lugar / modalidad | |
| Duración real | |
| Nivel de familiaridad con discapacidad (escala percibida 1–5) | |
| Vocabulario espontáneo sobre discapacidad | |
| Reacción ante la demo (confusión / interés / indiferencia) | |
| Términos clínicos que no entendió | |
| Citas textuales destacadas | |
| Necesidades institucionales no previstas | |
| Sugerencias de interoperabilidad con sus sistemas | |
