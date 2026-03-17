## Historia de Usuario

**Como** Médico  
**Deseo** que la IA generativa (GPT-4 u otro LLM) cree resúmenes y planes personalizados  
**Para** apoyar la toma de decisiones clínicas basadas en evidencia.

---

## Detalles Técnicos

| Campo | Detalle |
|-------|---------|
| **Backend** | Integrar API LLM (OpenAI GPT-4 / Abacus LLM) |
| **Frontend** | Mostrar resumen y recomendaciones en perfil del paciente |
| **Proceso** | Enviar datos clínicos + contexto al LLM, recibir texto enriquecido |
| **Stack** | FastAPI + openai SDK + React + jsPDF |
| **Estimación** | 21 puntos |
| **Sprint** | Sprint 8 y 9 (Semanas 19-22) |
| **Momento** | Momento 3 - Trabajo Integrador III |

---

## Dependencias

> ⚠️ Este issue **no puede comenzar** hasta que estén cerrados:
> - #4 HU-04: Integración del Modelo Predictivo (HybridModelDisability)
> - #6 HU-06: Pruebas de Integración y Rendimiento API

---

## Criterios de Aceptación

- [ ] Resumen clínico coherente y útil generado por el LLM
- [ ] Opción para exportar resumen y recomendaciones a PDF
- [ ] Disclaimer legal visible en la UI
- [ ] Tiempo de respuesta del LLM < 10 segundos
- [ ] Logs de uso del LLM implementados (sin guardar datos sensibles)

---

## Tareas

- [ ] Integrar SDK de OpenAI en el backend (`openai` o `httpx`)
- [ ] Diseñar prompt template con datos del paciente + score predictivo
- [ ] Implementar endpoint `POST /api/recommendations/{patient_id}`
- [ ] Implementar endpoint `POST /api/recommendations/{patient_id}/export` (PDF)
- [ ] Almacenar historial de recomendaciones generadas
- [ ] Desarrollar componente React `RecommendationCard` con disclaimer
- [ ] Agregar botón "Exportar a PDF" con `jsPDF` o similar
- [ ] Implementar logs de uso (timestamps, patient_id, sin PII del contenido)
- [ ] Manejar rate limits y errores de la API LLM

---

## Definition of Done (DoD)

- [ ] Integración completa con LLM funcionando en producción
- [ ] UI amigable con disclaimer legal visible
- [ ] Exportación a PDF sin errores
- [ ] Logs de uso implementados
- [ ] Código mergeado en `main`

---

## Rama Git

`feature/hu-07-llm-recommendations`
