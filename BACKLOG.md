# Backlog Maestro: Health Access Bridge (HAB)

**Proyecto:** Health Access Bridge  
**Metodología:** SCRUM  
**Duración Total:** 27 Semanas  

---

## MOMENTO 1: TRABAJO INTEGRADOR I (Semanas 1-9) - Avance 24%

### Épica 1: Estructuración y Diseño (Semanas 1-3)
*Artefactos: BPM, Release Plan, Arquitectura, Prototipo Figma.*

### Sprint 1: Gestión de Usuarios y Estructura Backend (Semanas 4-5)

#### HU-01: Sistema de Autenticación y Roles (RBAC)
- **Como** Administrador del sistema
- **Deseo** gestionar el acceso mediante roles (Admin, Médico)
- **Para** asegurar que solo personal autorizado acceda a la información clínica.

**Detalles:**
- **Entradas:** Email, password, selección de rol.
- **Proceso:** Encriptación de claves (Bcrypt), generación de JWT.
- **Salida:** Token de sesión con claims de rol.

**Criterios de Aceptación:**
- El Admin puede crear cuentas para Médicos.
- El Médico no puede acceder a funciones de configuración global.
- Login falla con credenciales erróneas.

**Tareas:**
- Configurar boilerplate de Python/FastAPI.
- Implementar Middleware de autorización por roles.
- Crear vista de Login en React.

**DoD:** Código en main, pruebas de login exitosas, documentación de endpoints.  
**Estimación:** 8 puntos.

---

### Sprint 2: Gestión de Pacientes y Base de Datos (Semanas 6-7)

#### HU-02: Registro y Precarga de Datos de Pacientes
- **Como** Médico
- **Deseo** visualizar y gestionar pacientes con datos precargados
- **Para** agilizar la consulta médica y no empezar desde cero con cada registro.

**Detalles:**
- **Entradas:** Script de migración/seed con datos demográficos base.
- **Proceso:** CRUD completo (Create, Read, Update, Delete) en base de datos relacional.
- **Salida:** Lista de pacientes con buscador y filtros.

**Criterios de Aceptación:**
- Al iniciar la app, deben existir al menos 10 pacientes de prueba.
- El Médico puede editar la historia clínica de un paciente existente.

**Tareas:**
- Diseñar esquema de base de datos (SQL).
- Crear script de "Seeding" para precarga de datos.
- Desarrollar componentes de tabla y formulario de edición.

**DoD:** CRUD funcional al 100%, base de datos normalizada, validación de campos obligatorios.  
**Estimación:** 13 puntos.

---

### Sprint 3: V1 Funcional y Pruebas (Semanas 8-9)

#### HU-03: Integración Frontend-Backend y Despliegue Local
- **Como** Desarrollador
- **Deseo** integrar las capas de la aplicación y realizar pruebas de estrés
- **Para** garantizar la estabilidad de la versión 1.0.

**Criterios de Aceptación:**
- El frontend consume datos reales del API.
- Pruebas de integración pasan con >80% de cobertura.

**DoD:** Despliegue local mediante Docker o script de inicio, reporte de pruebas unitarias.  
**Estimación:** 5 puntos.

---

## MOMENTO 2: TRABAJO INTEGRADOR II (Semanas 10-18) - Avance 60%

### Sprint 4 & 5: Inteligencia Predictiva (Semanas 10-13)

#### HU-04: Integración del Modelo Predictivo de Discapacidad (HybridModelDisability)
- **Como** Médico
- **Deseo** enviar datos del paciente al modelo predictivo alojado en el backend (https://github.com/jaquimbayoc7/HybridModelDisability)
- **Para** obtener un score de riesgo y recomendaciones personalizadas.

**Detalles:**
- **Backend:** Consumir el API REST del modelo HybridModelDisability.
- **Frontend:** Mostrar resultados de predicción en el perfil del paciente.
- **Proceso:** Serializar datos del paciente, enviar POST al endpoint predictivo, recibir respuesta JSON con score y detalles.

**Criterios de Aceptación:**
- El backend responde con predicción en menos de 3 segundos.
- El frontend muestra el score y recomendaciones claras.
- Manejo de errores y estados de carga.

**Tareas:**
- Implementar cliente HTTP en backend para consumir modelo.
- Crear endpoint REST que actúe como proxy seguro.
- Desarrollar componente React para mostrar predicción.
- Pruebas de integración end-to-end.

**DoD:** Predicción integrada, UI responsiva, logs de errores.  
**Estimación:** 21 puntos.

---

### Sprint 6 & 7: Capacidades PWA y Rendimiento (Semanas 14-17)

#### HU-05: Modo Offline y PWA
- **Como** Médico en zonas rurales
- **Deseo** acceder a la lista de pacientes sin conexión a internet
- **Para** garantizar la continuidad del servicio en áreas de baja conectividad.

**Tareas:**
- Configurar Service Worker.
- Implementar Manifiesto de aplicación.
- Estrategia de caché (Stale-while-revalidate).

**DoD:** Instalable en móvil/escritorio, carga básica sin internet.  
**Estimación:** 13 puntos.

---

### Sprint 7: Pruebas de Integración y Rendimiento

#### HU-06: Pruebas de integración backend-frontend y rendimiento API
- **Como** QA
- **Deseo** validar que la integración entre frontend y backend es estable y rápida
- **Para** asegurar la calidad y experiencia de usuario.

**Criterios de Aceptación:**
- Pruebas automatizadas de integración pasan.
- API responde en menos de 200ms bajo carga simulada.

**DoD:** Reporte de pruebas, corrección de bugs críticos.  
**Estimación:** 8 puntos.

---

## MOMENTO 3: TRABAJO INTEGRADOR III (Semanas 19-27) - Avance 100%

### Sprint 8 & 9: IA Generativa y Recomendaciones (Semanas 19-22)

#### HU-07: Orquestación con LLM para Recomendaciones Clínicas
- **Como** Médico
- **Deseo** que la IA generativa (GPT-4 u otro LLM) cree resúmenes y planes personalizados
- **Para** apoyar la toma de decisiones clínicas basadas en evidencia.

**Detalles:**
- **Backend:** Integrar API LLM (ej. OpenAI, Abacus LLM).
- **Frontend:** Mostrar resumen generado y recomendaciones en perfil paciente.
- **Proceso:** Enviar datos y contexto al LLM, recibir texto enriquecido.

**Criterios de Aceptación:**
- Resumen coherente y útil.
- Opción para exportar a PDF.
- Disclaimer legal visible.

**DoD:** Integración completa, UI amigable, logs de uso.  
**Estimación:** 21 puntos.

---

### Sprint 10 & 11: Dashboards y Cierre (Semanas 23-26)

#### HU-08: Dashboard de Análisis y Exportación
- **Como** Administrador / Médico
- **Deseo** visualizar estadísticas globales y exportar reportes
- **Para** análisis y toma de decisiones a nivel poblacional.

**Tareas:**
- Crear dashboards con gráficos interactivos (Chart.js, D3.js).
- Funcionalidad de exportar a Excel y PDF.
- Despliegue final en Render.

**DoD:** Dashboard funcional, exportación sin errores, documentación.  
**Estimación:** 13 puntos.

---

### Sprint 11: Pruebas Funcionales y Usabilidad

#### HU-09: Pruebas completas y feedback de usuarios
- **Como** QA y usuarios finales
- **Deseo** validar funcionalidad, usabilidad y accesibilidad
- **Para** entregar un producto estable y usable.

**Criterios de Aceptación:**
- Pruebas manuales y automatizadas completadas.
- Feedback documentado y corregido.

**DoD:** Reporte final de pruebas, correcciones aplicadas.  
**Estimación:** 8 puntos.

---

### Sprint 12: Entrega Final y Documentación (Semana 27)

#### HU-10: Despliegue final y generación de manuales
- **Como** Equipo de proyecto
- **Deseo** desplegar la versión estable en la nube y entregar documentación completa
- **Para** cerrar el proyecto con calidad y soporte.

**Tareas:**
- Despliegue en Render.
- Documentación técnica y manuales de usuario.
- Reportes finales.

**DoD:** Aplicación en producción, documentación entregada.  
**Estimación:** 5 puntos.
