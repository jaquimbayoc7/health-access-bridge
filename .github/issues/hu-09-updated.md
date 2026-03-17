## Historia de Usuario

**Como** QA y usuarios finales  
**Deseo** validar funcionalidad, usabilidad y accesibilidad  
**Para** entregar un producto estable y usable.

---

## Detalles Técnicos

| Campo | Detalle |
|-------|---------|
| **Entradas** | Aplicación completa desplegada |
| **Proceso** | Pruebas manuales + automatizadas + sesiones con usuarios |
| **Salida** | Reporte final de pruebas + bugs corregidos |
| **Stack** | Playwright + axe-core + Lighthouse |
| **Estimación** | 8 puntos |
| **Sprint** | Sprint 11 (Semanas 23-26) |
| **Momento** | Momento 3 - Trabajo Integrador III |

---

## Dependencias

> ⚠️ Este issue **no puede comenzar** hasta que estén cerrados:
> - #7 HU-07: Orquestación con LLM para Recomendaciones Clínicas
> - #8 HU-08: Dashboard de Análisis y Exportación

---

## Criterios de Aceptación

- [ ] Pruebas manuales completadas para todos los flujos críticos
- [ ] Pruebas automatizadas E2E con Playwright pasan al 100%
- [ ] Accesibilidad WCAG 2.1 nivel AA validada con axe-core
- [ ] Feedback de usuarios documentado y priorizado
- [ ] Bugs reportados corregidos antes de entrega final

---

## Tareas

- [ ] Definir plan de pruebas manuales (casos de uso por rol: Admin, Médico)
- [ ] Ejecutar pruebas manuales y documentar resultados
- [ ] Escribir suite completa de pruebas E2E con Playwright
- [ ] Ejecutar audit de accesibilidad con axe-core o Lighthouse
- [ ] Sesión de pruebas con usuarios reales (mínimo 3 personas)
- [ ] Documentar feedback en `docs/user-feedback.md`
- [ ] Priorizar y corregir bugs encontrados
- [ ] Generar reporte final de pruebas en `docs/test-report-final.md`

---

## Definition of Done (DoD)

- [ ] Reporte final de pruebas generado y documentado
- [ ] Todas las correcciones críticas aplicadas
- [ ] Suite E2E pasando al 100%
- [ ] Código mergeado en `main`

---

## Rama Git

`feature/hu-09-uat-testing`
