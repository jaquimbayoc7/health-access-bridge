# Documentación final del proyecto (Trabajo Integrador II y III)

Borrador **v0.5** de la documentación final que pide la guía de la docente Beatriz Eugenia Florián Gaviria, Ph.D. (asesora del proyecto: Deisy Chaves, Ph.D.) (10 secciones; los componentes obligatorios están marcados con [$] en la guía).

| Archivo | Contenido |
|---|---|
| `Documentacion_Final_HAB_borrador_v0.5.docx` | Documento en Word con formato ICONTEC (NTC 1486: carta, márgenes de 3, 3, 4 y 2 cm, Arial 12, interlineado 1,5, numeración arriba a la derecha) y citación y referencias en APA 7 |
| `fuente/c1.md` … `c5.md` | Texto de cada capítulo en Markdown con marcas propias (`[[T:..]]` tablas, `[[F:..]]` figuras, `[@clave]` citas) |
| `fuente/refs.js` | Referencias en APA 7; las marcadas con `bib: false` **no** vienen de `docs/reports/referencias_validacion_clinica.bib` y deben verificarse |
| `fuente/figs.py`, `figs2.py`, `fig/` | Generación de los diagramas BPMN y del modelo de datos, y de los gráficos (burndown, velocidad, validación clínica, SUS, pruebas) |
| `fuente/c4t/`, `fuente/ani/` | Capturas de los diagramas C4 (`docs/diagrams/`) y de los diagramas de Archify (`docs/presentation/animaciones/`) |
| `fuente/build.js` | Arma el Word con la librería `docx` (`npm install docx`; ajustar las rutas absolutas del encabezado del archivo) |

Al abrir el Word por primera vez, aceptar la actualización de campos para que se llene el **Contenido** con sus números de página.

Pendientes del autor antes de entregar: código estudiantil, ciudad de la portada, **recalcular con los datos originales la exactitud de la tríada del manuscrito (la sección 5.2.4 explica por qué el 92 % no es compatible con sus F1) y corregir en el manuscrito las variables del agrupamiento**, aprendizajes personales (sección 9.5, en borrador), y la revisión de los datos y de las referencias ajenas al `.bib`.

Las rutas a archivos del repositorio que aparecen en el documento son hipervínculos a la rama `master`: funcionan cuando esos archivos ya están promovidos a `master`.
