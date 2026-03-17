# Health Access Bridge — Frontend

## Descripción General

**Health Access Bridge** es un sistema inteligente de perfilamiento de discapacidad diseñado para profesionales de la salud. Permite evaluar y predecir barreras en personas con discapacidad mediante modelos híbridos de inteligencia artificial (Machine Learning). El frontend se conecta a una API REST desarrollada en FastAPI ([HybridModelDisability](https://github.com/jaquimbayoc7/HybridModelDisability)).

**URL de producción:** https://assist-reach-aid.lovable.app  
**API Backend:** https://hybridmodeldisability.onrender.com

---

## Tecnologías Utilizadas

| Tecnología | Uso |
|---|---|
| React 18 + TypeScript | Framework principal del frontend |
| Vite | Bundler y servidor de desarrollo |
| Tailwind CSS | Estilos y diseño responsivo |
| shadcn/ui | Componentes de interfaz reutilizables |
| React Router DOM | Navegación SPA con rutas protegidas |
| Recharts | Gráficas interactivas (pie charts, bar charts) |
| TanStack React Query | Gestión de estado del servidor |
| jsPDF + jspdf-autotable | Exportación de reportes en PDF |
| xlsx | Exportación de datos en Excel |
| Sonner | Notificaciones toast |
| Lucide React | Iconografía |

---

## Arquitectura del Proyecto

```
src/
├── assets/                  # Imágenes (hero, perfiles predictivos)
├── components/
│   ├── dashboard/           # MetricCard (tarjetas de métricas)
│   ├── layout/              # DashboardLayout, Header, AppSidebar
│   ├── ui/                  # Componentes shadcn/ui (button, card, table, etc.)
│   └── NavLink.tsx          # Componente de navegación activa
├── contexts/
│   ├── AuthContext.tsx       # Autenticación (login, logout, JWT)
│   └── LanguageContext.tsx   # Internacionalización (ES/EN)
├── hooks/                   # Custom hooks (use-mobile, use-toast)
├── pages/                   # Páginas principales de la aplicación
│   ├── LoginLanding.tsx     # Landing page + login
│   ├── Dashboard.tsx        # Panel principal
│   ├── Patients.tsx         # Gestión de pacientes (CRUD)
│   ├── Predictions.tsx      # Ejecución de predicciones IA
│   ├── Analytics.tsx        # Gráficas y estadísticas
│   ├── PredictiveGuide.tsx  # Guía de interpretación de perfiles
│   ├── AdminPanel.tsx       # Panel de administración de usuarios
│   ├── Settings.tsx         # Configuración (en desarrollo)
│   └── NotFound.tsx         # Página 404
├── services/
│   ├── api.ts               # Servicio de autenticación y admin (JWT, usuarios)
│   └── patients.ts          # Servicio de pacientes y predicciones
├── App.tsx                  # Enrutamiento principal
└── main.tsx                 # Punto de entrada
```

---

## Roles de Usuario

El sistema maneja **dos roles** con vistas diferenciadas:

| Rol | Acceso |
|---|---|
| **Médico** | Dashboard, Pacientes, Predicciones, Analíticas, Guía Predictiva, Configuración |
| **Administrador** | Dashboard (métricas de usuarios), Panel de Administración (CRUD de usuarios) |

---

## Flujo General de la Aplicación

### 1. Autenticación

```
Usuario → /login → Ingresa credenciales → API /users/login (OAuth2) → JWT Token
                                                                      ↓
                                                            Decodifica token (role)
                                                                      ↓
                                                   Admin → /admin  |  Médico → /dashboard
```

- El token JWT se almacena en `localStorage` y se envía como `Bearer` en cada petición.
- Al cerrar sesión se limpia el token y se redirige a `/login`.

---

## Pantallas Detalladas

### 🔐 Login Landing (`/login`)

**Archivo:** `src/pages/LoginLanding.tsx`

Página de aterrizaje que combina información del proyecto con el formulario de inicio de sesión.

**Secciones:**
- **Header:** Logo "Health Access Bridge" + selector de idioma (ES/EN).
- **Hero Section:** Título descriptivo del sistema, características clave (IA Predictiva, Gestión de Pacientes) e imagen representativa.
- **Formulario de Login:** Tabs para alternar entre acceso "Médico" y "Administrador". Campos de correo electrónico y contraseña. Envía credenciales a `POST /users/login` (formato `application/x-www-form-urlencoded`).
- **Footer:** Créditos del desarrollador.

**Comportamiento:** Si el usuario ya está autenticado, redirige automáticamente a `/dashboard`.

---

### 📊 Dashboard (`/dashboard`)

**Archivo:** `src/pages/Dashboard.tsx`

Panel principal con métricas y resúmenes en tiempo real. **La vista cambia según el rol:**

#### Vista Médico:
- **3 tarjetas métricas:** Total de pacientes, Predicciones realizadas, Tasa de éxito (%).
- **Pacientes recientes:** Lista de los últimos 5 pacientes registrados con nombre, edad, género y fecha de nacimiento.
- **Historial de predicciones:** Últimas 10 predicciones con nombre del paciente, descripción y badge de perfil (coloreado por nivel: verde ≤3, amarillo ≤6, rojo >6).

#### Vista Administrador:
- **3 tarjetas métricas:** Total de usuarios, Usuarios activos, Usuarios inactivos.
- **Gráfico de torta — Distribución por Rol:** Muestra proporción de administradores vs médicos.
- **Gráfico de torta — Estado de Usuarios:** Muestra proporción de usuarios activos vs inactivos.

---

### 👥 Pacientes (`/patients`) — Solo Médicos

**Archivo:** `src/pages/Patients.tsx`

Gestión completa de pacientes (CRUD) con diseño responsivo.

**Funcionalidades:**
- **Barra de búsqueda:** Filtrado en tiempo real por nombre.
- **Botones de exportación:** Descarga en Excel (.xlsx) y PDF con encabezado de reporte (fecha, hora, médico tratante).
- **Tabla de pacientes (desktop):** Columnas: Nombre, Edad, Género, Causa de Deficiencia, Categoría Física, Categoría Psicosocial, Nivel Global, Acciones (editar/eliminar).
- **Tarjetas de pacientes (móvil):** Vista adaptada con la misma información en formato card.
- **Diálogo de creación/edición:** Formulario completo con campos: nombre, fecha de nacimiento (calcula edad automáticamente), género, orientación sexual, causa de deficiencia, categorías física y psicosocial, niveles D1-D6 (0-100) y nivel global.
- **Confirmación de eliminación:** AlertDialog antes de eliminar un paciente.

**Endpoints consumidos:**
- `GET /patients/` — Listar pacientes
- `POST /patients/` — Crear paciente
- `PUT /patients/{id}` — Actualizar paciente
- `DELETE /patients/{id}` — Eliminar paciente

---

### 🧠 Predicciones (`/predictions`) — Solo Médicos

**Archivo:** `src/pages/Predictions.tsx`

Módulo para ejecutar predicciones de barreras de discapacidad usando el modelo de IA del backend.

**Secciones:**
- **Nueva Predicción:** Selector de paciente → muestra información resumida (nombre, edad, género, nivel global) → botón "Ejecutar Predicción" que envía los datos al modelo.
- **Historial de Predicciones:** Lista de pacientes con predicción completada, mostrando nombre, descripción del resultado y badge de perfil coloreado (0=verde, 1=azul, 2=amarillo, 3=naranja, 4=rojo).

**Endpoint consumido:**
- `POST /patients/{id}/predict` — Ejecutar predicción IA

---

### 📈 Analíticas (`/analytics`) — Solo Médicos

**Archivo:** `src/pages/Analytics.tsx`

Visualización de datos agregados sobre las predicciones realizadas.

**Gráficas:**
- **Distribución de Perfiles de Predicción:** Gráfico de torta que muestra la cantidad de pacientes por perfil (0, 1, 2) con porcentajes.

**Resumen Estadístico (4 métricas):**
- Total de pacientes
- Pacientes con predicciones
- Perfil promedio
- Nivel global promedio

---

### 📖 Guía Predictiva (`/predictive-guide`) — Solo Médicos

**Archivo:** `src/pages/PredictiveGuide.tsx`

Documentación clínica para interpretar los perfiles predictivos generados por el modelo de IA.

**Contenido por perfil (0, 1, 2):**
- **Perfil 0 — Barreras Bajas:** Paciente con alta funcionalidad y autonomía. Estrategias de refuerzo y prevención.
- **Perfil 1 — Barreras Moderadas/Mixtas:** Dificultades concentradas en áreas específicas. Intervenciones focalizadas.
- **Perfil 2 — Barreras Altas y Generalizadas:** Impacto significativo y transversal. Enfoque multidisciplinario.

Cada perfil incluye: imagen ilustrativa, interpretación clínica, características posibles y sugerencias de apoyo.

---

### 🔧 Panel de Administración (`/admin`) — Solo Administradores

**Archivo:** `src/pages/AdminPanel.tsx`

Gestión completa de usuarios del sistema.

**Secciones:**
- **Creación de Usuario:** Formulario con nombre completo, correo, contraseña y rol (Médico/Administrador). Al crear exitosamente, muestra un modal con las credenciales y botones para copiar al portapapeles.
- **Gestión de Usuarios:** Tabla con todos los usuarios del sistema. Filtros por nombre y rol. Columnas: Nombre, Email, Rol (badge), Estado (badge activo/inactivo), Acciones (switch para activar/desactivar).

**Endpoints consumidos:**
- `POST /admin/users/register` — Registrar nuevo usuario
- `GET /admin/users` — Listar usuarios
- `PATCH /admin/users/{id}/status` — Activar/desactivar usuario

---

### ⚙️ Configuración (`/settings`)

**Archivo:** `src/pages/Settings.tsx`

Página de configuración actualmente en desarrollo. Muestra un placeholder "Coming Soon".

---

## Internacionalización (i18n)

La aplicación soporta **español (ES)** e **inglés (EN)** mediante `LanguageContext`. El idioma se puede cambiar desde:
- El selector de idioma en la página de login (ícono de globo)
- Persiste durante la sesión del usuario

---

## Navegación y Layout

### Sidebar (`AppSidebar`)
- **Médicos ven:** Dashboard, Pacientes, Predicciones, Analíticas, Guía Predictiva
- **Admins ven:** Dashboard, Panel de Administración
- **Ambos ven:** Configuración, Cerrar Sesión
- La sidebar es colapsable (ícono/expandida)

### Header
- Muestra información del usuario autenticado
- Botón de toggle para la sidebar

---

## Variables de Entorno

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `VITE_API_URL` | URL base de la API backend | `https://hybridmodeldisability.onrender.com` |

---

## Instalación y Desarrollo Local

```bash
# Clonar el repositorio
git clone <URL_DEL_REPO>
cd health-access-bridge

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Construir para producción
npm run build
```

---

## Despliegue en Render (Static Site)

1. Conectar el repositorio GitHub en [Render](https://render.com)
2. Crear un **Static Site** con:
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
3. Agregar variable de entorno `VITE_API_URL` si se usa un backend diferente
4. Desplegar

---

## Autor

**Ing. Julián Andrés Quimbayo Castro**
