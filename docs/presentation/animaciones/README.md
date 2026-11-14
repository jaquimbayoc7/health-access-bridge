# Animaciones de Health Access Bridge (Archify)

Diagramas animados del proyecto desde la perspectiva del **médico** y del **administrador**, más el proceso de **validación clínica** con la médica revisora, hechos con [Archify](https://github.com/tt-a1i/archify) (licencia MIT, v3.0.1).

| Archivo | Qué muestra |
|---|---|
| `index.html` | Página de entrada con los seis diagramas y sus videos o capturas |
| `arquitectura-hab.html` | Arquitectura completa: actores, Render, túnel autenticado, PC propio con la IA y CI/CD |
| `servicio-icf.html` | Servicio ICF por dentro: entrada segura, reglas, embedding, pgvector, selección por la IA, respaldo y validación final |
| `recorrido-medico-pacientes.html` | Médico (1 de 2): acceso, registro de pacientes y predicción de barreras |
| `recorrido-medico-icf.html` | Médico (2 de 2): Perfil Funcional ICF con IA local, decisión y reporte |
| `recorrido-administrador.html` | Administrador: usuarios, límite de acceso (403) y salud del servicio de IA |
| `proceso-validacion-clinica.html` | Validación clínica (HU-07g): preparación, reunión y entrega, Fase A a ciegas y Fase B, cálculo con IC y κ ponderado, y veredicto. Tipo *workflow* con carriles |
| `video/*.webm` | Grabación de 14 s de cada animación (para insertar en la presentación) |
| `video/proceso-validacion-clinica.png` | Captura del diagrama de validación clínica (portada de su tarjeta; el video se exporta desde el visor con **Exportar**) |
| `fuentes/*.json` | Fuente de cada diagrama (esquema de Archify) |
| `construir.mjs` | Valida y genera los HTML (agrega el idioma español) |

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

## Memoria de casos (HU-07j, 13-nov-2026)

Las fuentes `fuentes/arquitectura-hab.json`, `fuentes/servicio-icf.json` y `fuentes/recorrido-medico-icf.json` ya muestran que **los casos que el médico confirma se guardan (sin identificadores) en una memoria vectorial y que el modelo los usa como ejemplos**:

- `arquitectura-hab`: nodo «Memoria de casos» dentro del PC propio, conectado al servicio ICF («guarda y recupera casos»); Caddy pasa de 3 a 4 rutas (`/suggest · /cases`).
- `servicio-icf`: el backend envía `POST /cases` a la memoria; el embedding busca casos parecidos y la memoria aporta «ejemplos» a la selección.
- `recorrido-medico-icf`: tras la decisión, `POST /cases` y el guardado en la memoria; la decisión incluye confirmar la gravedad y la justificación.

**Regenerados el 14-nov-2026** con Archify 3.2.0 (el `finalize` de `showcase` pasó en los tres; `construir.mjs` ahora acepta las traducciones en `locales/es.json` de la 3.2 y en `examples/locales/es.json` de la 3.0). Las capturas de `docs/documentacion-final/fuente/ani/` (arquitectura, servicio ICF y recorrido del médico) se volvieron a tomar y están en el Word v1.1. **Quedan sin regenerar** los videos `video/*.webm` de esas tres animaciones (se exportan desde el visor con **Exportar**).

## Datos y privacidad

Los diagramas no contienen datos de pacientes; las rutas, los textos y las cifras salen de este repositorio (`BACKLOG.md`, `docs/manuals/MANUAL_ICF.md`, `docs/diagrams/rag-icf-postgresql.md`).
