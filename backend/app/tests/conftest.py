"""
Fixtures compartidos para los tests de integración de Health Access Bridge.
Usa SQLite en memoria para aislar los tests del entorno real.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base
from app import dependencies, crud, schemas

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def override_dependency():
    app.dependency_overrides[dependencies.get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def admin_user(db):
    existing = crud.get_user_by_email(db, "admin@test.com")
    if existing:
        return existing
    user_in = schemas.UserCreate(
        email="admin@test.com",
        password="adminpass123",
        full_name="Admin Test",
        role="admin",
    )
    return crud.create_user(db, user_in)


@pytest.fixture
def medico_user(db):
    existing = crud.get_user_by_email(db, "medico@test.com")
    if existing:
        return existing
    user_in = schemas.UserCreate(
        email="medico@test.com",
        password="medicopass123",
        full_name="Médico Test",
        role="médico",
    )
    return crud.create_user(db, user_in)


@pytest.fixture
def admin_token(client, admin_user):
    response = client.post(
        "/users/login",
        data={"username": "admin@test.com", "password": "adminpass123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def medico_token(client, medico_user):
    response = client.post(
        "/users/login",
        data={"username": "medico@test.com", "password": "medicopass123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_headers_admin(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def auth_headers_medico(medico_token):
    return {"Authorization": f"Bearer {medico_token}"}


PATIENT_PAYLOAD = {
    "nombre_apellidos": "Juan Pérez García",
    "numero_documento": "1001234567",
    "fecha_nacimiento": "1990-05-15",
    "edad": 34,
    "genero": "masculino",
    "orientacion_sexual": "heterosexual",
    "causa_deficiencia": "Enfermedad general",
    "cat_fisica": "Sí",
    "cat_psicosocial": "No",
    "nivel_d1": 70,
    "nivel_d2": 60,
    "nivel_d3": 80,
    "nivel_d4": 50,
    "nivel_d5": 65,
    "nivel_d6": 75,
    "nivel_global": 67,
}
