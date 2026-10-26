# Pendientes y punto de partida para la próxima sesión

**Corte:** 27 de octubre de 2026 · HU-07 está completa (33 de 33 pts). `develop` tiene todo el trabajo de HU-07g y el reporte de afinamiento; `staging` y `master` están atrás: falta promover (ver 2, punto 2).
**Uso:** abrir este archivo al empezar la sesión siguiente y seguir en orden. Complementa [`BACKLOG.md`](../BACKLOG.md) (fuente de verdad del alcance) y [`reports/PROJECT_STATUS_M3.md`](reports/PROJECT_STATUS_M3.md).

---

## 1. Dónde estamos

| Dato | Valor |
|---|---|
| Avance del proyecto | **133 de 146 pts (91,1 %)** · Momento 1 100 % · Momento 2 100 % · **Momento 3: 46 de 59 pts (78,0 %)** |
| HU-07 (Perfil Funcional ICF) | **33 de 33 pts ✅**: 07a a 07h hechas. **07g cerrada el 27-oct** (3 pts acreditados por el responsable): tres rondas con la médica; con 24 casos nuevos cumplen precisión estricta 62,7 %, flexible 86,3 %, cobertura 69,0 % y actividades 100 %; el calificador (κ 0,312) no: NO CUMPLE por un criterio. Borrador de apoyo, sin uso clínico |
| Recomendado (no bloquea) | Segunda revisora, calificador con rango 0–4, apagar `ICF_MENTAL_LINK` (6 de 7 estructuras rechazadas en la ronda 3) y una cuarta ronda con casos nuevos |
| HU-08 (Dashboard y exportación) | **13 pts ✅ completada el 27-oct** (adelantada): dashboard con 10 gráficos y filtros, exportación a Excel y PDF, backend `/analytics/*`; verificada en DEV (CI verde, E2E 5/5 contra el frontend DEV) |
| Aún sin empezar | HU-09 Pruebas completas y feedback (8 pts) y HU-10 Despliegue final y manuales (5 pts) = 13 pts |
| Pruebas | backend 123 · frontend 61 · servicio ICF 101 (92 en CI, 9 locales) · E2E 17 · smoke 7 |
| Producción de la IA | PC propio (i5-13450HX, 32 GB, RTX 5050 de 8 GB): `gemma4:e4b`, ~2,6 s por sugerencia con el modelo en memoria; Tailscale Funnel + Caddy con token |
| Licencias | Verificadas: Gemma 4 Apache 2.0 (se usa); MedGemma no se usa (prohíbe uso clínico) → [`reports/LICENCIAS_COMPONENTES_ICF.md`](reports/LICENCIAS_COMPONENTES_ICF.md) |

---

## 2. Pendientes que dependen de usted

| # | Qué | Detalle |
|---|---|---|
| 1 | ~~Reunión con la revisora y cierre de HU-07g~~ **Hecho el 27-oct** | El responsable dejó las métricas como están y acreditó los 3 pts. Resultado, análisis y cierre: [`reports/PROTOCOLO_VALIDACION_CLINICA_HU07G.md`](reports/PROTOCOLO_VALIDACION_CLINICA_HU07G.md), secciones 8 a 14; reporte final: [`presentation/reporte-afinamiento-icf.html`](presentation/reporte-afinamiento-icf.html). |
| 2 | **Promoción** `develop` → `staging` → `master` | `develop` está por delante: motor corregido (ICF_S_EVIDENCE, ICF_MOTOR_LINK, ICF_MENTAL_LINK), scripts de validación, casos nuevos, protocolo, presentación con la sección «Afinamiento de los códigos ICF» y el reporte final. Agrupar en un PR `develop` → `staging` y luego `staging` → `master`. **Tras promover, actualizar los contadores de commits de `docs/presentation/index.html`** (hoy figuran 249 en `master`, que ya tiene 260) y revisar que la página oficial muestre 120/146. |
| 3 | Tablero de proyectos de GitHub | El token de `gh` no tiene el permiso `read:project`: **no se pudo actualizar el tablero**. Ejecutar `gh auth refresh -s read:project` (interactivo) y mover a Done HU-07g/#71 y HU-07/#7 (ambas ya están cerradas como issues desde el 27-oct), o hacerlo a mano en la web. |
| 4 | ~~Consulta regulatoria (INVIMA)~~ **Descartada** | Decisión del responsable (27-oct-2026): **no se realizará en este proyecto**. Consecuencia que se mantiene: la pantalla se presenta como **borrador de apoyo** y el uso clínico real no está aprobado. |
| 5 | ~~Catálogo de la OMS: permiso para mostrar títulos~~ **Descartado** | Decisión del responsable (27-oct-2026): **no se realizará en este proyecto**. Limitación aceptada: la aplicación muestra al médico el título de cada código; los reportes con títulos siguen sin publicarse (`data/private/`). |
| 6 | Presentación en Kimi | Usar [`presentation/KIMI_BRIEF_M3.md`](presentation/KIMI_BRIEF_M3.md) y reunir las capturas que el brief lista en la sección 9. |

## 3. Cierre de HU-07g (hecho el 27-oct-2026; se conserva como guía para una cuarta ronda)

1. Guardar la hoja llena en `data/private/icf/review/hoja_revision_llena.xlsx`.
2. Calcular métricas y veredicto (en Docker, ver comandos en la sección 6):
   `python scripts/review_sheet.py score <hoja_llena> --output informe_validacion.json`.
3. Copiar la Fase A a `reference/cases.json`: `... score <hoja_llena> --apply-expected` (queda `validated: true`). Desde ahí `evaluate.py` mide precisión real.
4. Documentar el resultado: nueva sección en `docs/reports/PROTOCOLO_VALIDACION_CLINICA_HU07G.md`, `BACKLOG.md`, `PROJECT_STATUS_M3.md`, issue #71 (cerrarlo), issue #7, presentación y `INSIGHTS_REPORT5.md` (o un Insights R6).
5. **Si CUMPLE:** acreditar los 3 pts; perfil usable como borrador de apoyo en un piloto con médicos.
   **Si NO CUMPLE:** revisar errores por componente; opciones: ajustar búsqueda o reglas, medir modelos de 12B a 31B (`gemma4:12b`, `26b`, `31b`; no se midieron), o limitar el alcance. No aprobar uso clínico.
6. Considerar una **segunda revisora** (hoy es una sola; no se mide acuerdo entre profesionales).

---

## 4. Pendientes del proyecto (siguiente trabajo de desarrollo)

| Prioridad | Qué | Nota |
|---|---|---|
| ✅ Hecha | **HU-08** Dashboard de análisis y exportación (13 pts, issue #8) | Completada el 27-oct; falta promover a QA y producción. |
| Alta | **HU-09** Pruebas completas y feedback de usuarios (8 pts, Sprint 11, issue #9) | UAT con usuarios reales; aquí encajan los médicos y la validación de la guía de uso. |
| Alta | **HU-10** Despliegue final y manuales (5 pts, Sprint 12, issue #10) | Incluye el manual de operación del servicio ICF (ya existe `docs/MANUAL_OPERACION_ICF.md`). |
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
| Operación del servicio ICF | `docs/MANUAL_OPERACION_ICF.md`, `icf-service/deploy/windows/README.md` |
| Diseño del RAG | `docs/diagrams/rag-icf-postgresql.md` |
| Presentación | `docs/presentation/index.html` (publicada desde `master`), brief para Kimi: `docs/presentation/KIMI_BRIEF_M3.md` |
| Animaciones (Archify): arquitectura, recorridos del médico y del administrador, y validación clínica con la médica | `docs/presentation/animaciones/` (ver su `README.md` para regenerarlas) |
