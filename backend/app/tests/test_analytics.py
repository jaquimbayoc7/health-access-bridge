"""
HU-08 — Pruebas del dashboard de analisis (GET /analytics/summary y /analytics/filters).

Cada prueba crea sus propios medicos con correos unicos para aislar sus pacientes del resto de la base de pruebas
compartida (SQLite de sesion).
"""
import itertools
import json

import pytest

from app import crud, models, schemas

_n = itertools.count(1)


def _login(client, email, password="pass12345"):
    r = client.post("/users/login", data={"username": email, "password": password})
    assert r.status_code == 200
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.fixture
def doctor(db):
    k = next(_n)
    return crud.create_user(db, schemas.UserCreate(
        email=f"analytics{k}@test.com", password="pass12345", full_name=f"Medico Analitica {k}", role="médico"))


@pytest.fixture
def doctor_headers(client, doctor):
    return _login(client, doctor.email)


def _patient(db, owner, edad=40, genero="Femenino", causa="Enfermedad general", fisica="Moderada",
             psico="Leve", niveles=(10, 20, 30, 40, 50, 60), nivel_global=35, perfil=None, active=True):
    k = next(_n)
    p = crud.create_user_patient(db, schemas.PatientCreate(
        numero_documento=f"9{k:09d}", nombre_apellidos=f"Nombre Secreto {k}", fecha_nacimiento="1980-01-01",
        edad=edad, genero=genero, orientacion_sexual="No informa", causa_deficiencia=causa,
        cat_fisica=fisica, cat_psicosocial=psico,
        nivel_d1=niveles[0], nivel_d2=niveles[1], nivel_d3=niveles[2], nivel_d4=niveles[3],
        nivel_d5=niveles[4], nivel_d6=niveles[5], nivel_global=nivel_global), owner.id)
    if perfil is not None:
        crud.update_patient_prediction(db, p.id, perfil, f"Perfil {perfil}")
    if not active:
        p.is_active = False
        db.commit()
    return p


def _icf(db, patient, items, model="gemma4:e4b"):
    result = {"model": model, "functions": [], "structures": [], "activities": []}
    key = {"b": "functions", "s": "structures", "d": "activities"}
    for comp, code, title in items:
        result[key[comp]].append({"code": code, "title": title, "qualifier": 3, "origin": "llm"})
    return crud.create_icf_batch(db, patient.id, result, None, None)


def _decide(db, row, status):
    row.status = status
    db.commit()


def _count(entries, key):
    return next((e["count"] for e in entries if e["key"] == key), 0)


class TestAuthAndPrivacy:
    def test_requires_authentication(self, client):
        assert client.get("/analytics/summary").status_code == 401
        assert client.get("/analytics/filters").status_code == 401

    def test_summary_never_exposes_identifying_data(self, client, db, doctor, doctor_headers):
        p = _patient(db, doctor)
        body = client.get("/analytics/summary", headers=doctor_headers).json()
        text = json.dumps(body, ensure_ascii=False)
        for secret in (p.nombre_apellidos, p.numero_documento, "No informa", "1980-01-01", doctor.email):
            assert secret not in text

    def test_doctor_cannot_filter_by_owner(self, client, doctor, doctor_headers):
        r = client.get(f"/analytics/summary?owner_id={doctor.id}", headers=doctor_headers)
        assert r.status_code == 403


class TestScope:
    def test_doctor_only_sees_own_patients(self, client, db, doctor, doctor_headers):
        other = crud.create_user(db, schemas.UserCreate(
            email=f"otro{next(_n)}@test.com", password="pass12345", full_name="Otro", role="médico"))
        _patient(db, doctor)
        _patient(db, doctor)
        _patient(db, other)
        body = client.get("/analytics/summary", headers=doctor_headers).json()
        assert body["scope"] == "propio"
        assert body["totals"]["patients"] == 2

    def test_admin_sees_everyone_and_can_filter_by_owner(self, client, db, doctor, auth_headers_admin):
        _patient(db, doctor)
        _patient(db, doctor)
        _patient(db, doctor)
        everyone = client.get("/analytics/summary", headers=auth_headers_admin).json()
        assert everyone["scope"] == "global"
        assert everyone["totals"]["patients"] >= 3
        mine = client.get(f"/analytics/summary?owner_id={doctor.id}", headers=auth_headers_admin).json()
        assert mine["scope"] == "propio"
        assert mine["totals"]["patients"] == 3

    def test_deleted_patients_are_excluded(self, client, db, doctor, doctor_headers):
        _patient(db, doctor)
        _patient(db, doctor, active=False)
        assert client.get("/analytics/summary", headers=doctor_headers).json()["totals"]["patients"] == 1

    def test_empty_scope_returns_zeros_not_errors(self, client, doctor_headers):
        body = client.get("/analytics/summary", headers=doctor_headers).json()
        assert body["totals"]["patients"] == 0
        assert body["totals"]["mean_age"] is None and body["totals"]["prediction_rate"] is None
        assert body["distributions"]["genero"] == []
        assert all(d["mean"] is None for d in body["domains"])
        assert body["icf"]["suggestions"] == 0 and body["icf"]["acceptance_rate"] is None


class TestAggregates:
    def test_distributions_totals_and_domain_means(self, client, db, doctor, doctor_headers):
        _patient(db, doctor, edad=10, genero="Masculino", fisica="Leve", niveles=(0, 10, 20, 30, 40, 50), nivel_global=20, perfil=0)
        _patient(db, doctor, edad=30, genero="Femenino", fisica="Moderada", niveles=(20, 30, 40, 50, 60, 70), nivel_global=40, perfil=1)
        _patient(db, doctor, edad=65, genero="Femenino", fisica="Moderada", niveles=(40, 50, 60, 70, 80, 90), nivel_global=60)
        body = client.get("/analytics/summary", headers=doctor_headers).json()
        t = body["totals"]
        assert t["patients"] == 3 and t["with_prediction"] == 2
        assert t["prediction_rate"] == pytest.approx(0.6667, abs=1e-4)
        assert t["mean_age"] == pytest.approx(35.0) and t["mean_global_level"] == pytest.approx(40.0)
        d = body["distributions"]
        assert _count(d["genero"], "Femenino") == 2 and _count(d["genero"], "Masculino") == 1
        assert _count(d["profile"], "Perfil 0") == 1 and _count(d["profile"], "Perfil 1") == 1
        assert _count(d["cat_fisica"], "Moderada") == 2 and _count(d["cat_fisica"], "Leve") == 1
        assert [e["key"] for e in d["cat_fisica"]] == ["Leve", "Moderada"]  # orden por gravedad, no alfabetico
        assert [e["key"] for e in d["age_group"]] == ["0-17", "30-44", "60+"]
        means = {x["domain"]: x["mean"] for x in body["domains"]}
        assert means == {"D1": 20.0, "D2": 30.0, "D3": 40.0, "D4": 50.0, "D5": 60.0, "D6": 70.0}

    def test_causes_are_limited_to_the_top_ones(self, client, db, doctor, doctor_headers):
        for i in range(10):
            _patient(db, doctor, causa=f"Causa {i}")
        assert len(client.get("/analytics/summary", headers=doctor_headers).json()["distributions"]["cause"]) == 8


class TestFilters:
    @pytest.fixture
    def populated(self, db, doctor):
        _patient(db, doctor, edad=10, genero="Masculino", causa="Accidente", perfil=0)
        _patient(db, doctor, edad=30, genero="Femenino", causa="Accidente", perfil=1)
        _patient(db, doctor, edad=65, genero="Femenino", causa="Enfermedad general", perfil=1)

    def _total(self, client, headers, query):
        r = client.get(f"/analytics/summary?{query}", headers=headers)
        assert r.status_code == 200
        return r.json()["totals"]["patients"]

    def test_each_filter(self, client, doctor_headers, populated):
        assert self._total(client, doctor_headers, "genero=Femenino") == 2
        assert self._total(client, doctor_headers, "edad_min=20&edad_max=70") == 2
        assert self._total(client, doctor_headers, "causa=Accidente") == 2
        assert self._total(client, doctor_headers, "perfil=1") == 2
        assert self._total(client, doctor_headers, "genero=Femenino&causa=Accidente&perfil=1") == 1

    def test_filters_are_echoed_and_empty_match_is_not_an_error(self, client, doctor_headers, populated):
        body = client.get("/analytics/summary?genero=Inexistente", headers=doctor_headers).json()
        assert body["totals"]["patients"] == 0 and body["filters"] == {"genero": "Inexistente"}

    def test_invalid_ranges_are_rejected(self, client, doctor_headers):
        assert client.get("/analytics/summary?edad_min=50&edad_max=20", headers=doctor_headers).status_code == 422
        assert client.get("/analytics/summary?edad_min=-1", headers=doctor_headers).status_code == 422
        assert client.get("/analytics/summary?perfil=abc", headers=doctor_headers).status_code == 422

    def test_filter_options_only_list_the_users_own_values(self, client, db, doctor, doctor_headers):
        _patient(db, doctor, genero="Femenino", causa="Causa Unica Propia", perfil=2)
        opts = client.get("/analytics/filters", headers=doctor_headers).json()
        assert opts == {"genero": ["Femenino"], "cause": ["Causa Unica Propia"], "profile": [2]}


class TestIcf:
    def test_acceptance_rate_by_component_and_status(self, client, db, doctor, doctor_headers):
        p = _patient(db, doctor)
        rows = _icf(db, p, [("b", "b730", "Fuerza"), ("b", "b280", "Dolor"), ("s", "s750", "Pierna"), ("d", "d450", "Andar")])
        _decide(db, rows[0], "aceptado")
        _decide(db, rows[1], "rechazado")
        _decide(db, rows[2], "editado")
        icf = client.get("/analytics/summary", headers=doctor_headers).json()["icf"]
        assert icf["suggestions"] == 4 and icf["patients_with_profile"] == 1
        assert icf["by_status"] == {"sugerido": 1, "aceptado": 1, "editado": 1, "rechazado": 1}
        assert icf["decided"] == 3 and icf["acceptance_rate"] == pytest.approx(0.6667, abs=1e-4)
        assert icf["by_component"]["b"]["acceptance_rate"] == pytest.approx(0.5)
        assert icf["by_component"]["s"]["acceptance_rate"] == 1.0
        assert icf["by_component"]["d"]["acceptance_rate"] is None  # sin decisiones no hay tasa
        assert icf["by_model"] == [{"key": "gemma4:e4b", "count": 4}]

    def test_regenerating_does_not_double_count(self, client, db, doctor, doctor_headers):
        p = _patient(db, doctor)
        old = _icf(db, p, [("b", "b730", "Fuerza")])
        _decide(db, old[0], "rechazado")
        _icf(db, p, [("b", "b730", "Fuerza"), ("b", "b280", "Dolor")])
        icf = client.get("/analytics/summary", headers=doctor_headers).json()["icf"]
        assert icf["suggestions"] == 2 and icf["by_status"]["rechazado"] == 0  # solo cuenta el ultimo lote

    def test_top_codes_are_ordered_by_frequency(self, client, db, doctor, doctor_headers):
        for _ in range(3):
            row = _icf(db, _patient(db, doctor), [("b", "b730", "Fuerza")])[0]
            _decide(db, row, "aceptado")
        _icf(db, _patient(db, doctor), [("b", "b280", "Dolor")])
        top = client.get("/analytics/summary", headers=doctor_headers).json()["icf"]["top_codes"]
        assert top[0] == {"code": "b730", "title": "Fuerza", "component": "b", "count": 3, "accepted": 3, "rejected": 0}
        assert top[1]["code"] == "b280"

    def test_filters_also_scope_the_icf_block(self, client, db, doctor, doctor_headers):
        _icf(db, _patient(db, doctor, genero="Femenino"), [("b", "b730", "Fuerza")])
        _icf(db, _patient(db, doctor, genero="Masculino"), [("b", "b280", "Dolor"), ("d", "d450", "Andar")])
        icf = client.get("/analytics/summary?genero=Masculino", headers=doctor_headers).json()["icf"]
        assert icf["suggestions"] == 2 and icf["patients_with_profile"] == 1
