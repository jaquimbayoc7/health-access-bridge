# User Personas — Health Access Bridge (HAB)

> **Método:** Derivadas del Diagrama de Afinidad — Método KJ (6 temas, 21 notas, 3 entrevistas)  
> **Fecha de elaboración:** Mayo 2026  
> **Herramienta:** Síntesis cualitativa de entrevistas E1, E2, E3

---

## ¿Por qué estas dos personas?

| Criterio | Persona 1 | Persona 2 |
|----------|-----------|-----------|
| **Origen** | Entrevista E1 — Dra. Emilly Maria Celis Barreto | Entrevista E2 — Laura Cangrejo Perafan |
| **Rol en HAB** | Usuario clínico — perfil operativo principal | Asistente administrativo — rol coordinación |
| **Nivel TI** | Avanzado | Intermedio |
| **Representa** | 80% de los usuarios del sistema | 20% del sistema, pero crítica para supervisión |

---

---

# �‍⚕️ PERSONA 1 — Dra. Emilly Maria Celis Barreto

```
┌─────────────────────────────────────────────────────────────────────┐
│  [Foto: psicóloga, bata institucional, consultorio rural, Huila]    │
│                                                                     │
│  Dra. Emilly Maria Celis Barreto                                         │
│  Profesional en Seguridad y Salud en el Trabajo · Programa PABS Discapacidad             │
│  ICBF — Neiva, Huila                          │
└─────────────────────────────────────────────────────────────────────┘
```

## Biografía

Emilly es Profesional en Seguridad y Salud en el Trabajo

---

## Contexto tecnológico

| Aspecto | Detalle |
|---------|---------|
| **Dispositivos** | Portátil HP (trabajo), iPhone 13 (personal) |
| **Sistemas que usa** | HIS institucional, Excel, Drive, SISPRO, RIPS |
| **Conectividad** | Buena en el hospital; intermitente en visitas domiciliarias (2G/3G) |
| **Comodidad con apps web** | ★★★★★ (5/5) |
| **Experiencia con ML** | Conoce el concepto; nunca ha usado un modelo predictivo clínico |

---

## Metas

1. **Registrar y actualizar** la historia clínica ICF de sus pacientes en el menor tiempo posible, idealmente desde el mismo consultorio o en campo.
2. **Ejecutar predicciones ML** para clasificar el perfil de barreras de acceso de sus pacientes y priorizar intervenciones.
3. **Acceder al historial completo** de un paciente sin depender de registros paralelos en Excel o cuadernos físicos.

---

## Frustraciones

1. **Sistemas fragmentados:** sus datos ICF están en Excel, los clínicos en el HIS; cruzarlos para generar reportes le consume horas al mes.
2. **Sin acceso offline:** cuando está en visita domiciliaria sin internet, no puede registrar en el sistema y debe hacerlo doble al regresar.
3. **Confianza limitada en el ML:** quiere saber si el modelo fue validado con datos de pacientes de su región antes de integrar los resultados en su criterio clínico.

---

## Comportamiento con HAB

- **Primera visita:** navega directamente a la pantalla de Pacientes, le llama la atención el buscador y la tabla paginada.
- **Flujo favorito:** Dashboard → Pacientes → formulario → Predicciones → resultado en badge de color.
- **Comportamiento de poder:** usa atajos de teclado, revisa la URL, abre la consola del navegador si algo falla.
- **Punto de fricción:** los nombres de los campos ICF (D1–D6) no tienen tooltips; aunque él los conoce, nota que un colega nuevo no los entendería.

---

## Cita representativa

> *"Llevo años con este sistema fragmentado. Si HAB me permite tener todo en un solo lugar y ejecutar la predicción sin salir de la plataforma, ya habrá valido la pena. Solo necesito que funcione cuando no hay señal."*

---

## Escenario de uso

**7:30 am — Consultorio, zona rural, Huila.**  
Emilly llega a la IPS. Abre HAB desde su portátil. Ve en el Dashboard que tiene 3 pacientes sin predicción actualizada en los últimos 30 días. Hace clic en el primero, actualiza los campos D3 y D5 que cambiaron en la última evaluación, ejecuta la predicción y obtiene "Perfil 1 — Barreras Moderadas". Lee la descripción en lenguaje natural, concuerda con su criterio, e imprime el PDF para incluirlo en el expediente físico.

**11:00 am — Visita domiciliaria (sin señal).**  
Emilly intenta abrir HAB en su teléfono pero no hay internet. Necesita que la app funcione offline y sincronice al volver a la IPS.

---

## Empathy Map

```
╔══════════════════════╦══════════════════════╗
║       PIENSA         ║        SIENTE        ║
║                      ║                      ║
║ "Si el modelo falla  ║ Frustración con la   ║
║  soy yo quien        ║ duplicidad de trabajo║
║  responde ante       ║ Orgullo al ver las   ║
║  el paciente"        ║ métricas de su       ║
║                      ║ población            ║
╠══════════════════════╬══════════════════════╣
║        DICE          ║         HACE         ║
║                      ║                      ║
║ "Necesito que        ║ Lleva dos registros  ║
║  funcione offline"   ║ paralelos (HIS+Excel)║
║ "¿El modelo está     ║ Genera reportes      ║
║  validado aquí?"     ║ manualmente cada mes ║
╚══════════════════════╩══════════════════════╝
         │ PAINS                  │ GAINS
         ▼                        ▼
  Sistema fragmentado       Historia clínica unificada
  Sin modo offline          Predicción ML integrada
  Reportes manuales         Exportación automática
  Confianza en ML dudosa    Validación del modelo
```

---

---

# �‍� PERSONA 2 — Laura Cangrejo Perafan

```
┌─────────────────────────────────────────────────────────────────────┐
│  [Foto: asistente administrativo, escritorio con computador, oficina pública]  │
│                                                                     │
│  Laura Cangrejo Perafan                                         │
│  Profesional · Programa PABS Discapacidad              │
│  Secretaría de Salud · Garzón, Huila                               │
└─────────────────────────────────────────────────────────────────────┘
```

## Biografía

Laura trabaja en la Alcaldía de Garzón, Huila como Profesional del programa PABS. Su labor es garantizar que los registros de los profesionales de municipios rurales estén actualizados, consolidar la información y generar reportes para el Ministerio de Salud. No tiene formación técnica en informática pero usa Excel, correo electrónico y SISPRO con soltura. Prefiere llamar por WhatsApp antes que navegar por menús de un sistema nuevo.

---

## Contexto tecnológico

| Aspecto | Detalle |
|---------|---------|
| **Dispositivos** | PC de escritorio (oficina), smartphone Samsung (personal) |
| **Sistemas que usa** | Excel, Outlook, SISPRO, plataforma Secretaría de Salud (legacy) |
| **Conectividad** | Buena en la oficina; usa datos móviles en campo |
| **Comodidad con apps web** | ★★★☆☆ (3/5) — cómoda con lo conocido, aprehensiva ante lo nuevo |
| **Experiencia con ML** | Ninguna — entiende el concepto como "el sistema que clasifica" |

---

## Metas

1. **Ver en tiempo real** el estado de los registros de los 12 médicos a su cargo sin tener que llamarlos individualmente.
2. **Generar reportes consolidados** por municipio para el Ministerio de Salud de forma rápida y sin cruzar archivos Excel.
3. **Gestionar accesos** de nuevos médicos al sistema de forma sencilla, sin necesidad de conocimientos técnicos.

---

## Frustraciones

1. **Sin visibilidad en tiempo real:** depende de que los médicos le envíen sus Excel por WhatsApp, y muchos lo hacen tarde o con datos incompletos.
2. **Ausencia de alertas automáticas:** dedica tiempo cada semana a recordar manualmente a los médicos que deben actualizar sus registros.
3. **Resistencia al aprendizaje:** le tomó 6 meses adaptarse al sistema legacy actual; tiene miedo de empezar de cero con una herramienta nueva y "quedar mal" frente a su jefe.

---

## Comportamiento con HAB

- **Primera visita:** va directo al módulo de Administración para ver la lista de médicos registrados.
- **Flujo favorito:** Admin → ver usuarios → Analytics → exportar reporte.
- **Comportamiento de aversión al riesgo:** antes de hacer cualquier acción, pregunta "¿esto tiene deshacer?" y prefiere botones con texto claro antes que íconos solos.
- **Punto de fricción:** el Dashboard le muestra métricas de sus propios pacientes (como si fuera médico), pero ella necesita un panel agregado por municipio.

---

## Cita representativa

> *"Mi mayor problema es que no tengo visibilidad de lo que pasa en los municipios. Si el sistema me mostrara en una sola pantalla: municipio, cuántos pacientes, cuándo fue el último registro y si hay predicciones sin hacer, eso cambiaría mi trabajo completamente."*

> *— Laura Cangrejo Perafan, Profesional, Alcaldía de Garzón, Huila*

---

## Escenario de uso

**Lunes 8:00 am — Oficina, Alcaldía de Garzón, Huila.**  
Laura llega y abre HAB. Va al módulo de Analytics. Ve que 3 municipios no tienen registros actualizados desde hace más de 15 días. El sistema le muestra una alerta visual. Hace clic en "Ver detalle" y puede identificar qué profesionales están atrasados. Les envía un correo desde el sistema con un solo clic. A las 10 am descarga el reporte consolidado en Excel para enviarlo a la coordinación departamental.

**Martes — Incorporación de nuevo profesional.**  
Ingresa al Panel de Administración, crea la cuenta con rol "Médico", asigna el municipio y envía las credenciales por correo. Todo en menos de 5 minutos, sin ayuda técnica.

---

## Empathy Map

```
╔══════════════════════╦══════════════════════╗
║       PIENSA         ║        SIENTE        ║
║                      ║                      ║
║ "¿Y si me equivoco   ║ Ansiedad ante        ║
║  y desactivo al      ║ herramientas nuevas  ║
║  médico equivocado?" ║ Alivio cuando el     ║
║ "¿Cómo sé que todos  ║ sistema hace lo que  ║
║  están al día?"      ║ espera               ║
╠══════════════════════╬══════════════════════╣
║        DICE          ║         HACE         ║
║                      ║                      ║
║ "Necesito verlo      ║ Llama por WhatsApp   ║
║  todo de un vistazo" ║ para recordar updates║
║ "¿Hay deshacer       ║ Copia datos a Excel  ║
║  en este botón?"     ║ "por si las dudas"   ║
╚══════════════════════╩══════════════════════╝
         │ PAINS                  │ GAINS
         ▼                        ▼
  Sin visibilidad en tiempo real  Panel coordinador por municipio
  Coordinación manual por WA      Alertas automáticas de inactividad
  Miedo a errores irreversibles   Botones con confirmación clara
  Reporte manual al Ministerio    Exportación programada automática
```

---

---

## Comparativa de Personas

| Dimensión | Dra. Emilly Maria Celis Barreto | Laura Cangrejo Perafan |
|-----------|---------------------------|----------------------------|
| **Rol** | Psicóloga clínica (operativa) | Asistente información (coordinación) |
| **Nivel TI** | Avanzado | Intermedio |
| **Motivación HAB** | Registro integrado + predicción ML | Visibilidad en tiempo real por municipio |
| **Mayor barrera** | Modo offline / validación del ML | Terminología clínica confusa / curva aprendizaje |
| **Valor del ML** | Apoyo clínico con validación | Priorización de recursos por municipio |
| **Dispositivo principal** | Portátil + smartphone | PC escritorio |
| **SUS esperado** | 80–90 | 65–75 |
| **NPS estimado** | 9/10 | 8/10 |

---

## Cómo informan el diseño

| Insight de persona | Decisión de diseño en HAB |
|-------------------|--------------------------|
| Emilly necesita modo offline | **PWA con Service Worker** para formularios de pacientes |
| Emilly quiere validación del modelo | **Ficha técnica del modelo** en Guía Predictiva |
| Laura necesita panel por municipio | **Dashboard de coordinación** (backlog futuro) |
| Laura no entiende D1–D6 | **Tooltips ICF** en todos los campos del formulario |
| Ambos necesitan exportación | **Excel y PDF** ya implementados en módulo Pacientes |
| Familiar/Cuidador (E3) pide notificaciones | **Notificaciones al cuidador** (backlog futuro) |
