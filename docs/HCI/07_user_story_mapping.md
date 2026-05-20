# User Story Mapping — Health Access Bridge (HAB)

> **Método:** User Story Mapping (Jeff Patton, 2014)  
> **Personas:** Dra. Emilly Maria Celis Barreto (SST — ICBF / Usuario institucional) + Laura Cangrejo Perafan (Profesional Alcaldía / Coordinación)  
> **Insumos:** 3 entrevistas + Diagrama de Afinidad Método KJ (6 temas, 21 notas) + Backlog SCRUM existente  
> **Fecha:** Mayo 2026

---

## Estructura del mapa

```
NIVEL 1 — ACTIVIDADES (backbone)  →  Lo que el usuario quiere LOGRAR
NIVEL 2 — TAREAS                  →  Pasos que realiza para lograrlo
NIVEL 3 — HISTORIAS DE USUARIO    →  Funcionalidades específicas del sistema
           ┌── Release 1 (MVP)
           ├── Release 2 (Iteración)
           └── Release 3 (Futuro)
```

---

---

## 🔑 ACTIVIDAD 1 — Autenticarse y acceder al sistema

> **Persona:** Ambas | **Tema de afinidad:** Accesibilidad Tecnológica + Confianza y Privacidad

### Tareas del usuario

| # | Tarea |
|---|-------|
| T1.1 | Ingresar al sistema con credenciales |
| T1.2 | Recuperar contraseña olvidada |
| T1.3 | Ser redirigido automáticamente según el rol |
| T1.4 | Cerrar sesión de forma segura |

### Historias de Usuario por Release

#### ✅ Release 1 — MVP (Implementado)

| ID | Historia | Criterio de aceptación |
|----|----------|----------------------|
| HU-01 | **Como médico**, quiero ingresar con mi correo y contraseña para acceder a mis pacientes. | Login exitoso redirige a /dashboard; credenciales incorrectas muestran mensaje descriptivo |
| HU-02 | **Como cualquier usuario**, quiero que el sistema me redirija automáticamente a mi panel según mi rol (admin → /admin, médico → /dashboard). | La redirección ocurre en < 1 seg después del login exitoso |
| HU-03 | **Como cualquier usuario**, quiero cerrar sesión y que mi token quede invalidado. | Logout limpia localStorage y redirige a /login |
| HU-04 | **Como cualquier usuario**, quiero que si mi sesión expira, el sistema me lleve automáticamente al login. | HTTP 401 → limpieza de token → redirección a /login |

#### 🔵 Release 2 — Iteración

| ID | Historia | Criterio de aceptación |
|----|----------|----------------------|
| HU-05 | **Como usuario**, quiero recuperar mi contraseña por correo electrónico si la olvido. | Flujo de reset password con token temporal por email |
| HU-06 | **Como administrador**, quiero ver un registro de los últimos accesos de cada médico al sistema. | Log de auditoría en panel admin con fecha/hora de último login |

#### 🟡 Release 3 — Futuro

| ID | Historia | Criterio de aceptación |
|----|----------|----------------------|
| HU-07 | **Como usuario**, quiero autenticarme con mi cuenta institucional (SSO / LDAP). | Integración con proveedor de identidad de la Secretaría de Salud |
| HU-08 | **Como médico**, quiero poder acceder al sistema desde el celular sin internet (modo offline). | PWA con Service Worker; sincronización al recuperar conectividad |

---

---

## 🗂️ ACTIVIDAD 2 — Gestionar pacientes con discapacidad

> **Persona:** Dra. Emilly Maria Celis Barreto | **Tema de afinidad:** Flujo Clínico + Curva de Aprendizaje

### Tareas del usuario

| # | Tarea |
|---|-------|
| T2.1 | Buscar un paciente existente |
| T2.2 | Registrar un nuevo paciente con datos ICF |
| T2.3 | Actualizar la historia clínica de un paciente |
| T2.4 | Eliminar un registro (con confirmación) |
| T2.5 | Exportar el listado de pacientes |
| T2.6 | Ver el perfil completo de un paciente |

### Historias de Usuario por Release

#### ✅ Release 1 — MVP (Implementado)

| ID | Historia | Criterio de aceptación |
|----|----------|----------------------|
| HU-09 | **Como médico**, quiero registrar un nuevo paciente con todos los campos ICF (D1–D6, nivel global, categorías) en un formulario modal. | Formulario con validación inline; POST exitoso persiste el registro; modal se cierra |
| HU-10 | **Como médico**, quiero buscar pacientes por nombre o número de documento en tiempo real. | Búsqueda con debounce 300ms; resultados actualizados sin recargar página |
| HU-11 | **Como médico**, quiero editar la historia clínica de uno de mis pacientes. | Modal pre-poblado con datos actuales; PUT actualiza el registro |
| HU-12 | **Como médico**, quiero eliminar un registro con un diálogo de confirmación para evitar errores. | Diálogo "¿Está seguro?" antes de DELETE; eliminación lógica (soft delete) |
| HU-13 | **Como médico**, quiero que solo yo pueda ver y editar mis propios pacientes. | El backend filtra por `owner_id`; el frontend no muestra pacientes de otros médicos |
| HU-14 | **Como médico**, quiero exportar mi listado de pacientes a Excel. | Botón "Exportar Excel" genera archivo `.xlsx` con SheetJS en el cliente |

#### 🔵 Release 2 — Iteración

| ID | Historia | Criterio de aceptación |
|----|----------|----------------------|
| HU-15 | **Como médico**, quiero ver tooltips explicativos en cada campo ICF del formulario para entender qué debo ingresar. | Cada campo D1–D6 tiene un ícono ⓘ con descripción ICF al hacer hover |
| HU-16 | **Como médico**, quiero exportar el perfil completo de un paciente (datos + predicción) en PDF. | Botón "Exportar PDF" genera documento con jsPDF desde el cliente |
| HU-17 | **Como médico**, quiero filtrar pacientes por perfil de predicción (Bajas / Moderadas / Altas). | Selector de filtro en la tabla; resultados se actualizan en tiempo real |
| HU-18 | **Como médico**, quiero adjuntar notas de texto libre a cada consulta de un paciente. | Campo de notas en el formulario; historial de notas visible en el perfil |

#### 🟡 Release 3 — Futuro

| ID | Historia | Criterio de aceptación |
|----|----------|----------------------|
| HU-19 | **Como médico**, quiero registrar pacientes cuando no tengo internet y que los datos se sincronicen automáticamente. | Service Worker almacena el formulario offline; sincroniza con el backend al reconectar |
| HU-20 | **Como médico**, quiero importar datos de pacientes desde un archivo Excel existente. | Carga masiva con validación de columnas ICF; informe de errores de importación |

---

---

## 🤖 ACTIVIDAD 3 — Ejecutar predicciones ML de perfil de barreras

> **Persona:** Dra. Emilly Maria Celis Barreto | **Tema de afinidad:** Interpretación del Modelo ML

### Tareas del usuario

| # | Tarea |
|---|-------|
| T3.1 | Seleccionar un paciente para predecir |
| T3.2 | Ejecutar la predicción |
| T3.3 | Interpretar el resultado del perfil |
| T3.4 | Ver el historial de predicciones del paciente |
| T3.5 | Consultar la guía clínica del perfil asignado |

### Historias de Usuario por Release

#### ✅ Release 1 — MVP (Implementado)

| ID | Historia | Criterio de aceptación |
|----|----------|----------------------|
| HU-21 | **Como médico**, quiero seleccionar un paciente y ejecutar el modelo ML para obtener su perfil de barreras de acceso. | POST /patients/{id}/predict retorna perfil en < 3 seg; resultado persiste en el registro |
| HU-22 | **Como médico**, quiero ver el resultado de la predicción con un badge codificado por color (verde/amarillo/rojo). | Badge visible inmediatamente; colores: verde=0 (Bajas), amarillo=1 (Moderadas), rojo=2 (Altas) |
| HU-23 | **Como médico**, quiero ver la descripción del perfil predictivo en lenguaje clínico. | Campo `prediction_description` visible en el resultado y en el perfil del paciente |

#### 🔵 Release 2 — Iteración

| ID | Historia | Criterio de aceptación |
|----|----------|----------------------|
| HU-24 | **Como médico**, quiero que el resultado de la predicción incluya una explicación de qué factores influyeron más. | Panel de "factores determinantes" con los 3 campos ICF de mayor peso en el resultado |
| HU-25 | **Como médico**, quiero ver el historial de predicciones de un paciente a lo largo del tiempo. | Timeline de predicciones con fecha, perfil y variación respecto a la anterior |
| HU-26 | **Como médico**, quiero ir directamente desde el resultado a la guía clínica del perfil asignado. | Enlace "Ver guía clínica →" en el resultado redirige a PredictiveGuide filtrado por perfil |

#### 🟡 Release 3 — Futuro

| ID | Historia | Criterio de aceptación |
|----|----------|----------------------|
| HU-27 | **Como médico**, quiero ejecutar predicciones en lote para todos mis pacientes sin predicción reciente. | Botón "Predecir todos" con barra de progreso; resultados persistidos en cada registro |
| HU-28 | **Como administrador**, quiero ver qué porcentaje de pacientes tienen predicción ejecutada vs. pendiente. | Métrica en Dashboard Admin: "X% con predicción actualizada (< 30 días)" |

---

---

## 📊 ACTIVIDAD 4 — Analizar estadísticas de la población clínica

> **Persona:** Dra. Emilly Maria Celis Barreto + Laura Cangrejo Perafan | **Tema de afinidad:** Visibilidad y Comunicación

### Tareas del usuario

| # | Tarea |
|---|-------|
| T4.1 | Ver distribución de perfiles de la población propia |
| T4.2 | Ver métricas demográficas (género, causa de deficiencia) |
| T4.3 | Comparar métricas entre períodos |
| T4.4 | Exportar reporte consolidado |

### Historias de Usuario por Release

#### ✅ Release 1 — MVP (Implementado)

| ID | Historia | Criterio de aceptación |
|----|----------|----------------------|
| HU-29 | **Como médico**, quiero ver una gráfica de torta con la distribución de perfiles predictivos de mis pacientes. | PieChart con Recharts; datos calculados del listado GET /patients/ |
| HU-30 | **Como médico**, quiero ver métricas de resumen en el Dashboard: total pacientes, predicciones ejecutadas, distribución de perfiles. | Tarjetas de métricas visibles al cargar el Dashboard |
| HU-31 | **Como médico**, quiero ver gráficas de barras por género y causa de deficiencia de mis pacientes. | BarChart en módulo Analytics con datos calculados en cliente |

#### 🔵 Release 2 — Iteración

| ID | Historia | Criterio de aceptación |
|----|----------|----------------------|
| HU-32 | **Como médico**, quiero exportar el reporte de análisis a PDF con las gráficas incluidas. | Botón "Exportar PDF" en Analytics genera documento con gráficas renderizadas |
| HU-33 | **Como Profesional**, quiero ver métricas agregadas por municipio en un panel de supervisión. | Dashboard de coordinación (rol Admin) con métricas por médico/municipio |
| HU-34 | **Como Profesional**, quiero recibir una alerta cuando un profesional no ha actualizado sus registros en más de 15 días. | Notificación in-app y email automático al admin si profesional inactivo > 15 días |

#### 🟡 Release 3 — Futuro

| ID | Historia | Criterio de aceptación |
|----|----------|----------------------|
| HU-35 | **Como Profesional**, quiero recibir un reporte semanal automático por correo con el estado de cada municipio. | Tarea programada en backend; email con resumen en HTML cada lunes a las 8am |
| HU-36 | **Como Profesional**, quiero ver la evolución temporal de los perfiles de un municipio en los últimos 12 meses. | Gráfica de líneas con datos históricos mensuales |

---

---

## 🛡️ ACTIVIDAD 5 — Administrar usuarios del sistema

> **Persona:** Laura Cangrejo Perafan (Admin) | **Tema de afinidad:** Confianza y Privacidad + Visibilidad

### Tareas del usuario

| # | Tarea |
|---|-------|
| T5.1 | Ver listado de médicos registrados |
| T5.2 | Crear cuenta de nuevo médico o admin |
| T5.3 | Activar / desactivar cuenta de un médico |
| T5.4 | Ver estado de actividad de cada médico |
| T5.5 | Restablecer contraseña de un médico |

### Historias de Usuario por Release

#### ✅ Release 1 — MVP (Implementado)

| ID | Historia | Criterio de aceptación |
|----|----------|----------------------|
| HU-37 | **Como administradora**, quiero ver la lista de todos los usuarios con su rol y estado (activo/inactivo). | Tabla en AdminPanel con badge de rol y estado; datos de GET /admin/users |
| HU-38 | **Como administradora**, quiero crear una cuenta de médico o administrador con nombre, correo y contraseña. | Modal de creación; POST /admin/users/register; nuevo usuario aparece en la tabla |
| HU-39 | **Como administradora**, quiero activar o desactivar la cuenta de un médico con un toggle. | PATCH /admin/users/{id}/status actualiza estado; badge cambia inmediatamente en la tabla |
| HU-40 | **Como administradora**, quiero que el sistema me impida acceder al panel de administración si no tengo el rol correcto. | Guard AdminRoute redirige a /dashboard si el rol no es admin |

#### 🔵 Release 2 — Iteración

| ID | Historia | Criterio de aceptación |
|----|----------|----------------------|
| HU-41 | **Como administradora**, quiero ver la fecha del último acceso de cada médico al sistema. | Columna "Último acceso" en la tabla de AdminPanel |
| HU-42 | **Como administradora**, quiero restablecer la contraseña de un médico sin necesidad de soporte técnico. | Botón "Reset contraseña" en el panel; envía email con contraseña temporal |
| HU-43 | **Como administradora**, quiero asignar un médico a un municipio específico para filtrar sus estadísticas. | Campo "municipio" en el perfil del usuario; visible en filtros del panel de análisis |

#### 🟡 Release 3 — Futuro

| ID | Historia | Criterio de aceptación |
|----|----------|----------------------|
| HU-44 | **Como administradora**, quiero importar un listado de médicos desde un archivo Excel para crear cuentas en lote. | Carga masiva con validación; informe de cuentas creadas / errores |
| HU-45 | **Como administradora**, quiero ver un log de auditoría con todas las acciones realizadas por cada usuario. | Panel de auditoría con filtros por usuario, acción y fecha |

---

---

## Resumen del User Story Map

```
ACTIVIDAD        │ Release 1 (MVP) │ Release 2 │ Release 3 │ Total
─────────────────┼─────────────────┼───────────┼───────────┼───────
1. Autenticación │ HU-01 a HU-04   │ HU-05-06  │ HU-07-08  │  8 HU
2. Pacientes     │ HU-09 a HU-14   │ HU-15-18  │ HU-19-20  │ 12 HU
3. Predicciones  │ HU-21 a HU-23   │ HU-24-26  │ HU-27-28  │  8 HU
4. Analytics     │ HU-29 a HU-31   │ HU-32-34  │ HU-35-36  │  8 HU
5. Admin usuarios│ HU-37 a HU-40   │ HU-41-43  │ HU-44-45  │  9 HU
─────────────────┼─────────────────┼───────────┼───────────┼───────
TOTAL            │     20 HU ✅    │   13 HU   │   12 HU   │ 45 HU
```

---

## Priorización por impacto en las personas

| Historia | Persona beneficiada | Tema de afinidad | Prioridad |
|----------|--------------------|-----------------|-----------| 
| HU-08 — Modo offline | Dra. Emilly Maria Celis Barreto | Accesibilidad | 🔴 Alta |
| HU-15 — Tooltips ICF | Laura Cangrejo Perafan (E2) | Curva aprendizaje | 🔴 Alta |
| HU-24 — Factores ML | Dra. Emilly Maria Celis Barreto | Interpretación ML | 🟠 Media |
| HU-33 — Panel coordinación | Laura Cangrejo Perafan | Visibilidad | 🟠 Media |
| HU-34 — Alerta inactividad | Laura Cangrejo Perafan | Comunicación | 🟠 Media |
| HU-26 — Enlace guía ICF | Familiar/Cuidador (E3) | Curva aprendizaje | 🟡 Media-baja |
| HU-35 — Reporte automático | Laura Cangrejo Perafan | Visibilidad | 🟡 Media-baja |
| HU-44 — Carga masiva | Laura Cangrejo Perafan | Eficiencia admin | 🟢 Baja |

---

## Trazabilidad con el Diagrama de Afinidad

| Tema de Afinidad | HUs relacionadas |
|-----------------|-----------------|
| 🔵 Accesibilidad Tecnológica | HU-07, HU-08, HU-15, HU-19, HU-20 |
| 🟢 Flujo Clínico y Fragmentación | HU-09, HU-11, HU-16, HU-17, HU-18, HU-20 |
| 🟡 Confianza y Privacidad | HU-03, HU-04, HU-13, HU-40, HU-45 |
| 🟠 Interpretación del ML | HU-21, HU-22, HU-23, HU-24, HU-25, HU-26, HU-27 |
| 🔴 Curva de Aprendizaje | HU-15, HU-12, HU-26, HU-42 |
| 🟣 Visibilidad y Comunicación | HU-28, HU-33, HU-34, HU-35, HU-36, HU-41 |
