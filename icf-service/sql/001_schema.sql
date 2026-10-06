-- HU-07a: esquema del servicio ICF local (PostgreSQL + pgvector)
CREATE EXTENSION IF NOT EXISTS vector;

-- Catalogo CIF-IA hasta el nivel cuyo codigo tiene 5 digitos. Se carga con scripts/load_catalog.py
CREATE TABLE IF NOT EXISTS icf_codes (
    code        TEXT PRIMARY KEY,
    component   CHAR(1)  NOT NULL CHECK (component IN ('b', 's', 'd', 'e')),
    chapter     SMALLINT NOT NULL,
    level       SMALLINT NOT NULL CHECK (level BETWEEN 2 AND 4),
    parent      TEXT REFERENCES icf_codes (code),
    title       TEXT NOT NULL,
    description TEXT,
    inclusions  TEXT,
    exclusions  TEXT,
    source      TEXT,
    embedding   vector(1024)  -- bge-m3
);

-- Embedding enriquecido de los codigos de nivel 2: titulo + titulos de sus hijos (scripts/embed_catalog.py --rich)
ALTER TABLE icf_codes ADD COLUMN IF NOT EXISTS embedding_rich vector(1024);

CREATE INDEX IF NOT EXISTS icf_codes_component_chapter_idx ON icf_codes (component, chapter);

-- Mapeo explicito niveles D1-D6 de HAB -> capitulo CIF-IA -> dominio oficial del Anexo 1239
CREATE TABLE IF NOT EXISTS icf_hab_domains (
    hab_domain      CHAR(2) PRIMARY KEY,
    chapter_code    TEXT NOT NULL,
    chapter_name    TEXT NOT NULL,
    official_domain TEXT,
    note            TEXT
);

-- Candidatos por dominio oficial transcritos del Anexo (pre-filtro antes de pgvector)
CREATE TABLE IF NOT EXISTS icf_domain_map (
    official_domain TEXT NOT NULL,
    code            TEXT NOT NULL REFERENCES icf_codes (code),
    hab_domain      CHAR(2) REFERENCES icf_hab_domains (hab_domain),
    PRIMARY KEY (official_domain, code)
);
-- Grupo de edad del instrumento del Anexo donde aparece el codigo: '6-17', '18+' o 'both'
ALTER TABLE icf_domain_map ADD COLUMN IF NOT EXISTS ages TEXT NOT NULL DEFAULT 'both';
