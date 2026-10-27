# Manual de usuario — Health Access Bridge

**Versión:** 1.0 · 27 de octubre de 2026 · **Para:** médicos y administradores · **Estado de la herramienta:** las sugerencias de la IA son un **borrador de apoyo**; la decisión clínica siempre es suya.

> Producción: https://hab-frontend.onrender.com · Pruebas (QA): https://hab-frontend-qa.onrender.com · Desarrollo: https://hab-frontend-dev.onrender.com
> La primera vez que el sistema no se ha usado en un rato puede tardar hasta un minuto en responder (el servidor «despierta»); espere y recargue.

## 1. Qué hace el sistema
1. **Registra pacientes** con sus datos clínicos y sociales.
2. **Predice el perfil de barreras de acceso** del paciente (perfil 0, 1 o 2).
3. **Sugiere el perfil funcional CIF** (códigos de funciones, estructuras, actividades y factores del entorno) con apoyo de IA; usted acepta, edita o rechaza cada código.
4. **Muestra un tablero de análisis** con gráficos, filtros y exportación a Excel y PDF.

Hay dos roles: **Médico** (trabaja con sus propios pacientes) y **Administrador** (gestiona usuarios y ve el análisis global).

## 2. Ingresar y salir
1. Abra la dirección del sistema y escriba su correo y contraseña; pulse **Iniciar sesión**.
2. La primera vez aparece una **guía de bienvenida**; puede recorrerla o cerrarla.
3. Para salir, abra el **menú de usuario** (arriba a la derecha) y cierre sesión desde allí. La sesión también se cierra sola tras un tiempo de inactividad.
4. Cambie el idioma (español/inglés) con el botón del **globo** del encabezado.

Si el sistema dice que las credenciales son incorrectas, revise el correo y la contraseña; si persiste, pida al administrador que verifique que su usuario esté activo.

## 3. Manual del médico

### 3.1 Registrar y gestionar pacientes (menú *Pacientes*)
- **Agregar:** pulse **Agregar paciente**, complete el formulario (nombre, documento, fecha de nacimiento y demás campos) y **Guardar**. Aparece un aviso de confirmación.
- **Buscar:** escriba en el buscador de la parte superior; la lista se filtra por nombre o documento.
- **Editar:** use el lápiz de la fila del paciente, cambie los datos y guarde.
- **Eliminar:** use la papelera de la fila y confirme. El paciente deja de aparecer en las listas (borrado lógico).
- **Exportar:** los botones **Excel** y **PDF** descargan la lista con los pacientes que usted ve.

Usted solo ve a sus propios pacientes; otro médico no ve los suyos.

### 3.2 Predicción de barreras (menú *Predicciones*)
1. Elija el paciente en la lista.
2. Pulse **Ejecutar predicción**. Al terminar aparece «Predicción completada» y el perfil asignado.
3. El perfil queda guardado en el paciente y se muestra en el Panel con un color: **0** gris, **1** verde, **2** azul.

### 3.3 Perfil funcional CIF (menú *Perfil funcional*)
Esta función usa IA y requiere que el servicio de IA esté encendido. No aplica a menores de 6 años.

1. Elija el paciente.
2. Escriba el **diagnóstico** y las **notas clínicas** (lo que usted observa: limitaciones, ayudas técnicas, entorno). Mientras más específico, mejor la sugerencia.
3. Pulse **Generar perfil funcional**. Tarda unos segundos.
4. El sistema propone hasta tres códigos por componente. Cada fila muestra código, título del catálogo CIF-IA, **calificador** (nivel de severidad), justificación y estado.
5. Para cada código, usted decide:
   - **Aceptar** si está de acuerdo.
   - **Editar** (lápiz) para cambiar el calificador o el código.
   - **Rechazar** si no corresponde.
6. Pulse **Descargar PDF** para el reporte del perfil, o copie el resultado.

**¿Qué significa el calificador?** Indica cuánto se afecta la función, la estructura o la actividad (escala genérica de la CIF, OMS 2001). La pantalla trae una guía desplegable «¿Qué significa el calificador?»:

| Calificador | Significado | Rango |
|---|---|---|
| 0 | Ninguna | 0–4 % |
| 1 | Leve | 5–24 % |
| 2 | Moderada | 25–49 % |
| 3 | Severa | 50–95 % |
| 4 | Completa | 96–100 % |
| 8 / 9 | Sin especificar / No aplicable | — |

En **estructuras (s)** además se indican la naturaleza del cambio y la localización; por defecto quedan «sin especificar» (8): edítelas.

**Importante:** el perfil es un borrador de apoyo, no un certificado ni un diagnóstico. Revise cada código antes de usarlo.

### 3.4 Tablero de análisis (menú *Análisis*)
Muestra datos **agregados** de sus pacientes (sin información que identifique a una persona).
- **Indicadores** en la parte superior (por ejemplo, el total de pacientes).
- **Gráficos** de género, edad, causa de la deficiencia, perfiles de barreras y otros.
- **Filtros** de género, edad, causa y perfil: al cambiarlos, todo el tablero se recalcula.
- **Pestaña «Perfil funcional ICF»:** cuántas sugerencias se generaron y la tasa de aceptación.
- **Exportar Excel** (5 hojas) y **Exportar PDF** (con los gráficos) respetan los filtros activos.

### 3.5 Ayuda
El **Centro de ayuda** y la **Guía predictiva** (menú lateral) explican los conceptos y los pasos. Los íconos de ayuda junto a los campos muestran definiciones al pasar el cursor o enfocar con el teclado.

## 4. Manual del administrador
- **Administración de usuarios (menú *Admin*):** cree un usuario (nombre, correo, contraseña y rol) con el formulario; busque por nombre; filtre por rol; **active o desactive** una cuenta con el interruptor de la fila. Un usuario desactivado no puede ingresar.
- **Análisis global:** en *Análisis* el administrador ve **todos los pacientes**; con el filtro de médico puede ver el tablero de un solo médico.
- El administrador no registra pacientes ni ejecuta predicciones (esas opciones no aparecen en su menú).
- **Contraseñas:** entregue una contraseña inicial segura y pida que se cambie; no las comparta por canales abiertos.

## 5. Accesibilidad y uso en el teléfono
- Todo el sistema se maneja con **teclado** (Tab, Mayús+Tab, Enter, Esc).
- Los botones de íconos tienen nombre para lectores de pantalla.
- La pantalla se adapta al teléfono: el menú lateral se contrae y las tablas pasan a tarjetas.

## 6. Problemas frecuentes
| Síntoma | Qué hacer |
|---|---|
| La pantalla tarda en cargar la primera vez | El servidor estaba dormido; espere hasta un minuto y recargue |
| «No se pudo conectar con el servidor de IA» al generar el perfil | El servicio de IA está apagado o sin conexión; el resto del sistema sigue funcionando. Avise al responsable técnico (ver el manual de operación del servicio ICF) |
| No veo un paciente que registré | Revise el buscador y los filtros; recuerde que solo ve los suyos |
| Sesión cerrada de repente | Se venció por inactividad; vuelva a ingresar |
| El PDF o el Excel no se descarga | Permita las descargas del sitio en su navegador |

## 7. Privacidad
Los datos de los pacientes son sensibles. No comparta su sesión, cierre sesión en equipos compartidos y exporte archivos solo cuando sea necesario. El tablero de análisis usa datos agregados. El servicio de IA corre en un equipo propio del proyecto y no envía la información clínica a servicios externos.

## 8. Dónde pedir ayuda
Escriba al responsable del proyecto o abra un reporte en https://github.com/jaquimbayoc7/health-access-bridge/issues indicando la pantalla, qué hizo y qué mensaje vio (sin incluir datos de pacientes).
