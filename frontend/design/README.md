# HAB — UI Design Files

Diseños visuales del frontend de **Health Access Bridge** generados con Windsurf Pencil.

## Archivo

| Archivo | Descripción |
|---------|-------------|
| `hab-designs.pen` | Archivo maestro con todos los screens del sistema |

## Screens incluidos

| Frame | Pantalla | Rol |
|-------|----------|-----|
| `01 — Login / Landing` | Página de inicio con hero section + formulario de login por rol | Público |
| `02 — Dashboard (Médico)` | Métricas de pacientes, tabla de recientes, historial de predicciones | Médico |
| `03 — Pacientes` | Listado con búsqueda, exportación Excel/PDF, acciones por fila | Médico |
| `04 — Predicciones` | Formulario de nueva predicción + historial de resultados | Médico |
| `05 — Análisis` | 4 métricas estadísticas + gráfico donut de perfiles | Médico |
| `06 — Panel de Administración` | Formulario de creación de usuario + tabla de gestión con toggle | Administrador |

## Cómo abrir

1. En Windsurf, haz clic derecho sobre `hab-designs.pen`
2. Selecciona **Open with Pencil**
3. Cada screen es un frame independiente en el canvas — usa el panel izquierdo para navegar entre ellos

## Paleta de colores

| Token | Color | Uso |
|-------|-------|-----|
| Primario | `#2563EB` | Botones, nav activo, acentos |
| Fondo app | `#F4F4F5` | Background de pantallas autenticadas |
| Fondo login | `#F8FAFF` | Landing/login |
| Superficie | `#FFFFFF` | Cards y paneles |
| Borde | `#E4E4E7` | Bordes de cards e inputs |
| Texto principal | `#18181B` | Headings y labels |
| Texto secundario | `#71717A` | Descripciones y placeholders |
| Éxito | `#16A34A` | Perfil 0, estado Activo |
| Advertencia | `#EAB308` | Perfil 1, métricas medias |
| Peligro | `#DC2626` | Perfil 2, acciones destructivas |
