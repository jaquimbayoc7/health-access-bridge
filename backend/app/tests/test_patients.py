"""
Tests de integración — HU-02: Registro y Precarga de Datos de Pacientes
"""
from .conftest import PATIENT_PAYLOAD


class TestPatientsAuth:
    def test_list_patients_unauthenticated(self, client):
        r = client.get("/patients/")
        assert r.status_code == 401

    def test_list_patients_as_admin_forbidden(self, client, auth_headers_admin):
        r = client.get("/patients/", headers=auth_headers_admin)
        assert r.status_code == 403

    def test_create_patient_unauthenticated(self, client):
        r = client.post("/patients/", json=PATIENT_PAYLOAD)
        assert r.status_code == 401


class TestPatientCRUD:
    def test_create_patient(self, client, auth_headers_medico):
        r = client.post("/patients/", json=PATIENT_PAYLOAD, headers=auth_headers_medico)
        assert r.status_code in (200, 201)
        body = r.json()
        assert body["nombre_apellidos"] == PATIENT_PAYLOAD["nombre_apellidos"]
        assert body["numero_documento"] == PATIENT_PAYLOAD["numero_documento"]
        assert "id" in body
        return body["id"]

    def test_list_patients(self, client, auth_headers_medico):
        r = client.get("/patients/", headers=auth_headers_medico)
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_list_patients_only_own(self, client, auth_headers_medico, db):
        """Un médico solo ve sus propios pacientes."""
        from app import crud, schemas
        other_medico = crud.get_user_by_email(db, "otro_medico_isolation@test.com")
        if not other_medico:
            other_medico = crud.create_user(
                db,
                schemas.UserCreate(
                    email="otro_medico_isolation@test.com",
                    password="pass12345",
                    full_name="Otro Medico Isolation",
                    role="médico",
                ),
            )
        login = client.post(
            "/users/login",
            data={"username": "otro_medico_isolation@test.com", "password": "pass12345"},
        )
        other_token = login.json()["access_token"]
        other_headers = {"Authorization": f"Bearer {other_token}"}

        r = client.get("/patients/", headers=other_headers)
        assert r.status_code == 200
        assert r.json() == []

    def test_get_patient_by_id(self, client, auth_headers_medico):
        create = client.post(
            "/patients/", json=PATIENT_PAYLOAD, headers=auth_headers_medico
        )
        patient_id = create.json()["id"]

        r = client.get(f"/patients/{patient_id}", headers=auth_headers_medico)
        assert r.status_code == 200
        assert r.json()["id"] == patient_id

    def test_get_patient_not_found(self, client, auth_headers_medico):
        r = client.get("/patients/99999", headers=auth_headers_medico)
        assert r.status_code == 404

    def test_update_patient(self, client, auth_headers_medico):
        create = client.post(
            "/patients/", json=PATIENT_PAYLOAD, headers=auth_headers_medico
        )
        patient_id = create.json()["id"]

        updated = {**PATIENT_PAYLOAD, "nombre_apellidos": "Juan Pérez Actualizado"}
        r = client.put(
            f"/patients/{patient_id}", json=updated, headers=auth_headers_medico
        )
        assert r.status_code == 200
        assert r.json()["nombre_apellidos"] == "Juan Pérez Actualizado"

    def test_delete_patient_soft(self, client, auth_headers_medico):
        create = client.post(
            "/patients/", json=PATIENT_PAYLOAD, headers=auth_headers_medico
        )
        patient_id = create.json()["id"]

        r = client.delete(f"/patients/{patient_id}", headers=auth_headers_medico)
        assert r.status_code == 200

        r2 = client.get(f"/patients/{patient_id}", headers=auth_headers_medico)
        assert r2.status_code == 404

    def test_delete_nonexistent_patient(self, client, auth_headers_medico):
        r = client.delete("/patients/99999", headers=auth_headers_medico)
        assert r.status_code == 404


class TestPatientSearch:
    def test_search_by_name(self, client, auth_headers_medico):
        payload = {**PATIENT_PAYLOAD, "nombre_apellidos": "María López Search", "numero_documento": "2009990001"}
        client.post("/patients/", json=payload, headers=auth_headers_medico)

        r = client.get("/patients/?search=María López", headers=auth_headers_medico)
        assert r.status_code == 200
        results = r.json()
        assert any("María" in p["nombre_apellidos"] for p in results)

    def test_search_by_documento(self, client, auth_headers_medico):
        payload = {**PATIENT_PAYLOAD, "nombre_apellidos": "Carlos Ruiz Search", "numero_documento": "3001112222"}
        client.post("/patients/", json=payload, headers=auth_headers_medico)

        r = client.get("/patients/?search=3001112222", headers=auth_headers_medico)
        assert r.status_code == 200
        results = r.json()
        assert any(p["numero_documento"] == "3001112222" for p in results)

    def test_search_no_results(self, client, auth_headers_medico):
        r = client.get("/patients/?search=xyzNoExiste999", headers=auth_headers_medico)
        assert r.status_code == 200
        assert r.json() == []

    def test_search_empty_returns_all(self, client, auth_headers_medico):
        r_all = client.get("/patients/", headers=auth_headers_medico)
        r_empty = client.get("/patients/?search=", headers=auth_headers_medico)
        assert r_all.status_code == 200
        assert r_empty.status_code == 200
        assert len(r_empty.json()) == len(r_all.json())


class TestPatientOwnership:
    def test_cannot_access_other_medico_patient(self, client, auth_headers_medico, db):
        from app import crud, schemas
        other = crud.get_user_by_email(db, "owner_test@test.com")
        if not other:
            other = crud.create_user(
                db,
                schemas.UserCreate(
                    email="owner_test@test.com",
                    password="pass12345",
                    full_name="Owner Test",
                    role="médico",
                ),
            )
        login = client.post(
            "/users/login",
            data={"username": "owner_test@test.com", "password": "pass12345"},
        )
        other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        create = client.post(
            "/patients/",
            json={**PATIENT_PAYLOAD, "numero_documento": "9998887777"},
            headers=other_headers,
        )
        patient_id = create.json()["id"]

        r = client.get(f"/patients/{patient_id}", headers=auth_headers_medico)
        assert r.status_code == 404
