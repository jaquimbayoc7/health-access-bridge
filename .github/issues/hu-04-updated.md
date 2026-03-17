## Historia de Usuario

**Como** Médico  
**Deseo** enviar datos del paciente al modelo predictivo alojado en el backend  
**Para** obtener un score de riesgo y recomendaciones personalizadas.

---

## Detalles Técnicos

| Campo | Detalle |
|-------|---------|
| **Modelo** | [HybridModelDisability](https://github.com/jaquimbayoc7/HybridModelDisability) |
| **Entradas** | Datos clínicos del paciente (JSON) |
| **Proceso** | POST al endpoint predictivo, respuesta JSON con score |
| **Salida** | Score de discapacidad + recomendaciones |
| **Stack** | FastAPI (proxy) + React (UI) + httpx |
| **Estimación** | 21 puntos |
| **Sprint** | Sprint 4 y 5 (Semanas 10-13) |
| **Momento** | Momento 2 - Trabajo Integrador II |

---

## Dependencias

> ⚠️ Este issue **no puede comenzar** hasta que estén cerrados:
> - #2 HU-02: Registro y Precarga de Datos de Pacientes
> - #3 HU-03: Integración Frontend-Backend y Despliegue Local

---

## Criterios de Aceptación

- [ ] El backend responde con predicción en menos de 3 segundos
- [ ] El frontend muestra el score y recomendaciones de forma clara
- [ ] Manejo de errores cuando el modelo no está disponible
- [ ] Estados de carga visibles (spinner/skeleton) durante la predicción
- [ ] El score se almacena en el perfil del paciente (`disability_score`)

---

## Tareas

- [ ] Revisar API del modelo [HybridModelDisability](https://github.com/jaquimbayoc7/HybridModelDisability) y documentar endpoints
- [ ] Implementar cliente HTTP con `httpx` en backend para consumir el modelo
- [ ] Crear endpoint proxy `POST /api/predictions/{patient_id}` (seguro, autenticado)
- [ ] Almacenar resultado de predicción en tabla `patients.disability_score`
- [ ] Desarrollar componente React `PredictionCard` con score visual
- [ ] Implementar manejo de errores y timeout (3 seg max)
- [ ] Pruebas de integración end-to-end del flujo de predicción
- [ ] Agregar logs de errores del modelo

---

## Definition of Done (DoD)

- [ ] Predicción integrada y funcionando end-to-end
- [ ] UI responsiva con score visible en perfil del paciente
- [ ] Logs de errores implementados
- [ ] Pruebas de integración pasando
- [ ] Código mergeado en `main`

---

## Rama Git

`feature/hu-04-predictive-model`
