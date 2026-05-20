# Plan de Investigación de Usuarios — HAB

> **Proyecto:** Health Access Bridge (HAB)  
> **Fase:** Investigación UX — Actividad HCI  
> **Método:** Entrevistas semiestructuradas + Diagrama de Afinidad + User Personas + User Story Mapping  
> **Estándar referencia:** ISO 9241-210:2019 (Diseño centrado en el ser humano para sistemas interactivos)

---

## 1. Objetivo general

Comprender las necesidades, comportamientos, frustraciones y expectativas de los usuarios potenciales de la plataforma HAB para informar decisiones de diseño de la interfaz, la arquitectura de información y las historias de usuario del sistema.

---

## 2. Preguntas de investigación

1. ¿Cómo realizan actualmente el seguimiento clínico de pacientes con discapacidad los profesionales de salud en zonas rurales?
2. ¿Qué barreras tecnológicas enfrentan los usuarios al adoptar nuevas herramientas digitales de salud?
3. ¿Qué información consideran crítica para el registro y la predicción de perfiles funcionales ICF?
4. ¿Cuánta confianza depositan los profesionales en los resultados de modelos de machine learning para decisiones clínicas?
5. ¿Qué funcionalidades son imprescindibles (must-have) vs. deseables (nice-to-have)?

---

## 3. Método de investigación

### 3.1 Tipo de entrevista
**Entrevista semiestructurada** — permite explorar temas predefinidos con flexibilidad para profundizar en respuestas relevantes.

- **Duración estimada:** 30–45 minutos por entrevista
- **Modalidad:** Presencial o videollamada (Zoom / Google Meet)
- **Registro:** Video con consentimiento firmado + notas del entrevistador
- **Análisis:** Transcripción → notas de afinidad → agrupación temática

### 3.2 Criterios de selección de participantes

| Criterio | Descripción |
|----------|-------------|
| **Rol** | Profesional de salud, coordinador administrativo, stakeholder externo (cuidador/familiar) |
| **Experiencia TI** | Combinación de niveles: avanzado, intermedio, novato, novato absoluto |
| **Contexto geográfico** | Preferiblemente zonas rurales o semi-rurales de Huila, Colombia |
| **Diversidad** | Combinación de sectores: salud clínica, administración pública y comunidad |
| **Disponibilidad** | Consentimiento explícito para grabación de video |

### 3.3 Tamaño de muestra

**3 participantes** (mínimo recomendado por Nielsen Norman Group para investigación cualitativa exploratoria):

| ID | Participante | Perfil | Nivel tecnológico | Justificación |
|----|-------------|--------|-------------------|---------------|
| E1 | Dra. Emilly Maria Celis Barreto | Profesional en Seguridad y Salud en el Trabajo | **Avanzado** | Usuaria clínica principal; aporta requerimientos funcionales profundos y perspectiva de salud mental en discapacidad |
| E2 | Laura Cangrejo Perafan | Profesional · Alcaldía de Neiva | **Intermedio** | Perfil administrativo; prioriza visibilidad de municipios, reportes y alertas |
| E3 | Familiar / Cuidador *(identidad protegida — HABEAS DATA)* | Cuidador principal de paciente con discapacidad motora | **Novato absoluto** | Stakeholder externo; revela necesidades de comunicación, continuidad asistencial y accesibilidad |

---

## 4. Protocolo de entrevista

```
Fase 1 — Apertura (5 min)
  └─ Presentación del investigador y del proyecto
  └─ Explicación del propósito: mejorar la interfaz, no evaluar al usuario
  └─ Firma del consentimiento informado
  └─ Solicitud de permiso para grabar

Fase 2 — Calentamiento (5 min)
  └─ Preguntas de contexto: rol, años de experiencia, dispositivos usados

Fase 3 — Exploración (20–30 min)
  └─ Bloque A: Flujo de trabajo actual (cómo gestiona pacientes hoy)
  └─ Bloque B: Necesidades y puntos de dolor
  └─ Bloque C: Expectativas hacia HAB (demo rápida de 5 min)

Fase 4 — Cierre (5 min)
  └─ Escala SUS simplificada (5 ítems)
  └─ Espacio para preguntas del participante
  └─ Agradecimiento
```

---

## 5. Variables a medir

| Variable | Indicador | Método de captura |
|----------|-----------|-------------------|
| Nivel de alfabetización digital | Dispositivos usados, frecuencia de uso de apps | Pregunta directa |
| Flujo de trabajo actual | Pasos descritos en la gestión de un paciente | Narrativa libre |
| Puntos de dolor | Menciones espontáneas de frustración | Notas de observación |
| Necesidades funcionales | Funcionalidades solicitadas / esperadas | Preguntas directas |
| Confianza en ML | Reacción ante demo de predicción | Escala Likert 1-5 |
| Usabilidad percibida | Escala SUS simplificada | Cuestionario post-demo |

---

## 6. Cronograma

| Semana | Actividad | Entregable |
|--------|-----------|------------|
| S1 | Preparación: guía, consentimiento, contacto participantes | Documentos listos |
| S2 | Entrevistas E1 y E2 (Dra. Emilly Maria Celis · Laura Cangrejo) | Videos + fichas diligenciadas |
| S2 | Entrevista E3 (Familiar / Cuidador anónimo) | Video + ficha diligenciada |
| S3 | Transcripción y elaboración de notas de afinidad | Notas brutas |
| S3 | Taller de afinidad (agrupación y categorización) | Diagrama de afinidad |
| S4 | Elaboración de user personas | 2 personas documentadas |
| S4 | User Story Mapping | Mapa de historias por release |
| S5 | Revisión, validación y entrega | Paquete HCI completo |

---

## 7. Consideraciones éticas

- Participación **voluntaria** con consentimiento escrito (HABEAS DATA — Ley 1581 de 2012)
- Los nombres y datos identificables serán **seudoanonimizados** en los documentos
- Los videos se almacenan en repositorio **privado** y se comparten solo con el equipo de investigación
- Los datos no serán usados para entrenar modelos de ML ni con fines comerciales
- Derecho de retiro en cualquier momento sin consecuencias

---

## 8. Herramientas utilizadas

| Herramienta | Uso |
|-------------|-----|
| Google Meet / Zoom | Videollamadas y grabación |
| Markdown / GitHub | Documentación del proceso |
| HTML/CSS (custom) | Diagrama de afinidad visual |
| Diagrams.net | Diagramas complementarios |
| HAB (demo QA) | Demo durante entrevista: `https://hab-frontend-qa.onrender.com` |
