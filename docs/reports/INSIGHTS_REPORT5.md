# GitHub Insights Report 5 — Health Access Bridge
> **Fuente:** GitHub API · `jaquimbayoc7/health-access-bridge` · `git log` · mediciones en el servidor físico
> **Período analizado:** 26 Feb 2026 – 6 Oct 2026 (acumulado total del proyecto)
> **Δ Desde último reporte:** 23 Sep 2026 – 6 Oct 2026 (inicio del Momento 3: HU-07a y HU-07b, y el episodio del modelo local Qwen)
> **Generado:** 6 Oct 2026

Este reporte tiene un tema central: **lo que pasó con el modelo local `qwen2.5:3b`** y cómo cambió la arquitectura de HU-07. Los datos técnicos completos (entorno, tablas, método) están en [`PRUEBAS_HU07_SERVIDOR_FISICO.md`](./PRUEBAS_HU07_SERVIDOR_FISICO.md); aquí se resumen los **hallazgos y lo aprendido**.

---

## 1. Resumen del Repositorio

| Campo | Valor | Δ vs. Reporte 4 (23 Sep) |
|-------|-------|--------------------------|
| **Repositorio** | [jaquimbayoc7/health-access-bridge](https://github.com/jaquimbayoc7/health-access-bridge) | — |
| **Visibilidad** | Público | — |
| **Lenguaje principal** | TypeScript | — |
| **Tamaño total** | 8,140 KB | +381 KB |
| **Último push** | 6 Oct 2026 | +13 días |
| **Issues (sin PRs)** | 16 (5 abiertas, 11 cerradas) | sin cambio |
| **Pull Requests** | 43 (42 mergeados) | +40 |
| **Issues + PRs numerados** | 59 | +40 |
| **Ramas activas** | `master`, `develop`, `staging` | = (las tres ramas extra creadas durante la sesión se eliminaron el 5-oct) |
| **Entornos** | QA y PROD: backend y frontend responden 200 | = |

---

## 2. Distribución de Lenguajes

| Lenguaje | Bytes | % del total | Δ vs. R4 |
|----------|-------|------------|----------|
| **TypeScript** | 339,228 | **63.1 %** | −16.3 pp |
| **Python** | 185,575 | **34.5 %** | +16.8 pp |
| JavaScript | 4,555 | 0.8 % | = |
| CSS | 3,652 | 0.7 % | = |
| Shell | 2,550 | 0.5 % | = |
| HTML | 1,148 | 0.2 % | = |
| Dockerfile | 739 | 0.1 % | +319 bytes |
| Procfile | 54 | < 0.1 % | = |
| **Total** | **537,501** | 100 % | +112,951 bytes |

> **Insight:** Python pasó de 75 KB a 186 KB en dos semanas. Casi todo es el nuevo `icf-service/` (33 archivos, ~2.400 líneas de Python con sus pruebas y scripts de medición). El proyecto dejó de ser «un frontend con una API»: ahora tiene un segundo servicio con su propia base de datos, scripts de evaluación y suite de pruebas.

---

## 3. Actividad de Commits

### 3.1 Totales y velocidad

| Métrica | Reporte 4 (23 Sep) | Reporte 5 (6 Oct) | Δ |
|---------|-------------------|-------------------|---|
| **Total de commits (`master`)** | 146 | 221 | +75 |
| **Días activos** | 18 | 21 | +3 |
| **Período total** | 209 días | 222 días | +13 días |
| **Velocidad global** | 0.70 commits/día | 0.99 commits/día | +0.29 |
| **Velocidad en el período Δ** | — | **5.0 commits por día calendario** (65 commits en 13 días, todos concentrados el 5 y 6 de octubre) | ✨ |

*Nota de conteo:* el +75 incluye 10 commits del 23 de septiembre posteriores al conteo del Reporte 4; los otros 65 son del 5 y el 6 de octubre.

### 3.2 Distribución total por tipo (Conventional Commits)

| Tipo | # Commits | % | Δ vs. R4 |
|------|-----------|---|-----------|
| `fix:` | 58 | 26.2 % | +7 |
| `docs:` | 56 | 25.3 % | +14 |
| `feat:` | 45 | 20.4 % | +8 |
| Otros (merges y sin prefijo) | 44 | 19.9 % | +39 |
| `chore:` | 10 | 4.5 % | = |
| `ci:` | 5 | 2.3 % | +4 |
| `perf:` | 2 | 0.9 % | ✨ nuevo tipo |
| `test:` | 1 | 0.5 % | ✨ nuevo tipo |
| **Total** | **221** | 100 % | +75 |

> **Insight:** los +39 de «otros» son casi todos **commits de merge** de PR. Es decir, más de la mitad de la actividad del período (39 de 65) fue **mover cambios entre ramas**, no escribir código nuevo. Ver §8.

### 3.3 Timeline de actividad — Δ desde Reporte 4

| Fecha | # Commits | Actividad principal |
|-------|-----------|---------------------|
| **5 Oct 2026** | 35 | Migración de los workflows a Ubuntu 26, `workflow_dispatch`, rediseño del despliegue a Render (y su corrección), revisión del Anexo 1239 y de la CIF-IA, extracción del catálogo de 1.593 códigos por OCR, diagrama y apartado «Códigos CIF» de la presentación |
| **6 Oct 2026** | 30 | HU-07a (servidor, túnel, catálogo, embeddings), HU-07b (motor, evaluación, pruebas con Qwen), decisión de pasar a un modelo externo, y actualización de documentos |

---

## 4. Estado de Issues y Backlog

| Estado | R4 (23 Sep) | R5 (6 Oct) | Δ |
|--------|-------------|------------|---|
| Issues abiertas (sin PRs) | 5 | **5** | = |
| Issues cerradas (sin PRs) | 11 | **11** | = |
| PRs mergeados | 3 | **42** | +39 |

| Milestone | Cerradas | Abiertas | Estado en GitHub | Estado real |
|-----------|----------|----------|------------------|-------------|
| Momento 1 | 7 | 0 | ✅ 100 % | ✅ 100 % |
| Momento 2 | 4 | 0 | ✅ 100 % | ✅ 100 % |
| Momento 3 | 0 | 5 | 🔴 0 % | 🟡 **13 de 57 pts (23 %)** |

> **Insight (brecha de seguimiento):** GitHub dice que el Momento 3 va en 0 %, pero HU-07a y HU-07b (13 pts) están completadas. La causa es que las sub-historias 07a–07g **viven solo en el `BACKLOG.md`, no como issues**; el milestone solo ve las 5 issues grandes. Además, el issue [#7](https://github.com/jaquimbayoc7/health-access-bridge/issues/7) todavía dice «LLM local» y 25 pts. Es la misma clase de desfase que los reportes anteriores corrigieron (R2 y R3).

---

## 5. Story Points y Velocity

```
R4 (23 Sep): ██████████████████████████░░░░  87 / 138 pts  (63.0 %)
R5 (6 Oct):  ████████████████████████████░░  100 / 144 pts (69.4 %)
```

El avance subió **+13 pts** (HU-07a 5 y HU-07b 8), y el alcance creció **+6 pts** (HU-07f y HU-07g, consecuencia directa de lo medido con Qwen). El proyecto tiene 44 pts pendientes.

---

## 6. El episodio del modelo local Qwen (5–6 Oct 2026)

### 6.1 Qué se hizo

Se montó el servidor físico (Intel i3, 12 GB, sin GPU) con Ollama (`qwen2.5:3b` para generar y `bge-m3` para embeddings), PostgreSQL con pgvector, un túnel (Tailscale Funnel + Caddy con token) y el catálogo CIF-IA de 1.593 códigos. Sobre eso se construyó el motor de sugerencia y un conjunto de herramientas de medición. Se evaluó con 25 casos sintéticos (21 con «pistas» orientativas no validadas por un médico).

### 6.2 Línea de tiempo de las mediciones

| Etapa | Latencia por sugerencia | Qué se descubrió |
|---|---|---|
| Prueba mínima del modelo | 4,1 s (8,8 s por Funnel) | La conexión Render → servidor funciona y está protegida |
| Motor v1 (el modelo ordena todo y justifica) | **55,6 s** | Leer el prompt costó 35 s y escribir 16 s; el JSON Schema no influía |
| Motor v2 (actividades sin modelo, prompt corto) | **22,9 s** | Menos tokens = menos espera, pero la calidad seguía floja |
| Modo calidad (12 candidatos con justificación) | 46 s | Más tiempo no mejoró la selección |
| Solo similitud (sin modelo de generación) | **0,6 s** | Seleccionó mejor que el modelo |

### 6.3 Hipótesis puestas a prueba

| Hipótesis | Resultado | Evidencia |
|---|---|---|
| El JSON Schema con lista cerrada frena la generación | ❌ Refutada | 15,3 s con esquema y 15,4 s con JSON simple |
| El tiempo se va escribiendo la respuesta | ⚠️ Parcial | Leer el prompt (35 s) pesó más que escribir (16 s) |
| Enviar dos veces el mismo prompt mide la velocidad real | ❌ Falsa | La caché de Ollama mostraba la lectura casi instantánea (92 ms) |
| Un modelo local de 3B elige mejor que la búsqueda por similitud | ❌ Refutada | Precisión en funciones: 29 % (similitud) contra 23 % (rápido) y 20 % (calidad) |
| Más candidatos y justificación del modelo mejoran la calidad | ❌ Refutada con Qwen | El modo calidad fue el peor de los tres |
| El cuello de botella de calidad es la búsqueda de candidatos | ✅ Confirmada | Buscar solo en códigos de 3 dígitos subió la cobertura de 11 % a 40 % en funciones y de 48 % a 86 % en estructuras |
| Pedirle al modelo que describa el diagnóstico antes de buscar ayuda | ❌ Refutada | Cobertura de 3 % en funciones; inventaba estructuras («glóbulos rojos» para esquizofrenia) |
| Enriquecer el texto de cada código con los títulos de sus hijos ayuda | ❌ Refutada | 33 % frente a 40 % sin enriquecer |

**8 hipótesis, 1 confirmada.** Casi todo lo que se esperaba de «afinar el modelo» resultó falso; lo que sí funcionó fue **mejorar qué se le ofrece a elegir**.

### 6.4 Defectos que solo aparecieron al leer salidas reales

| Defecto | Por qué no lo vieron las pruebas |
|---|---|
| El filtro por categoría se aplicaba después de buscar: el caso de esquizofrenia no devolvía funciones | Las pruebas con repositorio simulado no reproducían una lista de candidatos de otro capítulo |
| Códigos «otros especificados / no especificados» (`b798`, `s199`, `d298`) entre las sugerencias | Los títulos del catálogo están truncados por el OCR; el filtro por título dejaba pasar casos |
| Una ruta nueva en Caddy podía quedar sin pedir el token | Solo se detectó probando con Caddy real, no leyendo la configuración |

### 6.5 Lo que se aprendió

1. **Medir antes de optimizar.** La primera medición real (55 s) contradijo la estimación (~25 s). La causa estaba en un dato que no se había medido: la velocidad de lectura de prompts nuevos en ese equipo.
2. **Las métricas pueden mentir sin avisar.** El script de diagnóstico mostraba una lectura de prompt de 92 ms; era un artefacto de la caché. Se corrigió para separar «prompt nuevo» de «prompt en caché».
3. **Un modelo pequeño no compensa una mala lista de opciones.** El modelo solo elige lo que la búsqueda le da; la calidad se decidió en la búsqueda, no en la generación.
4. **No se debe presentar como precisión lo que no lo es.** Las pistas las puso el desarrollador, no un médico: sirven para comparar variantes, y así se documentó. La confiabilidad clínica solo la mide la revisión médica (HU-07g).
5. **Descartar rápido fue barato.** Dos días de trabajo bastaron para saber que el modelo local no servía, antes de construir backend y pantalla sobre él.
6. **El diseño modular permitió el giro.** El servicio ya aislaba el proveedor del modelo, así que pasar a un modelo externo no obliga a rehacer el motor, y la similitud quedó como respaldo.

### 6.6 Decisión resultante

El modelo de selección pasa a ser **externo (Claude Sonnet 5.5)**; el catálogo, los embeddings, la búsqueda y las reglas siguen en el servidor propio. Esto **reemplaza la decisión del Reporte 4 §6.4** («Ollama sobre servidor propio y modelo open-weight gratuito»), que se tomó antes de medir. Consecuencia nueva y abierta: con un modelo externo, los datos clínicos salen de la infraestructura propia, lo que exige revisión legal o ética (Ley 1581 de 2012) antes de usarlo con pacientes reales.

---

## 7. Cobertura de Pruebas

| Capa | R4 (23 Sep) | R5 (6 Oct) | Δ |
|------|------------|-----------|---|
| Backend (pytest) | 44 tests | **52 tests** | +8 (diagnóstico `/icf/health`) |
| Frontend (Vitest + RTL) | 16 tests | 16 tests | = |
| **Servicio ICF (pytest)** | — | **68 tests** (65 sin base de datos + 3 de integración con PostgreSQL real) | ✨ nuevo |
| E2E (Playwright) | 7 specs | 7 specs | = |
| Smoke (CI/CD) | 2 | 7 pasos (4 en QA, 3 en producción) | +5 (el R4 contó 2) |
| **Total (backend + frontend + servicio ICF)** | 60 | **136** | +76 |

**Brecha:** las 68 pruebas del servicio ICF **no corren en el pipeline de CI** (hoy se ejecutan en local o en un contenedor); solo las de backend y frontend están integradas. Las pruebas del servicio ICF incluyen pruebas contra un PostgreSQL con pgvector real y contra un Ollama simulado. La configuración de Caddy con la ruta nueva se verificó además **de forma manual** con Caddy real (no es una prueba automática del repositorio). Las mediciones con el modelo real solo se pueden ejecutar en el servidor.

---

## 8. Proceso: lo que funcionó y lo que no

| Aspecto | Dato |
|---|---|
| PRs mergeados en el período | 39 (de 3 a 42 en total) |
| PRs solo el 6 de octubre | 16 (#44–#59), casi todos de **promoción** (`develop` → `staging` → `master`) |
| Commits directos a `develop` con bypass de la regla «solo por PR» | **16 pushes** (más 1 avance rápido a `staging`), informados al propietario en cada entrega pero **sin pedir confirmación antes de cada push** |
| Cambios que se saltaron `staging` | PRs #45, #46 y #47 fueron de `develop` directo a `master`; se corrigió el 6-oct dejando `staging` igual a `master` con un avance rápido |
| Un push con una prueba fallando | Commit `949748f` subió con una prueba roja por encadenar `commit` y `push` sin comprobar el resultado; se corrigió en minutos (`176f9e3`) |
| Ramas auxiliares | 3 ramas extra creadas durante la sesión y eliminadas a pedido del propietario |
| Incidente de seguridad contenido | Un token del túnel se pegó en una conversación y se rotó. Durante la configuración, Funnel quedó apuntando un tiempo directo a Ollama (sin autenticación): el síntoma fue que el token viejo seguía funcionando tras rotarlo. Se corrigió con `tailscale funnel reset` y volviendo a apuntar al proxy con token |

> **Insights de proceso:**
> 1. **La protección de rama dejó de proteger en la práctica.** Con un único desarrollador, el bypass del propietario permite saltarse la regla, y se usó 17 veces. No hay daño visible, pero la regla «solo por PR» ya no cumple lo que se buscó cuando se activó (R4 §8).
> 2. **Promover cuesta más que escribir.** Más de la mitad de los commits fueron merges, y 16 PRs en un día para mover cambios mayormente de documentación. Conviene **agrupar promociones** en lugar de promover cada cambio.
> 3. **El token expuesto se detectó por una prueba de comportamiento, no por una revisión.** La prueba «el token viejo todavía funciona» destapó que el túnel estaba abierto. Vale la pena dejar esa prueba (sin token, token falso, token correcto) como paso fijo al configurar cualquier túnel.

---

## 9. Resumen de Hallazgos

| # | Insight | Impacto | Δ vs. R4 |
|---|---------|---------|----------|
| 1 | **El modelo local Qwen no sirve como selector**: peor que la similitud sola y de 24 a 46 s por sugerencia | 🟡 Cambia la arquitectura de HU-07 | ✨ Nuevo |
| 2 | **La calidad se decide en la búsqueda de candidatos**, no en el modelo (11 % → 40 % de cobertura al buscar solo en códigos de 3 dígitos) | 🟢 Mejora real y barata | ✨ Nuevo |
| 3 | **HU-07 pasa a modelo externo (Claude Sonnet 5.5)**: reemplaza la decisión del R4 §6.4 | 🟡 Nueva dependencia externa y de costo | ✨ Nuevo |
| 4 | **Privacidad: los datos clínicos saldrían de la infraestructura propia** (Ley 1581 de 2012) | 🔴 Pendiente de decisión del responsable | ✨ Nuevo |
| 5 | **Servidor propio, túnel y catálogo operativos** (QA verificado: `/icf/health` en 943 ms) | 🟢 Positivo | ✨ Nuevo |
| 6 | **13 pts completados, +6 pts de alcance** (HU-07f y HU-07g); 100 / 144 pts (69,4 %) | 🟢 Positivo | ✨ Nuevo |
| 7 | **Confiabilidad clínica aún sin medir**: las cifras usan pistas no validadas por un médico | 🟡 Limitación documentada | ✨ Nuevo |
| 8 | **Brecha de seguimiento**: el milestone del M3 marca 0 % con 13 pts hechos; el issue #7 está desactualizado | 🟡 Desfase de GitHub | ✨ Nuevo |
| 9 | **Protección de rama eludida 17 veces** (bypass del propietario) y 16 PRs de promoción en un día | 🟡 Hallazgo de proceso | ✨ Nuevo |
| 10 | **Persiste el patrón de corrección retrospectiva**: este reporte corrige una decisión del R4 (modelo gratuito en servidor propio), tomada antes de medir | 🟡 Observación de proceso | = Patrón recurrente |

---

## 10. Comparativo R1 → R5

| Métrica | R1 (20 Mar) | R2 (16 Abr) | R3 (18 Sep) | R4 (23 Sep) | R5 (6 Oct) | Δ R4→R5 |
|---------|------------|------------|------------|------------|------------|---------|
| Total commits | 43 | 65 | 128 | 146 | 221 | +75 |
| Issues + PRs numerados | 13 | 16 | 16 | 19 | 59 | +40 |
| Story Points completados | 47 | 63 | 87 | 87 | 100 | +13 |
| Total del proyecto (pts) | — | — | 134 | 134 → 138 | 144 | +6 |
| Avance del proyecto | 40.9 % | 48.1 % | 64.9 % | 64.9 % | 69.4 % | +4.5 pp |
| Tests (backend + frontend + servicio ICF) | 32 | 53 | 60 | 60 | 136 | +76 |
| PRs mergeados (acumulado) | 0 | 0 | 0 | 3 | 42 | +39 |
| Tamaño repo (KB) | — | 4,521 | 7,617 | 7,759 | 8,140 | +381 |
| Servicios desplegables | 2 | 2 | 2 | 2 | 2 + servicio ICF en servidor propio | +1 |

*Nota:* el avance de R4 (64.9 %) se calculó sobre 134 pts; sobre el total actual de 144 sería 60,4 %. El total subió por la reestimación de HU-07 (21 → 25 → 31 pts), no por trabajo nuevo fuera de ella.

---

## 11. Recomendaciones

1. **Aprobar el plan de HU-07f a HU-07e** (modelo externo con comparación, validación clínica, backend, pantalla y cierre), con la decisión de privacidad y la clave de API como requisitos previos.
2. **Resolver la privacidad antes de usar datos reales:** revisión legal o ética, y hasta entonces el modelo externo solo con datos sintéticos.
3. **Medir con un médico.** Es lo único que convierte las cifras orientativas en confiabilidad clínica y permite fijar el umbral de uso (HU-07g).
4. **Crear las sub-historias 07a–07g como issues** y actualizar el issue #7, para que el milestone refleje el avance real.
5. **Decidir la política de la protección de rama:** o se restringe el bypass del propietario, o se acepta que con un solo desarrollador la regla es indicativa y se documenta así.
6. **Agrupar las promociones** `develop` → `staging` → `master` (por ejemplo, una por hito) en lugar de una por cambio.
7. **Integrar las pruebas del servicio ICF al pipeline de CI** (las que no necesitan base de datos corren sin servicios; las 3 de integración requieren un PostgreSQL con pgvector).
8. **Dejar como paso fijo** la prueba de túnel (sin token, token falso, token correcto) al configurar cualquier acceso externo.

---

*Datos extraídos de la API de GitHub (`gh api`), `git log` local y las mediciones ejecutadas en el servidor físico el 5 y 6 de octubre de 2026 (detalle en `PRUEBAS_HU07_SERVIDOR_FISICO.md`).*
