# Licencias de los componentes del Perfil Funcional ICF (HU-07)

**Fecha de verificación:** 7 de octubre de 2026 (fuentes oficiales abajo).
**Alcance:** lo que usa o usó el servicio ICF. No es asesoría legal: ver las recomendaciones al final.

## 1. Resumen

| Componente | Uso en el proyecto | Licencia | ¿Permite este uso? |
|---|---|---|---|
| **Gemma 4 (`gemma4:e4b`)** | Modelo de selección de códigos, **en producción** | **Apache 2.0** (desde Gemma 4, abril de 2026) | ✅ Sí, incluido el uso comercial; sin restricciones de uso especiales |
| **bge-m3** | Embeddings para la búsqueda, **en producción** | **MIT** | ✅ Sí |
| **Ollama** | Servidor del modelo, **en producción** | **MIT** | ✅ Sí |
| **PostgreSQL + pgvector** | Base del catálogo, **en producción** | Licencia PostgreSQL (tipo BSD/MIT) | ✅ Sí |
| **Caddy** | Proxy con token, **en producción** | Apache 2.0 | ✅ Sí |
| **MedGemma** (`medgemma:4b`) | Solo **medido** en HU-07f; **no se usa** | Términos de *Health AI Developer Foundations* (HAI-DEF) | ❌ **No para uso clínico**; descartado |
| **Qwen2.5 3B** (`qwen2.5:3b`) | Solo **medido** en HU-07b; **no se usa** | Qwen Research License (investigación y evaluación; el uso comercial requiere licencia aparte) | ❌ Descartado por calidad y por licencia |
| **Catálogo CIF-IA** (títulos y definiciones) | Datos de la búsqueda y de los títulos mostrados | Derechos de autor de la OMS | ⚠️ Uso interno; **no se publica** en el repositorio |
| **Tailscale Funnel** | Túnel público autenticado | Términos del servicio de Tailscale (el cliente es de código abierto) | ✅ Uso actual; revisar límites del plan si crece |

## 2. Detalle y conclusiones

### Gemma 4: resuelto

Google publicó Gemma 4 el 2 de abril de 2026 bajo **Apache License 2.0**, dejando atrás la licencia propia con restricciones de uso que tenían las versiones anteriores. La página de `gemma4:e4b` en Ollama y la página de licencia de Gemma 4 de Google confirman Apache 2.0. Apache 2.0 permite usar, modificar y distribuir, también con fines comerciales, conservando el aviso de licencia y los avisos de derechos.

**Conclusión:** el pendiente «verificar licencias de Gemma» queda **cerrado**: el modelo en producción se puede usar. Si se accede a Gemma por las APIs o Vertex de Google (no es el caso: corre local), aplicarían además los términos de esas plataformas.

### MedGemma: descartado para este uso

MedGemma se rige por los términos de *Health AI Developer Foundations*. Esos términos definen el **uso clínico** como «cualquier uso en el diagnóstico o tratamiento de pacientes (incluso como parte de un estudio de investigación)», lo prohíben salvo que se cumpla la normativa y obligan a quien lo despliega a buscar la autorización regulatoria correspondiente. Google lo describe como punto de partida que requiere validación y adaptación, no listo para decisiones clínicas.

**Conclusión:** MedGemma **no se usa en producción** (ya se había descartado por calidad: `gemma4:e4b` fue mejor en las pruebas) y **no se debe usar** mientras el perfil acompañe un proceso clínico. Queda solo como referencia en los informes.

### Qwen2.5 3B: descartado

Se midió en HU-07b y se descartó por calidad. Además su licencia (Qwen Research) no permite el uso comercial sin un acuerdo, así que tampoco habría sido adecuado para producción.

### Catálogo CIF-IA

Los títulos y definiciones tienen derechos de autor de la OMS. El proyecto los usa internamente para buscar y mostrar al médico el título de cada código, y **no los publica**: viven en `data/private/` (ignorado por git) y los reportes con títulos (como la hoja de revisión clínica) se comparten solo por canales privados. Falta confirmar con la entidad que corresponda si la visualización de los títulos a los médicos dentro de la aplicación requiere permiso explícito para un despliegue real.

## 3. Recomendaciones

1. **Conservar los avisos de licencia:** Apache 2.0 y MIT piden mantener el texto de la licencia y los avisos al redistribuir. El proyecto no redistribuye los modelos (se descargan con Ollama), por lo que basta con documentarlos aquí.
2. **Marco regulatorio colombiano:** una licencia permisiva del modelo no equivale a autorización regulatoria. Si el perfil llegara a usarse como parte de un proceso clínico real, consulte al INVIMA si el software puede considerarse **dispositivo médico** (software como dispositivo médico) y a un asesor jurídico. Mientras tanto la pantalla lo presenta como **borrador de apoyo** y la decisión es siempre del profesional.
3. **Datos personales:** Ley 1581 de 2012. El modelo corre en infraestructura propia y no se envían nombre, documento ni orientación sexual (ver `docs/MANUAL_OPERACION_ICF.md`).
4. **Vigilar cambios:** si se cambia de modelo (`ICF_LLM_MODEL`), repetir esta verificación antes de usarlo.

## 4. Fuentes consultadas (7 de octubre de 2026)

- Licencia de Gemma 4 (Google): <https://ai.google.dev/gemma/docs/gemma_4_license> — Apache License 2.0.
- Modelo `gemma4:e4b` en Ollama: <https://ollama.com/library/gemma4:e4b> — Apache License 2.0.
- Anuncio de Gemma 4 con Apache 2.0: <https://tech.slashdot.org/story/26/04/02/1735238/google-announces-gemma-4-open-ai-models-switches-to-apache-20-license>
- Términos de Health AI Developer Foundations (MedGemma): <https://developers.google.com/health-ai-developer-foundations/terms> (última modificación 15-nov-2024).
- MedGemma, términos de uso: <https://developers.google.com/health-ai-developer-foundations/medgemma>
- bge-m3 (MIT) en Ollama: <https://ollama.com/library/bge-m3:567m>
- Qwen2.5-3B (Qwen Research License): <https://en.immers.cloud/ai/Qwen/qwen2.5-3b-instruct>, resumen de terceros; la licencia original está en la tarjeta del modelo de Alibaba Cloud.
- Ollama (MIT): <https://github.com/ollama/ollama>; Caddy (Apache 2.0): <https://github.com/caddyserver/caddy>; pgvector (licencia PostgreSQL): <https://github.com/pgvector/pgvector/blob/master/LICENSE>.

**Nota de confianza:** las licencias de Gemma 4, Ollama, Caddy, pgvector y los términos de HAI-DEF se verificaron en la fuente oficial. La de bge-m3 y la de Qwen2.5 3B se tomaron de páginas de terceros y de la ficha del modelo; como ninguna se usa para algo que dependa de esa licencia (bge-m3 es MIT, permisiva; Qwen está descartado), el riesgo es bajo, pero conviene leer la licencia original si alguna vez se vuelve a considerar Qwen.
