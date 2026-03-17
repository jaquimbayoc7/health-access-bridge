## Historia de Usuario

**Como** Médico en zonas rurales  
**Deseo** acceder a la lista de pacientes sin conexión a internet  
**Para** garantizar la continuidad del servicio en áreas de baja conectividad.

---

## Detalles Técnicos

| Campo | Detalle |
|-------|---------|
| **Entradas** | App web cargada previamente en el navegador |
| **Proceso** | Service Worker intercepta requests, sirve datos desde caché |
| **Salida** | Lista de pacientes disponible sin conexión |
| **Stack** | React + Vite + vite-plugin-pwa + IndexedDB |
| **Estimación** | 13 puntos |
| **Sprint** | Sprint 6 y 7 (Semanas 14-17) |
| **Momento** | Momento 2 - Trabajo Integrador II |

---

## Dependencias

> ⚠️ Este issue **no puede comenzar** hasta que estén cerrados:
> - #2 HU-02: Registro y Precarga de Datos de Pacientes
> - #3 HU-03: Integración Frontend-Backend y Despliegue Local

---

## Criterios de Aceptación

- [ ] La app es instalable en móvil y escritorio (PWA)
- [ ] La lista de pacientes carga sin conexión a internet
- [ ] Los datos se sincronizan al recuperar la conexión
- [ ] Icono de app y splash screen configurados
- [ ] Notificación visible al usuario cuando está en modo offline
- [ ] Lighthouse PWA score > 90

---

## Tareas

- [ ] Configurar `vite-plugin-pwa` en `vite.config.ts`
- [ ] Implementar `manifest.json` con iconos, nombre y colores de tema
- [ ] Configurar Service Worker con estrategia `stale-while-revalidate`
- [ ] Definir estrategia de caché para rutas críticas (`/api/patients`)
- [ ] Implementar almacenamiento local con IndexedDB para datos de pacientes
- [ ] Mostrar banner offline/online con estado de conectividad
- [ ] Pruebas en modo avión (Lighthouse PWA audit)

---

## Definition of Done (DoD)

- [ ] App instalable en móvil/escritorio
- [ ] Carga básica sin internet (pacientes en caché)
- [ ] Lighthouse PWA score > 90
- [ ] Código mergeado en `main`

---

## Rama Git

`feature/hu-05-pwa-offline`
