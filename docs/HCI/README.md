# HCI — Investigación de Usuarios · Health Access Bridge

> **Actividad:** Entrevistas, Diagrama de Afinidad, User Personas y User Story Mapping  
> **Aplicación:** Health Access Bridge (HAB) — plataforma de gestión clínica para pacientes con discapacidad  
> **Metodología:** Investigación de usuarios centrada en el ser humano (ISO 9241-210)

---

## Artefactos

| # | Documento | Descripción | Estado |
|---|-----------|-------------|--------|
| 01 | [Plan de Investigación](./01_plan_investigacion.md) | Objetivo, método, criterios de selección, cronograma | ✅ |
| 02 | [Guía de Entrevista](./02_guia_entrevista.md) | Guía semiestructurada con 3 bloques temáticos y escala SUS | ✅ |
| 03 | [Consentimiento Informado](./03_consentimiento_informado.md) | Formato firmable, cumple HABEAS DATA Colombia | ✅ |
| 04 | [Fichas de Entrevistas](./04_fichas_entrevistas.md) | 3 fichas diligenciadas (1 avanzado · 1 intermedio · 1 familiar/cuidador anónimo) | ✅ |
| 05 | [Diagrama de Afinidad](./05_diagrama_afinidad.html) | HTML dinámico — 7 pasos Método KJ · 21 notas · 6 temas | ✅ |
| 06 | [User Personas](./06_user_personas.md) | Dra. Amparo Medina Salazar + Willians Aguilar Rodriguez con empathy map | ✅ |
| 07 | [User Story Mapping](./07_user_story_mapping.md) | Backbone + tareas + HU organizadas en 3 releases | ✅ |

---

## Perfiles de usuarios entrevistados

| ID | Participante | Perfil | Rol en HAB | Nivel tecnológico |
|----|-------------|--------|------------|-------------------|
| E1 | Dra. Amparo Medina Salazar | Profesional en Psicología | Usuario clínico | **Avanzado** |
| E2 | Willians Aguilar Rodriguez | Asistente de información · Secretaría de Salud de Garzón | Administrador | Intermedio |
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
| **Dra. Amparo Medina Salazar** | Psicóloga — usuaria avanzada | Registro rápido, predicción ML confiable, modo offline |
| **Willians Aguilar Rodriguez** | Asistente información Secretaría de Salud | Panel de municipios, alertas automáticas, lenguaje claro |
