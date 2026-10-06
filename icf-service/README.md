# icf-service — servidor local de IA para HU-07 (códigos CIF)

Componentes que corren en el servidor propio (Linux). El backend de Render solo lo alcanza por el túnel autenticado.

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

`app.py` expone `POST /suggest` y `GET /health` en `127.0.0.1:8100`. Flujo: reglas fijas (edad, calificador, capítulos con nivel ≥ 5) → un embedding del contexto clínico → **d** (actividades): lista cerrada del Anexo, ordenada por calificador y por similitud, **sin modelo de generación** → **b** y **s** (funciones y estructuras): los 6 candidatos más cercanos por pgvector, y `qwen2.5:3b` elige y ordena entre ellos devolviendo solo códigos (JSON Schema donde los candidatos son un `enum`) → validación contra el catálogo. Los títulos salen del catálogo y los calificadores de las reglas, nunca del modelo. Si el modelo falla, devuelve igual los códigos más cercanos, marcados con su origen (`rules`, `similarity` o `llm`).

**Por qué este diseño (medido en el servidor, i3 sin GPU):** leer el prompt cuesta ~0,05 s por token (21 tok/s) y escribir la respuesta ~0,1 s por token (10 tok/s). La primera versión mandaba 760 tokens y pedía 167 de salida: ~55 s por sugerencia. Ahora el modelo solo trabaja en b y s, con un prompt corto cuya parte fija va primero (Ollama la reutiliza entre peticiones) y salida solo de códigos. Con `ICF_USE_LLM=false` el servicio funciona sin el modelo de generación (b y s por similitud), en un par de segundos. La entrada rechaza cualquier campo que no sea de la lista (nombre, documento y orientación sexual no pueden llegar).

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

Calidad de la búsqueda de funciones y estructuras: compara 4 formas de buscar (texto actual, solo lo clínico, solo códigos de 3 dígitos y 3 dígitos con embedding enriquecido con los títulos de sus hijos) y mide cuántas de las pistas orientativas de `reference/retrieval_hints.json` quedan entre los 6 y los 12 primeros candidatos (no es precisión clínica; las pistas no están validadas por un médico). Primero hay que calcular el embedding enriquecido (unos 150 códigos, menos de un minuto):

```bash
sudo docker run --rm --network host --env-file .env -v "$PWD:/srv" -w /srv icf-service python scripts/embed_catalog.py --rich
sudo docker run --rm --network host --env-file .env -v "$PWD:/srv" -w /srv icf-service python scripts/probe_retrieval.py
```

Diagnóstico de velocidad (dónde se va el tiempo y qué variante de prompt es más rápida; compara salida con y sin justificación, formato JSON Schema, contexto reducido y menos candidatos):

```bash
sudo docker run --rm --network host --env-file .env -v "$PWD:/srv" -w /srv icf-service python scripts/benchmark_llm.py
```

Variables opcionales del servicio (en el `.env`; reiniciar el contenedor al cambiarlas): `ICF_USE_LLM` (`true`/`false`), `ICF_LLM_NUM_PREDICT` (tope de tokens de salida, 120), `ICF_LLM_NUM_CTX` (contexto, 1024) e `ICF_SERVICE_LLM_TIMEOUT_S` (90).

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
| `ICF_LLM_TIMEOUT_S` | `20` |
| `ICF_LLM_KEEP_ALIVE` | `30m` |

Comprobación: con un token de login de administrador, `GET /icf/health` debe devolver `reachable: true` y `model_available: true`. La respuesta nunca incluye la URL ni el token.

## Medidas de referencia (05-oct-2026, i3 / 12 GB, sin GPU)

`qwen2.5:3b` (Q4_K_M, 1.9 GB): 4,1 s en red local con el modelo cargado y 8,8 s en una llamada por Funnel (aún sin repetir la medición para separar arranque en frío de red). Por eso el timeout es 20 s y el LLM solo elige entre una lista cerrada de candidatos. `gemma4:e4b` ocupa 9,6 GB y no cabe junto a Qwen en 12 GB.
