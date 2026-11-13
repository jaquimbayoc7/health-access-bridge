-- HU-07j: memoria de casos confirmados por el medico (base vectorial).
-- Un caso = el texto clinico (diagnostico CIE y notas, sin identificadores) de una generacion del perfil.
-- Sus codigos confirmados se guardan aparte; el servicio crea estas tablas al arrancar si no existen.
CREATE TABLE IF NOT EXISTS icf_cases (
    case_key    TEXT PRIMARY KEY,          -- lote de sugerencias del backend (uuid); no identifica a la persona
    context     TEXT NOT NULL,             -- texto que se vectoriza (mismo formato que usa /suggest)
    diag        TEXT,                      -- diagnostico CIE, para mostrarlo como ejemplo
    age_group   TEXT,
    embedding   vector(1024) NOT NULL,     -- bge-m3
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS icf_case_codes (
    case_key            TEXT NOT NULL REFERENCES icf_cases (case_key) ON DELETE CASCADE,
    item_ref            INTEGER NOT NULL,  -- id de la sugerencia en el backend
    component           CHAR(1) NOT NULL CHECK (component IN ('b', 's', 'd')),
    code                TEXT NOT NULL,
    status              TEXT NOT NULL CHECK (status IN ('aceptado', 'editado')),
    qualifier           SMALLINT,
    qualifier_cn        SMALLINT,
    qualifier_cl        SMALLINT,
    qualifier_suggested SMALLINT,          -- lo que sugirio el sistema (para medir el acuerdo)
    justification       TEXT,              -- la del medico si la escribio; si no, la del modelo
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (case_key, item_ref)
);
