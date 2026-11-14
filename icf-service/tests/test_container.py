"""El contenedor debe llevar todo lo que el servicio lee en tiempo de ejecucion (HU-07j: sql/002_cases.sql)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_dockerfile_copies_the_case_schema_the_service_reads_at_runtime():
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf8")
    assert re.search(r"^COPY\s+sql/002_cases\.sql\s+\./sql/002_cases\.sql\s*$", dockerfile, re.M)
    assert (ROOT / "sql" / "002_cases.sql").exists()


def test_the_schema_path_matches_the_container_layout():
    """En el contenedor el codigo vive en /srv/icf/repository.py y el SQL en /srv/sql/: dos niveles arriba del modulo."""
    from icf import repository

    assert Path(repository.__file__).resolve().parent.parent.joinpath("sql", "002_cases.sql").exists()


def test_default_similarity_threshold_and_compose_pass_the_memory_settings(monkeypatch):
    """HU-07j: umbral por defecto 0.70 (evaluacion dejando un caso fuera) y las tres variables llegan al contenedor."""
    from icf.config import load_settings

    for name in ("ICF_CASE_MIN_SIMILARITY", "ICF_CASE_EXAMPLES", "ICF_CASE_MEMORY"):
        monkeypatch.delenv(name, raising=False)
    settings = load_settings()
    assert (settings.case_min_similarity, settings.case_examples, settings.case_memory) == (0.70, 3, True)
    compose = (ROOT / "deploy" / "windows" / "docker-compose.yml").read_text(encoding="utf8")
    for name in ("ICF_CASE_MEMORY", "ICF_CASE_EXAMPLES", "ICF_CASE_MIN_SIMILARITY"):
        assert f"{name}: ${{{name}:-" in compose
