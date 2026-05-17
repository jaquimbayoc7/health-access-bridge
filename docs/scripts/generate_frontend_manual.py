"""
Generador del Manual de Usuario Frontend — Health Access Bridge (HAB)
Ejecutar: py docs/generate_frontend_manual.py
Salida:   docs/Manual_Frontend_HAB.pdf
"""

import os
from fpdf import FPDF
from PIL import Image as PILImage

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "..", "frontend", "design", "images")
OUTPUT     = os.path.join(BASE_DIR, "Manual_Frontend_HAB.pdf")

# ── Palette ──────────────────────────────────────────────────────────────────
PRIMARY = (31,  56,  100)
ACCENT  = (46,  116, 181)
LIGHT   = (214, 228, 240)
WHITE   = (255, 255, 255)
DARK    = (45,  45,  45)
GRAY    = (110, 110, 110)
GREEN   = (21,  87,  36)
GREENBG = (212, 237, 218)


# ── Sanitize ─────────────────────────────────────────────────────────────────

_REPLACEMENTS = {
    '\u2014': '-',   '\u2013': '-',   '\u2012': '-',
    '\u2019': "'",   '\u2018': "'",
    '\u201c': '"',   '\u201d': '"',
    '\u2192': '->',  '\u2190': '<-',
    '\u26a0': '(!)', '\u00b7': '*',
    '\u00e9': 'e',   '\u00e1': 'a',   '\u00ed': 'i',
    '\u00f3': 'o',   '\u00fa': 'u',   '\u00f1': 'n',
    '\u00fc': 'u',   '\u00f6': 'o',   '\u00e4': 'a',
    '\u00e2': 'a',   '\u00ea': 'e',   '\u00ee': 'i',
    '\u00f4': 'o',   '\u00fb': 'u',   '\u00c9': 'E',
    '\u00c1': 'A',   '\u00cd': 'I',   '\u00d3': 'O',
    '\u00da': 'U',   '\u00d1': 'N',
}

def s(text):
    """Sanitize text to latin-1 safe ASCII for built-in fpdf fonts."""
    for ch, rep in _REPLACEMENTS.items():
        text = text.replace(ch, rep)
    return text


# ── Helpers ───────────────────────────────────────────────────────────────────

def img_path(filename):
    return os.path.join(IMAGES_DIR, filename)


def img_display_dims(filename, max_w_mm=175, max_h_mm=105):
    """Return (w, h) in mm preserving aspect ratio within max bounds."""
    path = img_path(filename)
    if not os.path.exists(path):
        return max_w_mm, 60
    with PILImage.open(path) as im:
        pw, ph = im.size
    aspect = ph / pw
    w = max_w_mm
    h = w * aspect
    if h > max_h_mm:
        h = max_h_mm
        w = h / aspect
    return round(w, 1), round(h, 1)


# ── PDF Class ─────────────────────────────────────────────────────────────────

class ManualPDF(FPDF):

    def header(self):
        pass

    def footer(self):
        if self.page_no() <= 2:          # cover + TOC have no footer
            return
        self.set_y(-14)
        self.set_draw_color(*LIGHT)
        self.set_line_width(0.3)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(1)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        page_label = s(f"Health Access Bridge  |  Manual de Usuario Frontend  |  Pag. {self.page_no() - 2}")
        self.cell(0, 6, page_label, align="C")  # already sanitized
        self.set_text_color(*DARK)

    # ── Building blocks ────────────────────────────────────────────────────

    def colored_band(self, y, h, color=None):
        color = color or PRIMARY
        self.set_fill_color(*color)
        self.rect(0, y, 210, h, "F")

    def section_title(self, text, sub=None):
        y0 = self.get_y()
        self.colored_band(y0, 14)
        self.set_xy(15, y0 + 3)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*WHITE)
        self.cell(0, 7, s(text), new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*DARK)
        self.ln(3)
        if sub:
            self.set_x(15)
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(*GRAY)
            self.multi_cell(180, 5, s(sub))
            self.set_text_color(*DARK)
            self.ln(2)

    def bullet(self, text, indent=20):
        self.set_x(indent)
        # small filled square bullet
        bx, by = self.get_x(), self.get_y() + 1.8
        self.set_fill_color(*ACCENT)
        self.rect(bx, by, 1.8, 1.8, "F")
        self.set_x(indent + 4)
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK)
        self.multi_cell(175 - indent, 5, s(text))

    def badge(self, text, bg=None, fg=None):
        bg = bg or ACCENT
        fg = fg or WHITE
        self.set_fill_color(*bg)
        self.set_text_color(*fg)
        self.set_font("Helvetica", "B", 8)
        self.set_x(15)
        st = s(text)
        self.cell(len(st) * 2.4 + 6, 5.5, f"  {st}  ", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*DARK)
        self.ln(2)

    def kv_table(self, rows, col_widths, headers=None):
        if headers:
            y0 = self.get_y()
            self.set_fill_color(*PRIMARY)
            self.rect(15, y0, 180, 8, "F")
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*WHITE)
            self.set_y(y0 + 1)
            x = 17
            for h, w in zip(headers, col_widths):
                self.set_x(x); self.cell(w, 6, s(str(h))); x += w
            self.ln(7)
        for i, row in enumerate(rows):
            y0 = self.get_y()
            self.set_fill_color(*(LIGHT if i % 2 == 0 else WHITE))
            self.rect(15, y0, 180, 7, "F")
            x = 17
            for v, w in zip(row, col_widths):
                self.set_x(x)
                if v in ("Solo Admin",):
                    self.set_font("Helvetica", "B", 8.5)
                    self.set_text_color(*PRIMARY)
                else:
                    self.set_font("Helvetica", "", 8.5)
                    self.set_text_color(*DARK)
                self.cell(w, 7, s(str(v)))
                x += w
            self.ln(7)

    def embed_image(self, filename, caption=None):
        path = img_path(filename)
        if not os.path.exists(path):
            self.set_x(15)
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(*GRAY)
            self.cell(0, 8, f"[Imagen no disponible: {filename}]", new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(*DARK)
            return
        w, h = img_display_dims(filename)
        x_offset = (180 - w) / 2 + 15      # center within margins
        # thin border box
        self.set_draw_color(*LIGHT)
        self.set_line_width(0.4)
        self.rect(x_offset - 1, self.get_y() - 1, w + 2, h + 2, "D")
        self.image(path, x=x_offset, y=self.get_y(), w=w, h=h)
        self.set_y(self.get_y() + h + 3)
        if caption:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(*GRAY)
            self.cell(0, 5, caption, align="C", new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(*DARK)
        self.ln(3)


# ── Screens data ──────────────────────────────────────────────────────────────

SCREENS = [
    {
        "num": "2",
        "image": "1-Login.png",
        "title": "2. Acceso al Sistema - Login",
        "role": "Público",
        "role_color": GRAY,
        "desc": (
            "La pantalla de Login es el único punto de entrada a la plataforma HAB. "
            "El sistema recibe las credenciales del usuario (correo y contraseña), valida "
            "contra el backend mediante JWT y redirige automáticamente según el rol "
            "asignado: el Administrador llega al Panel de Administración y el Médico "
            "al Dashboard principal."
        ),
        "features": [
            "Formulario de autenticacion con validacion de campos en tiempo real.",
            "Autenticacion JWT - token Bearer almacenado en localStorage.",
            "Redireccion automatica por rol: Admin -> /admin  |  Medico -> /dashboard.",
            "Mensaje de error descriptivo ante credenciales incorrectas o cuenta inactiva.",
            "Interfaz responsiva compatible con escritorio y dispositivos moviles.",
        ],
    },
    {
        "num": "3",
        "image": "2-Admin.png",
        "title": "3. Panel de Administracion",
        "role": "Solo Admin",
        "role_color": PRIMARY,
        "desc": (
            "Vista exclusiva del rol Administrador. Permite gestionar cuentas de médicos "
            "y otros administradores: creación de nuevos usuarios, activación/desactivación "
            "de cuentas y visualización del estado global del sistema. El acceso está "
            "protegido por el guard AdminRoute — cualquier otro rol es redirigido."
        ),
        "features": [
            "Tabla de usuarios con badge de rol y estado activo/inactivo.",
            "Formulario modal para crear nuevos usuarios (medico o admin).",
            "Toggle de activacion/desactivacion - endpoint PATCH /admin/users/{id}/status.",
            "Admin: redirige a /dashboard si el rol no es admin.",
            "Estadisticas globales: total de usuarios y pacientes en el sistema.",
        ],
    },
    {
        "num": "4",
        "image": "3-DashMedico.png",
        "title": "4. Dashboard del Medico",
        "role": "Medico / Admin",
        "role_color": ACCENT,
        "desc": (
            "Pagina principal del medico tras iniciar sesion. Presenta un resumen de "
            "metricas clave: total de pacientes registrados, predicciones ejecutadas, "
            "distribucion de perfiles de discapacidad y accesos rapidos a los modulos "
            "mas utilizados. Los datos se calculan en cliente sin endpoints adicionales."
        ),
        "features": [
            "Tarjetas de metricas: total pacientes, predicciones ejecutadas, perfiles activos.",
            "Lista de acceso rapido a los ultimos 5 pacientes registrados.",
            "Indicador visual de distribucion de perfiles (Bajas / Moderadas / Altas).",
            "Navegacion contextual adaptada al rol del usuario autenticado.",
            "Datos obtenidos de GET /patients/ y calculados en cliente (sin endpoints extra).",
        ],
    },
    {
        "num": "5",
        "image": "4-Pacientes.png",
        "title": "5. Gestion de Pacientes",
        "role": "Medico / Admin",
        "role_color": ACCENT,
        "desc": (
            "Nucleo de la gestion clinica. Permite registrar, editar y gestionar la "
            "historia clinica de pacientes con discapacidad. El Administrador puede ver y "
            "editar todos los registros del sistema; el Medico solo tiene acceso a los "
            "suyos propios (aislamiento por rol garantizado en backend y frontend)."
        ),
        "features": [
            "Tabla paginada con busqueda en tiempo real por nombre o numero de documento (debounce 300ms).",
            "Formulario modal de creacion/edicion con validacion de todos los campos ICF.",
            "Eliminacion logica (soft delete) con confirmacion de dialogo.",
            "Exportacion a Excel (SheetJS) y PDF (jsPDF) directamente desde el cliente.",
            "Campos clinicos: niveles de dificultad D1-D6 (0-100), nivel global y categorias.",
            "Aislamiento por rol: medico solo ve y edita sus propios registros.",
        ],
    },
    {
        "num": "6",
        "image": "5-Predicciones.png",
        "title": "6. Modulo de Predicciones ML",
        "role": "Medico / Admin",
        "role_color": ACCENT,
        "desc": (
            "Permite ejecutar el modelo de inteligencia artificial HybridModelDisability "
            "(K-Means + Gradient Boosting) sobre los datos clinicos de un paciente. "
            "El resultado clasifica al paciente en uno de tres perfiles de barreras de "
            "acceso a la salud y queda persistido en el registro clinico."
        ),
        "features": [
            "Selector de paciente con busqueda para ejecutar la prediccion.",
            "Llamada en tiempo real a POST /patients/{id}/predict.",
            "Badge codificado por color: Verde (Bajas) | Amarillo (Moderadas) | Rojo (Altas).",
            "Historial de predicciones por paciente con descripcion del perfil asignado.",
            "Resultado persistido en prediction_profile y prediction_description del registro.",
        ],
    },
    {
        "num": "7",
        "image": "6-Analisis.png",
        "title": "7. Analisis y Estadisticas",
        "role": "Medico / Admin",
        "role_color": ACCENT,
        "desc": (
            "Provee visualizaciones estadisticas de la poblacion de pacientes mediante "
            "graficas interactivas Recharts. Incluye distribucion de perfiles predictivos, "
            "metricas demograficas y tablas de resumen para la toma de decisiones "
            "clinicas a nivel poblacional."
        ),
        "features": [
            "Grafica de torta (PieChart) con distribucion de perfiles 0/1/2.",
            "Graficas de barras para metricas demograficas (genero, causa de deficiencia).",
            "Tabla resumen con conteo y porcentaje por perfil predictivo.",
            "Tooltips interactivos al pasar el cursor sobre los elementos de la grafica.",
            "Datos obtenidos de GET /patients/ y calculados en cliente.",
        ],
    },
    {
        "num": "8",
        "image": "7-GuiaPrediccion.png",
        "title": "8. Guia de Prediccion ICF",
        "role": "Medico / Admin",
        "role_color": ACCENT,
        "desc": (
            "Recurso de referencia clinica que explica la interpretacion de los tres "
            "perfiles del modelo HybridModelDisability. Describe los criterios de "
            "clasificacion, las caracteristicas tipicas de cada perfil y las "
            "recomendaciones de intervencion basadas en el marco ICF "
            "(Clasificacion Internacional del Funcionamiento)."
        ),
        "features": [
            "Descripcion detallada de los 3 perfiles: Barreras Bajas, Moderadas y Altas.",
            "Criterios clinicos de clasificacion por nivel de dificultad (D1-D6).",
            "Recomendaciones de intervencion diferenciadas por perfil.",
            "Glosario de terminos ICF integrado en la interfaz.",
            "Contenido estatico - no requiere llamadas a la API.",
        ],
    },
    {
        "num": "9",
        "image": "8-PerfilICF.png",
        "title": "9. Perfil Funcional ICF",
        "role": "Medico / Admin",
        "role_color": ACCENT,
        "desc": (
            "Muestra la visualizacion detallada del perfil de funcionamiento del paciente "
            "basado en la Clasificacion Internacional del Funcionamiento, la Discapacidad "
            "y la Salud (ICF/CIF). Permite al medico interpretar graficamente los niveles "
            "de dificultad en cada dimension funcional del paciente."
        ),
        "features": [
            "Visualizacion grafica de los niveles D1-D6 y nivel global del paciente.",
            "Representacion de las dimensiones ICF con comparativa de umbrales por perfil.",
            "Integrado con el perfil de prediccion almacenado en el registro del paciente.",
            "Exportable como parte del historial clinico del paciente.",
        ],
    },
]


# ── Build ──────────────────────────────────────────────────────────────────────

def build():
    pdf = ManualPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(15, 15, 15)

    # ═══════════════════════════════════════════════════════
    # COVER
    # ═══════════════════════════════════════════════════════
    pdf.add_page()

    # Top band
    pdf.colored_band(0, 45)

    # Title in top band
    pdf.set_xy(15, 12)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 10, "Manual de Usuario", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_xy(15, 26)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "Frontend - Health Access Bridge (HAB)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)

    # Portada image
    portada = img_path("Portada.png")
    if os.path.exists(portada):
        w, h = img_display_dims("Portada.png", max_w_mm=160, max_h_mm=90)
        x_off = (180 - w) / 2 + 15
        pdf.image(portada, x=x_off, y=50, w=w, h=h)
        pdf.set_y(50 + h + 6)
    else:
        pdf.set_y(55)

    # Divider
    pdf.set_draw_color(*LIGHT)
    pdf.set_line_width(0.5)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(6)

    # Meta box
    meta_y = pdf.get_y()
    pdf.set_fill_color(*LIGHT)
    pdf.rect(30, meta_y, 150, 36, "F")
    meta = [
        ("Version",     "1.0.0"),
        ("Plataforma",  "Web - React 18 + TypeScript + Vite"),
        ("Estilos",     "TailwindCSS + shadcn/ui"),
        ("Fecha",       "Mayo 2026"),
        ("Repositorio", "github.com/jaquimbayoc7/health-access-bridge"),
    ]
    pdf.set_y(meta_y + 5)
    for label, value in meta:
        pdf.set_x(36)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*PRIMARY)
        pdf.cell(38, 5.5, label + ":")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK)
        pdf.cell(0, 5.5, value, new_x="LMARGIN", new_y="NEXT")

    # Bottom band
    pdf.colored_band(272, 25)
    pdf.set_xy(15, 278)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 5, "https://hab-frontend.onrender.com  ·  https://hab-frontend-qa.onrender.com  ·  https://hab-frontend-dev.onrender.com", align="C")

    # ═══════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ═══════════════════════════════════════════════════════
    pdf.add_page()
    pdf.colored_band(0, 18)
    pdf.set_xy(15, 5)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 8, "Tabla de Contenidos", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)
    pdf.ln(8)

    toc = [
        ("1.", "Introduccion y Stack Tecnologico"),
        ("2.", "Acceso al Sistema - Login"),
        ("3.", "Panel de Administracion  (Solo Admin)"),
        ("4.", "Dashboard del Medico"),
        ("5.", "Gestion de Pacientes"),
        ("6.", "Modulo de Predicciones ML"),
        ("7.", "Analisis y Estadisticas"),
        ("8.", "Guia de Prediccion ICF"),
        ("9.", "Perfil Funcional ICF"),
        ("10.", "Flujos de Usuario y Roles"),
        ("11.", "Credenciales de Prueba"),
    ]
    for i, (num, title) in enumerate(toc):
        y0 = pdf.get_y()
        pdf.set_fill_color(*(LIGHT if i % 2 == 0 else WHITE))
        pdf.rect(15, y0, 180, 9, "F")
        pdf.set_x(18)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*PRIMARY)
        pdf.cell(14, 9, num)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*DARK)
        pdf.cell(0, 9, s(title), new_x="LMARGIN", new_y="NEXT")

    # ═══════════════════════════════════════════════════════
    # SECTION 1 — INTRODUCTION
    # ═══════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title(
        "1. Introduccion y Stack Tecnologico",
        "Health Access Bridge - plataforma web inteligente para la gestion clinica de pacientes con discapacidad.",
    )

    pdf.set_font("Helvetica", "", 10)
    pdf.set_x(15)
    pdf.multi_cell(
        180, 5.5,
        "La aplicacion HAB provee interfaces diferenciadas por rol (Administrador / Medico) para el "
        "registro, analisis predictivo y visualizacion de perfiles de barreras de acceso a la salud "
        "en zonas rurales. Desplegada en tres ambientes (DEV / QA / PROD) con pipeline CI/CD "
        "automatizado mediante GitHub Actions + Render Cloud.",
    )
    pdf.ln(5)

    # Stack table
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*PRIMARY)
    pdf.set_x(15)
    pdf.cell(0, 6, "Stack Tecnologico:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)

    stack = [
        ("Framework",     "React 18 + TypeScript 5"),
        ("Build Tool",    "Vite 5"),
        ("Estilos",       "TailwindCSS 3 + shadcn/ui (Radix UI)"),
        ("Graficas",      "Recharts 2"),
        ("Routing",       "React Router DOM 6"),
        ("Estado",        "Context API + TanStack React Query 5"),
        ("Iconos",        "Lucide React"),
        ("Exportacion",   "SheetJS (Excel) + jsPDF (PDF)"),
        ("Testing",       "Vitest + React Testing Library (16 tests)"),
        ("Deploy",        "Render Cloud — 3 ambientes independientes"),
    ]
    pdf.kv_table(stack, col_widths=[45, 135])
    pdf.ln(6)

    # Ambientes
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*PRIMARY)
    pdf.set_x(15)
    pdf.cell(0, 6, "Ambientes de despliegue:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)
    ambientes = [
        ("PROD",  "https://hab-frontend.onrender.com"),
        ("QA",    "https://hab-frontend-qa.onrender.com"),
        ("DEV",   "https://hab-frontend-dev.onrender.com"),
    ]
    pdf.kv_table(ambientes, col_widths=[20, 160])

    # ═══════════════════════════════════════════════════════
    # SCREEN SECTIONS (2–9)
    # ═══════════════════════════════════════════════════════
    for screen in SCREENS:
        pdf.add_page()
        pdf.section_title(screen["title"])
        pdf.badge(screen["role"], bg=screen["role_color"])

        # Image
        pdf.embed_image(screen["image"], caption=s(f"Figura {screen['num']}. {screen['title'].split('. ', 1)[-1]}"))

        # Description
        pdf.set_x(15)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*DARK)
        pdf.multi_cell(
        180, 5.5, s(screen["desc"]))
        pdf.ln(4)

        # Features
        pdf.set_x(15)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*PRIMARY)
        pdf.cell(0, 6, "Funcionalidades principales:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*DARK)
        for f in screen["features"]:
            pdf.bullet(f)

    # ═══════════════════════════════════════════════════════
    # SECTION 10 — USER FLOWS
    # ═══════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("10. Flujos de Usuario y Roles", "Rutas disponibles y permisos por rol en la aplicacion.")

    routes = [
        ("/",                 "Redirect",        "Todos",       "Redirige a /dashboard"),
        ("/login",            "LoginLanding",    "Publico",     "Pantalla de autenticacion"),
        ("/dashboard",        "Dashboard",       "Ambos",       "Resumen y metricas del medico"),
        ("/patients",         "Patients",        "Ambos",       "CRUD de pacientes"),
        ("/predictions",      "Predictions",     "Ambos",       "Prediccion ML HybridModelDisability"),
        ("/analytics",        "Analytics",       "Ambos",       "Graficas y estadisticas"),
        ("/predictive-guide", "PredictiveGuide", "Ambos",       "Guia clinica de perfiles ICF"),
        ("/settings",         "Settings",        "Ambos",       "Configuracion de cuenta"),
        ("/admin",            "AdminPanel",       "Solo Admin",  "Gestion de usuarios — guard AdminRoute"),
        ("*",                 "NotFound",        "Todos",       "Pagina 404"),
    ]
    pdf.kv_table(
        routes,
        col_widths=[42, 38, 28, 72],
        headers=["Ruta", "Componente", "Acceso", "Descripcion"],
    )
    pdf.ln(6)

    # Auth flow
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*PRIMARY)
    pdf.set_x(15)
    pdf.cell(0, 6, "Flujo de autenticacion:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)
    flow_steps = [
        "Usuario ingresa email y contraseña en /login.",
        "El frontend llama a POST /users/login → recibe token JWT.",
        "El token se almacena en localStorage y en ApiService (en memoria).",
        "Se consulta GET /users/me → se obtiene el rol del usuario.",
        "Admin -> redirige a /admin  |  Medico -> redirige a /dashboard.",
        "En cada request posterior, el token se envia como Authorization: Bearer <token>.",
        "Si el token expira (HTTP 401), PatientService limpia el storage y redirige a /login.",
    ]
    for step in flow_steps:
        pdf.bullet(step)

    # ═══════════════════════════════════════════════════════
    # SECTION 11 — CREDENTIALS
    # ═══════════════════════════════════════════════════════
    pdf.ln(8)
    pdf.section_title("11. Credenciales de Prueba", "Disponibles en los 3 ambientes (seed idempotente).")

    creds = [
        ("Admin",    "administrador@salud.co", "adminpassword",        "Ve los 10 pacientes de todos los medicos"),
        ("Medico 1", "medico1@salud.co",        "medico123",     "5 pacientes propios asignados"),
        ("Medico 2", "medico2@salud.co",        "medico123",     "5 pacientes propios asignados"),
    ]
    pdf.kv_table(
        creds,
        col_widths=[24, 65, 32, 59],
        headers=["Rol", "Email", "Contraseña", "Notas"],
    )
    pdf.ln(4)

    # Warning note
    pdf.set_fill_color(*LIGHT)
    note_y = pdf.get_y()
    pdf.rect(30, note_y, 150, 30, "F")
    pdf.set_xy(19, note_y + 3)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(133, 100, 4)
    pdf.cell(0, 4, "(!)  Nota de seguridad:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(19)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.cell(0, 4, "Estas credenciales son exclusivamente para entornos de prueba (DEV / QA). No usar en produccion real.")
    pdf.set_text_color(*DARK)

    # ═══════════════════════════════════════════════════════
    # SAVE
    # ═══════════════════════════════════════════════════════
    pdf.output(OUTPUT)
    print(f"\nManual PDF generado exitosamente:\n  {OUTPUT}")


if __name__ == "__main__":
    build()
