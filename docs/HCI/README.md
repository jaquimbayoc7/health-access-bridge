# HCI — Investigación de Usuarios · Health Access Bridge

> **Actividad:** Entrevistas, Diagrama de Afinidad, User Personas, User Story Mapping y Test de Usuario  
> **Aplicación:** Health Access Bridge (HAB) — plataforma de gestión clínica para pacientes con discapacidad  
> **Metodología:** Investigación de usuarios centrada en el ser humano (ISO 9241-210)

---

## Artefactos

| # | Documento | Descripción | Estado |
|---|-----------|-------------|--------|
| 01 | [Plan de Investigación](./01_plan_investigacion.md) | Objetivo, método, criterios de selección, cronograma | ✅ |
| 02 | [Guía de Entrevista — Perfil Salud](./02_guia_entrevista.md) | Guía semiestructurada para profesionales del sector salud | ✅ |
| 02b | [Guía de Entrevista — Perfil No Clínico](./02b_guia_entrevista_no_salud.md) | Guía adaptada para perfiles fuera del gremio de salud (SST, Alcaldía, ICBF, ONG) | ✅ |
| 03 | [Consentimiento Informado](./03_consentimiento_informado.md) | Formato firmable, cumple HABEAS DATA Colombia | ✅ |
| 04 | [Fichas de Entrevistas](./04_fichas_entrevistas.md) | 3 fichas diligenciadas (1 avanzado · 1 intermedio · 1 familiar/cuidador anónimo) | ✅ |
| 05 | [Diagrama de Afinidad](./05_diagrama_afinidad.html) | HTML dinámico — 7 pasos Método KJ · 21 notas · 6 temas | ✅ |
| 06 | [User Personas](./06_user_personas.md) | Dra. Emilly Maria Celis Barreto + Laura Cangrejo Perafan con empathy map | ✅ |
| 07 | [User Story Mapping](./07_user_story_mapping.md) | Backbone + tareas + HU organizadas en 3 releases | ✅ |
| 08 | [Test de Usuario — Fase 4 Final](./08_test_de_usuario.md) | Guión de tareas HAB · protocolo · encuesta sociodemográfica · satisfacción post-test · estilos de interacción (Kolb) · heurísticas emocionales | ✅ |

---

## Perfiles de usuarios entrevistados

| ID | Participante | Perfil | Rol en HAB | Nivel tecnológico |
|----|-------------|--------|------------|-------------------|
| E1 | Dra. Emilly Maria Celis Barreto | Profesional en Seguridad y Salud en el Trabajo | Usuario clínico | **Avanzado** |
| E2 | Laura Cangrejo Perafan | Profesional · Alcaldía de Neiva | Administrador | Intermedio |
| E3 | Familiar / Cuidador *(anónimo)* | Cuidador principal de paciente con discapacidad | Stakeholder externo | **Novato absoluto** |

---

## Grupos temáticos — Diagrama de Afinidad

1. 🔵 **Accesibilidad tecnológica** — conectividad, dispositivos, idioma de la interfaz
2. 🟢 **Flujo clínico** — registro ICF, flujo de consulta, tiempo de captura de datos
3. 🟡 **Confianza y privacidad** — seguridad de datos, rol del administrador, HABEAS DATA
4. 🟠 **Predicción y resultados ML** — interpretación del modelo, confianza clínica, exportación
5. 🔴 **Curva de aprendizaje** — capacitación, tooltips, mensajes de error
6. 🟣 **Colaboración y comunicación** — notificaciones, reporte entre profesionales

---

## Personas derivadas

| Persona | Perfil | Necesidad central |
|---------|--------|-------------------|
| **Dra. Emilly Maria Celis Barreto** | Profesional SST — ICBF | Registro rápido, predicción ML confiable, modo offline |
| **Laura Cangrejo Perafan** | Profesional — Alcaldía de Neiva | Panel de municipios, alertas automáticas, lenguaje claro |

---

## Fase 4 — Test de Usuario

> **Documento:** [`08_test_de_usuario.md`](./08_test_de_usuario.md)  
> **Método:** Test de usabilidad moderado con pensamiento en voz alta + observación + instrumentos cuantitativos y cualitativos  
> **Demo:** `https://hab-frontend-qa.onrender.com`

### Tareas evaluadas

| Tarea | Descripción | Tiempo estimado |
|-------|-------------|----------------|
| T1 | Registrar un nuevo paciente con datos ICF básicos | 3 min |
| T2 | Buscar un paciente existente y revisar su perfil completo | 2 min |
| T3 | Ejecutar una predicción ML e interpretar el resultado (badge de riesgo) | 3 min |

### Instrumentos incluidos

| Instrumento | Propósito |
|-------------|----------|
| Guión de tareas + Protocolo | Estructura y orden de la sesión |
| Encuesta sociodemográfica | Caracterización del participante (rol, edad, nivel TI) |
| Encuesta post-test de satisfacción | Escala 1-5 en 5 dimensiones — máx. 25 puntos |
| Test de estilos de interacción (Kolb) | Clasifica al usuario en EC · OR · CA · EA |
| Registro de heurísticas emocionales | Observación de 10 expresiones faciales/corporales con Tiempo + Cantidad |
| Tabla resumen del observador | Consolidación de resultados por participante y tarea |
