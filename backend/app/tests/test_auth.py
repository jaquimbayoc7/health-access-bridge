"""
Tests de integración — HU-01: Autenticación y Control de Acceso (RBAC)
"""


class TestHealthEndpoint:
    def test_health_ok(self, client):
        r = client.get("/health")
        assert r.status_code == 200

    def test_root_ok(self, client):
        r = client.get("/")
        assert r.status_code == 200


class TestLogin:
    def test_login_success_admin(self, client, admin_user):
        r = client.post(
            "/users/login",
            data={"username": "admin@test.com", "password": "adminpass123"},
        )
        assert r.status_code == 200
        body = r.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"

    def test_login_success_medico(self, client, medico_user):
        r = client.post(
            "/users/login",
            data={"username": "medico@test.com", "password": "medicopass123"},
        )
        assert r.status_code == 200
        assert "access_token" in r.json()

    def test_login_wrong_password(self, client, admin_user):
        r = client.post(
            "/users/login",
            data={"username": "admin@test.com", "password": "wrongpass"},
        )
        assert r.status_code == 401

    def test_login_nonexistent_user(self, client):
        r = client.post(
            "/users/login",
            data={"username": "noexiste@test.com", "password": "pass"},
        )
        assert r.status_code == 401

    def test_login_missing_fields(self, client):
        r = client.post("/users/login", data={})
        assert r.status_code == 422


class TestGetCurrentUser:
    def test_me_authenticated(self, client, auth_headers_medico, medico_user):
        r = client.get("/users/me", headers=auth_headers_medico)
        assert r.status_code == 200
        body = r.json()
        assert body["email"] == "medico@test.com"
        assert body["role"] == "médico"

    def test_me_unauthenticated(self, client):
        r = client.get("/users/me")
        assert r.status_code == 401

    def test_me_invalid_token(self, client):
        r = client.get("/users/me", headers={"Authorization": "Bearer token_invalido"})
        assert r.status_code == 401


class TestAdminEndpoints:
    def test_list_users_as_admin(self, client, auth_headers_admin):
        r = client.get("/admin/users", headers=auth_headers_admin)
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_list_users_as_medico_forbidden(self, client, auth_headers_medico):
        r = client.get("/admin/users", headers=auth_headers_medico)
        assert r.status_code == 403

    def test_list_users_unauthenticated(self, client):
        r = client.get("/admin/users")
        assert r.status_code == 401

    def test_register_user_as_admin(self, client, auth_headers_admin):
        r = client.post(
            "/admin/users/register",
            json={
                "email": "nuevo_medico@test.com",
                "password": "pass12345",
                "full_name": "Nuevo Médico",
                "role": "médico",
            },
            headers=auth_headers_admin,
        )
        assert r.status_code in (200, 201)
        body = r.json()
        assert body["email"] == "nuevo_medico@test.com"

    def test_register_duplicate_email(self, client, auth_headers_admin, admin_user):
        r = client.post(
            "/admin/users/register",
            json={
                "email": "admin@test.com",
                "password": "pass12345",
                "full_name": "Otro Admin",
                "role": "admin",
            },
            headers=auth_headers_admin,
        )
        assert r.status_code == 400

    def test_register_user_as_medico_forbidden(self, client, auth_headers_medico):
        r = client.post(
            "/admin/users/register",
            json={
                "email": "otro@test.com",
                "password": "pass12345",
                "full_name": "Otro",
                "role": "médico",
            },
            headers=auth_headers_medico,
        )
        assert r.status_code == 403

    def test_toggle_user_status(self, client, auth_headers_admin, medico_user):
        r = client.patch(
            f"/admin/users/{medico_user.id}/status",
            json={"is_active": False},
            headers=auth_headers_admin,
        )
        assert r.status_code == 200
        assert r.json()["is_active"] is False

        r2 = client.patch(
            f"/admin/users/{medico_user.id}/status",
            json={"is_active": True},
            headers=auth_headers_admin,
        )
        assert r2.status_code == 200
        assert r2.json()["is_active"] is True

    def test_toggle_nonexistent_user(self, client, auth_headers_admin):
        r = client.patch(
            "/admin/users/99999/status",
            json={"is_active": False},
            headers=auth_headers_admin,
        )
        assert r.status_code == 404
