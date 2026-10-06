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

Pruebas (no necesitan la base): `pytest`. La prueba del catálogo real se omite si el TSV no está.

## Túnel autenticado (Caddy + Tailscale Funnel)

Funnel publica en internet y Ollama no tiene autenticación, así que **Funnel siempre apunta a Caddy (11435), nunca a Ollama (11434)**.

`/etc/caddy/Caddyfile` (genera el token con `openssl rand -hex 32` y guárdalo fuera del repo):

```
:11435 {
    bind 127.0.0.1
    @sintoken not header Authorization "Bearer TOKEN"
    respond @sintoken "No autorizado" 401
    reverse_proxy 127.0.0.1:11434
}
```

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
