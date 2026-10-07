# Servicio ICF en producción: PC propio con Windows (HU-07h)

Producción corre en el PC propio (Intel i5-13450HX, 32 GB de RAM, NVIDIA RTX 5050 de 8 GB). **No se compra hardware.**

```
Render (backend) ──HTTPS + token──▶ Tailscale Funnel ──▶ Caddy (127.0.0.1:11435)
                                                          ├─ /suggest, /health ─▶ servicio ICF (contenedor, sin puerto publicado)
                                                          └─ /api/tags ─────────▶ Ollama en Windows (GPU, 127.0.0.1:11434)
servicio ICF ──▶ PostgreSQL + pgvector (contenedor, solo 127.0.0.1:5433) y Ollama (embeddings y gemma4:e4b)
```

- **Ollama** corre instalado en Windows (usa la GPU). Modelos: `gemma4:e4b` (generación) y `bge-m3` (embeddings).
- **Docker Desktop** corre la base, el servicio ICF y Caddy (`restart: unless-stopped`).
- **Caddy** exige el token Bearer en todas las rutas y solo deja pasar `/suggest`, `/health` y `/api/tags`; el resto responde 404 (por ejemplo, `/api/generate` de Ollama no se expone).
- **Tailscale Funnel** publica solo el puerto 11435.
- **Los secretos** (token y clave de la base) viven en `%USERPROFILE%\.hab-icf\.env`, **fuera del repositorio y de OneDrive**.
- **Nada de pacientes se guarda en este PC.** La base solo tiene el catálogo CIF-IA y sus embeddings (se reconstruyen, ver abajo). Las sugerencias y las decisiones del médico se guardan en la base del backend en Render.

## Mediciones (07-oct-2026, RTX 5050 de 8 GB)

| Situación | Tiempo por sugerencia |
|---|---|
| Modelo en memoria (uso normal) | ~2,6 s |
| Primer pedido tras 30 min sin uso (carga del modelo) | ~18 s |
| 3 médicos a la vez | 2,7 a 7,2 s |
| 5 médicos a la vez | 2,7 a 11,6 s |

El backend espera hasta 90 s (`ICF_SUGGEST_TIMEOUT_S`). Si el servicio no responde, la pantalla avisa y el resto de la aplicación sigue funcionando.

## Primera instalación (ya hecha el 07-oct-2026)

Requisitos: Docker Desktop, Ollama con los dos modelos (`ollama pull gemma4:e4b`, `ollama pull bge-m3`) y Tailscale con la sesión iniciada.

```powershell
cd icf-service\deploy\windows
.\init-env.ps1                                   # crea %USERPROFILE%\.hab-icf\.env (token y clave aleatorios, no se muestran)
docker compose --env-file "$env:USERPROFILE\.hab-icf\.env" up -d --build
& "C:\Program Files\Tailscale\tailscale.exe" funnel --bg 11435
.\check.ps1 -Public -Suggest                     # debe terminar en "Todo correcto."
```

## Operación diaria

| Qué | Comando |
|---|---|
| Comprobar todo (local) | `.\check.ps1` |
| Comprobar también la vía pública y una sugerencia | `.\check.ps1 -Public -Suggest` |
| Ver el estado de los contenedores | `docker ps` |
| Ver los registros del servicio | `docker logs icf-service --tail 50` |
| Reiniciar el servicio | `docker compose --env-file "$env:USERPROFILE\.hab-icf\.env" restart icf-service` |
| Ver el túnel | `tailscale funnel status` |
| Apagar el túnel (corta el acceso desde Render) | `tailscale funnel --https=443 off` |
| Volver a encenderlo | `tailscale funnel --bg 11435` |

La URL pública es la del nodo en Tailscale (`tailscale status --json`, campo `Self.DNSName`), sin barra final. Esa URL va en Render como `ICF_LLM_URL`.

## Después de reiniciar el PC

Todo vuelve solo cuando **inicia sesión el usuario de Windows**: Ollama y Docker Desktop arrancan con la sesión, los contenedores se reinician solos y el túnel persiste. Si nadie inicia sesión, el servicio no está disponible y el backend usa el respaldo por similitud. Después de reiniciar, ejecuta `.\check.ps1 -Public` para confirmar.

## Energía

Con corriente alterna, la suspensión y la hibernación están en «nunca» (configurado el 07-oct-2026). Con batería, el equipo se suspende a los 10 minutos: **mantén el cargador conectado**. Revisa también en *Panel de control → Opciones de energía → Elegir el comportamiento del cierre de la tapa* que, «con corriente», diga «No hacer nada»; en este equipo no se pudo comprobar desde la línea de comandos. Con la tapa cerrada el equipo necesita ventilación.

Para volver a los valores originales: `powercfg /change standby-timeout-ac 30` y `powercfg /change hibernate-timeout-ac 180`.

## Rotar el token

1. `.\init-env.ps1 -Rotar` (genera token y clave nuevos; **no** cambia la clave que ya tiene la base).
2. Si rotas la clave de la base, primero cámbiala dentro de la base: `"ALTER USER icf_user PASSWORD '<nueva>';" | docker exec -i icf-db psql -U icf_user -d icf`.
3. `docker compose --env-file "$env:USERPROFILE\.hab-icf\.env" up -d`.
4. Actualiza `ICF_LLM_TOKEN` en Render (los tres ambientes) con el valor nuevo y reinicia cada servicio.
5. `.\check.ps1 -Public`.

El token nunca se pega en chats, issues ni commits. Si se expone, se rota de inmediato.

## Reconstruir la base (catálogo y embeddings)

El catálogo CIF-IA está en `data\private\icf\catalog_cifia.tsv` (derechos de la OMS, no se publica). Con los contenedores arriba:

```powershell
$envFile = "$env:USERPROFILE\.hab-icf\.env"
$pw = ((Get-Content $envFile | Where-Object { $_ -like "ICF_DB_PASSWORD=*" }) -split "=",2)[1]
cd <raiz del repositorio>
docker run --rm --network hab-icf_default `
  -e "ICF_DATABASE_URL=postgresql://icf_user:$pw@icf-db:5432/icf" -e OLLAMA_URL=http://host.docker.internal:11434 `
  -v "${PWD}:/work" -w /work/icf-service icf-service python scripts/load_catalog.py
# repetir con scripts/embed_catalog.py (unos minutos; se puede reanudar)
```

## Riesgos y límites

- Es un equipo personal: puede apagarse, suspenderse o perder internet. Mitigación: respaldo por similitud en el backend, arranque automático y esta guía.
- No hay redundancia. Una sola máquina atiende a uno o pocos médicos a la vez.
- Licencias de Gemma y MedGemma por verificar antes de uso clínico real.
- Con datos reales, las notas libres pueden contener datos identificables: la pantalla lo advierte y el servicio no los guarda.
