"""Causas de la deficiencia del Anexo Tecnico de la Resolucion 1239 de 2022."""
import pytest

from app.causes import OFFICIAL_CAUSES, is_official, normalize_cause


def test_official_list_has_21_options_in_3_groups():
    assert len(OFFICIAL_CAUSES) == 21
    groups = {}
    for cause in OFFICIAL_CAUSES:
        groups.setdefault(cause["group"], []).append(cause["name"])
    assert {g: len(v) for g, v in groups.items()} == {"De nacimiento": 4, "Adquirida": 16, "No se identifica": 1}
    assert len({c["name"] for c in OFFICIAL_CAUSES}) == 21


def test_the_five_options_of_the_patient_form_are_official():
    for name in (
        "Enfermedad general", "Accidente de tránsito", "Alteración genética o hereditaria",
        "Complicaciones durante el parto", "Violencia por delincuencia común",
    ):
        assert is_official(name)


@pytest.mark.parametrize("raw,expected", [
    ("Enfermedad general", "Enfermedad general"),
    ("  accidente de transito ", "Accidente de tránsito"),
    ("ENVEJECIMIENTO", "Envejecimiento"),
    ("Accidente laboral", "Accidente de trabajo"),
    ("Lesión deportiva", "Accidente deportivo"),
    ("Enfermedad degenerativa", "Enfermedad general"),
    ("Enfermedad cardiovascular", "Enfermedad general"),
])
def test_normalize_maps_clear_cases(raw, expected):
    assert normalize_cause(raw) == expected


@pytest.mark.parametrize("raw", ["Enfermedad congénita", "Parálisis cerebral", "Trauma craneoencefálico"])
def test_ambiguous_values_are_not_guessed(raw):
    assert normalize_cause(raw) == raw
    assert not is_official(raw)


def test_normalize_handles_empty_values():
    assert normalize_cause(None) is None
    assert normalize_cause("   ") is None


def test_causes_endpoint_requires_auth_and_lists_options(client, auth_headers_medico):
    assert client.get("/icf/causes").status_code == 401
    r = client.get("/icf/causes", headers=auth_headers_medico)
    assert r.status_code == 200
    assert len(r.json()) == 21 and {"name", "group"} <= set(r.json()[0])
