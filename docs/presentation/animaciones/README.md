# Animaciones de Health Access Bridge (Archify)

Diagramas animados del proyecto desde la perspectiva del **médico** y del **administrador**, hechos con [Archify](https://github.com/tt-a1i/archify) (licencia MIT, v3.0.1).

| Archivo | Qué muestra |
|---|---|
| `index.html` | Página de entrada con los cuatro diagramas y sus videos |
| `arquitectura-hab.html` | Arquitectura completa: actores, Render, túnel autenticado, PC propio con la IA y CI/CD |
| `recorrido-medico-pacientes.html` | Médico (1 de 2): acceso, registro de pacientes y predicción de barreras |
| `recorrido-medico-icf.html` | Médico (2 de 2): Perfil Funcional ICF con IA local, decisión y reporte |
| `recorrido-administrador.html` | Administrador: usuarios, límite de acceso (403) y salud del servicio de IA |
| `video/*.webm` | Grabación de 14 s de cada animación (para insertar en la presentación) |
| `fuentes/*.json` | Fuente de cada diagrama (esquema de Archify) |
| `construir.mjs` | Valida y genera los HTML (agrega el idioma español) |
| `.evidencia/` | Resúmenes de validación de la última construcción |

Cada HTML es autosuficiente: se abre en el navegador sin instalar nada. Controles útiles: interruptor de movimiento (Activa / Quieta), **Ruta** (trazar el camino entre dos nodos), **Lente**, buscador de nodos, tema claro/oscuro y **Exportar** (PNG, SVG, WebM).

## Cómo regenerarlos

Archify necesita Node 18 o superior y un Chrome o Chromium para su verificación en navegador. Este repositorio no incluye Archify; se clona aparte:

```bash
git clone --depth 1 https://github.com/tt-a1i/archify
export ARCHIFY_CHROME=/ruta/a/chrome            # solo si Archify no encuentra Chrome
cd docs/presentation/animaciones
node construir.mjs /ruta/a/archify/archify/bin/archify.mjs                    # todos
node construir.mjs /ruta/a/archify/archify/bin/archify.mjs recorrido-medico-icf   # uno
```

`construir.mjs` pasa cada diagrama por `finalize` de Archify (validación del esquema, entrega, comprobaciones y verificación en navegador real, perfil `showcase`). Si falla, el mensaje indica qué ajustar. Límites que conviene saber para editar los JSON:

- Secuencia: un mensaje cada 28 px como mínimo; ancho máximo de 1085 px y alto máximo de unos 696 px (para que el texto siga legible en pantalla de 1440 px); por eso el recorrido del médico se dividió en dos diagramas.
- La unidad de ayuda del visor en español sale de `examples/locales/es.json` de Archify.

**Nota sobre Windows + OneDrive:** la herramienta escribe archivos temporales y los renombra; sobre una carpeta sincronizada o montada en Docker puede fallar. Se construyó en un directorio de trabajo del contenedor y se copiaron solo los HTML.

## Datos y privacidad

Los diagramas no contienen datos de pacientes; las rutas, los textos y las cifras salen de este repositorio (`BACKLOG.md`, `docs/MANUAL_OPERACION_ICF.md`, `docs/diagrams/rag-icf-postgresql.md`).
