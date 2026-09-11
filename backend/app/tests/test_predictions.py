"""
Tests de integración — HU-06: Predicción ML end-to-end (Patients -> HybridModelDisability)

Estos tests validan la integración completa del flujo de prediccion:
  1. Autenticacion del medico
  2. Creacion de un paciente con niveles ICF (D1-D6)
  3. Ejecucion de POST /patients/{id}/predict
  4. Persistencia del resultado en el registro del paciente

El modelo ML real (`model_pipeline.joblib`) se reemplaza con un dummy via
monkeypatch para que la suite sea rapida, determinista y no dependa de que
el archivo del modelo este presente en el entorno de CI.
"""
import pytest

from .conftest import PATIENT_PAYLOAD
from app.routers import patients as patients_router


class _DummyModel:
    """Modelo falso que simula HybridModelDisability sin cargar joblib."""

    def __init__(self, profile: int = 1):
        self.profile = profile

    def predict(self, df):
        return [self.profile] * len(df)


def _create_patient(client, headers, **overrides):
    payload = {**PATIENT_PAYLOAD, **overrides}
    r = client.post("/patients/", json=payload, headers=headers)
    assert r.status_code in (200, 201)
    return r.json()["id"]


class TestPredictionEndpoint:
    def test_predict_unauthenticated(self, client):
        r = client.post("/patients/1/predict")
        assert r.status_code == 401

    def test_predict_nonexistent_patient(self, client, auth_headers_medico, monkeypatch):
        monkeypatch.setattr(patients_router, "get_model", lambda: _DummyModel())
        r = client.post("/patients/999999/predict", headers=auth_headers_medico)
        assert r.status_code == 404

    def test_predict_other_medico_patient_forbidden(self, client, auth_headers_medico, db, monkeypatch):
        """Un medico no puede predecir sobre un paciente que no le pertenece.

        read_patient() devuelve 403 (no 404) cuando el paciente existe pero
        pertenece a otro medico -- mismo criterio de ownership que GET/PUT/DELETE."""
        from app import crud, schemas

        other = crud.get_user_by_email(db, "predict_owner@test.com")
        if not other:
            other = crud.create_user(
                db,
                schemas.UserCreate(
                    email="predict_owner@test.com",
                    password="pass12345",
                    full_name="Predict Owner",
                    role="médico",
                ),
            )
        login = client.post(
            "/users/login",
            data={"username": "predict_owner@test.com", "password": "pass12345"},
        )
        other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
        patient_id = _create_patient(client, other_headers, numero_documento="5551112222")

        monkeypatch.setattr(patients_router, "get_model", lambda: _DummyModel())
        r = client.post(f"/patients/{patient_id}/predict", headers=auth_headers_medico)
        assert r.status_code == 403

    @pytest.mark.parametrize("profile,expected_desc", [
        (0, "Perfil de Barreras Bajas"),
        (1, "Perfil de Barreras Moderadas"),
        (2, "Perfil de Barreras Altas"),
    ])
    def test_predict_success_all_profiles(self, client, auth_headers_medico, monkeypatch, profile, expected_desc):
        monkeypatch.setattr(patients_router, "get_model", lambda: _DummyModel(profile=profile))
        patient_id = _create_patient(client, auth_headers_medico, numero_documento=f"600{profile}000111")

        r = client.post(f"/patients/{patient_id}/predict", headers=auth_headers_medico)
        assert r.status_code == 200
        body = r.json()
        assert body["profile"] == profile
        assert body["description"] == expected_desc

    def test_predict_persists_result_on_patient(self, client, auth_headers_medico, monkeypatch):
        """El resultado de la prediccion debe persistir en el registro del paciente."""
        monkeypatch.setattr(patients_router, "get_model", lambda: _DummyModel(profile=2))
        patient_id = _create_patient(client, auth_headers_medico, numero_documento="7001112223")

        predict_response = client.post(f"/patients/{patient_id}/predict", headers=auth_headers_medico)
        assert predict_response.status_code == 200

        get_response = client.get(f"/patients/{patient_id}", headers=auth_headers_medico)
        assert get_response.status_code == 200
        body = get_response.json()
        assert body.get("prediction_profile") == 2
        assert body.get("prediction_description") == "Perfil de Barreras Altas"

    def test_predict_model_unavailable_returns_503(self, client, auth_headers_medico, monkeypatch):
        def _raise_runtime_error():
            raise RuntimeError("Modelo no encontrado")

        monkeypatch.setattr(patients_router, "get_model", _raise_runtime_error)
        patient_id = _create_patient(client, auth_headers_medico, numero_documento="8001112224")

        r = client.post(f"/patients/{patient_id}/predict", headers=auth_headers_medico)
        assert r.status_code == 503

    def test_predict_model_exception_returns_500(self, client, auth_headers_medico, monkeypatch):
        class _BrokenModel:
            def predict(self, df):
                raise ValueError("input inesperado")

        monkeypatch.setattr(patients_router, "get_model", lambda: _BrokenModel())
        patient_id = _create_patient(client, auth_headers_medico, numero_documento="9001112225")

        r = client.post(f"/patients/{patient_id}/predict", headers=auth_headers_medico)
        assert r.status_code == 500


class TestPredictionResponseTime:
    """Verifica que el endpoint de prediccion responde dentro de un umbral razonable
    con el modelo dummy (proxy de latencia de la capa API, sin contar inferencia real)."""

    def test_predict_response_under_threshold(self, client, auth_headers_medico, monkeypatch):
        import time

        monkeypatch.setattr(patients_router, "get_model", lambda: _DummyModel())
        patient_id = _create_patient(client, auth_headers_medico, numero_documento="1112223334")

        start = time.perf_counter()
        r = client.post(f"/patients/{patient_id}/predict", headers=auth_headers_medico)
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert r.status_code == 200
        assert elapsed_ms < 200, f"El endpoint tardo {elapsed_ms:.1f}ms (umbral: 200ms)"
