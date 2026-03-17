## Historia de Usuario

**Como** QA  
**Deseo** validar que la integración entre frontend y backend es estable y rápida  
**Para** asegurar la calidad y experiencia de usuario.

---

## Detalles Técnicos

| Campo | Detalle |
|-------|---------|
| **Entradas** | Suite de pruebas automatizadas |
| **Proceso** | Ejecución de pruebas de integración y carga |
| **Salida** | Reporte de cobertura + métricas de rendimiento |
| **Stack** | pytest + Playwright + k6 o locust |
| **Estimación** | 8 puntos |
| **Sprint** | Sprint 7 (Semanas 14-17) |
| **Momento** | Momento 2 - Trabajo Integrador II |

---

## Dependencias

> ⚠️ Este issue **no puede comenzar** hasta que estén cerrados:
> - #4 HU-04: Integración del Modelo Predictivo (HybridModelDisability)
> - #5 HU-05: Modo Offline y PWA

---

## Criterios de Aceptación

- [ ] Pruebas automatizadas de integración pasan al 100%
- [ ] API responde en menos de 200ms bajo carga simulada (100 usuarios concurrentes)
- [ ] No hay bugs críticos bloqueantes sin resolver
- [ ] Reporte de pruebas generado y documentado en `/docs/test-report.md`
- [ ] Pruebas E2E cubren flujos: login, CRUD pacientes, predicción

---

## Tareas

- [ ] Configurar suite de pruebas de integración con pytest
- [ ] Escribir pruebas E2E con Playwright para flujos críticos (login, CRUD pacientes, predicción)
- [ ] Configurar prueba de carga con k6 o locust (100 usuarios concurrentes)
- [ ] Identificar y documentar bottlenecks de rendimiento
- [ ] Corregir bugs críticos encontrados
- [ ] Generar reporte HTML de pruebas
- [ ] Documentar resultados en `docs/test-report.md`

---

## Definition of Done (DoD)

- [ ] Reporte de pruebas generado
- [ ] API < 200ms bajo carga simulada
- [ ] Todos los bugs críticos corregidos
- [ ] Código mergeado en `main`

---

## Rama Git

`feature/hu-06-integration-tests`
