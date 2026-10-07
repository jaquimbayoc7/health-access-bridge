"""
HU-07c — Pruebas de las sugerencias de codigos CIF-IA.
El servicio ICF real no existe en CI: se simula icf_client.post_suggest.
"""
import itertools
import json
from urllib import error

import pytest

from app import crud, models, schemas
from app.services import icf_client
from .conftest import PATIENT_PAYLOAD

SECRET_URL = "https://servidor-secreto.example.ts.net"
SECRET_TOKEN = "token-super-secreto-123"
_counter = itertools.count(1)


def _service_result(**overrides):
    result = {
        "applicable": True,
        "model": "gemma4:e4b",
        "llm_used": True,
        "latency_ms": 3400,
        "warnings": [],
        "functions": [
            {"code": "b730", "title": "Fuerza muscular", "qualifier": 3, "justification": "Debilidad", "origin": "llm"},
            {"code": "b280", "title": "Sensación de dolor", "qualifier": 3, "justification": "Dolor", "origin": "llm"},
        ],
        "structures": [
            {"code": "s750", "title": "Estructura de la extremidad inferior", "qualifier": 3,
             "qualifier_cn": 8, "qualifier_cl": 8, "justification": "", "origin": "llm"},
        ],
        "activities": [
            {"code": "d450", "title": "Andar", "qualifier": 3, "justification": "", "origin": "rules"},
        ],
    }
    result.update(overrides)
    return result


@pytest.fixture
def configured(monkeypatch):
    monkeypatch.setenv("ICF_LLM_URL", SECRET_URL)
    monkeypatch.setenv("ICF_LLM_TOKEN", SECRET_TOKEN)


@pytest.fixture
def fake_service(monkeypatch, configured):
    """Simula el servicio ICF y guarda lo que se le envia."""
    calls = []

    def _post(url, token, payload, timeout):
        calls.append({"url": url, "token": token, "payload": payload, "timeout": timeout})
        return _service_result()

    monkeypatch.setattr(icf_client, "post_suggest", _post)
    return calls


def _make_patient(db, owner_id, **overrides):
    data = dict(PATIENT_PAYLOAD)
    data["numero_documento"] = f"ICF{next(_counter):07d}"
    data["nombre_apellidos"] = "Nombre Secreto Apellido"
    data["orientacion_sexual"] = "orientacion-secreta"
    data.update(overrides)
    return crud.create_user_patient(db, schemas.PatientCreate(**data), owner_id)


@pytest.fixture
def patient(db, medico_user):
    return _make_patient(db, medico_user.id)


@pytest.fixture
def other_medico_headers(client, db):
    email = "otro_medico_icf@test.com"
    if not crud.get_user_by_email(db, email):
        crud.create_user(db, schemas.UserCreate(email=email, password="otropass123", full_name="Otro", role="médico"))
    r = client.post("/users/login", data={"username": email, "password": "otropass123"})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def _generate(client, headers, patient_id, body=None):
    return client.post(f"/patients/{patient_id}/icf-suggestions", json=body or {}, headers=headers)


class TestGenerate:
    def test_requires_auth(self, client, patient):
        assert client.post(f"/patients/{patient.id}/icf-suggestions", json={}).status_code == 401

    def test_generates_and_stores_grouped_items(self, client, auth_headers_medico, patient, fake_service):
        r = _generate(client, auth_headers_medico, patient.id)
        assert r.status_code == 200
        body = r.json()
        assert [i["code"] for i in body["functions"]] == ["b730", "b280"]
        assert [i["code"] for i in body["structures"]] == ["s750"]
        assert [i["code"] for i in body["activities"]] == ["d450"]
        assert body["model"] == "gemma4:e4b" and body["llm_used"] is True and body["latency_ms"] == 3400
        assert all(i["status"] == "sugerido" for g in ("functions", "structures", "activities") for i in body[g])
        s = body["structures"][0]
        assert (s["qualifier"], s["qualifier_cn"], s["qualifier_cl"]) == (3, 8, 8)

    def test_service_gets_token_and_suggest_timeout(self, client, auth_headers_medico, patient, fake_service):
        _generate(client, auth_headers_medico, patient.id)
        call = fake_service[0]
        assert call["url"] == SECRET_URL and call["token"] == SECRET_TOKEN
        assert call["timeout"] == 90.0

    def test_payload_never_contains_identifying_data(self, client, auth_headers_medico, patient, fake_service):
        _generate(client, auth_headers_medico, patient.id,
                  {"diag_cie": " M54 Dorsalgia ", "clinical_notes": "Lumbalgia cronica"})
        payload = fake_service[0]["payload"]
        raw = json.dumps(payload, ensure_ascii=False)
        for secret in ("Nombre Secreto", patient.numero_documento, "orientacion-secreta"):
            assert secret not in raw
        assert set(payload) <= {
            "age", "gender", "cause", "cat_fisica", "cat_psicosocial", "levels",
            "prediction_description", "diag_cie", "clinical_notes",
        }
        assert payload["age"] == 34 and payload["levels"] == {"D1": 70, "D2": 60, "D3": 80, "D4": 50, "D5": 65, "D6": 75}
        assert payload["diag_cie"] == "M54 Dorsalgia" and payload["clinical_notes"] == "Lumbalgia cronica"

    def test_cause_is_normalized_to_the_official_list(self, client, auth_headers_medico, db, medico_user, fake_service):
        legacy = _make_patient(db, medico_user.id, causa_deficiencia="Accidente laboral")
        _generate(client, auth_headers_medico, legacy.id)
        assert fake_service[-1]["payload"]["cause"] == "Accidente de trabajo"

    def test_snapshot_of_clinical_inputs_is_saved(self, client, auth_headers_medico, patient, fake_service, db):
        _generate(client, auth_headers_medico, patient.id, {"diag_cie": "G80 Paralisis cerebral", "clinical_notes": "Espastica"})
        row = db.query(models.IcfSuggestion).filter_by(patient_id=patient.id).first()
        assert row.diag_cie == "G80 Paralisis cerebral" and row.clinical_notes == "Espastica" and row.model == "gemma4:e4b"

    def test_rejects_extra_fields_in_body(self, client, auth_headers_medico, patient, fake_service):
        r = _generate(client, auth_headers_medico, patient.id, {"nombre_apellidos": "x"})
        assert r.status_code == 422
        assert fake_service == []

    def test_under_six_is_rejected_without_calling_service(self, client, auth_headers_medico, db, medico_user, fake_service):
        child = _make_patient(db, medico_user.id, edad=5)
        r = _generate(client, auth_headers_medico, child.id)
        assert r.status_code == 422
        assert "menores de 6" in r.json()["detail"]
        assert fake_service == []

    def test_unknown_patient(self, client, auth_headers_medico, fake_service):
        assert _generate(client, auth_headers_medico, 999999).status_code == 404

    def test_medico_cannot_use_other_medicos_patient(self, client, other_medico_headers, patient, fake_service):
        assert _generate(client, other_medico_headers, patient.id).status_code == 403
        assert fake_service == []

    def test_admin_can_generate(self, client, auth_headers_admin, patient, fake_service):
        assert _generate(client, auth_headers_admin, patient.id).status_code == 200

    def test_not_configured_gives_503(self, client, auth_headers_medico, patient, monkeypatch):
        monkeypatch.delenv("ICF_LLM_URL", raising=False)
        monkeypatch.delenv("ICF_LLM_TOKEN", raising=False)
        r = _generate(client, auth_headers_medico, patient.id)
        assert r.status_code == 503 and "no esta configurado" in r.json()["detail"]

    def test_service_down_gives_503_without_leaking(self, client, auth_headers_medico, patient, configured, monkeypatch):
        def _raise(url, token, payload, timeout):
            raise error.URLError(f"fallo contra {url} con {token}")

        monkeypatch.setattr(icf_client, "post_suggest", _raise)
        r = _generate(client, auth_headers_medico, patient.id)
        assert r.status_code == 503
        assert SECRET_TOKEN not in r.text and "servidor-secreto" not in r.text

    def test_timeout_gives_503(self, client, auth_headers_medico, patient, configured, monkeypatch):
        def _raise(url, token, payload, timeout):
            raise TimeoutError("timed out")

        monkeypatch.setattr(icf_client, "post_suggest", _raise)
        assert _generate(client, auth_headers_medico, patient.id).status_code == 503

    def test_rejected_token_is_reported_without_detail(self, client, auth_headers_medico, patient, configured, monkeypatch):
        def _raise(url, token, payload, timeout):
            raise error.HTTPError(url, 401, "Unauthorized", {}, None)

        monkeypatch.setattr(icf_client, "post_suggest", _raise)
        r = _generate(client, auth_headers_medico, patient.id)
        assert r.status_code == 503 and "rechazado" in r.json()["detail"]
        assert SECRET_TOKEN not in r.text

    def test_invalid_response_gives_503(self, client, auth_headers_medico, patient, configured, monkeypatch):
        def _raise(url, token, payload, timeout):
            raise ValueError("no es json")

        monkeypatch.setattr(icf_client, "post_suggest", _raise)
        assert _generate(client, auth_headers_medico, patient.id).status_code == 503

    def test_service_says_not_applicable(self, client, auth_headers_medico, patient, configured, monkeypatch):
        monkeypatch.setattr(
            icf_client, "post_suggest",
            lambda *a: {"applicable": False, "message": "No aplica", "model": "x"},
        )
        r = _generate(client, auth_headers_medico, patient.id)
        assert r.status_code == 422 and r.json()["detail"] == "No aplica"

    def test_malformed_and_extra_items_are_dropped(self, client, auth_headers_medico, patient, configured, monkeypatch):
        funcs = [
            {"code": "b730", "title": "Fuerza muscular", "qualifier": 3, "origin": "llm"},
            {"code": "b280"},  # sin titulo
            "basura",
            {"code": "b710", "title": "Movilidad de las articulaciones", "qualifier": 3, "origin": "llm"},
            {"code": "b740", "title": "Resistencia muscular", "qualifier": 3, "origin": "llm"},
            {"code": "b147", "title": "Funciones psicomotoras", "qualifier": 3, "origin": "llm"},
        ]
        monkeypatch.setattr(icf_client, "post_suggest", lambda *a: _service_result(functions=funcs))
        body = _generate(client, auth_headers_medico, patient.id).json()
        assert len(body["functions"]) <= 3
        assert all(i["title"] for i in body["functions"])

    def test_llm_error_adds_warning_and_keeps_similarity_origin(self, client, auth_headers_medico, patient, configured, monkeypatch):
        fallback = [{"code": "b730", "title": "Fuerza muscular", "qualifier": 3, "origin": "similarity"}]
        monkeypatch.setattr(
            icf_client, "post_suggest",
            lambda *a: _service_result(llm_used=False, llm_error="JSON invalido", functions=fallback),
        )
        body = _generate(client, auth_headers_medico, patient.id).json()
        assert body["llm_used"] is False
        assert body["functions"][0]["origin"] == "similarity"
        assert any("similitud" in w for w in body["warnings"])


class TestRead:
    def test_empty_when_never_generated(self, client, auth_headers_medico, patient):
        r = client.get(f"/patients/{patient.id}/icf-suggestions", headers=auth_headers_medico)
        assert r.status_code == 200
        body = r.json()
        assert body["batch_id"] is None and body["functions"] == [] and body["structures"] == [] and body["activities"] == []

    def test_returns_only_the_latest_batch_and_keeps_history(self, client, auth_headers_medico, patient, configured, monkeypatch, db):
        monkeypatch.setattr(icf_client, "post_suggest", lambda *a: _service_result())
        first = _generate(client, auth_headers_medico, patient.id).json()
        second_fn = [{"code": "b710", "title": "Movilidad de las articulaciones", "qualifier": 2, "origin": "llm"}]
        monkeypatch.setattr(icf_client, "post_suggest", lambda *a: _service_result(functions=second_fn))
        second = _generate(client, auth_headers_medico, patient.id).json()
        assert first["batch_id"] != second["batch_id"]

        got = client.get(f"/patients/{patient.id}/icf-suggestions", headers=auth_headers_medico).json()
        assert got["batch_id"] == second["batch_id"]
        assert [i["code"] for i in got["functions"]] == ["b710"]
        assert db.query(models.IcfSuggestion).filter_by(patient_id=patient.id).count() == 4 + 3  # historial conservado

    def test_read_requires_ownership(self, client, other_medico_headers, patient):
        assert client.get(f"/patients/{patient.id}/icf-suggestions", headers=other_medico_headers).status_code == 403

    def test_read_requires_auth(self, client, patient):
        assert client.get(f"/patients/{patient.id}/icf-suggestions").status_code == 401


def _first_item(client, headers, patient_id, group="functions"):
    return client.get(f"/patients/{patient_id}/icf-suggestions", headers=headers).json()[group][0]


class TestDecide:
    @pytest.fixture
    def generated(self, client, auth_headers_medico, patient, fake_service):
        _generate(client, auth_headers_medico, patient.id)
        return patient

    def _patch(self, client, headers, item_id, body):
        return client.patch(f"/icf/suggestions/{item_id}", json=body, headers=headers)

    def test_accept(self, client, auth_headers_medico, generated, db, medico_user):
        item = _first_item(client, auth_headers_medico, generated.id)
        r = self._patch(client, auth_headers_medico, item["id"], {"status": "aceptado"})
        assert r.status_code == 200 and r.json()["status"] == "aceptado"
        row = db.get(models.IcfSuggestion, item["id"])
        assert row.decided_by_id == medico_user.id and row.decided_at is not None

    def test_reject(self, client, auth_headers_medico, generated):
        item = _first_item(client, auth_headers_medico, generated.id)
        assert self._patch(client, auth_headers_medico, item["id"], {"status": "rechazado"}).json()["status"] == "rechazado"

    def test_edit_qualifier(self, client, auth_headers_medico, generated):
        item = _first_item(client, auth_headers_medico, generated.id)
        r = self._patch(client, auth_headers_medico, item["id"], {"status": "editado", "qualifier": 2})
        assert r.status_code == 200
        assert r.json()["qualifier"] == 2 and r.json()["status"] == "editado" and r.json()["code"] == item["code"]

    def test_edit_structure_nature_and_location(self, client, auth_headers_medico, generated):
        item = _first_item(client, auth_headers_medico, generated.id, "structures")
        r = self._patch(client, auth_headers_medico, item["id"], {"status": "editado", "qualifier_cn": 2, "qualifier_cl": 5})
        assert r.status_code == 200
        assert (r.json()["qualifier"], r.json()["qualifier_cn"], r.json()["qualifier_cl"]) == (3, 2, 5)

    def test_edit_code_keeps_original(self, client, auth_headers_medico, generated):
        item = _first_item(client, auth_headers_medico, generated.id)
        r = self._patch(client, auth_headers_medico, item["id"],
                        {"status": "editado", "code": "b7300", "title": "Potencia de músculos aislados"})
        assert r.status_code == 200
        body = r.json()
        assert body["code"] == "b7300" and body["original_code"] == item["code"]
        # una segunda edicion no pisa el codigo original sugerido por la maquina
        r2 = self._patch(client, auth_headers_medico, item["id"],
                         {"status": "editado", "code": "b7301", "title": "Potencia de los músculos de una extremidad"})
        assert r2.json()["original_code"] == item["code"]

    def test_edit_without_changes_is_rejected(self, client, auth_headers_medico, generated):
        item = _first_item(client, auth_headers_medico, generated.id)
        assert self._patch(client, auth_headers_medico, item["id"], {"status": "editado"}).status_code == 422

    def test_edit_code_needs_title(self, client, auth_headers_medico, generated):
        item = _first_item(client, auth_headers_medico, generated.id)
        assert self._patch(client, auth_headers_medico, item["id"], {"status": "editado", "code": "b7300"}).status_code == 422

    def test_edit_code_must_keep_component(self, client, auth_headers_medico, generated):
        item = _first_item(client, auth_headers_medico, generated.id)
        r = self._patch(client, auth_headers_medico, item["id"], {"status": "editado", "code": "d450", "title": "Andar"})
        assert r.status_code == 422

    def test_nature_location_only_for_structures(self, client, auth_headers_medico, generated):
        item = _first_item(client, auth_headers_medico, generated.id)
        assert self._patch(client, auth_headers_medico, item["id"], {"status": "editado", "qualifier_cn": 2}).status_code == 422

    def test_accept_cannot_change_content(self, client, auth_headers_medico, generated):
        item = _first_item(client, auth_headers_medico, generated.id)
        assert self._patch(client, auth_headers_medico, item["id"], {"status": "aceptado", "qualifier": 1}).status_code == 422

    def test_cannot_set_back_to_suggested(self, client, auth_headers_medico, generated):
        item = _first_item(client, auth_headers_medico, generated.id)
        assert self._patch(client, auth_headers_medico, item["id"], {"status": "sugerido"}).status_code == 422

    def test_invalid_values(self, client, auth_headers_medico, generated):
        item = _first_item(client, auth_headers_medico, generated.id)
        assert self._patch(client, auth_headers_medico, item["id"], {"status": "editado", "qualifier": 7}).status_code == 422
        assert self._patch(client, auth_headers_medico, item["id"], {"status": "editado", "code": "x1", "title": "t"}).status_code == 422
        assert self._patch(client, auth_headers_medico, item["id"], {"status": "otro"}).status_code == 422

    def test_other_medico_cannot_decide(self, client, auth_headers_medico, other_medico_headers, generated):
        item = _first_item(client, auth_headers_medico, generated.id)
        assert self._patch(client, other_medico_headers, item["id"], {"status": "aceptado"}).status_code == 403

    def test_admin_can_decide(self, client, auth_headers_medico, auth_headers_admin, generated):
        item = _first_item(client, auth_headers_medico, generated.id)
        assert self._patch(client, auth_headers_admin, item["id"], {"status": "aceptado"}).status_code == 200

    def test_unknown_item_and_no_auth(self, client, auth_headers_medico):
        assert self._patch(client, auth_headers_medico, 999999, {"status": "aceptado"}).status_code == 404
        assert client.patch("/icf/suggestions/1", json={"status": "aceptado"}).status_code == 401

    def test_decision_is_returned_on_read(self, client, auth_headers_medico, generated):
        item = _first_item(client, auth_headers_medico, generated.id)
        self._patch(client, auth_headers_medico, item["id"], {"status": "aceptado"})
        assert _first_item(client, auth_headers_medico, generated.id)["status"] == "aceptado"
