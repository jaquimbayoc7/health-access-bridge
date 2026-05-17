# Guía de Entrevista Semiestructurada — HAB

> **Uso:** Documento de apoyo para el entrevistador. No leer literalmente; seguir el hilo natural de la conversación.  
> **Duración estimada:** 35–45 minutos  
> **Aplicación a evaluar:** Health Access Bridge (HAB) — `https://hab-frontend-qa.onrender.com`

---

## Instrucciones para el entrevistador

- Presentarse brevemente y explicar que la sesión busca **mejorar la aplicación**, no evaluar al usuario.
- Aclarar que **no hay respuestas correctas o incorrectas**.
- Solicitar consentimiento verbal para grabar, además del consentimiento firmado.
- Tomar notas en papel o digitalmente durante la sesión.
- Usar **sondas de profundización** cuando sea necesario: *"¿Puedes contarme más sobre eso?"* / *"¿Qué pasó después?"* / *"¿Por qué es importante para ti?"*
- Evitar preguntas leading como "¿No crees que sería mejor si...?"

---

## BLOQUE 0 — Presentación y contexto (5 min)

> Leer textualmente al inicio:

*"Buenos días/tardes. Mi nombre es [NOMBRE]. Estoy realizando una investigación de usuarios para mejorar una plataforma de gestión clínica llamada Health Access Bridge. Quiero entender cómo trabajan profesionales como usted en su día a día, qué herramientas usan y qué dificultades encuentran. No hay respuestas buenas ni malas. ¿Tiene alguna duda antes de empezar?"*

---

## BLOQUE A — Contexto y perfil del usuario (8 min)

### Preguntas de apertura (todos los perfiles)

**A1.** ¿Podría contarme brevemente cuál es su rol en la institución de salud donde trabaja y cuántos años lleva ejerciéndolo?

**A2.** En un día típico de trabajo, ¿cuáles son las principales actividades que realiza con pacientes con discapacidad?

**A3.** ¿Qué herramientas digitales utiliza actualmente para gestionar información de pacientes? (ej. Excel, sistema HIS, papel, apps móviles)

**A4.** ¿Con qué frecuencia usa estas herramientas y desde qué dispositivo? (computador de escritorio, portátil, celular, tablet)

**A5.** En una escala del 1 al 5, ¿cómo calificaría su comodidad con el uso de aplicaciones web en general? *(1 = muy poco cómodo, 5 = muy cómodo)*

---

## BLOQUE B — Flujo de trabajo actual y puntos de dolor (15 min)

**B1.** Cuando recibe un paciente nuevo con discapacidad, ¿cómo es el proceso de registro de su información clínica? ¿Podría describir paso a paso lo que hace?

**B2.** ¿Qué información clínica considera **imprescindible** registrar de un paciente con discapacidad? ¿Hay algún dato que actualmente no puede capturar con las herramientas que tiene?

**B3.** ¿Cuánto tiempo le toma registrar a un paciente nuevo de inicio a fin? ¿Le parece razonable ese tiempo?

**B4.** ¿Ha tenido que buscar información de un paciente registrado con anterioridad? ¿Fue fácil encontrarla?

**B5.** ¿Qué es lo que más le **frustra** o complica de las herramientas digitales que usa hoy para el trabajo clínico?

**B6.** ¿Ha experimentado problemas de conectividad a internet en su lugar de trabajo? ¿Cómo afecta eso su trabajo?

> *Para el perfil administrativo (E2): agregar*

**B7-ADM.** ¿Cómo gestiona actualmente los accesos y permisos del personal de salud a los sistemas de información? ¿Qué tan frecuente es crear o desactivar usuarios?

> *Para el perfil familiar/cuidador (E3): agregar*

**B7-FAM.** ¿Cómo recibe actualmente información sobre el seguimiento de salud del familiar que cuida? ¿Le gustaría poder acceder a algún tipo de reporte o resumen?

---

## BLOQUE C — Demo de HAB y expectativas (12 min)

> *Mostrar brevemente las pantallas de la aplicación en el ambiente QA (5 min de navegación guiada). Mostrar: Login → Dashboard → Pacientes → Predicciones.*

**C1.** Después de ver esta primera vista de la aplicación, ¿cuál es su impresión inicial?

**C2.** ¿Hay alguna función que haya visto que le parezca especialmente **útil** para su trabajo?

**C3.** ¿Hay algo que le haya parecido **confuso** o que no entendió a primera vista?

**C4.** El sistema tiene un módulo de predicción que, con los datos clínicos del paciente, clasifica automáticamente su perfil de barreras de acceso a la salud. ¿Utilizaría ese resultado en sus decisiones clínicas? ¿Por qué sí o por qué no?

**C5.** Si pudiera **agregar o cambiar** una sola cosa de esta aplicación para que fuera más útil en su trabajo diario, ¿qué sería?

**C6.** ¿Qué tan probable es que recomiende una herramienta como esta a un colega? *(Escala 0–10, tipo NPS)*

---

## BLOQUE D — Escala SUS Simplificada (5 min)

> *Instrucción: "A continuación voy a leerle 5 afirmaciones sobre la aplicación que acaba de ver. Por favor responda qué tan de acuerdo está con cada una, en una escala de 1 (totalmente en desacuerdo) a 5 (totalmente de acuerdo)."*

| # | Afirmación | 1 | 2 | 3 | 4 | 5 |
|---|-----------|---|---|---|---|---|
| SUS1 | Me sentiría cómodo/a usando esta aplicación con frecuencia | ☐ | ☐ | ☐ | ☐ | ☐ |
| SUS2 | Encontré la aplicación innecesariamente compleja | ☐ | ☐ | ☐ | ☐ | ☐ |
| SUS3 | Creo que la mayoría de profesionales de salud podrían aprender a usar esta aplicación rápidamente | ☐ | ☐ | ☐ | ☐ | ☐ |
| SUS4 | Me sentí seguro/a con respecto a la privacidad de los datos al usar esta aplicación | ☐ | ☐ | ☐ | ☐ | ☐ |
| SUS5 | Necesitaría capacitación antes de poder usar esta aplicación con confianza | ☐ | ☐ | ☐ | ☐ | ☐ |

> **Puntuación SUS:** (SUS1+SUS3+SUS4−3) × 12.5 + (15 − SUS2×2.5 − SUS5×2.5)  
> Puntaje ≥ 68 → Usabilidad aceptable | ≥ 80 → Buena | ≥ 90 → Excelente

---

## Cierre (2 min)

*"Hemos llegado al final de la entrevista. ¿Tiene alguna pregunta o comentario adicional que desee compartir? Muchas gracias por su tiempo y disposición. Sus respuestas son muy valiosas para mejorar esta herramienta."*

---

## Notas del entrevistador

| Campo | Observación |
|-------|-------------|
| Fecha y hora | |
| Lugar / plataforma | |
| Duración real | |
| Observaciones de lenguaje no verbal | |
| Citas destacadas (textual) | |
| Comportamiento ante la demo | |
| Emociones percibidas | |
| Temas emergentes no previstos | |
