## Historia de Usuario

**Como** Equipo de proyecto  
**Deseo** desplegar la versión estable en la nube y entregar documentación completa  
**Para** cerrar el proyecto con calidad y soporte.

---

## Detalles Técnicos

| Campo | Detalle |
|-------|---------|
| **Plataforma** | Render (Web Service + Static Site + PostgreSQL managed) |
| **Config** | `render.yaml` Blueprint |
| **Estimación** | 5 puntos |
| **Sprint** | Sprint 12 (Semana 27) |
| **Momento** | Momento 3 - Trabajo Integrador III |

---

## Dependencias

> ⚠️ Este issue **no puede comenzar** hasta que estén cerrados:
> - #8 HU-08: Dashboard de Análisis y Exportación
> - #9 HU-09: Pruebas Completas y Feedback de Usuarios

---

## Criterios de Aceptación

- [ ] Aplicación accesible en URL de producción (Render)
- [ ] Base de datos PostgreSQL en producción con datos reales
- [ ] Documentación técnica completa entregada
- [ ] Manual de usuario entregado
- [ ] Pipeline CI/CD configurado (auto-deploy desde rama `main`)

---

## Tareas

- [ ] Revisar y validar `render.yaml` Blueprint completo
- [ ] Configurar variables de entorno en Render Dashboard
- [ ] Ejecutar migraciones Alembic en base de datos de producción
- [ ] Ejecutar seed inicial en producción (admin user)
- [ ] Verificar que frontend consume API de producción correctamente
- [ ] Configurar dominio personalizado (si aplica)
- [ ] Escribir documentación técnica en `docs/technical-docs.md`
- [ ] Escribir manual de usuario en `docs/user-manual.md`
- [ ] Generar reporte final del proyecto
- [ ] Demo de entrega al cliente/docente

---

## Definition of Done (DoD)

- [ ] Aplicación en producción accesible y funcional
- [ ] Documentación técnica y manual de usuario entregados
- [ ] Reporte final del proyecto entregado
- [ ] Código mergeado en `main` con tag de versión `v1.0.0`

---

## Rama Git

`feature/hu-10-production-deploy`
