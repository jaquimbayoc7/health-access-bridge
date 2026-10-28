import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, Rectangle, FancyArrowPatch
import os

OUT = os.path.join(os.path.dirname(__file__), 'fig')
os.makedirs(OUT, exist_ok=True)
plt.rcParams['font.family'] = 'DejaVu Sans'
INK = '#1e293b'
BLUE = '#2563eb'
GREEN = '#15803d'
ORANGE = '#c2410c'
PURPLE = '#6d28d9'
GRAY = '#64748b'
LIGHT = {'blue': '#dbeafe', 'green': '#dcfce7', 'orange': '#ffedd5', 'purple': '#ede9fe', 'gray': '#f1f5f9', 'red': '#fee2e2', 'yellow': '#fef9c3'}


def box(ax, x, y, w, h, text, fc='#ffffff', ec=INK, fs=8.5, bold=False, r=0.08, lw=1.3, color=INK):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0.0,rounding_size={r}', fc=fc, ec=ec, lw=lw)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=fs, color=color, fontweight='bold' if bold else 'normal', wrap=True)


def arrow(ax, p1, p2, color=INK, style='-|>', ls='-', lw=1.3, rad=0.0, label=None, lpos=0.5, fs=7.5, loff=(0, 0.08)):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=11, color=color, lw=lw, ls=ls, connectionstyle=f'arc3,rad={rad}', shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    if label:
        mx = p1[0] + (p2[0] - p1[0]) * lpos + loff[0]
        my = p1[1] + (p2[1] - p1[1]) * lpos + loff[1]
        ax.text(mx, my, label, fontsize=fs, ha='center', va='bottom', color=GRAY)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=170, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# ---------------------------------------------------------------- BPMN helpers
def lanes(ax, names, width, lane_h, top):
    ys = []
    for i, n in enumerate(names):
        y = top - (i + 1) * lane_h
        ax.add_patch(Rectangle((0, y), width, lane_h, fc='white' if i % 2 == 0 else '#f8fafc', ec=INK, lw=1.1))
        ax.add_patch(Rectangle((0, y), 0.55, lane_h, fc=LIGHT['blue'], ec=INK, lw=1.1))
        ax.text(0.27, y + lane_h / 2, n, rotation=90, ha='center', va='center', fontsize=8.5, fontweight='bold', color=INK)
        ys.append(y + lane_h / 2)
    return ys


def task(ax, cx, cy, text, w=1.55, h=0.62, fc='#ffffff'):
    box(ax, cx - w / 2, cy - h / 2, w, h, text, fc=fc, fs=7.2)
    return cx, cy, w, h


def event(ax, cx, cy, kind='start', label=None):
    lw = 1.4 if kind == 'start' else 3.0
    ax.add_patch(Circle((cx, cy), 0.17, fc='white', ec=GREEN if kind == 'start' else ORANGE, lw=lw))
    if label:
        ax.text(cx, cy - 0.3, label, ha='center', va='top', fontsize=7, color=GRAY)


def gateway(ax, cx, cy, text):
    ax.add_patch(Polygon([(cx - 0.26, cy), (cx, cy + 0.26), (cx + 0.26, cy), (cx, cy - 0.26)], fc=LIGHT['yellow'], ec=INK, lw=1.3))
    ax.text(cx, cy, 'X', ha='center', va='center', fontsize=8, fontweight='bold')
    ax.text(cx, cy + 0.34, text, ha='center', va='bottom', fontsize=7, color=INK)


def bpmn(name, title, lane_names, width, lane_h, draw):
    n = len(lane_names)
    fig, ax = plt.subplots(figsize=(width * 0.92, n * lane_h * 0.92 + 0.5))
    ax.set_xlim(-0.05, width + 0.05)
    ax.set_ylim(-0.05, n * lane_h + 0.45)
    ax.axis('off')
    top = n * lane_h
    ax.text(width / 2, top + 0.2, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color=INK)
    ys = lanes(ax, lane_names, width, lane_h, top)
    draw(ax, ys)
    save(fig, name)


# ---------------------------------------------------------------- BPMN 1: registro y prediccion
def d1(ax, ys):
    m, s, ml = ys
    event(ax, 1.1, m, 'start', 'Inicio')
    task(ax, 2.3, m, 'Iniciar sesión\n(correo y contraseña)')
    task(ax, 2.3, s, 'Validar credenciales\ny emitir JWT')
    gateway(ax, 3.8, s, '¿Válidas?')
    task(ax, 3.8, m, 'Mostrar error\nde acceso', fc=LIGHT['red'])
    task(ax, 5.4, m, 'Registrar paciente\n(datos y niveles D1–D6)')
    task(ax, 5.4, s, 'Guardar paciente\n(dueño = médico)')
    task(ax, 7.0, m, 'Solicitar\npredicción')
    task(ax, 7.0, ml, 'Calcular perfil\n0, 1 o 2')
    task(ax, 8.6, s, 'Guardar perfil\ny devolver resultado')
    task(ax, 8.6, m, 'Ver perfil y\nhistorial')
    event(ax, 9.9, m, 'end', 'Fin')
    arrow(ax, (1.27, m), (1.52, m))
    arrow(ax, (2.3, m - 0.31), (2.3, s + 0.31))
    arrow(ax, (3.08, s), (3.54, s))
    arrow(ax, (3.8, s + 0.26), (3.8, m - 0.31), label='No', lpos=0.5, loff=(0.18, -0.02))
    arrow(ax, (4.06, s), (5.4 - 0.78, s - 0.0), label='Sí', loff=(0, 0.05))
    arrow(ax, (3.8 - 0.78, m), (2.3 + 0.78, m), ls='--', color=GRAY)
    arrow(ax, (5.4, s + 0.31), (5.4, m - 0.31), rad=0)
    arrow(ax, (5.4 + 0.78, m), (7.0 - 0.78, m))
    arrow(ax, (7.0, m - 0.31), (7.0, ml + 0.31))
    arrow(ax, (7.0 + 0.78, ml), (8.6 - 0.2, s - 0.31), rad=0.0)
    arrow(ax, (8.6, s + 0.31), (8.6, m - 0.31))
    arrow(ax, (8.6 + 0.78, m), (9.73, m))


bpmn('bpmn-registro-prediccion.png', 'Proceso 1. Ingreso, registro del paciente y predicción de barreras', ['Médico', 'Sistema HAB\n(frontend y backend)', 'Modelo\npredictivo'], 10.3, 1.35, d1)


# ---------------------------------------------------------------- BPMN 2: perfil ICF
def d2(ax, ys):
    m, b, s = ys
    event(ax, 1.0, m, 'start', 'Inicio')
    task(ax, 2.2, m, 'Elegir paciente,\nescribir diagnóstico\ny notas')
    task(ax, 2.2, b, 'Armar el contexto\n(sin nombre ni\ndocumento)')
    gateway(ax, 3.75, b, '¿Edad ≥ 6?')
    task(ax, 3.75, m, 'Informar: no\naplica', fc=LIGHT['red'])
    task(ax, 5.3, b, 'Enviar al servicio\n(HTTPS + token)')
    task(ax, 5.3, s, 'Aplicar reglas del\nAnexo 1239')
    task(ax, 6.95, s, 'Buscar candidatos\n(embedding + pgvector)')
    task(ax, 8.6, s, 'Modelo elige entre\ncandidatos y\nvalida con catálogo')
    gateway(ax, 10.15, s, '¿Responde?')
    task(ax, 10.15, b, 'Respaldo por\nsimilitud', fc=LIGHT['orange'])
    task(ax, 11.8, b, 'Guardar lote de\nsugerencias')
    task(ax, 11.8, m, 'Aceptar, editar\no rechazar\ncada código')
    task(ax, 13.45, b, 'Guardar la\ndecisión')
    task(ax, 13.45, m, 'Descargar\nborrador (PDF)')
    event(ax, 14.75, m, 'end', 'Fin')
    arrow(ax, (1.17, m), (1.42, m))
    arrow(ax, (2.2, m - 0.4), (2.2, b + 0.4))
    arrow(ax, (3.0, b), (3.49, b))
    arrow(ax, (3.75, b + 0.26), (3.75, m - 0.31), label='No', loff=(0.2, -0.05))
    arrow(ax, (4.01, b), (4.52, b), label='Sí', loff=(0, 0.05))
    arrow(ax, (5.3, b - 0.31), (5.3, s + 0.31))
    arrow(ax, (6.08, s), (6.17, s))
    arrow(ax, (7.73, s), (7.82, s))
    arrow(ax, (9.4, s), (9.89, s))
    arrow(ax, (10.15, s - 0.26), (10.15, b + 0.31), label='No', loff=(0.2, -0.02))
    arrow(ax, (10.41, s), (11.6, b - 0.31), rad=0.0, label='Sí', lpos=0.35, loff=(0, 0.05))
    arrow(ax, (10.93, b), (11.02, b))
    arrow(ax, (11.8, b + 0.31), (11.8, m - 0.45))
    arrow(ax, (12.4, m), (12.67, m))
    arrow(ax, (13.45, m - 0.4), (13.45, b + 0.31))
    arrow(ax, (14.23, m), (14.58, m), ls='--', color=GRAY)


bpmn('bpmn-perfil-icf.png', 'Proceso 2. Generación del perfil funcional CIF y decisión del médico', ['Médico', 'Backend HAB', 'Servicio ICF\n(PC propio)'], 15.2, 1.55, d2)


# ---------------------------------------------------------------- BPMN 3: usuarios y analisis
def d3(ax, ys):
    a, s = ys
    event(ax, 1.0, a, 'start', 'Inicio')
    task(ax, 2.4, a, 'Crear usuario\n(nombre, correo, rol)')
    task(ax, 2.4, s, 'Validar y guardar\n(contraseña con Bcrypt)')
    task(ax, 4.2, a, 'Activar o\ndesactivar cuenta')
    task(ax, 4.2, s, 'Actualizar estado;\nbloquear el ingreso\nsi está inactiva')
    task(ax, 6.0, a, 'Abrir el análisis\ny elegir filtros')
    task(ax, 6.0, s, 'Calcular agregados\n(sin datos identificables)')
    task(ax, 7.8, a, 'Exportar a\nExcel o PDF')
    event(ax, 9.0, a, 'end', 'Fin')
    arrow(ax, (1.17, a), (1.62, a))
    arrow(ax, (2.4, a - 0.31), (2.4, s + 0.31))
    arrow(ax, (2.78, s + 0.31), (3.42, a - 0.0), rad=0.0)
    arrow(ax, (4.2, a - 0.31), (4.2, s + 0.31))
    arrow(ax, (4.98, s), (5.22, a - 0.0), rad=0.0)
    arrow(ax, (6.0, a - 0.31), (6.0, s + 0.31))
    arrow(ax, (6.78, s), (7.02, a - 0.0), rad=0.0)
    arrow(ax, (8.58, a), (8.83, a))


bpmn('bpmn-administracion-analisis.png', 'Proceso 3. Administración de usuarios y análisis agregado', ['Administrador', 'Sistema HAB'], 9.5, 1.5, d3)


# ---------------------------------------------------------------- Arquitectura por capas
def arch():
    fig, ax = plt.subplots(figsize=(10.5, 7.2))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 7.2)
    ax.axis('off')
    layers = [
        ('Presentación', 'blue', ['React 18 +\nTypeScript', 'Vite · Tailwind\nshadcn/ui', 'Recharts\n(gráficos)', 'jsPDF y xlsx\n(exportación)', 'ES / EN ·\nWCAG 2.2 AA']),
        ('API y seguridad', 'green', ['FastAPI: routers\nusers, admin, patients,\nicf y analytics', 'JWT + Bcrypt', 'RBAC: Admin / Médico', 'CORS por ambiente']),
        ('Lógica y servicios', 'purple', ['Predicción de barreras\n(K-Means + Boosting)', 'Cliente del servicio ICF\n(tiempos y respaldo)', 'Agregados del dashboard', 'CRUD (SQLAlchemy)']),
        ('IA generativa local\n(PC propio)', 'orange', ['Reglas del\nAnexo 1239', 'Embeddings\nbge-m3', 'Selección:\ngemma4:e4b (Ollama)', 'Validación contra el\ncatálogo CIF-IA', 'Caddy + token']),
        ('Datos', 'gray', ['PostgreSQL (Render)\nusers · patients · icf_suggestions', 'PostgreSQL + pgvector (PC)\ncatálogo CIF-IA, 1.593 códigos']),
        ('Infraestructura\ny calidad', 'red', ['Render:\n3 ambientes', 'GitHub Actions\n(3 flujos)', 'Tailscale Funnel', 'pytest · Vitest\nPlaywright · axe']),
    ]
    h = 1.0
    gap = 0.12
    y = 7.1
    for name, col, comps in layers:
        y -= h + gap
        ax.add_patch(FancyBboxPatch((0.1, y), 10.3, h, boxstyle='round,pad=0,rounding_size=0.08', fc=LIGHT[col], ec=INK, lw=1.2))
        ax.text(0.28, y + h / 2, name, ha='left', va='center', fontsize=9.5, fontweight='bold', color=INK, wrap=True)
        n = len(comps)
        x0, x1 = 2.55, 10.25
        cw = (x1 - x0 - 0.12 * (n - 1)) / n
        for i, c in enumerate(comps):
            box(ax, x0 + i * (cw + 0.12), y + 0.14, cw, h - 0.28, c, fc='white', fs=7.4)
    ax.set_title('Arquitectura general por capas de Health Access Bridge', fontsize=11, fontweight='bold', pad=6)
    save(fig, 'arquitectura-capas.png')


arch()


# ---------------------------------------------------------------- Modelo de datos
def erd():
    fig, ax = plt.subplots(figsize=(11, 6.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.6)
    ax.axis('off')

    def table(x, y, w, title, rows, col):
        rh = 0.27
        h = rh * (len(rows) + 1)
        ax.add_patch(Rectangle((x, y - h), w, h, fc='white', ec=INK, lw=1.3))
        ax.add_patch(Rectangle((x, y - rh), w, rh, fc=col, ec=INK, lw=1.3))
        ax.text(x + w / 2, y - rh / 2, title, ha='center', va='center', fontsize=9, fontweight='bold')
        for i, (n, t, k) in enumerate(rows):
            yy = y - rh * (i + 1.5)
            ax.text(x + 0.08, yy, k, fontsize=6.8, va='center', color=ORANGE, fontweight='bold')
            ax.text(x + 0.42, yy, n, fontsize=7.2, va='center')
            ax.text(x + w - 0.08, yy, t, fontsize=6.8, va='center', ha='right', color=GRAY)
        return (x, y - h, w, h)

    u = table(0.2, 6.3, 2.8, 'users', [('id', 'int', 'PK'), ('email', 'string · único', ''), ('full_name', 'string', ''), ('hashed_password', 'string', ''), ('is_active', 'bool', ''), ('role', 'admin | médico', '')], LIGHT['blue'])
    p = table(4.1, 6.3, 3.1, 'patients', [('id', 'int', 'PK'), ('numero_documento', 'string', ''), ('nombre_apellidos', 'string', ''), ('fecha_nacimiento / edad', 'date / int', ''), ('genero · orientacion_sexual', 'string', ''), ('causa_deficiencia', 'string', ''), ('cat_fisica · cat_psicosocial', 'string', ''), ('nivel_d1 … nivel_d6', 'int 0–100', ''), ('nivel_global', 'int', ''), ('prediction_profile / _description', 'int / string', ''), ('is_active', 'bool (borrado lógico)', ''), ('owner_id', 'int', 'FK')], LIGHT['green'])
    i = table(8.0, 6.3, 2.85, 'icf_suggestions', [('id', 'int', 'PK'), ('patient_id', 'int', 'FK'), ('batch_id', 'uuid (un lote)', ''), ('position', 'int', ''), ('component', 'b | s | d', ''), ('code · title', 'string', ''), ('qualifier (0–4)', 'int', ''), ('qualifier_cn · _cl', 'int (solo s)', ''), ('justification', 'string', ''), ('origin', 'llm|similarity|rules', ''), ('status', 'sugerido…rechazado', ''), ('original_code · model', 'string', ''), ('diag_cie · clinical_notes', 'string', ''), ('created_at', 'datetime', '')], LIGHT['orange'])
    arrow(ax, (3.0, 5.2), (4.1, 5.2), style='-', lw=1.4)
    ax.text(3.55, 5.27, '1', ha='center', fontsize=8, fontweight='bold')
    ax.text(3.95, 5.27, 'N', ha='center', fontsize=8, fontweight='bold')
    ax.text(3.55, 4.95, 'es dueño de', ha='center', fontsize=7, color=GRAY)
    arrow(ax, (7.2, 4.4), (8.0, 4.4), style='-', lw=1.4)
    ax.text(7.45, 4.47, '1', ha='center', fontsize=8, fontweight='bold')
    ax.text(7.85, 4.47, 'N', ha='center', fontsize=8, fontweight='bold')
    ax.text(7.6, 4.15, 'tiene', ha='center', fontsize=7, color=GRAY)
    ax.text(0.2, 3.2, 'Notas del modelo', fontsize=8.5, fontweight='bold')
    ax.text(0.2, 2.45, '• Regenerar el perfil crea un lote nuevo (batch_id) y conserva\n   los anteriores: queda la trazabilidad de qué sugirió la máquina\n   y qué decidió el profesional.\n• No hay migraciones: las tablas se crean con create_all.\n• El catálogo CIF-IA (1.593 códigos) y sus embeddings viven en\n   otra base (PostgreSQL + pgvector) en el PC del servicio ICF y\n   no guardan datos de pacientes.', fontsize=7.6, va='top', color=INK, linespacing=1.45)
    ax.set_title('Modelo de datos (backend de HAB)', fontsize=11, fontweight='bold', pad=4)
    save(fig, 'modelo-datos.png')


erd()


# ---------------------------------------------------------------- Despliegue
def deploy():
    fig, ax = plt.subplots(figsize=(11, 6.8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.8)
    ax.axis('off')

    def group(x, y, w, h, title, col, ls='-'):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=0.1', fc=LIGHT[col], ec=INK, lw=1.3, ls=ls))
        ax.text(x + 0.12, y + h - 0.14, title, fontsize=9, fontweight='bold', va='top')

    group(0.1, 4.6, 2.4, 2.1, 'Cliente', 'gray')
    box(ax, 0.3, 4.75, 2.0, 0.6, 'Navegador web\n(escritorio o teléfono)', fs=7.8)
    group(0.1, 0.2, 2.4, 3.9, 'GitHub', 'gray')
    box(ax, 0.3, 2.8, 2.0, 0.65, 'Repositorio\ndevelop · staging · master', fs=7.6)
    box(ax, 0.3, 1.6, 2.0, 0.8, 'GitHub Actions\nci-dev · ci-qa · ci-prod\n(aprobación manual en prod)', fs=7.4)
    group(2.9, 0.2, 4.6, 6.5, 'Render (nube) — 3 ambientes: DEV · QA · PROD', 'orange')
    for k, (nm, yy) in enumerate([('DEV', 4.9), ('QA', 3.3), ('PROD', 1.7)]):
        ax.text(3.05, yy + 0.95, nm, fontsize=8, fontweight='bold', color=ORANGE)
        box(ax, 3.55, yy + 0.35, 1.7, 0.6, 'Frontend\n(sitio estático)', fc='white', fs=7.4)
        box(ax, 5.45, yy + 0.35, 1.9, 0.6, 'Backend FastAPI\n(servicio web)', fc='white', fs=7.4)
        box(ax, 5.45, yy - 0.4, 1.9, 0.6, 'PostgreSQL', fc=LIGHT['purple'], fs=7.4)
        arrow(ax, (5.25, yy + 0.65), (5.45, yy + 0.65))
        arrow(ax, (6.4, yy + 0.35), (6.4, yy + 0.2))
    group(8.0, 0.2, 2.9, 6.5, 'PC propio (Windows 11)', 'green')
    box(ax, 8.2, 5.55, 2.5, 0.65, 'Tailscale Funnel\n(HTTPS, puerto 11435)', fc='white', fs=7.4)
    box(ax, 8.2, 4.4, 2.5, 0.65, 'Caddy (Docker)\nexige token Bearer', fc='white', fs=7.4)
    box(ax, 8.2, 3.25, 2.5, 0.65, 'Servicio ICF (Docker)\nreglas + RAG', fc='white', fs=7.4)
    box(ax, 8.2, 2.1, 2.5, 0.65, 'PostgreSQL + pgvector\n(Docker) catálogo CIF-IA', fc=LIGHT['purple'], fs=7.2)
    box(ax, 8.2, 0.95, 2.5, 0.65, 'Ollama (Windows, GPU)\ngemma4:e4b · bge-m3', fc='white', fs=7.4)
    arrow(ax, (9.45, 5.55), (9.45, 5.05))
    arrow(ax, (9.45, 4.4), (9.45, 3.9))
    arrow(ax, (9.45, 3.25), (9.45, 2.75))
    ax.annotate('', xy=(10.85, 1.27), xytext=(10.85, 3.57), arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.2))
    arrow(ax, (2.3, 5.05), (3.55, 5.55), label='HTTPS', lpos=0.5, loff=(0, 0.05))
    arrow(ax, (7.35, 5.55), (8.2, 5.85), color=ORANGE, ls='--', label='HTTPS + token', lpos=0.5, loff=(0, 0.08))
    arrow(ax, (1.3, 1.6), (3.0, 1.3), color=PURPLE, ls='--', label='despliegue', lpos=0.5, loff=(0, -0.28))
    arrow(ax, (1.3, 2.8), (1.3, 2.4), color=GRAY)
    ax.set_title('Diagrama de despliegue', fontsize=11, fontweight='bold', pad=4)
    save(fig, 'despliegue.png')


deploy()


# ---------------------------------------------------------------- Graficos de gestion y calidad
def charts():
    # burndown
    labels = ['Inicio', 'S1', 'S2', 'S3', 'S3.5', 'S4-5', 'S6-7', 'S7', 'S8', 'S8-9\n(26-oct)', 'S11\n(27-oct)']
    real = [146, 138, 125, 99, 83, 83, 67, 59, 59, 13, 5]
    ideal = [146 * (1 - i / 12) for i in range(11)]
    fig, ax = plt.subplots(figsize=(8.2, 4.0))
    ax.plot(labels, ideal, color=GRAY, ls='--', lw=1.4, label='Ideal')
    ax.plot(labels, real, color=BLUE, lw=2.2, marker='o', label='Real (puntos restantes)')
    for x, v in zip(labels, real):
        ax.annotate(str(v), (x, v), textcoords='offset points', xytext=(0, 7), ha='center', fontsize=7.5, color=BLUE)
    ax.set_ylabel('Puntos de historia restantes')
    ax.set_ylim(0, 160)
    ax.grid(axis='y', alpha=0.25)
    ax.spines[['top', 'right']].set_visible(False)
    ax.legend(frameon=False, fontsize=8)
    plt.setp(ax.get_xticklabels(), fontsize=7.5)
    save(fig, 'burndown.png')

    # velocity
    sp = ['Sprint 1', 'Sprint 2', 'Sprint 3', 'Sprint 3.5', 'Sprint 4-5\n(adelantado)', 'Sprint 6-7', 'Sprint 7', 'Sprint 8-9\n(HU-07 + HU-08)', 'Sprint 11\n(HU-09)']
    done = [8, 13, 26, 16, 21, 16, 8, 46, 8]
    plan = [8, 13, 26, 16, 21, 16, 8, 33, 8]
    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    x = range(len(sp))
    ax.bar(x, done, color=BLUE, width=0.6, label='Completados')
    ax.bar(x, plan, fill=False, ec=GRAY, ls='--', width=0.6, label='Planificados')
    for i, v in enumerate(done):
        ax.text(i, v + 0.8, str(v), ha='center', fontsize=8)
    ax.set_xticks(list(x))
    ax.set_xticklabels(sp, fontsize=7.2)
    ax.set_ylabel('Puntos de historia')
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', alpha=0.25)
    ax.legend(frameon=False, fontsize=8)
    save(fig, 'velocidad.png')

    # validacion clinica
    crit = ['Precisión\nestricta (b+s)', 'Precisión\nflexible (b+s)', 'Cobertura\na ciegas (b+s)', 'Calificador\n(κ ponderado)']
    r1 = [0.591, 0.788, 0.552, 0.576]
    r2 = [0.710, 0.871, 0.582, 0.540]
    r3 = [0.627, 0.863, 0.690, 0.312]
    meta = [0.60, 0.80, 0.60, 0.50]
    fig, ax = plt.subplots(figsize=(8.4, 4.2))
    w = 0.24
    xs = range(4)
    ax.bar([i - w for i in xs], r1, w, color='#93c5fd', label='Ronda 1 (diagnóstico)')
    ax.bar(list(xs), r2, w, color='#3b82f6', label='Ronda 2 (motor corregido, mismos casos)')
    ax.bar([i + w for i in xs], r3, w, color='#1e3a8a', label='Ronda 3 (casos nuevos)')
    for i, m in enumerate(meta):
        ax.plot([i - 1.5 * w, i + 1.5 * w], [m, m], color=ORANGE, lw=2.2)
    ax.plot([], [], color=ORANGE, lw=2.2, label='Meta')
    for i, v in enumerate(r3):
        ax.text(i + w, v + 0.015, f'{v:.3f}'.replace('.', ','), ha='center', fontsize=7.5)
    ax.set_xticks(list(xs))
    ax.set_xticklabels(crit, fontsize=8)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel('Valor (0 a 1)')
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', alpha=0.25)
    ax.legend(frameon=False, fontsize=7.5, loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.2))
    save(fig, 'validacion-clinica.png')

    # SUS
    sus = [80, 85, 75, 87.5, 90, 87.5, 80, 72.5, 82.5, 72.5]
    roles = ['M', 'A', 'A', 'M', 'M', 'A', 'M', 'A', 'M', 'A']
    fig, ax = plt.subplots(figsize=(8.2, 3.8))
    cols = [BLUE if r == 'M' else ORANGE for r in roles]
    ax.bar([f'P{i+1:02d}' for i in range(10)], sus, color=cols, width=0.62)
    ax.axhline(68, color=GRAY, ls='--', lw=1.3)
    ax.text(9.45, 69.2, 'Promedio de referencia: 68', ha='right', fontsize=7.5, color=GRAY)
    ax.axhline(80.3, color=GREEN, ls='--', lw=1.3)
    ax.text(9.45, 81.5, 'Excelente: 80,3', ha='right', fontsize=7.5, color=GREEN)
    for i, v in enumerate(sus):
        ax.text(i, v + 1.0, str(v).replace('.', ','), ha='center', fontsize=7.6)
    ax.set_ylim(0, 100)
    ax.set_ylabel('Puntaje SUS (0–100)')
    ax.bar([], [], color=BLUE, label='Médico')
    ax.bar([], [], color=ORANGE, label='Administrador')
    ax.legend(frameon=False, fontsize=8, loc='lower right')
    ax.spines[['top', 'right']].set_visible(False)
    save(fig, 'sus.png')

    # modelos
    mods = ['Similitud\nsola', 'qwen2.5:3b\ncalidad', 'medgemma:4b\ncalidad', 'gemma4:e2b\ncalidad', 'gemma4:e4b\nrápido', 'gemma4:e4b\ncalidad']
    prec = [29, 19, 30, 32, 33, 43]
    fig, ax = plt.subplots(figsize=(8.2, 3.9))
    cols = [GRAY, GRAY, GRAY, GRAY, '#93c5fd', BLUE]
    ax.bar(mods, prec, color=cols, width=0.62)
    for i, v in enumerate(prec):
        ax.text(i, v + 0.8, f'{v} %', ha='center', fontsize=8)
    ax.set_ylabel('Precisión de funciones (b), %')
    ax.set_ylim(0, 52)
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', alpha=0.25)
    plt.setp(ax.get_xticklabels(), fontsize=7.6)
    save(fig, 'modelos-escalera.png')

    # pruebas
    caps = ['Backend\n(pytest)', 'Frontend\n(Vitest)', 'Servicio ICF\n(pytest)', 'E2E\n(Playwright)', 'Smoke\n(CI)', 'Aceptación\n(UAT)', 'Accesibilidad\n(axe-core)']
    n = [123, 61, 101, 20, 7, 18, 3]
    fig, ax = plt.subplots(figsize=(8.2, 3.8))
    ax.bar(caps, n, color=[GREEN, BLUE, PURPLE, ORANGE, GRAY, '#0e7490', '#be185d'], width=0.62)
    for i, v in enumerate(n):
        ax.text(i, v + 2, str(v), ha='center', fontsize=8.5)
    ax.set_ylabel('Pruebas')
    ax.set_ylim(0, 140)
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', alpha=0.25)
    plt.setp(ax.get_xticklabels(), fontsize=7.6)
    save(fig, 'pruebas.png')


charts()
print('figuras:', sorted(os.listdir(OUT)))
