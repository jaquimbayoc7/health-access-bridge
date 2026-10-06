# icf-service — servicio ICF en servidor propio para HU-07 (códigos CIF)

Componentes que corren en el servidor propio (Linux). El backend de Render solo lo alcanza por el túnel autenticado.

> **Estado y decisión (06-oct-2026).** Este servicio se construyó y se midió con un modelo de generación local (`qwen2.5:3b` en Ollama). Las pruebas en el servidor físico (i3, 12 GB, sin GPU) mostraron que ese modelo **no mejora la selección sobre la búsqueda por similitud sola y tarda de 24 a 46 s por sugerencia**, por lo que la selección pasa a un **modelo externo, Claude Sonnet 5.5, llamado desde este servicio (HU-07f, pendiente)**. El catálogo, los embeddings, la búsqueda, las reglas y el respaldo por similitud siguen en este servidor, y Ollama queda solo para los embeddings. Hoy el código implementa el proveedor local (`ollama`) y el modo `ICF_USE_LLM=false` (solo similitud, 0,6 s); el proveedor `anthropic` aún no existe. Resultados completos: [`docs/reports/PRUEBAS_HU07_SERVIDOR_FISICO.md`](../docs/reports/PRUEBAS_HU07_SERVIDOR_FISICO.md). **Privacidad:** con un modelo externo el diagnóstico y las notas salen de la infraestructura propia; hasta contar con revisión legal o ética, usarlo solo con datos sintéticos.

```
Render (backend HAB) ──HTTPS──► Tailscale Funnel ──► Caddy 127.0.0.1:11435 (exige Bearer) ──► Ollama 127.0.0.1:11434
                                                  PostgreSQL + pgvector 127.0.0.1:5433 (catálogo CIF-IA)
```

Diseño completo: [`docs/diagrams/rag-icf-postgresql.md`](../docs/diagrams/rag-icf-postgresql.md).

## Qué incluye HU-07a

| Pieza | Archivo |
|---|---|
| Base PostgreSQL + pgvector | `docker-compose.yml`, `sql/001_schema.sql` |
| Lectura y validación del catálogo CIF-IA | `icf/catalog.py` |
| Mapeo D1–D6 → capítulo CIF-IA → dominio oficial, calificador 0–4, candidatos del Anexo 1239 | `icf/domain_map.py` |
| Carga del catálogo y del mapeo | `scripts/load_catalog.py` |
| Embeddings con Ollama (bge-m3) | `scripts/embed_catalog.py` |
| Diagnóstico Render → servidor (`GET /icf/health`, solo admin) | `backend/app/routers/icf.py` |

## Catálogo (no está en el repositorio)

El catálogo CIF-IA tiene derechos de autor de la OMS. Vive solo en local, en `data/private/icf/catalog_cifia.tsv` (ruta ignorada por git). Cópialo al servidor por Tailscale:

```bash
scp data/private/icf/catalog_cifia.tsv usuario@IP-TAILSCALE:~/health-access-bridge/data/private/icf/
```

Faltan 3 códigos sin definición en el libro (b1125, b239, d341); están fuera del catálogo hasta resolverlos.

## Puesta en marcha en el servidor

```bash
cd icf-service
cp .env.example .env            # edita ICF_DB_PASSWORD y la misma clave dentro de ICF_DATABASE_URL
docker compose up -d
ollama pull bge-m3              # modelo de embeddings (qwen2.5:3b ya está instalado)

python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
export $(grep -v '^#' .env | xargs)
python scripts/load_catalog.py --dry-run   # valida el TSV
python scripts/load_catalog.py             # carga icf_codes, mapeo D1-D6 y candidatos
python scripts/embed_catalog.py            # calcula embeddings (reanudable)
```

Si el servidor no tiene Git, Compose ni `python3-venv` (caso del servidor actual): descarga el proyecto como zip desde GitHub, crea la base con `docker run -d --name icf-db --restart unless-stopped -e POSTGRES_USER=... -e POSTGRES_PASSWORD=... -e POSTGRES_DB=icf -p 127.0.0.1:5433:5432 -v icf_pgdata:/var/lib/postgresql/data pgvector/pgvector:pg16` y ejecuta los scripts dentro de `python:3.11-slim` con `--network host --env-file .env`.

Pruebas (no necesitan la base): `pytest`. La prueba del catálogo real se omite si el TSV no está.

## Servicio de sugerencia (HU-07b)

`app.py` expone `POST /suggest` y `GET /health` en `127.0.0.1:8100`. Flujo: reglas fijas (edad, calificador, capítulos con nivel ≥ 5) → un embedding del contexto clínico → **d** (actividades): lista cerrada del Anexo, ordenada por calificador y por similitud, **sin modelo de generación** → **b** y **s** (funciones y estructuras): los candidatos más cercanos por pgvector **entre los códigos de 3 dígitos** (12 en modo calidad, 6 en rápido; se excluyen los «otros/no especificados», códigos terminados en 8 y 9), y `qwen2.5:3b` elige y ordena entre ellos (JSON Schema donde los candidatos son un `enum`; en modo calidad con una justificación corta por código) → validación contra el catálogo. Los títulos salen del catálogo y los calificadores de las reglas, nunca del modelo. Si el modelo falla, devuelve igual los códigos más cercanos, marcados con su origen (`rules`, `similarity` o `llm`).

**Por qué este diseño (medido en el servidor, i3 sin GPU):** leer el prompt cuesta ~0,05 s por token (21 tok/s) y escribir la respuesta ~0,1 s por token (10 tok/s). La primera versión mandaba 760 tokens y pedía 167 de salida: ~55 s por sugerencia. Ahora el modelo solo trabaja en b y s, y hay dos modos (`ICF_MODE`): **calidad** (predeterminado: 12 candidatos y justificación corta del modelo, ~40 s) y **rápido** (6 candidatos y solo códigos, ~20 s). Con `ICF_USE_LLM=false` el servicio funciona sin el modelo de generación (b y s por similitud), en un par de segundos.

**Por qué 12 candidatos y solo códigos de 3 dígitos:** el modelo solo puede elegir lo que la búsqueda le ofrece. Con las pistas orientativas de `reference/retrieval_hints.json` (no validadas por un médico), buscar entre todos los niveles dejaba la lista llena de hermanos casi idénticos (`b2800`, `b2801`, `b2802`...). Limitar la búsqueda a los códigos de 3 dígitos subió la cobertura de funciones de 11 % a 23 % con 6 candidatos y a 40 % con 12, y la de estructuras de 43 % a 71 % con 6 y 86 % con 12. Enriquecer el texto de cada código con los títulos de sus hijos no mejoró (se descartó). El perfil llega entonces con un nivel menos de detalle (`b730` en lugar de `b7300`); el médico puede afinarlo. La entrada rechaza cualquier campo que no sea de la lista (nombre, documento y orientación sexual no pueden llegar).

Levantar el servicio en el servidor (después de cargar el catálogo y los embeddings):

```bash
cd ~/health-access-bridge/icf-service
sudo docker build -t icf-service .
sudo docker run -d --name icf-service --restart unless-stopped --network host --env-file .env icf-service
curl -s http://127.0.0.1:8100/health      # debe mostrar codes y codes_with_embedding en 1593
```

Actualizar el Caddyfile con el bloque de la sección siguiente y reiniciar Caddy. Prueba de extremo a extremo (el primer intento tarda más porque carga los modelos):

```bash
curl -s http://127.0.0.1:8100/suggest -H 'Content-Type: application/json' -d '{"age":35,"cat_fisica":"Severa","cat_psicosocial":"Moderada","cause":"Accidente de transito","levels":{"D1":10,"D4":60,"D5":55},"diag_cie":"S78 Amputacion traumatica"}'
```

Evaluación con el set de referencia (`reference/cases.json`, 25 casos sintéticos): mide JSON válido, códigos fuera del catálogo y latencia p50/p95; la precisión se calcula cuando el médico completa `expected` y marca `validated`:

```bash
sudo docker run --rm --network host --env-file .env -v "$PWD:/srv" -w /srv icf-service python scripts/evaluate.py --output informe.json
```

¿El modelo elige mejor que la similitud sola? `compare_modes.py` corre los 21 casos con pistas en tres modos (`similitud` sin modelo, `rapido` y `calidad`) y compara precisión, cobertura y latencia (las pistas son orientativas y no están validadas por un médico: sirven para comparar modos, no como precisión clínica). Tarda unos 20 minutos, así que conviene correrlo en segundo plano:

```bash
sudo docker run -d --name icf-compare --network host --env-file .env -v "$PWD:/srv" -w /srv icf-service python scripts/compare_modes.py --output comparacion.json
sudo docker logs -f icf-compare      # Ctrl+C para dejar de mirar; el proceso sigue
```

Calidad de la búsqueda de funciones y estructuras: compara 3 formas de buscar (texto con todo, solo lo clínico, y solo códigos de 3 dígitos —la que usa el motor—) y mide cuántas de las pistas orientativas de `reference/retrieval_hints.json` quedan entre los 6 y los 12 primeros candidatos (no es precisión clínica; las pistas no están validadas por un médico):

```bash
sudo docker run --rm --network host --env-file .env -v "$PWD:/srv" -w /srv icf-service python scripts/probe_retrieval.py
```

Diagnóstico de velocidad (dónde se va el tiempo y qué variante de prompt es más rápida; compara salida con y sin justificación, formato JSON Schema, contexto reducido y menos candidatos):

```bash
sudo docker run --rm --network host --env-file .env -v "$PWD:/srv" -w /srv icf-service python scripts/benchmark_llm.py
```

Variables opcionales del servicio (en el `.env`; reiniciar el contenedor al cambiarlas): `ICF_MODE` (`calidad` por defecto, o `rapido`), `ICF_USE_LLM` (`true`/`false`), y para afinar un modo: `ICF_BODY_CANDIDATES` (12 o 6), `ICF_LLM_JUSTIFY` (`true`/`false`), `ICF_LLM_NUM_PREDICT` (300 o 120), `ICF_LLM_NUM_CTX` (2048 o 1024) e `ICF_SERVICE_LLM_TIMEOUT_S` (120). El backend de Render debe esperar 90 s (`ICF_LLM_TIMEOUT_S`) mientras se use un modelo con latencia de decenas de segundos; con el modelo externo se espera mucho menos.

## Túnel autenticado (Caddy + Tailscale Funnel)

Funnel publica en internet y Ollama no tiene autenticación, así que **Funnel siempre apunta a Caddy (11435), nunca a Ollama (11434)**.

`/etc/caddy/Caddyfile` (genera el token con `openssl rand -hex 32` y guárdalo fuera del repo):

```
:11435 {
    bind 127.0.0.1
    route {
        @sintoken not header Authorization "Bearer TOKEN"
        respond @sintoken "No autorizado" 401
        @servicio path /suggest /health
        reverse_proxy @servicio 127.0.0.1:8100
        reverse_proxy 127.0.0.1:11434
    }
}
```

El bloque `route` es obligatorio: fija el orden de las directivas y garantiza que **el token se exige antes de cualquier ruta**. Sin él, Caddy puede atender `/suggest` sin pedir el token (probado). `/suggest` y `/health` van al servicio ICF (puerto 8100); todo lo demás va a Ollama.

```bash
sudo caddy validate --config /etc/caddy/Caddyfile && sudo systemctl restart caddy
sudo tailscale funnel --bg --https=443 http://127.0.0.1:11435
tailscale funnel status          # debe mostrar el destino 127.0.0.1:11435
```

Comprobación desde fuera de la tailnet: sin token o con token falso debe dar `401`; con el token correcto, `GET /api/tags` lista los modelos. Para apagar el túnel: `sudo tailscale funnel reset`. Para rotar el token, reescribe el Caddyfile, reinicia Caddy y actualiza `ICF_LLM_TOKEN` en Render.

## Variables en Render (backend QA y producción)

| Variable | Valor |
|---|---|
| `ICF_LLM_URL` | URL pública de Funnel, sin `/` final |
| `ICF_LLM_TOKEN` | el token del Caddyfile (secreto) |
| `ICF_LLM_MODEL` | `qwen2.5:3b` |
| `ICF_LLM_TIMEOUT_S` | `90` (se cargó `20` el 06-oct-2026 y se queda corto: una sugerencia con el modelo local tarda de 24 a 55 s) |
| `ICF_LLM_KEEP_ALIVE` | `30m` |

Comprobación: con un token de login de administrador, `GET /icf/health` debe devolver `reachable: true` y `model_available: true`. La respuesta nunca incluye la URL ni el token.

## Medidas de referencia (5 y 6 de octubre de 2026, i3 / 12 GB, sin GPU)

`qwen2.5:3b` (Q4_K_M, 1,9 GB): una respuesta mínima tarda 4,1 s en red local y 8,8 s por Funnel; leer el prompt cuesta ~0,05 s por token (21 tok/s) y escribir ~0,1 s por token (10 tok/s). El motor completo tardó 55,6 s en la primera versión, 22,9 s tras reducir lo que se le envía, y en la comparación final 24 s (modo rápido) y 46 s (modo calidad), contra 0,6 s de la similitud sola; además, el modelo local empeoró la selección frente a la similitud. `gemma4:e4b` ocupa 9,6 GB, no cabe junto a Qwen en 12 GB y no se evaluó. Tablas completas y método en [`docs/reports/PRUEBAS_HU07_SERVIDOR_FISICO.md`](../docs/reports/PRUEBAS_HU07_SERVIDOR_FISICO.md). El `ICF_LLM_TIMEOUT_S` de Render debe ser de 90 s mientras se use un modelo con latencia de decenas de segundos.
