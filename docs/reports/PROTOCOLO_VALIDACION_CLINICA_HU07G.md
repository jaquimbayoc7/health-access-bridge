# Protocolo de validación clínica del Perfil Funcional ICF (HU-07g)

**Fecha:** 7 de octubre de 2026
**Estado:** instrumento listo y **umbrales aprobados por el responsable el 7 de octubre de 2026**; **pendiente la revisión de la profesional de salud** (Emilly Maria Celis), con quien se reúne la próxima semana (fecha por definir).
**Para quién:** la revisora y el responsable del proyecto.

## 1. Qué se mide y por qué

Hasta ahora las cifras de calidad del sistema (por ejemplo, `gemma4:e4b` con 43 % de precisión en funciones frente a 29 % de la búsqueda sola) se calcularon con **pistas orientativas que no validó ningún profesional**: sirven para comparar modelos, no para decir si los códigos son clínicamente adecuados. Esta validación mide eso: **si los códigos de la CIF-IA que sugiere el sistema son los que elegiría una profesional de la salud**, y si el calificador de gravedad es razonable.

El resultado no certifica a nadie. El Perfil Funcional ICF es un borrador de apoyo; el certificado lo emite el equipo multidisciplinario en el RLCPD (Resolución 1239 de 2022).

## 2. Material

| Pieza | Dónde |
|---|---|
| 24 casos sintéticos aplicables (el caso C10, menor de 6 años, no aplica) | `icf-service/reference/cases.json` |
| Hoja de revisión en Excel con la sugerencia actual del sistema (`gemma4:e4b`) | `data/private/icf/review/hoja_revision.xlsx` |
| Generador y calculadora de métricas | `icf-service/scripts/review_sheet.py`, `icf-service/icf/review.py` |
| Pruebas automáticas de la lógica y del Excel | `icf-service/tests/test_review.py` |

La hoja **no está en el repositorio**: trae títulos del catálogo CIF-IA, que tiene derechos de la OMS. Se entrega a la revisora por un canal privado y no se publica. Los casos son inventados: no hay datos de personas reales.

## 3. Guía para la revisora (unos 60 a 90 minutos)

1. **Fase A, a ciegas.** En la hoja «Fase A (a ciegas)», para cada caso lea los datos y escriba los códigos de **funciones (b)** y **estructuras (s)** que usted elegiría (máximo 3 por componente, separados por coma, por ejemplo `b730, b735`). No abra la hoja «Fase B» hasta terminar: ver la sugerencia antes sesgaría su criterio. Si el caso no tiene deficiencia en funciones o estructuras, déjelo vacío.
2. **Fase B, valorar la sugerencia.** En «Fase B (sugerencias)», para cada código elija en las columnas amarillas:
   - *Valoración:* **Adecuado** (lo habría elegido), **Aceptable** (razonable, pero no es el más preciso) o **No adecuado**.
   - *¿Calificador correcto?:* **Sí**, **Parcial** o **No** (la gravedad 0 a 4 asignada).
3. **Faltantes.** En la hoja «Faltantes», por caso, escriba los códigos que a su juicio faltan.
4. Guarde con otro nombre (por ejemplo `hoja_revision_llena.xlsx`) y devuélvala.

Qué tener en cuenta: el calificador sale de los niveles D1–D6 del paciente por capítulo (aproximación); en estructuras, naturaleza y localización quedan «sin especificar» (8) y no se evalúan; las actividades (d) salen de una lista cerrada del Anexo y se valoran aparte. El caso C19 (sin dificultad en ningún dominio) debe quedar **sin códigos**: si el sistema sugiere alguno, es un error.

## 4. Métricas y umbrales

| Métrica | Cómo se calcula | Umbral aprobado |
|---|---|---|
| Casos revisados | casos con al menos una valoración | ≥ 20 de 24 |
| Precisión estricta b+s | «Adecuado» / códigos b y s valorados | ≥ 60 % |
| Precisión flexible b+s | («Adecuado» + «Aceptable») / valorados | ≥ 80 % |
| Cobertura a ciegas b+s | de lo que la revisora eligió en la Fase A, cuánto estaba en la sugerencia | ≥ 60 % |
| Calificadores correctos b+s | Sí = 1, Parcial = 0,5, No = 0 | ≥ 80 % |
| Precisión flexible d | igual que b+s, solo actividades | ≥ 80 % |

Los códigos se comparan por su forma de 3 dígitos (`b730`); si la revisora escribe uno más específico (`b7301`), cuenta para `b730`.

**Umbrales aprobados por el responsable del proyecto el 7 de octubre de 2026.** Se presentan a la revisora en la reunión de la próxima semana; si ella plantea un ajuste clínico, se cambia en `THRESHOLDS` de `icf-service/icf/review.py` y se documenta aquí.

**Veredicto:** `CUMPLE` si se alcanzan todos los criterios; `NO CUMPLE` si alguno falla; `INCOMPLETO` si falta algún dato.

## 5. Qué se hace con el resultado

```powershell
# con la hoja llena, en un equipo con Python y openpyxl (o en un contenedor python:3.11-slim)
python scripts/review_sheet.py score ..\data\private\icf\review\hoja_revision_llena.xlsx --output informe_validacion.json
python scripts/review_sheet.py score hoja_revision_llena.xlsx --apply-expected   # copia la Fase A a reference/cases.json
```

- `--apply-expected` deja la elección a ciegas de la revisora como `expected` en `cases.json` y marca los casos como `validated`. A partir de ahí `evaluate.py` mide **precisión real** y se pueden comparar modelos con un criterio clínico.
- **Si CUMPLE:** el perfil se puede usar como borrador de apoyo en un piloto con médicos, con la leyenda de borrador que ya muestra la pantalla.
- **Si NO CUMPLE:** se revisan los errores por componente (la hoja trae los comentarios) y se decide entre ajustar la búsqueda o las reglas, probar un modelo mayor (de 12B a 31B, aún sin medir) o limitar el alcance (por ejemplo, solo actividades y funciones). No se aprueba el uso clínico.

## 6. Límites de esta validación

- **Una sola revisora**: no se mide el acuerdo entre profesionales. Con una segunda revisora sobre los mismos casos se podría medir.
- **24 casos sintéticos**: dan una idea de la calidad, no una garantía en pacientes reales. Los casos de audición, visión y discapacidad intelectual son pocos porque el sistema captura sobre todo discapacidad física y psicosocial.
- **Sesgo de anclaje**: por eso existe la Fase A a ciegas.
- **El caso C10 (menor de 6 años)** se omite: el sistema responde «no aplica» por diseño.
- Los umbrales los fijó el responsable del proyecto; no son una norma clínica y la revisora puede proponer ajustes.

## 7. Pendientes

1. Presentar los umbrales a la revisora en la reunión de la próxima semana (ya aprobados por el responsable).
2. Entregar `hoja_revision.xlsx` a la revisora por un canal privado.
3. Recibir la hoja llena, correr `score` y documentar el resultado en este archivo y en `BACKLOG.md`. Con eso se completa HU-07g.
