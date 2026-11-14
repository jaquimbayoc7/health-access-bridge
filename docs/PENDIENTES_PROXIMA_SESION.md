# Estado final del proyecto y recomendaciones abiertas

**Corte:** 28 de octubre de 2026 · **proyecto cerrado: 146 de 146 pts (100 %)**; HU-01 a HU-13 completas. `develop`, `staging` y `master` quedaron al día por los PR #83 a #90 que hizo el responsable (producción, QA y DEV con el dashboard de análisis); solo falta promover lo posterior (corrección de fechas, nueva presentación, README y diagramas).
**Uso:** abrir este archivo al empezar la sesión siguiente y seguir en orden. Complementa [`BACKLOG.md`](../BACKLOG.md) (fuente de verdad del alcance) y [`reports/PROJECT_STATUS_M3.md`](reports/PROJECT_STATUS_M3.md).

---

## 1. Dónde estamos

| Dato | Valor |
|---|---|
| Avance del proyecto | **146 de 146 pts (100 %)** · Momentos 1, 2 y 3 al 100 % · proyecto cerrado el 28-oct-2026 |
| HU-07 (Perfil Funcional ICF) | **33 de 33 pts ✅**: 07a a 07h hechas. **07g cerrada el 26-oct** (3 pts acreditados por el responsable): tres rondas con la médica; con 24 casos nuevos cumplen precisión estricta 62,7 %, flexible 86,3 %, cobertura 69,0 % y actividades 100 %; el calificador (κ 0,312) no: NO CUMPLE por un criterio. Borrador de apoyo, sin uso clínico |
| Recomendado (no bloquea) | Calificador con rango 0–4, apagar `ICF_MENTAL_LINK` (6 de 7 estructuras rechazadas en la ronda 3) y una cuarta ronda con casos nuevos. **Descartada** la segunda revisora (27-oct, por tiempo) |
| Decisiones de alcance del 27-oct-2026 (por tiempo) | **No se harán:** segunda revisora clínica, revisión de accesibilidad con lector de pantalla y exigir lint y tipos en el CI. Quedan documentadas como limitaciones en los manuales, el reporte de HU-09 y el Insights Report 6 |
| HU-08 (Dashboard y exportación) | **13 pts ✅ completada el 26-oct** (adelantada): dashboard con 10 gráficos y filtros, exportación a Excel y PDF, backend `/analytics/*`; verificada en DEV (CI verde, E2E 5/5 contra el frontend DEV) |
| HU-09 (Pruebas y feedback) | **8 pts ✅ completada el 27-oct**: UAT 18/18 y accesibilidad WCAG 2.2 AA con 0 violaciones en DEV, sesión de 10 usuarios (SUS medio 81,25) y guía de calificadores ICF; ver `docs/reports/REPORTE_FINAL_PRUEBAS_HU09.md` |
| HU-10 (Despliegue final y manuales, 5 pts) | **✅ completada el 28-oct-2026**: despliegue verificado en los tres ambientes, tres manuales (`docs/manuals/`), documentación final en Word según la guía de la profesora (`docs/documentacion-final/`), Insights Report 6, diagramas C4 y Archify actualizados y limpieza de archivos de IA sin uso |
| Pruebas | backend 123 · frontend 61 · servicio ICF 101 (92 en CI, 9 locales) · E2E 20 (+18 de aceptación bajo demanda) · smoke 7 |
| Producción de la IA | PC propio (i5-13450HX, 32 GB, RTX 5050 de 8 GB): `gemma4:e4b`, ~2,6 s por sugerencia con el modelo en memoria; Tailscale Funnel + Caddy con token |
| Licencias | Verificadas: Gemma 4 Apache 2.0 (se usa); MedGemma no se usa (prohíbe uso clínico) → [`reports/LICENCIAS_COMPONENTES_ICF.md`](reports/LICENCIAS_COMPONENTES_ICF.md) |

---

## 2. Pendientes que dependen de usted

| # | Qué | Detalle |
|---|---|---|
| 1 | ~~Reunión con la revisora y cierre de HU-07g~~ **Hecho el 26-oct** | El responsable dejó las métricas como están y acreditó los 3 pts. Resultado, análisis y cierre: [`reports/PROTOCOLO_VALIDACION_CLINICA_HU07G.md`](reports/PROTOCOLO_VALIDACION_CLINICA_HU07G.md), secciones 8 a 14; reporte final: [`presentation/reporte-afinamiento-icf.html`](presentation/reporte-afinamiento-icf.html). |
| 1b | **Mejora HU-07i** (13-nov-2026): la gravedad de b y s la confirma el médico en la pantalla | Hecha en `develop` (código, pruebas, manuales y documentación final). Las capturas `img/09` a `img/11` de `docs/manuals/` y los PDF de los manuales **deben regenerarse con la aplicación desplegada**; el Word de la documentación final ya está actualizado en la v1.1 (al abrirlo, actualizar los campos para el Contenido). Al desplegar, las columnas nuevas de `icf_suggestions` se agregan solas al arrancar el backend. |
| 1c | **Mejora HU-07j** (13-nov-2026): memoria de casos y justificación editable | Capturas (`img/10`, `11`, `19`, `20`), manuales en PDF y Word v1.1 con la figura nueva ya actualizados el 13-nov-2026; el PDF del perfil se corrigió (la kappa y las flechas no se dibujaban). Hecha y **desplegada** en `develop`, `staging` y `master` (13-nov-2026, PR #107 a #110; los tres backends publican los campos nuevos). **Activada y verificada en el PC del servicio ICF el 13-nov-2026** (tras corregir que el `Dockerfile` no copiaba `sql/002_cases.sql`; `icf_case_codes` llegó a 7 filas con una prueba real). Para repetirla en otro equipo: reconstruir la imagen, aplicar el `Caddyfile` nuevo (expone `/cases`) y reiniciar; las tablas `icf_cases` e `icf_case_codes` se crean solas. Con `ICF_CASE_EXAMPLES=0` solo guarda; el efecto del uso como ejemplos se midió de forma exploratoria el 14-nov con los 46 casos de la profesional dejando un caso fuera (cobertura a ciegas de 0,661 a 0,746 con similitud ≥ 0,70; protocolo, sección 17) y falta confirmarlo con casos reales. |
| 1e | **Trabajos futuros (cierre del 14-nov-2026)** | (a) Confirmar con casos reales el umbral 0,70 de la memoria repitiendo `evaluate_memory.py` cuando haya casos suficientes. (b) Mejorar el κ del calificador de severidad alimentando el sistema con la historia clínica y casos reales confirmados por médicos y midiendo con `case_memory_report.py` (≥ 30 pares); se espera que estabilice el servicio, hipótesis aún no medida. |
| 1d | **Qué queda (14-nov-2026)** | (1) ~~Regenerar los diagramas de Archify~~ **hecho el 14-nov** (HTML y capturas del Word); quedan por exportar los videos `video/*.webm` de esas tres animaciones. (2) **Cargar casos reales validados** en la memoria y medir con `icf-service/scripts/case_memory_report.py` (≥ 30 pares) antes de usar la gravedad guardada para predecir. (3) Respaldo con `pg_dump` de `icf_cases` e `icf_case_codes` y borrar `casos.sql` de la carpeta del repositorio. (4) Promover lo posterior a `74cecd8` a `staging` y `master`. (5) Opcional: etiqueta `v1.0.0`. **Memoria (14-nov):** ya tiene los 46 casos de la médica; para que el umbral 0,70 y los ejemplos rijan en el PC del servicio hay que traer el código nuevo, reconstruir la imagen y reiniciar (`docker compose ... up -d --build`); el compose ya pasa `ICF_CASE_*` desde `%USERPROFILE%\.hab-icf\.env`. Los casos `medica-…` están respaldados en `%USERPROFILE%\.hab-icf\respaldos\casos-20261114.sql`. **Ya no se puede:** validar de nuevo con la médica ni probar modelos de 12 o 26 mil millones de parámetros (GPU de 8 GB). |
| 2 | ~~Promoción `develop` → `staging` → `master`~~ **Hecha el 13-nov-2026** | PR #107 a #110 (HU-07i y HU-07j incluidas); el CI de producción pasó y DEV, QA y producción publican los campos nuevos en `/openapi.json`. Los contadores de `docs/presentation/index.html` se actualizaron con `master` (330 commits, 27 días activos, 85 PR fusionados, 24 issues cerrados, 87 merges). Cualquier cambio posterior a `74cecd8` (por ejemplo este ajuste) vuelve a `develop` y requiere un PR nuevo. Queda por revisar a ojo que ReDoc (`docs/api/redoc-api.html`) cargue con el esquema nuevo. |
| 3 | Tablero de proyectos de GitHub | El token de `gh` no tiene el permiso `read:project`: **no se pudo actualizar el tablero**. Ejecutar `gh auth refresh -s read:project` (interactivo) y mover a Done HU-07g/#71 y HU-07/#7 (ambas ya están cerradas como issues desde el 26-oct), o hacerlo a mano en la web. |
| 4 | ~~Consulta regulatoria (INVIMA)~~ **Descartada** | Decisión del responsable (26-oct-2026): **no se realizará en este proyecto**. Consecuencia que se mantiene: la pantalla se presenta como **borrador de apoyo** y el uso clínico real no está aprobado. |
| 5 | ~~Catálogo de la OMS: permiso para mostrar títulos~~ **Descartado** | Decisión del responsable (26-oct-2026): **no se realizará en este proyecto**. Limitación aceptada: la aplicación muestra al médico el título de cada código; los reportes con títulos siguen sin publicarse (`data/private/`). |
| 6 | ~~Presentación en Kimi~~ **Retirada** | El brief para esa herramienta de IA se eliminó del repositorio el 28-oct-2026 (no se requiere para la operación); el dato de energía que contenía quedó en `docs/reports/PRUEBAS_HU07F_MODELOS_ABIERTOS.md`. |

## 3. Cierre de HU-07g (hecho el 26-oct-2026; se conserva como guía para una cuarta ronda)

1. Guardar la hoja llena en `data/private/icf/review/hoja_revision_llena.xlsx`.
2. Calcular métricas y veredicto (en Docker, ver comandos en la sección 6):
   `python scripts/review_sheet.py score <hoja_llena> --output informe_validacion.json`.
3. Copiar la Fase A a `reference/cases.json`: `... score <hoja_llena> --apply-expected` (queda `validated: true`). Desde ahí `evaluate.py` mide precisión real.
4. Documentar el resultado: nueva sección en `docs/reports/PROTOCOLO_VALIDACION_CLINICA_HU07G.md`, `BACKLOG.md`, `PROJECT_STATUS_M3.md`, issue #71 (cerrarlo), issue #7, presentación y `INSIGHTS_REPORT5.md` (o un Insights R6).
5. **Si CUMPLE:** acreditar los 3 pts; perfil usable como borrador de apoyo en un piloto con médicos.
   **Si NO CUMPLE:** revisar errores por componente; opciones: ajustar búsqueda o reglas, medir modelos de 12B a 31B (`gemma4:12b`, `26b`, `31b`; no se midieron), o limitar el alcance. No aprobar uso clínico.
6. ~~Segunda revisora~~ **Descartada por tiempo** (decisión del responsable, 27-oct-2026): hay una sola revisora y no se mide el acuerdo entre profesionales; es un límite aceptado y documentado.

---

## 4. Pendientes del proyecto (siguiente trabajo de desarrollo)

| Prioridad | Qué | Nota |
|---|---|---|
| ✅ Hecha | **HU-08** Dashboard de análisis y exportación (13 pts, issue #8) | Completada el 26-oct; falta promover a QA y producción. |
| Alta | **HU-09** Pruebas completas y feedback de usuarios (8 pts, Sprint 11, issue #9) | UAT con usuarios reales; aquí encajan los médicos y la validación de la guía de uso. |
| Alta | **HU-10** Despliegue final y manuales (5 pts, Sprint 12, issue #10) | Incluye el manual de operación del servicio ICF (ya existe `docs/manuals/MANUAL_ICF.md`). |
| Media | Deuda de lint heredada | 5 errores en `Login.test.tsx`, `command.tsx`, `textarea.tsx`, `useJWTExpiry.ts` y `api.ts` (no son de HU-07). Abrir un ticket. |
| Media | Release Plan R3 | Mantener `RELEASE_PLAN.md` al día (sus riesgos se actualizaron el 7-oct). |
| Media | Insights Report 6 | Al cerrar M3 o al promover a `master`. Hoy `INSIGHTS_REPORT5.md` tiene 3 adendas del 7-oct. |
| Baja | Cobertura de más categorías de discapacidad | HAB captura 2 de las 7 categorías; la sugerencia es más débil para visión, audición e intelectual. |
| Baja | Medición de energía de la CPU y del equipo completo | Solo se midió la GPU (ver brief, sección 7). |
| Baja | Mensajes de commit con BOM | `e885800` y `99fac83` salieron con una marca invisible al inicio; no se reescribe el historial. |

## 5. Cuidados recurrentes (para no repetir errores)

- **Cifras que se desactualizan solas:** la presentación tiene números fijos (commits, PRs, issues, lenguajes, puntos). Revisar `docs/presentation/index.html` en cada cierre; los commits se cuentan con `git rev-list --count origin/master` (la rama oficial; cada PR de promoción agrega merges).
- **Nunca** imprimir el token ni la clave de la base. Los secretos viven en `%USERPROFILE%\.hab-icf\.env` (fuera de OneDrive y de git).
- Los reportes con títulos del catálogo de la OMS **no se suben** a git (`data/private/` está ignorado).
- `render.yaml`: `ICF_LLM_TIMEOUT_S` figura en 20 s en los tres ambientes mientras el backend espera hasta 90 s para la sugerencia (`ICF_SUGGEST_TIMEOUT_S`); verificar si el valor de 20 s afecta `/icf/health`.
- Cada push a `develop` desde la cuenta propietaria **se salta la regla de pull request** (GitHub lo avisa). Es un hallazgo de proceso ya documentado; si el curso exige PR, abrir PRs desde ramas de trabajo.

## 6. Cómo retomar técnicamente

| Qué | Cómo (Windows + PowerShell; no hay Python ni Node instalados) |
|---|---|
| Git | `C:\Users\jaqui\AppData\Local\GitHubDesktop\app-3.6.6\resources\app\git\cmd\git.exe`; para `gh` agregar esa carpeta al `PATH` de la sesión |
| GitHub CLI | `C:\Program Files\GitHub CLI\gh.exe` (en PowerShell 5.1, usar `--jq` con `@tsv` y sin barras invertidas) |
| Commits | `git commit -F archivo` con el mensaje escrito **sin BOM** (`[IO.File]::WriteAllText(..., New-Object System.Text.UTF8Encoding($false))`) |
| Editar texto en lote | Scripts de Python dentro de Docker (`python:3.12-slim`) montando el repo en `/repo`; los archivos pueden ser CRLF |
| Tests del backend | Docker (imagen `hab-backend-test`) · frontend: `node:20-slim` con `npm run test` · servicio ICF: `python:3.11-slim` con `pip install -r requirements.txt -r requirements-review.txt && pytest` |
| E2E | `mcr.microsoft.com/playwright:v1.63.0-noble` con `PLAYWRIGHT_BASE_URL=https://hab-frontend-dev.onrender.com` |
| Servicio ICF local | `icf-service\deploy\windows\check.ps1 -Public -Suggest` (debe terminar en «Todo correcto.»); red de Docker `hab-icf_default` |
| Hoja de revisión | `docker run ... python scripts/review_sheet.py generate|score` (ver docstring del script) |
| El sandbox bloquea | `Remove-Item` sobre rutas temporales y comandos que contienen cadenas como `/<script>` o `/patients/`; escribir esos scripts con la herramienta de archivos |

## 7. Mapa de documentos

| Tema | Archivo |
|---|---|
| Alcance, HUs, estados | `BACKLOG.md` |
| Plan de releases y riesgos | `docs/reports/RELEASE_PLAN.md` |
| Estado del Momento 3 | `docs/reports/PROJECT_STATUS_M3.md` |
| Reportes de insights (R1 a R5, con 3 adendas del 7-oct en R5) | `docs/reports/INSIGHTS_REPORT*.md` |
| Pruebas y casos | `docs/reports/TESTING_REPORT.md`, `docs/reports/TEST_CASES.md` |
| Pruebas de modelos | `docs/reports/PRUEBAS_HU07_SERVIDOR_FISICO.md`, `docs/reports/PRUEBAS_HU07F_MODELOS_ABIERTOS.md` |
| Validación clínica y licencias | `docs/reports/PROTOCOLO_VALIDACION_CLINICA_HU07G.md`, `docs/reports/LICENCIAS_COMPONENTES_ICF.md` |
| Operación del servicio ICF | `docs/manuals/MANUAL_ICF.md`, `icf-service/deploy/windows/README.md` |
| Diseño del RAG | `docs/diagrams/rag-icf-postgresql.md` |
| Presentación | `docs/presentation/index.html` (publicada desde `master`) |
| Animaciones (Archify): arquitectura, recorridos del médico y del administrador, y validación clínica con la médica | `docs/presentation/animaciones/` (ver su `README.md` para regenerarlas) |
