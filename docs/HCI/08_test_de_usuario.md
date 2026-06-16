# Test de Usuario — Health Access Bridge (HAB)

> **Actividad:** Act_19 — Test de Usuario · Fase 4 Final  
> **Proyecto:** Health Access Bridge (HAB) — plataforma de gestión clínica para pacientes con discapacidad  
> **Metodología:** Test de usabilidad con observación + instrumentos cualitativos y cuantitativos  
> **Demo de referencia:** `https://hab-frontend-qa.onrender.com`  
> **Fecha de aplicación:** Junio 2026

---

## Objetivo del test

Evaluar la usabilidad, la carga cognitiva y la respuesta emocional de usuarios reales ante las funcionalidades centrales de HAB, identificando fricciones, puntos de confusión y oportunidades de mejora antes del lanzamiento de Release 2.

---

## Participantes

| ID | Participante | Perfil | Rol en HAB | Nivel TI | Corresponde a |
|----|-------------|--------|------------|----------|---------------|
| P1 | Dra. Emilly Maria Celis Barreto | Profesional SST — ICBF Neiva | Usuario institucional operativo | **Avanzado** | Entrevista E1 |
| P2 | Laura Cangrejo Perafan | Profesional — Alcaldía de Neiva | Coordinación y supervisión | **Intermedio** | Entrevista E2 |
| P3 | Familiar / Cuidador *(anónimo)* | Cuidador principal de paciente con discapacidad motora | Stakeholder externo | **Novato absoluto** | Entrevista E3 |

---

---

## SECCIÓN 1 — Guión de Tareas

> Las tareas están ordenadas de **menor a mayor complejidad**. El moderador entrega este guión impreso o en pantalla secundaria al inicio de la sesión. No se debe revelar el orden de dificultad al participante.

---

### Tareas

**Tarea 1 — Registrar un nuevo paciente**

> Usted deberá ingresar al sistema HAB y registrar un nuevo paciente con los datos básicos que se le proporcionan en la ficha de referencia. Asegúrese de completar al menos los campos obligatorios del formulario ICF. *(Tiempo estimado: 3 minutos)*

**Tarea 2 — Buscar un paciente y revisar su perfil**

> Usted deberá buscar en el sistema al paciente "Carlos Medina Ospina" y navegar hasta visualizar su perfil completo, incluyendo su historial y las dimensiones ICF registradas. *(Tiempo estimado: 2 minutos)*

**Tarea 3 — Ejecutar una predicción ML e interpretar el resultado**

> Usted deberá seleccionar un paciente existente, ejecutar una predicción de perfil de riesgo desde la sección de Predicciones y describir en voz alta lo que indica el resultado (color del badge y categoría). *(Tiempo estimado: 3 minutos)*

---

---

## SECCIÓN 2 — Protocolo de Sesión

### 2.1 Preparación del sitio

- Adecuación del espacio físico o virtual (sala tranquila / sala de videollamada sin interrupciones)
- Configuración de la cámara o herramienta de grabación de pantalla
- Apertura de la demo HAB en el navegador: `https://hab-frontend-qa.onrender.com`
- Preparación de la ficha de referencia del paciente ficticio para la Tarea 1
- Verificación de credenciales de prueba: `usuario@hab-demo.co` / `hab2026`
- Disposición de los instrumentos impresos (encuestas, guión de tareas)

### 2.2 Presentación del sistema

- Familiarizar al participante con el entorno de prueba (laptop/tablet, navegador, demo)
- Explicar que se evalúa el **sistema**, no al usuario: no hay respuestas correctas ni incorrectas
- Pedir al participante que **piense en voz alta** mientras realiza las tareas
- Solicitar consentimiento para grabación de pantalla y/o video (ver `03_consentimiento_informado.md`)
- Colocar o activar el instrumento de observación (hoja de heurísticas emocionales, Sección 6)

### 2.3 Explicación de la prueba

- Presentar brevemente el propósito de HAB (2 minutos máximo)
- Entregar el guión de tareas (Sección 1)
- Indicar el tiempo estimado por tarea
- Aclarar que el moderador no puede dar pistas durante la ejecución; solo puede responder si el participante queda completamente bloqueado

### 2.4 Realización de las pruebas

- Ejecutar las tareas en el orden establecido (1 → 2 → 3)
- El observador registra en tiempo real:
  - Tiempo efectivo de cada tarea
  - Errores o caminos incorrectos
  - Expresiones verbales y gestuales (hoja de heurísticas emocionales)
- Al finalizar cada tarea, el moderador anota si fue **completada / completada con ayuda / no completada**

### 2.5 Verificación y cierre

- Aplicar la **Encuesta Sociodemográfica** (Sección 3)
- Aplicar la **Encuesta Post-Test de Satisfacción** (Sección 4)
- Aplicar el **Test de Estilos de Interacción** (Sección 5) si el tiempo lo permite
- Revisar y organizar los registros obtenidos
- Agradecer al participante y recordar la confidencialidad de los datos

---

---

## SECCIÓN 3 — Encuesta Sociodemográfica

> *Cordial saludo. El equipo de desarrollo de Health Access Bridge está realizando una evaluación de experiencia de usuario de su plataforma de gestión clínica para personas con discapacidad. Dado que usted participó en esta sesión de prueba, le solicitamos completar la siguiente encuesta. La información será manejada de forma anónima y confidencial conforme a la Ley 1581 de 2012 (HABEAS DATA).*

---

**Nombre** (opcional): \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

**1. Su rol principal es:**

- [ ] Profesional de salud (médico, enfermero, PST, fisioterapeuta, etc.)
- [ ] Profesional administrativo (coordinación, alcaldía, secretaría de salud)
- [ ] Familiar / cuidador de persona con discapacidad
- [ ] Otro — ¿Cuál? \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

**2. Su edad está entre:**

- [ ] 20–30 años
- [ ] 31–40 años
- [ ] 41–50 años
- [ ] 51–60 años
- [ ] Más de 60 años

---

**3. Su último nivel de estudios es:**

- [ ] Técnico / Tecnológico
- [ ] Pregrado
- [ ] Especialización
- [ ] Maestría
- [ ] Doctorado
- [ ] Otro — ¿Cuál? \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

**4. ¿Con qué frecuencia utiliza plataformas digitales de salud o sistemas de información clínica?**

- [ ] Todos los días
- [ ] Varias veces por semana
- [ ] Una vez a la semana
- [ ] Ocasionalmente (una vez al mes o menos)
- [ ] Nunca antes de hoy

---

**5. ¿Tiene alguna sugerencia o comentario sobre la sesión de hoy?**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

---

## SECCIÓN 4 — Encuesta Post-Test de Satisfacción

> *Marque con una X sobre el número que mejor represente su experiencia. 1 = Muy inadecuado · 5 = Muy adecuado.*

---

**1. ¿Cómo se sintió realizando las tareas en HAB?**

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| Muy incómodo/a | | | | Muy cómodo/a |

---

**2. ¿La explicación inicial sobre el sistema fue suficiente para entender lo que debía hacer?**

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| Muy insuficiente | | | | Muy suficiente |

---

**3. ¿Cree usted que el tiempo asignado fue suficiente para completar cada tarea?**

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| Muy insuficiente | | | | Muy suficiente |

---

**4. ¿La ubicación de los elementos en la interfaz (menús, botones, formularios) le resultó clara?**

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| Muy confusa | | | | Muy clara |

---

**5. En general, ¿qué tan fácil le resultó usar HAB para completar las tareas?**

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| Muy difícil | | | | Muy fácil |

---

**Puntuación total (suma de las 5 respuestas):** \_\_\_\_ / 25

> **Interpretación de referencia:** 20–25 = Muy satisfactorio · 15–19 = Satisfactorio · 10–14 = Mejorable · < 10 = Crítico

---

---

## SECCIÓN 5 — Test de Estilos de Interacción (Tipo de Usuario)

> *Deberá asignar una puntuación de 1 a 4 a cada situación de una fila, respondiendo a la pregunta del encabezado. Coloque **4** a la situación que más lo representa y **1** a la que menos. No puede repetir un puntaje dentro de una fila.*
>
> **4** = Lo que más se parece a usted · **3** = Lo segundo · **2** = Lo tercero · **1** = Lo que menos se parece

| Cuando aprendo / interactúo: | Prefiero valerme de mis sensaciones y sentimientos | Prefiero mirar y atender | Prefiero pensar en las ideas | Prefiero hacer cosas directamente |
|---|---|---|---|---|
| **Cuando aprendo:** | Prefiero valerme de mis sensaciones y sentimientos | Prefiero mirar y atender | Prefiero pensar en las ideas | Prefiero hacer cosas | | | |
| **Aprendo mejor cuando:** | Confío en mis corazonadas y sentimientos | Atiendo y observo cuidadosamente | Confío en mis pensamientos lógicos | Trabajo duramente para que las cosas queden realizadas |
| **Cuando estoy aprendiendo:** | Tengo sentimientos y reacciones fuertes | Soy reservado y tranquilo | Busco razonar sobre las cosas que están sucediendo | Me siento responsable de las cosas |
| **Aprendo a través de:** | Sentimientos | Observaciones | Razonamientos | Acciones |
| **Cuando aprendo:** | Estoy abierto a nuevas experiencias | Tomo en cuenta todos los aspectos relacionados | Prefiero analizar las cosas dividiéndolas en sus partes | Prefiero hacer las cosas directamente |
| **Cuando estoy aprendiendo:** | Soy una persona intuitiva | Soy una persona observadora | Soy una persona lógica | Soy una persona activa |
| **Aprendo mejor a través de:** | Las relaciones con mis compañeros | La observación | Teorías racionales | La práctica de los temas tratados |
| **Cuando aprendo:** | Me siento involucrado en los temas tratados | Me tomo mi tiempo antes de actuar | Prefiero las teorías y las ideas | Prefiero ver los resultados a través de mi propio trabajo |
| **Aprendo mejor cuando:** | Me baso en mis intuiciones y sentimientos | Me baso en observaciones personales | Tomo en cuenta mis propias ideas sobre el tema | Pruebo personalmente la tarea |
| **Cuando estoy aprendiendo:** | Soy una persona abierta | Soy una persona reservada | Soy una persona racional | Soy una persona responsable |
| **Cuando aprendo:** | Me involucro | Prefiero observar | Prefiero evaluar las cosas | Prefiero asumir una actitud activa |
| **Aprendo mejor cuando:** | Soy receptivo y de mente abierta | Soy cuidadoso | Analizo las ideas | Soy práctico |
| **Total de la suma de cada columna →** | **EC** (Experiencia Concreta) | **OR** (Observación Reflexiva) | **CA** (Conceptualización Abstracta) | **EA** (Experimentación Activa) |

---

### Interpretación del perfil (Kolb)

| Estilo dominante | Perfil de interacción |
|------------------|-----------------------|
| **EC alto** (Experiencia Concreta) | Usuario empático, orientado a las personas; aprende haciendo y sintiendo. Prefiere interfaces cálidas, con guía visual y apoyo humano. |
| **OR alto** (Observación Reflexiva) | Usuario reflexivo; observa antes de actuar. Valora tutoriales, demos y documentación detallada antes de explorar. |
| **CA alto** (Conceptualización Abstracta) | Usuario analítico; prefiere entender el modelo mental del sistema antes de operar. Tolera interfaces complejas si la lógica es clara. |
| **EA alto** (Experimentación Activa) | Usuario pragmático; aprende explorando. Prefiere shortcuts, atajos y resultados rápidos. Baja tolerancia a flujos largos. |

---

---

## SECCIÓN 6 — Registro de Heurísticas Emocionales (Observación)

> *Este instrumento es diligenciado por el **observador**, no por el participante. Registre cada vez que se presente la expresión indicada: anote el minuto aproximado en **Tiempo** y el número acumulado de veces en **Cantidad**.*

**Participante:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Fecha:** \_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Tarea observada:** T1 / T2 / T3 *(marque)*

---

| # | Heurística emocional | Interpretación | Tiempo (min:seg) | Cantidad |
|---|----------------------|----------------|-----------------|----------|
| 1 | **FRUNCIR EL CEÑO** | Desagrado · percepción de dificultad · confusión · reflexión profunda | | |
| 2 | **ELEVAR LAS CEJAS** | Expresión de sorpresa · inseguridad · incredulidad · exasperación | | |
| 3 | **DESVIAR LA MIRADA** | Culpa · vergüenza · sumisión · pérdida de foco | | |
| 4 | **SONREÍR** | Satisfacción · logro percibido · agrado con el sistema | | |
| 5 | **APRETAR LOS LABIOS** | Frustración · confusión · ansiedad · nerviosismo | | |
| 6 | **MOVER LA BOCA (sin hablar)** | Incertidumbre · sensación de estar perdido en la interfaz | | |
| 7 | **EXPRESARSE ORALMENTE** | Suspiros · jadeos · exclamaciones · frustración verbalizada | | |
| 8 | **TOCARSE LA CARA CON LAS MANOS** | Confusión · cansancio · incertidumbre · pérdida de orientación | | |
| 9 | **RECLINARSE HACIA ATRÁS** | Rechazo · negativa · deseo de alejarse de la actividad | | |
| 10 | **INCLINARSE HACIA ADELANTE** | Atención concentrada · acercarse para leer · frustración activa | | |

---

**Notas de observación libre:**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

---

## SECCIÓN 7 — Resumen de Resultados por Participante (Observador)

> *Completar al finalizar cada sesión. Usar una fila por participante y tarea.*

| Participante | Tarea | ¿Completada? | Tiempo real | Errores / desvíos observados | Heurística emocional dominante | Puntuación satisfacción (Secc. 4) |
|---|---|---|---|---|---|---|
| P1 — Emilly | T1 | ☐ Sí ☐ Con ayuda ☐ No | | | | |
| P1 — Emilly | T2 | ☐ Sí ☐ Con ayuda ☐ No | | | | |
| P1 — Emilly | T3 | ☐ Sí ☐ Con ayuda ☐ No | | | | |
| P2 — Laura | T1 | ☐ Sí ☐ Con ayuda ☐ No | | | | |
| P2 — Laura | T2 | ☐ Sí ☐ Con ayuda ☐ No | | | | |
| P2 — Laura | T3 | ☐ Sí ☐ Con ayuda ☐ No | | | | |
| P3 — Cuidador | T1 | ☐ Sí ☐ Con ayuda ☐ No | | | | |
| P3 — Cuidador | T2 | ☐ Sí ☐ Con ayuda ☐ No | | | | |
| P3 — Cuidador | T3 | ☐ Sí ☐ Con ayuda ☐ No | | | | |

---

### Hallazgos esperados por perfil (referencia previa de entrevistas)

| Participante | Punto de fricción anticipado | Origen |
|---|---|---|
| P1 — Emilly (avanzada) | Tooltips ausentes en campos ICF (D1–D6); campos sin etiqueta clara para usuario nuevo | Entrevista E1 — Ficha `04_fichas_entrevistas.md` |
| P2 — Laura (intermedia) | Panel de municipios y filtros de reporte; terminología clínica no familiar | Entrevista E2 |
| P3 — Cuidador (novato) | Flujo de registro complejo; terminología ICF desconocida; falta de modo de ayuda contextual | Entrevista E3 |

---

---

## Referencias cruzadas

| Documento | Relación |
|-----------|----------|
| [`01_plan_investigacion.md`](./01_plan_investigacion.md) | Protocolo base de investigación UX |
| [`03_consentimiento_informado.md`](./03_consentimiento_informado.md) | Debe firmarse antes de la sesión |
| [`04_fichas_entrevistas.md`](./04_fichas_entrevistas.md) | Hallazgos previos que orientan los puntos de fricción esperados |
| [`06_user_personas.md`](./06_user_personas.md) | Perfiles P1 y P2 detallados |
| [`07_user_story_mapping.md`](./07_user_story_mapping.md) | Tareas T1–T3 derivan de actividades A2 (gestión pacientes) y A3 (predicción ML) del mapa |
