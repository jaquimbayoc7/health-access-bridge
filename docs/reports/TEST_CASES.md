# Casos de Prueba — Health Access Bridge
**Estándar:** Gherkin (BDD — Behaviour Driven Development)  
**Última actualización:** Abril 2026  
**Momento:** 1 (Completado)  
**Total de pruebas:** 53 automatizadas (35 backend · 16 frontend · 2 smoke)

---

## Índice

| Suite | HU | Archivo | Casos |
|-------|----|---------|-------|
| [Smoke Tests CI/CD](#suite-1--smoke-tests-en-producción-hu-11) | HU-11 | `ci-prod.yml` | 2 |
| [Backend — Auth & RBAC](#suite-2--autenticación-y-rbac-hu-12) | HU-12 | `test_auth.py` | 18 |
| [Backend — Pacientes](#suite-3--gestión-de-pacientes-hu-12) | HU-12 | `test_patients.py` | 17 |
| [Frontend — AuthContext](#suite-4--authcontext-hu-13) | HU-13 | `AuthContext.test.tsx` | 4 |
| [Frontend — Login](#suite-5--página-de-login-hu-13) | HU-13 | `Login.test.tsx` | 4 |
| [Frontend — DashboardLayout](#suite-6--dashboardlayout-hu-13) | HU-13 | `DashboardLayout.test.tsx` | 4 |
| [Frontend — Pacientes UI](#suite-7--gestión-de-pacientes-ui-hu-13) | HU-13 | `Patients.test.tsx` | 4 |

---

## Suite 1 — Smoke Tests en Producción (HU-11)

**Archivo:** `.github/workflows/ci-prod.yml` · Job: `api-smoke-tests-prod`  
**Ejecución:** Automática post-deploy en `master`, con espera de 90s para inicialización del contenedor Render  
**Issues:** [#14](https://github.com/jaquimbayoc7/health-access-bridge/issues/14)

```gherkin
Feature: Smoke Tests de Producción
  Como equipo de desarrollo
  Quiero verificar automáticamente que el backend esté disponible después de cada despliegue
  Para garantizar que el servicio de producción responde correctamente

  Background:
    Given el pipeline de CI/CD ejecutó un despliegue exitoso en Render producción
    And han transcurrido al menos 90 segundos desde el inicio del contenedor

  Scenario: TC-S01 — Health check responde HTTP 200
    Given el endpoint de salud está expuesto en GET /health
    When el job smoke test realiza una petición GET a /health
    Then la respuesta debe tener código de estado 200
    And el servicio se considera operativo

  Scenario: TC-S02 — Endpoint de login es alcanzable
    Given el endpoint de autenticación está expuesto en POST /users/login
    When el job smoke test realiza una petición POST a /users/login sin credenciales
    Then la respuesta debe tener código de estado 200, 401 o 422
    And el endpoint no debe retornar un error de red (5xx)
    And el pipeline continúa si todos los checks pasan
```

---

## Suite 2 — Autenticación y RBAC (HU-12)

**Archivo:** `backend/app/tests/test_auth.py`  
**Framework:** pytest · FastAPI TestClient · SQLite en memoria  
**Issues:** [#15](https://github.com/jaquimbayoc7/health-access-bridge/issues/15)

```gherkin
Feature: Sistema de Salud — Endpoints Básicos
  Como sistema de monitoreo
  Quiero verificar que los endpoints de health y root respondan
  Para confirmar que el servidor está activo

  Background:
    Given la base de datos de prueba está inicializada en SQLite en memoria
    And el cliente de prueba FastAPI está disponible

  Scenario: TC-B01 — Health check retorna HTTP 200
    Given el servidor backend está corriendo
    When se realiza una petición GET a /health
    Then la respuesta debe tener código de estado 200

  Scenario: TC-B02 — Root endpoint retorna HTTP 200
    Given el servidor backend está corriendo
    When se realiza una petición GET a /
    Then la respuesta debe tener código de estado 200
```

```gherkin
Feature: Login de Usuarios
  Como usuario del sistema (Admin o Médico)
  Quiero iniciar sesión con mis credenciales
  Para obtener un token JWT y acceder al sistema

  Background:
    Given la base de datos de prueba está inicializada
    And existen los usuarios de prueba: admin@test.com (admin) y medico@test.com (médico)

  Scenario: TC-B03 — Login exitoso como Administrador
    Given el usuario "admin@test.com" existe con contraseña "adminpass123" y rol "admin"
    When se realiza POST /users/login con username "admin@test.com" y password "adminpass123"
    Then la respuesta debe tener código de estado 200
    And el cuerpo contiene el campo "access_token"
    And el campo "token_type" es "bearer"

  Scenario: TC-B04 — Login exitoso como Médico
    Given el usuario "medico@test.com" existe con contraseña "medicopass123" y rol "médico"
    When se realiza POST /users/login con username "medico@test.com" y password "medicopass123"
    Then la respuesta debe tener código de estado 200
    And el cuerpo contiene el campo "access_token"

  Scenario: TC-B05 — Login con contraseña incorrecta
    Given el usuario "admin@test.com" existe en el sistema
    When se realiza POST /users/login con username "admin@test.com" y password "wrongpass"
    Then la respuesta debe tener código de estado 401

  Scenario: TC-B06 — Login con usuario inexistente
    Given el email "noexiste@test.com" no está registrado en el sistema
    When se realiza POST /users/login con username "noexiste@test.com" y password "pass"
    Then la respuesta debe tener código de estado 401

  Scenario: TC-B07 — Login sin campos requeridos
    Given el endpoint /users/login requiere username y password
    When se realiza POST /users/login con un body vacío {}
    Then la respuesta debe tener código de estado 422
    And el cuerpo contiene los errores de validación de campos faltantes
```

```gherkin
Feature: Perfil del Usuario Autenticado
  Como usuario autenticado
  Quiero consultar mi perfil actual
  Para verificar mis datos de sesión

  Background:
    Given el usuario "medico@test.com" está autenticado y tiene un token JWT válido

  Scenario: TC-B08 — Obtener perfil con token válido
    Given el header Authorization contiene un Bearer token válido
    When se realiza GET /users/me con el header de autenticación
    Then la respuesta debe tener código de estado 200
    And el cuerpo contiene "email" con valor "medico@test.com"
    And el cuerpo contiene "role" con valor "médico"

  Scenario: TC-B09 — Acceso sin token es rechazado
    Given no se envía header Authorization
    When se realiza GET /users/me sin autenticación
    Then la respuesta debe tener código de estado 401

  Scenario: TC-B10 — Acceso con token inválido es rechazado
    Given el header Authorization contiene "Bearer token_invalido"
    When se realiza GET /users/me con el token inválido
    Then la respuesta debe tener código de estado 401
```

```gherkin
Feature: Gestión de Usuarios — Endpoints Admin
  Como administrador del sistema
  Quiero gestionar los usuarios de la plataforma
  Para controlar el acceso al sistema

  Background:
    Given existen los usuarios: admin@test.com (admin) y medico@test.com (médico)
    And el administrador tiene un token JWT válido con rol "admin"
    And el médico tiene un token JWT válido con rol "médico"

  Scenario: TC-B11 — Admin lista todos los usuarios
    Given el header contiene el token del administrador
    When se realiza GET /admin/users
    Then la respuesta debe tener código de estado 200
    And el cuerpo es una lista (array JSON)

  Scenario: TC-B12 — Médico no puede listar usuarios (403 Forbidden)
    Given el header contiene el token del médico
    When se realiza GET /admin/users
    Then la respuesta debe tener código de estado 403

  Scenario: TC-B13 — Acceso sin autenticación a /admin/users es rechazado
    Given no se envía header Authorization
    When se realiza GET /admin/users
    Then la respuesta debe tener código de estado 401

  Scenario: TC-B14 — Admin registra un nuevo usuario
    Given el header contiene el token del administrador
    When se realiza POST /admin/users/register con body:
      | campo      | valor                    |
      | email      | nuevo_medico@test.com    |
      | password   | pass12345                |
      | full_name  | Nuevo Médico             |
      | role       | médico                   |
    Then la respuesta debe tener código de estado 200 o 201
    And el cuerpo contiene "email" con valor "nuevo_medico@test.com"

  Scenario: TC-B15 — Registro rechaza email duplicado
    Given el usuario "admin@test.com" ya existe en el sistema
    When se realiza POST /admin/users/register con email "admin@test.com"
    Then la respuesta debe tener código de estado 400

  Scenario: TC-B16 — Médico no puede registrar usuarios (403 Forbidden)
    Given el header contiene el token del médico
    When se realiza POST /admin/users/register con datos de un nuevo usuario
    Then la respuesta debe tener código de estado 403

  Scenario: TC-B17 — Admin desactiva y reactiva un usuario
    Given el médico "medico@test.com" está activo (is_active: true)
    When se realiza PATCH /admin/users/{id}/status con body {"is_active": false}
    Then la respuesta debe tener código de estado 200
    And el cuerpo contiene "is_active" con valor false
    When se realiza PATCH /admin/users/{id}/status con body {"is_active": true}
    Then la respuesta debe tener código de estado 200
    And el cuerpo contiene "is_active" con valor true

  Scenario: TC-B18 — Toggle de usuario inexistente retorna 404
    Given el usuario con id 99999 no existe en el sistema
    When se realiza PATCH /admin/users/99999/status con body {"is_active": false}
    Then la respuesta debe tener código de estado 404
```

---

## Suite 3 — Gestión de Pacientes (HU-12)

**Archivo:** `backend/app/tests/test_patients.py`  
**Framework:** pytest · FastAPI TestClient · SQLite en memoria  
**Issues:** [#15](https://github.com/jaquimbayoc7/health-access-bridge/issues/15)

```gherkin
Feature: Control de Acceso a Pacientes
  Como sistema de control de acceso
  Quiero verificar que solo los roles autorizados puedan acceder a los pacientes
  Para garantizar la seguridad de los datos clínicos

  Background:
    Given la base de datos de prueba está inicializada
    And el médico "medico@test.com" tiene token JWT válido
    And el administrador "admin@test.com" tiene token JWT válido

  Scenario: TC-B19 — Listar pacientes sin autenticación es rechazado
    Given no se envía header Authorization
    When se realiza GET /patients/
    Then la respuesta debe tener código de estado 401

  Scenario: TC-B20 — Administrador no puede listar pacientes directamente (403)
    Given el header contiene el token del administrador
    When se realiza GET /patients/ con el token de admin
    Then la respuesta debe tener código de estado 403

  Scenario: TC-B21 — Crear paciente sin autenticación es rechazado
    Given no se envía header Authorization
    When se realiza POST /patients/ con un payload válido de paciente
    Then la respuesta debe tener código de estado 401
```

```gherkin
Feature: CRUD Completo de Pacientes
  Como médico autenticado
  Quiero crear, consultar, actualizar y eliminar pacientes
  Para gestionar la historia clínica de mis pacientes

  Background:
    Given el médico "medico@test.com" tiene token JWT válido
    And el sistema tiene disponible el payload de paciente de prueba con documento "1234567890"

  Scenario: TC-B22 — Médico crea un nuevo paciente
    Given el header contiene el token del médico
    When se realiza POST /patients/ con el payload de paciente válido
    Then la respuesta debe tener código de estado 200 o 201
    And el cuerpo contiene "nombre_apellidos" con el valor del payload
    And el cuerpo contiene "numero_documento" con el valor del payload
    And el cuerpo contiene un campo "id" generado automáticamente

  Scenario: TC-B23 — Médico lista sus pacientes
    Given el header contiene el token del médico
    When se realiza GET /patients/
    Then la respuesta debe tener código de estado 200
    And el cuerpo es una lista (array JSON)

  Scenario: TC-B24 — Médico solo ve sus propios pacientes (aislamiento)
    Given existe un segundo médico "otro_medico_isolation@test.com" sin pacientes registrados
    And el segundo médico tiene token JWT válido
    When el segundo médico realiza GET /patients/
    Then la respuesta debe tener código de estado 200
    And el cuerpo es una lista vacía []

  Scenario: TC-B25 — Médico obtiene paciente por ID
    Given el médico creó previamente un paciente y obtuvo su {patient_id}
    When se realiza GET /patients/{patient_id} con el token del médico
    Then la respuesta debe tener código de estado 200
    And el cuerpo contiene "id" con valor {patient_id}

  Scenario: TC-B26 — Consultar paciente inexistente retorna 404
    Given el paciente con id 99999 no existe en el sistema
    When se realiza GET /patients/99999 con el token del médico
    Then la respuesta debe tener código de estado 404

  Scenario: TC-B27 — Médico actualiza la historia clínica de un paciente
    Given el médico creó previamente un paciente y obtuvo su {patient_id}
    When se realiza PUT /patients/{patient_id} con "nombre_apellidos": "Juan Pérez Actualizado"
    Then la respuesta debe tener código de estado 200
    And el cuerpo contiene "nombre_apellidos" con valor "Juan Pérez Actualizado"

  Scenario: TC-B28 — Médico elimina un paciente (soft delete)
    Given el médico creó previamente un paciente y obtuvo su {patient_id}
    When se realiza DELETE /patients/{patient_id} con el token del médico
    Then la respuesta debe tener código de estado 200
    When se realiza GET /patients/{patient_id}
    Then la respuesta debe tener código de estado 404

  Scenario: TC-B29 — Eliminar paciente inexistente retorna 404
    Given el paciente con id 99999 no existe en el sistema
    When se realiza DELETE /patients/99999 con el token del médico
    Then la respuesta debe tener código de estado 404
```

```gherkin
Feature: Búsqueda de Pacientes
  Como médico autenticado
  Quiero buscar pacientes por nombre o número de documento
  Para encontrar rápidamente a un paciente específico

  Background:
    Given el médico "medico@test.com" tiene token JWT válido
    And ha registrado previamente pacientes de prueba en el sistema

  Scenario: TC-B30 — Buscar paciente por nombre
    Given el médico registró el paciente "María López Search" con documento "2009990001"
    When se realiza GET /patients/?search=María López
    Then la respuesta debe tener código de estado 200
    And el resultado contiene al menos un paciente cuyo nombre incluye "María"

  Scenario: TC-B31 — Buscar paciente por número de documento
    Given el médico registró el paciente "Carlos Ruiz Search" con documento "3001112222"
    When se realiza GET /patients/?search=3001112222
    Then la respuesta debe tener código de estado 200
    And el resultado contiene al menos un paciente con "numero_documento" igual a "3001112222"

  Scenario: TC-B32 — Búsqueda sin resultados retorna lista vacía
    Given no existe ningún paciente con términos "xyzNoExiste999"
    When se realiza GET /patients/?search=xyzNoExiste999
    Then la respuesta debe tener código de estado 200
    And el cuerpo es una lista vacía []

  Scenario: TC-B33 — Búsqueda con query vacío retorna todos los pacientes
    Given el médico tiene pacientes registrados
    When se realiza GET /patients/ sin parámetro de búsqueda
    And se realiza GET /patients/?search= con búsqueda vacía
    Then ambas respuestas deben tener código de estado 200
    And ambas respuestas deben retornar el mismo número de pacientes
```

```gherkin
Feature: Propiedad y Aislamiento de Pacientes entre Médicos
  Como sistema de seguridad clínica
  Quiero asegurar que un médico no pueda acceder a los pacientes de otro médico
  Para proteger la privacidad de los datos clínicos (RBAC por propiedad)

  Background:
    Given existen dos médicos distintos en el sistema
    And cada médico tiene su propio token JWT válido

  Scenario: TC-B35 — Médico no puede acceder al paciente de otro médico
    Given el médico "owner_test@test.com" creó un paciente con documento "9998887777"
    And el médico "owner_test@test.com" es el owner del paciente {patient_id}
    When el médico "medico@test.com" realiza GET /patients/{patient_id}
    Then la respuesta debe tener código de estado 404
    And el paciente no es accesible por un médico que no sea su owner
```

---

## Suite 4 — AuthContext (HU-13)

**Archivo:** `frontend/src/__tests__/AuthContext.test.tsx`  
**Framework:** Vitest · React Testing Library · renderHook · MemoryRouter  
**Issues:** [#16](https://github.com/jaquimbayoc7/health-access-bridge/issues/16)

```gherkin
Feature: Contexto de Autenticación (AuthContext)
  Como usuario de la aplicación React
  Quiero que el estado de autenticación sea gestionado correctamente por el contexto
  Para que mi sesión persista y mis datos estén disponibles en toda la app

  Background:
    Given el AuthProvider envuelve la aplicación en un MemoryRouter
    And el servicio apiService está mockeado (login, getCurrentUser, setToken, clearToken)
    And el localStorage está limpio antes de cada test

  Scenario: TC-F01 — Estado inicial sin sesión activa
    Given no existe token ni usuario en localStorage
    When se renderiza el hook useAuth()
    And el estado de carga (isLoading) resuelve a false
    Then el usuario (user) debe ser null

  Scenario: TC-F02 — Login almacena usuario en estado y localStorage
    Given apiService.login responde con { access_token: "test-token", token_type: "bearer" }
    And apiService.getCurrentUser responde con { id: 1, email: "admin@hab.co", role: "admin" }
    When se llama result.current.login("admin@hab.co", "adminpassword")
    Then result.current.user no debe ser null
    And result.current.user.email debe ser "admin@hab.co"
    And localStorage debe contener la clave "user" con el perfil del usuario

  Scenario: TC-F03 — Logout limpia estado y localStorage
    Given existe "authToken" y "user" en localStorage con una sesión activa de "medico@hab.co"
    When se llama result.current.logout()
    Then result.current.user debe ser null
    And localStorage no debe contener la clave "authToken"
    And localStorage no debe contener la clave "user"

  Scenario: TC-F04 — Credenciales inválidas no actualizan el estado de usuario
    Given apiService.login responde con un error "Unauthorized"
    When se llama result.current.login("bad@email.com", "wrongpassword")
    Then la función debe lanzar una excepción
    And result.current.user debe permanecer null
```

---

## Suite 5 — Página de Login (HU-13)

**Archivo:** `frontend/src/__tests__/Login.test.tsx`  
**Framework:** Vitest · React Testing Library · userEvent · MemoryRouter  
**Issues:** [#16](https://github.com/jaquimbayoc7/health-access-bridge/issues/16)

```gherkin
Feature: Página de Login
  Como usuario no autenticado
  Quiero ver y usar el formulario de inicio de sesión
  Para acceder al sistema con mis credenciales

  Background:
    Given el componente Login se renderiza dentro de un MemoryRouter
    And useAuth devuelve { user: null, login: vi.fn(), isLoading: false }
    And useLanguage devuelve { language: "en", t: (key) => key }

  Scenario: TC-F05 — Formulario muestra los campos de email y contraseña
    Given el usuario accede a la página de login
    When el componente Login se monta
    Then debe existir un elemento con id "email" en el DOM
    And debe existir un elemento con id "password" en el DOM

  Scenario: TC-F06 — Botón de submit se deshabilita durante el proceso de login
    Given useAuth.login devuelve una Promise que nunca resuelve (simula carga)
    And el usuario ingresó "user@test.com" en el campo email
    And el usuario ingresó "password123" en el campo password
    When el usuario hace clic en el botón de login
    Then el botón debe mostrar estado "loading" y estar deshabilitado (disabled)

  Scenario: TC-F07 — Usuario ya autenticado no ve el formulario de login
    Given useAuth devuelve { user: { id: 1, email: "doc@hab.co", role: "médico" } }
    When el componente Login se monta con un usuario ya autenticado
    Then el elemento <form> no debe estar presente en el DOM

  Scenario: TC-F08 — Header contiene el botón de cambio de idioma
    Given el componente Login se renderiza normalmente
    When se obtienen todos los elementos button del DOM
    Then debe haber al menos 2 botones (language toggle + login submit)
```

---

## Suite 6 — DashboardLayout (HU-13)

**Archivo:** `frontend/src/__tests__/DashboardLayout.test.tsx`  
**Framework:** Vitest · React Testing Library · MemoryRouter · Routes  
**Issues:** [#16](https://github.com/jaquimbayoc7/health-access-bridge/issues/16)

```gherkin
Feature: Layout Protegido del Dashboard
  Como usuario de la aplicación
  Quiero que el layout del dashboard proteja las rutas según el estado de autenticación
  Para evitar acceso no autorizado y mostrar la UI correcta según el rol

  Background:
    Given el componente DashboardLayout está configurado como layout de rutas protegidas
    And useLanguage devuelve { language: "en", t: (key) => key }

  Scenario: TC-F09 — Muestra spinner mientras la autenticación está resolviendo
    Given useAuth devuelve { user: null, isLoading: true }
    When el DashboardLayout se monta
    Then debe existir un elemento con clase "animate-spin" en el DOM

  Scenario: TC-F10 — Redirige al usuario no autenticado a /login
    Given useAuth devuelve { user: null, isLoading: false }
    And el usuario intenta navegar a /dashboard
    When el DashboardLayout evalúa el estado de autenticación
    Then el componente de la ruta /login debe renderizarse (data-testid="login-page")
    And el contenido protegido no debe ser visible

  Scenario: TC-F11 — Usuario autenticado ve el contenido protegido (outlet)
    Given useAuth devuelve { user: { id: 1, email: "medico@hab.co", role: "médico" } }
    And el usuario navega a /dashboard
    When el DashboardLayout evalúa el estado de autenticación
    Then el outlet de contenido protegido debe renderizarse (data-testid="protected-content")

  Scenario: TC-F12 — Sidebar muestra "userList" solo a admin, no a médico
    Given existe una lista de items del menú: dashboard, patients, predictions, analytics, predictiveGuide, userList
    When se aplica el filtro de roles para el rol "admin"
    Then la lista filtrada contiene "userList"
    And la lista filtrada NO contiene "patients", "predictions", "analytics", "predictiveGuide"
    When se aplica el filtro de roles para el rol "médico"
    Then la lista filtrada contiene "patients", "predictions", "analytics", "predictiveGuide"
    And la lista filtrada NO contiene "userList"
```

---

## Suite 7 — Gestión de Pacientes UI (HU-13)

**Archivo:** `frontend/src/__tests__/Patients.test.tsx`  
**Framework:** Vitest · React Testing Library · userEvent · MemoryRouter  
**Issues:** [#16](https://github.com/jaquimbayoc7/health-access-bridge/issues/16)

```gherkin
Feature: Gestión de Pacientes — Interfaz de Usuario
  Como médico autenticado en la interfaz web
  Quiero interactuar con la lista de pacientes mediante la UI
  Para buscar, crear y eliminar pacientes desde el navegador

  Background:
    Given el componente Patients se renderiza dentro de un MemoryRouter
    And useAuth devuelve { user: { id: 1, email: "medico@hab.co", role: "médico" } }
    And useLanguage devuelve { language: "en", t: (key) => key }
    And patientService.getPatients está mockeado

  Scenario: TC-F13 — La página de pacientes muestra el campo de búsqueda
    Given patientService.getPatients resuelve con una lista vacía []
    When el componente Patients se monta y la carga finaliza
    Then debe existir un input con placeholder "search" en el DOM

  Scenario: TC-F14 — Muestra mensaje de estado vacío cuando no hay pacientes
    Given patientService.getPatients resuelve con una lista vacía []
    When el componente Patients renderiza la lista
    Then debe existir en el DOM el texto "noPatientsYet"

  Scenario: TC-F15 — Botón "Agregar Paciente" abre el diálogo de creación
    Given patientService.getPatients resuelve con una lista vacía []
    And el componente Patients está montado y cargado
    When el usuario hace clic en el botón "addPatient"
    Then debe aparecer en el DOM un elemento con role "dialog"

  Scenario: TC-F16 — Clic en el ícono de eliminar activa el AlertDialog de confirmación
    Given patientService.getPatients resuelve con el paciente { nombre_apellidos: "Juan Pérez", id: 1 }
    When el componente Patients carga y muestra al paciente "Juan Pérez"
    And el usuario hace clic en el botón de ícono de eliminar (SVG, sin texto)
    Then debe aparecer en el DOM un elemento con role "alertdialog"
```

---

## Trazabilidad de Pruebas

| Código | Historia de Usuario | Suite | Archivo Fuente | Estado |
|--------|--------------------|----|----------------|--------|
| TC-S01 | HU-11 Smoke Tests | Smoke | `ci-prod.yml` | ✅ Pasando |
| TC-S02 | HU-11 Smoke Tests | Smoke | `ci-prod.yml` | ✅ Pasando |
| TC-B01 | HU-12 Backend | Auth | `test_auth.py::TestHealthEndpoint` | ✅ Pasando |
| TC-B02 | HU-12 Backend | Auth | `test_auth.py::TestHealthEndpoint` | ✅ Pasando |
| TC-B03 | HU-12 Backend | Auth | `test_auth.py::TestLogin` | ✅ Pasando |
| TC-B04 | HU-12 Backend | Auth | `test_auth.py::TestLogin` | ✅ Pasando |
| TC-B05 | HU-12 Backend | Auth | `test_auth.py::TestLogin` | ✅ Pasando |
| TC-B06 | HU-12 Backend | Auth | `test_auth.py::TestLogin` | ✅ Pasando |
| TC-B07 | HU-12 Backend | Auth | `test_auth.py::TestLogin` | ✅ Pasando |
| TC-B08 | HU-12 Backend | Auth | `test_auth.py::TestGetCurrentUser` | ✅ Pasando |
| TC-B09 | HU-12 Backend | Auth | `test_auth.py::TestGetCurrentUser` | ✅ Pasando |
| TC-B10 | HU-12 Backend | Auth | `test_auth.py::TestGetCurrentUser` | ✅ Pasando |
| TC-B11 | HU-12 Backend | Admin | `test_auth.py::TestAdminEndpoints` | ✅ Pasando |
| TC-B12 | HU-12 Backend | Admin | `test_auth.py::TestAdminEndpoints` | ✅ Pasando |
| TC-B13 | HU-12 Backend | Admin | `test_auth.py::TestAdminEndpoints` | ✅ Pasando |
| TC-B14 | HU-12 Backend | Admin | `test_auth.py::TestAdminEndpoints` | ✅ Pasando |
| TC-B15 | HU-12 Backend | Admin | `test_auth.py::TestAdminEndpoints` | ✅ Pasando |
| TC-B16 | HU-12 Backend | Admin | `test_auth.py::TestAdminEndpoints` | ✅ Pasando |
| TC-B17 | HU-12 Backend | Admin | `test_auth.py::TestAdminEndpoints` | ✅ Pasando |
| TC-B18 | HU-12 Backend | Admin | `test_auth.py::TestAdminEndpoints` | ✅ Pasando |
| TC-B19 | HU-12 Backend | Patients | `test_patients.py::TestPatientsAuth` | ✅ Pasando |
| TC-B20 | HU-12 Backend | Patients | `test_patients.py::TestPatientsAuth` | ✅ Pasando |
| TC-B21 | HU-12 Backend | Patients | `test_patients.py::TestPatientsAuth` | ✅ Pasando |
| TC-B22 | HU-12 Backend | CRUD | `test_patients.py::TestPatientCRUD` | ✅ Pasando |
| TC-B23 | HU-12 Backend | CRUD | `test_patients.py::TestPatientCRUD` | ✅ Pasando |
| TC-B24 | HU-12 Backend | CRUD | `test_patients.py::TestPatientCRUD` | ✅ Pasando |
| TC-B25 | HU-12 Backend | CRUD | `test_patients.py::TestPatientCRUD` | ✅ Pasando |
| TC-B26 | HU-12 Backend | CRUD | `test_patients.py::TestPatientCRUD` | ✅ Pasando |
| TC-B27 | HU-12 Backend | CRUD | `test_patients.py::TestPatientCRUD` | ✅ Pasando |
| TC-B28 | HU-12 Backend | CRUD | `test_patients.py::TestPatientCRUD` | ✅ Pasando |
| TC-B29 | HU-12 Backend | CRUD | `test_patients.py::TestPatientCRUD` | ✅ Pasando |
| TC-B30 | HU-12 Backend | Search | `test_patients.py::TestPatientSearch` | ✅ Pasando |
| TC-B31 | HU-12 Backend | Search | `test_patients.py::TestPatientSearch` | ✅ Pasando |
| TC-B32 | HU-12 Backend | Search | `test_patients.py::TestPatientSearch` | ✅ Pasando |
| TC-B33 | HU-12 Backend | Search | `test_patients.py::TestPatientSearch` | ✅ Pasando |
| TC-B35 | HU-12 Backend | Ownership | `test_patients.py::TestPatientOwnership` | ✅ Pasando |
| TC-F01 | HU-13 Frontend | AuthContext | `AuthContext.test.tsx` | ✅ Pasando |
| TC-F02 | HU-13 Frontend | AuthContext | `AuthContext.test.tsx` | ✅ Pasando |
| TC-F03 | HU-13 Frontend | AuthContext | `AuthContext.test.tsx` | ✅ Pasando |
| TC-F04 | HU-13 Frontend | AuthContext | `AuthContext.test.tsx` | ✅ Pasando |
| TC-F05 | HU-13 Frontend | Login | `Login.test.tsx` | ✅ Pasando |
| TC-F06 | HU-13 Frontend | Login | `Login.test.tsx` | ✅ Pasando |
| TC-F07 | HU-13 Frontend | Login | `Login.test.tsx` | ✅ Pasando |
| TC-F08 | HU-13 Frontend | Login | `Login.test.tsx` | ✅ Pasando |
| TC-F09 | HU-13 Frontend | Dashboard | `DashboardLayout.test.tsx` | ✅ Pasando |
| TC-F10 | HU-13 Frontend | Dashboard | `DashboardLayout.test.tsx` | ✅ Pasando |
| TC-F11 | HU-13 Frontend | Dashboard | `DashboardLayout.test.tsx` | ✅ Pasando |
| TC-F12 | HU-13 Frontend | Dashboard | `DashboardLayout.test.tsx` | ✅ Pasando |
| TC-F13 | HU-13 Frontend | Patients UI | `Patients.test.tsx` | ✅ Pasando |
| TC-F14 | HU-13 Frontend | Patients UI | `Patients.test.tsx` | ✅ Pasando |
| TC-F15 | HU-13 Frontend | Patients UI | `Patients.test.tsx` | ✅ Pasando |
| TC-F16 | HU-13 Frontend | Patients UI | `Patients.test.tsx` | ✅ Pasando |

---

## Resumen de Cobertura

| Componente | Tests | Estado |
|-----------|-------|--------|
| `/health` · `/` (system) | 2 | ✅ 100% |
| `POST /users/login` (auth) | 5 | ✅ 100% |
| `GET /users/me` (JWT) | 3 | ✅ 100% |
| `/admin/users` (RBAC admin) | 8 | ✅ 100% |
| `/patients/` (acceso auth) | 3 | ✅ 100% |
| `/patients/` CRUD | 8 | ✅ 100% |
| `/patients/?search=` | 4 | ✅ 100% |
| Aislamiento por médico | 1 | ✅ 100% |
| `AuthContext` React | 4 | ✅ 100% |
| `Login` page | 4 | ✅ 100% |
| `DashboardLayout` | 4 | ✅ 100% |
| `Patients` page UI | 4 | ✅ 100% |
| Smoke Tests CI/CD | 2 | ✅ 100% |
| **TOTAL** | **53** | **✅ 100%** |
