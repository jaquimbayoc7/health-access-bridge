# Manual de operación del Perfil Funcional ICF (HU-07)

**Para quién:** quien administra el sistema (no necesita saber programar).
**Última actualización:** 7 de octubre de 2026.
**Complementa:** [`icf-service/deploy/windows/README.md`](../icf-service/deploy/windows/README.md) (comandos del PC de producción) y [`docs/diagrams/rag-icf-postgresql.md`](diagrams/rag-icf-postgresql.md) (diseño).

---

## 1. Cómo funciona, en una página

```
Médico (navegador) ─▶ Backend en Render ─HTTPS + token─▶ Túnel (Tailscale Funnel) ─▶ PC de producción
                                                                                      ├─ Servicio ICF (catálogo CIF-IA + reglas)
                                                                                      └─ Ollama: bge-m3 (búsqueda) + gemma4:e4b (selección)
```

- El médico pide el perfil desde la pantalla «Perfil Funcional ICF». El backend guarda el resultado (sugerencias y decisiones) en su propia base en Render.
- El PC de producción **no guarda datos de pacientes**: solo tiene el catálogo CIF-IA y sus embeddings, que se reconstruyen.
- Si el PC no responde, el backend usa la **búsqueda por similitud** como respaldo (menos precisa, 0,6 s) y el resto de la aplicación sigue funcionando. Si el servicio falla del todo, la pantalla muestra un aviso.
- Ningún dato clínico sale hacia servicios de terceros: el modelo corre en el PC propio.

## 2. Requisitos de la máquina

| Recurso | Mínimo medido | PC de producción |
|---|---|---|
| Modelo de generación | `gemma4:e4b` | `gemma4:e4b` |
| GPU | NVIDIA con 8 GB de memoria (~3 s por sugerencia) | RTX 5050 de 8 GB |
| Solo CPU (sin GPU) | funciona, ~15 s por sugerencia | no aplica |
| RAM | 16 GB | 32 GB |
| Software | Docker Desktop, Ollama, Tailscale | instalados |

Medido el 7-oct-2026: modelo en memoria ~2,6 s; primer pedido tras 30 min sin uso ~18 s; 3 médicos a la vez hasta 7,2 s; 5 a la vez hasta 11,6 s. Informe completo: [`PRUEBAS_HU07F_MODELOS_ABIERTOS.md`](reports/PRUEBAS_HU07F_MODELOS_ABIERTOS.md).

## 3. Ollama y los modelos

Ollama se instala en Windows (usa la GPU) y necesita dos modelos:

```powershell
ollama pull gemma4:e4b    # selección de códigos (generación)
ollama pull bge-m3        # embeddings para la búsqueda por significado
ollama list               # debe mostrar ambos
```

Cambiar de modelo no requiere tocar código: se cambia `ICF_LLM_MODEL` (en el PC y en Render). Gemma 4 razona antes de responder; por eso `ICF_LLM_THINK=false`.

## 4. Variables de configuración

| Dónde | Variable | Valor / uso |
|---|---|---|
| PC (`%USERPROFILE%\.hab-icf\.env`) | `ICF_LLM_MODEL` | `gemma4:e4b` |
| PC | `ICF_LLM_THINK` | `false` |
| PC | `ICF_LLM_NUM_GPU` | opcional; `0` fuerza CPU |
| PC | `ICF_DB_PASSWORD`, `ICF_TOKEN` | aleatorios, creados por `init-env.ps1`; **nunca** en chats ni en el repositorio |
| Render (los 3 ambientes) | `ICF_LLM_URL` | URL pública del túnel, sin barra final |
| Render | `ICF_LLM_TOKEN` | el mismo token del PC |
| Render | `ICF_LLM_MODEL` | `gemma4:e4b` |
| Render | `ICF_LLM_TIMEOUT_S`, `ICF_SUGGEST_TIMEOUT_S` | tiempos de espera (la sugerencia espera hasta 90 s) |

Después de cambiar una variable en Render hay que reiniciar el servicio.

## 5. Operación diaria

Todo corre solo cuando **inicia sesión el usuario de Windows** (Ollama, Docker Desktop y el túnel). Mantenga el cargador conectado: con corriente alterna la suspensión y la hibernación están en «nunca».

| Qué | Cómo |
|---|---|
| Comprobar que todo funciona | en `icf-service\deploy\windows`: `.\check.ps1 -Public -Suggest` (debe terminar en «Todo correcto.») |
| Ver desde Render | consultar `GET /icf/health` del backend con una sesión de administrador (responde si el modelo está disponible) |
| Reiniciar el servicio ICF | `docker compose --env-file "$env:USERPROFILE\.hab-icf\.env" restart icf-service` |
| Cortar el acceso desde Render | `tailscale funnel --https=443 off` |
| Volver a abrirlo | `tailscale funnel --bg 11435` |

Después de **reiniciar el PC**: iniciar sesión, esperar uno o dos minutos y ejecutar `.\check.ps1 -Public`.

## 6. Si algo falla

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| La pantalla dice que no se pudo generar el perfil | PC apagado, sin sesión, sin internet o túnel caído | Revisar que el PC esté encendido con la sesión iniciada; `.\check.ps1 -Public`; `tailscale funnel status` |
| Las sugerencias llegan con origen «Similitud» y no «Modelo» | Ollama o el modelo no responden y el sistema usó el respaldo | `ollama list`; reiniciar Ollama; `.\check.ps1 -Suggest` |
| El primer pedido tarda ~20 s | Modelo descargado de memoria tras 30 min sin uso | Normal; los siguientes tardan ~3 s |
| `/icf/health` da 401 | Token distinto entre Render y el PC | Igualar `ICF_LLM_TOKEN` con el del PC y reiniciar Render |
| `/icf/health` da 403 desde la URL pública de Ollama | Ollama rechaza `Host` no local | Ya resuelto en el `Caddyfile` (`header_up Host`); si reaparece, revisar que Caddy esté arriba |
| Muy lento o sin GPU | Otra aplicación usa la GPU, o el controlador falló | Cerrar aplicaciones pesadas; `nvidia-smi`; reiniciar Ollama |
| La base del servicio está vacía o dañada | Contenedor recreado sin volumen | Reconstruir el catálogo y los embeddings (sección «Reconstruir la base» del README del despliegue) |

## 7. Seguridad y privacidad

- Al servicio solo viajan edad, género, causa, categorías, niveles D1–D6, la predicción y, si el médico los escribe, el diagnóstico y las notas. **Nunca** el nombre, el documento ni la orientación sexual.
- Caddy exige el token en todas las rutas y solo deja pasar `/suggest`, `/health` y `/api/tags`.
- Rotación del token: ver «Rotar el token» en el README del despliegue. Si el token se expone, se rota de inmediato.
- Las notas libres pueden contener datos identificables si el médico los escribe: la pantalla lo advierte y el servicio no los guarda.
- Marco legal: Ley 1581 de 2012 (protección de datos personales). El perfil es un **borrador de apoyo**: la decisión es del profesional y el certificado oficial lo emite el equipo multidisciplinario en el RLCPD (Resolución 1239 de 2022).

## 8. Pruebas automáticas

| Qué | Dónde | Cómo correrlo |
|---|---|---|
| Servicio ICF (67 pasan, 8 se omiten en CI) | `icf-service/tests/` | `cd icf-service && pytest` (el CI lo corre en los 3 ambientes) |
| Backend de sugerencias | `backend/app/tests/` (`test_icf_*.py`) | `cd backend && pytest app/tests/` |
| Pantalla y guía (unitarias) | `frontend/src/__tests__/FunctionalProfile.test.tsx`, `IcfGuide.test.tsx` | `cd frontend && npm run test` |
| Hoja de revisión clínica (generar y calcular métricas) | `icf-service/scripts/review_sheet.py` | ver el protocolo de HU-07g |
| Pantalla de extremo a extremo (5 casos, servicio ICF simulado) | `frontend/e2e/functional-profile.spec.ts` | `cd frontend && npx playwright test e2e/functional-profile.spec.ts` (con `PLAYWRIGHT_BASE_URL`) |

Las 8 pruebas omitidas en el CI (integración con PostgreSQL + pgvector y casos de referencia) necesitan el catálogo CIF-IA, que tiene derechos de la OMS y no está en el repositorio. Se corren en el PC de producción o de pruebas con `ICF_TEST_DATABASE_URL`.

## 9. Pendientes conocidos

- **Validación clínica (HU-07g):** el instrumento está listo (`reports/PROTOCOLO_VALIDACION_CLINICA_HU07G.md`); hasta que la profesional de salud devuelva la hoja, las cifras de precisión son orientativas.
- **Licencias (verificadas el 07-oct-2026):** Gemma 4 es Apache 2.0 y se puede usar; MedGemma no se usa porque sus términos prohíben el uso clínico. Detalle en [`reports/LICENCIAS_COMPONENTES_ICF.md`](reports/LICENCIAS_COMPONENTES_ICF.md). Si se cambia `ICF_LLM_MODEL`, repetir la verificación.
- Es un equipo personal sin redundancia: si se apaga, el respaldo por similitud mantiene el servicio con menos precisión.
