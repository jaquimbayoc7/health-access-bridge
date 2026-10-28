import figs
from figs import *   # helpers y estilos


def bpmn2(name, title, lane_names, width, lane_h, draw, fs_lane=9):
    n = len(lane_names)
    fig, ax = plt.subplots(figsize=(width * 0.95, n * lane_h * 0.95 + 0.6))
    ax.set_xlim(-0.05, width + 0.05)
    ax.set_ylim(-0.05, n * lane_h + 0.5)
    ax.axis('off')
    top = n * lane_h
    ax.text(width / 2, top + 0.25, title, ha='center', va='center', fontsize=12, fontweight='bold', color=INK)
    ys = []
    for i, nm in enumerate(lane_names):
        y = top - (i + 1) * lane_h
        ax.add_patch(Rectangle((0, y), width, lane_h, fc='white' if i % 2 == 0 else '#f8fafc', ec=INK, lw=1.1))
        ax.add_patch(Rectangle((0, y), 0.7, lane_h, fc=LIGHT['blue'], ec=INK, lw=1.1))
        ax.text(0.35, y + lane_h / 2, nm, rotation=90, ha='center', va='center', fontsize=fs_lane, fontweight='bold', color=INK, linespacing=1.2)
        ys.append(y + lane_h / 2)
    draw(ax, ys)
    save(fig, name)


def T(ax, cx, cy, text, w=1.72, h=0.72, fc='#ffffff', fs=8.0):
    box(ax, cx - w / 2, cy - h / 2, w, h, text, fc=fc, fs=fs)


def E(ax, cx, cy, kind, label):
    event(ax, cx, cy, kind, label)


# --------------------------- Proceso 1
def p1(ax, ys):
    m, s, ml = ys
    E(ax, 1.3, m, 'start', 'Inicio')
    T(ax, 2.9, m, 'Iniciar sesión\n(correo y contraseña)')
    T(ax, 2.9, s, 'Validar credenciales\ny emitir el JWT')
    gateway(ax, 4.75, s, '¿Válidas?')
    T(ax, 4.75, m, 'Mostrar error\nde acceso', fc=LIGHT['red'])
    T(ax, 6.55, m, 'Registrar paciente\n(datos y D1–D6)')
    T(ax, 6.55, s, 'Guardar el paciente\n(dueño: el médico)')
    T(ax, 8.4, m, 'Solicitar la\npredicción')
    T(ax, 8.4, ml, 'Calcular el perfil\nde barreras (0, 1 o 2)')
    T(ax, 10.25, s, 'Guardar el perfil y\ndevolver el resultado')
    T(ax, 10.25, m, 'Ver perfil e\nhistorial')
    E(ax, 11.6, m, 'end', 'Fin')
    arrow(ax, (1.47, m), (2.12, m))
    arrow(ax, (2.9, m - 0.35), (2.9, s + 0.35))
    arrow(ax, (3.68, s), (4.49, s))
    arrow(ax, (4.75, s + 0.26), (4.75, m - 0.35), label='No', loff=(0.22, -0.05))
    arrow(ax, (5.01, s), (5.77, s), label='Sí', loff=(0, 0.05))
    arrow(ax, (3.97, m), (3.68, m), ls='--', color=GRAY)
    arrow(ax, (6.55, s + 0.35), (6.55, m - 0.35))
    arrow(ax, (7.33, m), (7.62, m))
    arrow(ax, (8.4, m - 0.35), (8.4, ml + 0.35))
    arrow(ax, (9.18, ml), (10.25, s - 0.35))
    arrow(ax, (10.25, s + 0.35), (10.25, m - 0.35))
    arrow(ax, (11.03, m), (11.43, m))


bpmn2('bpmn-registro-prediccion.png', 'Proceso 1. Ingreso, registro del paciente y predicción de barreras', ['Médico', 'Sistema HAB', 'Modelo\npredictivo'], 12.2, 1.45, p1)


# --------------------------- Proceso 2
def p2(ax, ys):
    m, b, s = ys
    E(ax, 1.3, m, 'start', 'Inicio')
    T(ax, 3.0, m, 'Elegir paciente y\nescribir diagnóstico\ny notas', w=1.78, h=0.8)
    T(ax, 3.0, b, 'Armar el contexto\n(sin nombre ni\ndocumento)', w=1.78, h=0.8)
    gateway(ax, 4.95, b, '¿Edad ≥ 6 años?')
    T(ax, 4.95, m, 'Informar:\nno aplica', fc=LIGHT['red'])
    T(ax, 6.9, b, 'Enviar al servicio\n(HTTPS + token)', w=1.78)
    T(ax, 6.9, s, 'Reglas del Anexo 1239\ny búsqueda de\ncandidatos', w=1.78, h=0.8)
    T(ax, 8.85, s, 'El modelo elige y\nse valida contra\nel catálogo', w=1.78, h=0.8)
    gateway(ax, 10.55, s, '¿Respondió?')
    T(ax, 12.4, s, 'Respaldo por\nsimilitud', fc=LIGHT['orange'])
    T(ax, 10.55, b, 'Guardar el lote\nde sugerencias', w=1.78)
    T(ax, 10.55, m, 'Aceptar, editar\no rechazar cada\ncódigo', w=1.78, h=0.8)
    T(ax, 12.4, b, 'Guardar la\ndecisión', w=1.55)
    T(ax, 12.4, m, 'Descargar el\nborrador (PDF)')
    E(ax, 13.75, m, 'end', 'Fin')
    arrow(ax, (1.47, m), (2.15, m))
    arrow(ax, (3.0, m - 0.4), (3.0, b + 0.4))
    arrow(ax, (3.85, b), (4.69, b))
    arrow(ax, (4.95, b + 0.26), (4.95, m - 0.35), label='No', loff=(0.22, -0.05))
    arrow(ax, (5.21, b), (6.05, b), label='Sí', loff=(0, 0.05))
    arrow(ax, (6.9, b - 0.35), (6.9, s + 0.4))
    arrow(ax, (7.75, s), (8.0, s))
    arrow(ax, (9.7, s), (10.29, s))
    arrow(ax, (10.55, s + 0.26), (10.55, b - 0.35), label='Sí', loff=(0.22, -0.02))
    arrow(ax, (10.81, s), (11.62, s), label='No', loff=(0, 0.05))
    arrow(ax, (12.4, s + 0.35), (12.4, b - 0.35), ls='--', color=ORANGE)
    arrow(ax, (11.62, b), (11.4, b), ls='--', color=ORANGE)
    arrow(ax, (10.55, b + 0.35), (10.55, m - 0.4))
    arrow(ax, (11.4, m), (11.62, m))
    arrow(ax, (12.4, m - 0.35), (12.4, b + 0.35), color=GRAY, ls='--')
    arrow(ax, (13.18, m), (13.58, m))


bpmn2('bpmn-perfil-icf.png', 'Proceso 2. Generación del perfil funcional CIF y decisión del médico', ['Médico', 'Backend HAB', 'Servicio ICF\n(PC propio)'], 14.3, 1.6, p2)


# --------------------------- Proceso 3
def p3(ax, ys):
    a, s = ys
    E(ax, 1.3, a, 'start', 'Inicio')
    T(ax, 3.0, a, 'Crear un usuario\n(nombre, correo, rol)', w=1.75)
    T(ax, 3.0, s, 'Validar y guardar\n(contraseña con Bcrypt)', w=1.75)
    T(ax, 5.1, a, 'Activar o desactivar\nla cuenta', w=1.75)
    T(ax, 5.1, s, 'Actualizar el estado\n(bloquea el ingreso)', w=1.75)
    T(ax, 7.2, a, 'Abrir el análisis y\nelegir los filtros', w=1.75)
    T(ax, 7.2, s, 'Calcular los agregados\n(sin datos personales)', w=1.75)
    T(ax, 9.3, a, 'Exportar a\nExcel o PDF', w=1.75)
    E(ax, 10.7, a, 'end', 'Fin')
    arrow(ax, (1.47, a), (2.12, a))
    arrow(ax, (3.0, a - 0.35), (3.0, s + 0.35))
    arrow(ax, (3.88, s), (4.22, a - 0.0))
    arrow(ax, (5.1, a - 0.35), (5.1, s + 0.35))
    arrow(ax, (5.98, s), (6.32, a))
    arrow(ax, (7.2, a - 0.35), (7.2, s + 0.35))
    arrow(ax, (8.08, s), (8.42, a))
    arrow(ax, (10.18, a), (10.53, a))


bpmn2('bpmn-administracion-analisis.png', 'Proceso 3. Administración de usuarios y análisis agregado', ['Administrador', 'Sistema HAB'], 11.4, 1.5, p3)


# --------------------------- ERD
def erd2():
    fig, ax = plt.subplots(figsize=(11.5, 5.6))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 5.6)
    ax.axis('off')

    def table(x, y, w, title, rows, col):
        rh = 0.28
        h = rh * (len(rows) + 1)
        ax.add_patch(Rectangle((x, y - h), w, h, fc='white', ec=INK, lw=1.3))
        ax.add_patch(Rectangle((x, y - rh), w, rh, fc=col, ec=INK, lw=1.3))
        ax.text(x + w / 2, y - rh / 2, title, ha='center', va='center', fontsize=10, fontweight='bold')
        for i, (n, t, k) in enumerate(rows):
            yy = y - rh * (i + 1.5)
            ax.text(x + 0.08, yy, k, fontsize=7.6, va='center', color=ORANGE, fontweight='bold')
            ax.text(x + 0.45, yy, n, fontsize=8, va='center')
            ax.text(x + w - 0.08, yy, t, fontsize=7.4, va='center', ha='right', color=GRAY)

    table(0.2, 5.2, 2.9, 'users', [('id', 'int', 'PK'), ('email', 'string · único', ''), ('full_name', 'string', ''), ('hashed_password', 'string', ''), ('is_active', 'bool', ''), ('role', 'admin | médico', '')], LIGHT['blue'])
    table(4.2, 5.2, 3.3, 'patients', [('id', 'int', 'PK'), ('numero_documento', 'string', ''), ('nombre_apellidos', 'string', ''), ('fecha_nacimiento · edad', 'date · int', ''), ('genero · orientacion_sexual', 'string', ''), ('causa_deficiencia', 'string', ''), ('cat_fisica · cat_psicosocial', 'string', ''), ('nivel_d1 … nivel_d6', 'int 0–100', ''), ('nivel_global', 'int', ''), ('prediction_profile', 'int', ''), ('prediction_description', 'string', ''), ('is_active', 'bool (borrado lógico)', ''), ('owner_id', 'int', 'FK')], LIGHT['green'])
    table(8.3, 5.2, 3.0, 'icf_suggestions', [('id', 'int', 'PK'), ('patient_id', 'int', 'FK'), ('batch_id', 'uuid (un lote)', ''), ('position', 'int', ''), ('component', 'b | s | d', ''), ('code · title', 'string', ''), ('qualifier (0–4)', 'int', ''), ('qualifier_cn · qualifier_cl', 'int (solo s)', ''), ('justification', 'string', ''), ('origin', 'llm | similarity | rules', ''), ('status', 'sugerido … rechazado', ''), ('original_code · model', 'string', ''), ('diag_cie · clinical_notes', 'string', ''), ('created_at', 'datetime', '')], LIGHT['orange'])
    arrow(ax, (3.1, 4.3), (4.2, 4.3), style='-', lw=1.5)
    ax.text(3.3, 4.38, '1', ha='center', fontsize=9, fontweight='bold')
    ax.text(4.0, 4.38, 'N', ha='center', fontsize=9, fontweight='bold')
    ax.text(3.65, 4.05, 'es dueño de', ha='center', fontsize=8, color=GRAY)
    arrow(ax, (7.5, 3.3), (8.3, 3.3), style='-', lw=1.5)
    ax.text(7.7, 3.38, '1', ha='center', fontsize=9, fontweight='bold')
    ax.text(8.1, 3.38, 'N', ha='center', fontsize=9, fontweight='bold')
    ax.text(7.9, 3.05, 'tiene', ha='center', fontsize=8, color=GRAY)
    ax.text(0.2, 2.95, 'Notas del modelo\n• Regenerar el perfil crea un lote nuevo\n  (batch_id) y conserva los anteriores:\n  queda la trazabilidad de qué sugirió\n  la máquina y qué decidió el médico.\n• No hay migraciones: las tablas se\n  crean con create_all.\n• El catálogo CIF-IA (1.593 códigos) y\n  sus embeddings viven en otra base\n  (PostgreSQL + pgvector) del PC del\n  servicio ICF y no guardan datos de\n  pacientes.', fontsize=8.2, va='top', color=INK, linespacing=1.45)
    save(fig, 'modelo-datos.png')


erd2()


# --------------------------- Despliegue
def deploy2():
    fig, ax = plt.subplots(figsize=(11.5, 6.6))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 6.6)
    ax.axis('off')

    def group(x, y, w, h, title, col):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=0.1', fc=LIGHT[col], ec=INK, lw=1.3))
        ax.text(x + 0.12, y + h - 0.14, title, fontsize=9.5, fontweight='bold', va='top')

    group(0.1, 4.5, 2.4, 2.0, 'Cliente', 'gray')
    box(ax, 0.3, 4.7, 2.0, 0.65, 'Navegador web\n(escritorio o teléfono)', fs=8.2)
    group(0.1, 0.2, 2.4, 3.9, 'GitHub', 'gray')
    box(ax, 0.3, 2.8, 2.0, 0.7, 'Repositorio\ndevelop · staging · master', fs=8)
    box(ax, 0.3, 1.5, 2.0, 0.95, 'GitHub Actions\nci-dev · ci-qa · ci-prod\n(aprobación manual\nen producción)', fs=7.8)
    group(2.9, 0.2, 4.6, 6.3, 'Render (nube) · 3 ambientes', 'orange')
    for nm, yy in [('DEV', 4.85), ('QA', 3.25), ('PROD', 1.65)]:
        ax.text(3.05, yy + 0.65, nm, fontsize=9, fontweight='bold', color=ORANGE)
        box(ax, 3.7, yy + 0.3, 1.55, 0.65, 'Frontend\n(sitio estático)', fc='white', fs=8)
        box(ax, 5.45, yy + 0.3, 1.9, 0.65, 'Backend FastAPI\n(servicio web)', fc='white', fs=8)
        box(ax, 5.45, yy - 0.5, 1.9, 0.6, 'PostgreSQL', fc=LIGHT['purple'], fs=8)
        arrow(ax, (5.25, yy + 0.62), (5.45, yy + 0.62))
        arrow(ax, (6.4, yy + 0.3), (6.4, yy + 0.1))
    group(8.0, 0.2, 3.35, 6.3, 'PC propio (Windows 11)', 'green')
    box(ax, 8.25, 5.3, 2.85, 0.7, 'Tailscale Funnel\n(HTTPS, puerto 11435)', fc='white', fs=8)
    box(ax, 8.25, 4.2, 2.85, 0.7, 'Caddy (Docker)\nexige el token Bearer', fc='white', fs=8)
    box(ax, 8.25, 3.1, 2.85, 0.7, 'Servicio ICF (Docker)\nreglas + RAG', fc='white', fs=8)
    box(ax, 8.2, 1.2, 1.45, 1.05, 'PostgreSQL +\npgvector (Docker)\ncatálogo CIF-IA', fc=LIGHT['purple'], fs=7.3)
    box(ax, 9.75, 1.2, 1.45, 1.05, 'Ollama (Windows)\nGPU: gemma4:e4b\ny bge-m3', fc='white', fs=7.3)
    arrow(ax, (9.67, 5.3), (9.67, 4.9))
    arrow(ax, (9.67, 4.2), (9.67, 3.8))
    arrow(ax, (8.9, 3.1), (8.95, 2.25))
    arrow(ax, (10.4, 3.1), (10.45, 2.25))
    arrow(ax, (2.3, 5.05), (3.7, 5.5), label='HTTPS', lpos=0.45, loff=(-0.1, 0.1))
    arrow(ax, (7.35, 5.5), (8.25, 5.65), color=ORANGE, ls='--')
    ax.text(7.8, 5.82, 'HTTPS +\ntoken', fontsize=7.4, ha='center', color=ORANGE)
    arrow(ax, (1.3, 2.8), (1.3, 2.45), color=GRAY)
    arrow(ax, (2.3, 1.9), (2.9, 1.9), color=PURPLE, ls='--', lw=1.6)
    ax.text(1.4, 1.2, 'despliegue automático\nen cada rama', fontsize=7.4, ha='center', color=PURPLE)
    save(fig, 'despliegue.png')


deploy2()
print('figuras v2 listas')
