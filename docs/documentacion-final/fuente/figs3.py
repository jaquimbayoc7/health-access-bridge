"""Diagramas de la base de datos: el del backend con su nota al dia y el de la base vectorial del servicio ICF (HU-07j).

Uso (desde esta carpeta):  python figs3.py
Escribe fig/modelo-datos.png (misma figura de figs2.py con la nota actualizada) y fig/modelo-datos-vectorial.png.
"""
from figs import *  # helpers y estilos


def table(ax, x, y, w, title, rows, col, nx=0.5):
    rh = 0.28
    h = rh * (len(rows) + 1)
    ax.add_patch(Rectangle((x, y - h), w, h, fc='white', ec=INK, lw=1.3))
    ax.add_patch(Rectangle((x, y - rh), w, rh, fc=col, ec=INK, lw=1.3))
    ax.text(x + w / 2, y - rh / 2, title, ha='center', va='center', fontsize=10, fontweight='bold')
    for i, (n, t, k) in enumerate(rows):
        yy = y - rh * (i + 1.5)
        ax.text(x + 0.08, yy, k, fontsize=7.6, va='center', color=ORANGE, fontweight='bold')
        ax.text(x + nx, yy, n, fontsize=8, va='center')
        ax.text(x + w - 0.08, yy, t, fontsize=7.4, va='center', ha='right', color=GRAY)
    return y - h


def erd_backend():
    fig, ax = plt.subplots(figsize=(11.5, 5.6))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 5.6)
    ax.axis('off')
    table(ax, 0.2, 5.2, 2.9, 'users', [('id', 'int', 'PK'), ('email', 'string · único', ''), ('full_name', 'string', ''), ('hashed_password', 'string', ''), ('is_active', 'bool', ''), ('role', 'admin | médico', '')], LIGHT['blue'])
    table(ax, 4.2, 5.2, 3.3, 'patients', [('id', 'int', 'PK'), ('numero_documento', 'string', ''), ('nombre_apellidos', 'string', ''), ('fecha_nacimiento · edad', 'date · int', ''), ('genero · orientacion_sexual', 'string', ''), ('causa_deficiencia', 'string', ''), ('cat_fisica · cat_psicosocial', 'string', ''), ('nivel_d1 … nivel_d6', 'int 0–100', ''), ('nivel_global', 'int', ''), ('prediction_profile', 'int', ''), ('prediction_description', 'string', ''), ('is_active', 'bool (borrado lógico)', ''), ('owner_id', 'int', 'FK')], LIGHT['green'])
    table(ax, 8.1, 5.2, 3.35, 'icf_suggestions', [('id', 'int', 'PK'), ('patient_id', 'int', 'FK'), ('batch_id', 'uuid (un lote)', ''), ('position', 'int', ''), ('component', 'b | s | d', ''), ('code · title', 'string', ''), ('qualifier (0–4)', 'int', ''), ('qualifier_cn · _cl', 'int (solo s)', ''), ('qualifier_suggested', 'int · sistema', ''), ('qualifier_confirmed', 'bool · médico', ''), ('justification', 'modelo', ''), ('justification_medico', 'médico', ''), ('origin', 'llm | similarity | rules', ''), ('status', 'sugerido … rechazado', ''), ('original_code · model', 'string', ''), ('diag_cie · clinical_notes', 'string', ''), ('created_at', 'datetime', '')], LIGHT['orange'])
    arrow(ax, (3.1, 4.3), (4.2, 4.3), style='-', lw=1.5)
    ax.text(3.3, 4.38, '1', ha='center', fontsize=9, fontweight='bold')
    ax.text(4.0, 4.38, 'N', ha='center', fontsize=9, fontweight='bold')
    ax.text(3.65, 4.05, 'es dueño de', ha='center', fontsize=8, color=GRAY)
    arrow(ax, (7.5, 3.3), (8.1, 3.3), style='-', lw=1.5)
    ax.text(7.65, 3.38, '1', ha='center', fontsize=9, fontweight='bold')
    ax.text(7.95, 3.38, 'N', ha='center', fontsize=9, fontweight='bold')
    ax.text(7.8, 3.05, 'tiene', ha='center', fontsize=8, color=GRAY)
    ax.text(0.2, 2.95, 'Notas del modelo\n• Regenerar el perfil crea un lote nuevo\n  (batch_id) y conserva los anteriores:\n  queda la trazabilidad de qué sugirió\n  la máquina y qué decidió el médico.\n• No hay migraciones: las tablas se\n  crean con create_all y las columnas\n  nuevas se agregan al arrancar.\n• El catálogo CIF-IA y la memoria de casos\n  confirmados viven en otra base\n  (PostgreSQL + pgvector) del PC del\n  servicio ICF, sin identificadores\n  de pacientes (figura de la base vectorial).', fontsize=8.2, va='top', color=INK, linespacing=1.45)
    save(fig, 'modelo-datos.png')


def erd_vectorial():
    def vt(*a):
        return table(*a, nx=0.9)

    fig, ax = plt.subplots(figsize=(12, 6.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.6)
    ax.axis('off')
    ax.add_patch(Rectangle((0.1, 0.1), 7.45, 6.4, fc='#f8fafc', ec='#cbd5e1', lw=1, ls='--'))
    ax.add_patch(Rectangle((7.7, 0.1), 4.2, 6.4, fc='#fffaf0', ec='#fdba74', lw=1, ls='--'))
    ax.text(0.25, 6.33, 'Conocimiento: catálogo CIF-IA (no cambia con el uso)', fontsize=9, fontweight='bold', color=GRAY, va='center')
    ax.text(7.85, 6.33, 'Memoria de casos (crece con el uso)', fontsize=9, fontweight='bold', color=ORANGE, va='center')
    vt(ax, 0.25, 6.0, 3.7, 'icf_codes', [('code', 'text', 'PK'), ('component', 'b | s | d | e', ''), ('chapter · level', 'int', ''), ('parent', 'text', 'FK'), ('title', 'text (de la OMS)', ''), ('description', 'text', ''), ('inclusions · exclusions', 'text', ''), ('embedding', 'vector(1024)', '')], LIGHT['blue'])
    vt(ax, 4.5, 6.0, 3.0, 'icf_hab_domains', [('hab_domain', 'D1 … D6', 'PK'), ('chapter_code', 'd1 … d6', ''), ('chapter_name', 'text', ''), ('official_domain', 'text', ''), ('note', 'text', '')], LIGHT['green'])
    vt(ax, 4.5, 3.95, 3.0, 'icf_domain_map', [('official_domain', 'text', 'PK'), ('code', 'text', 'PK · FK'), ('hab_domain', 'D1 … D6', 'FK'), ('ages', '6-17 | 18+ | both', '')], LIGHT['green'])
    vt(ax, 7.85, 6.0, 3.9, 'icf_cases', [('case_key', 'uuid del lote', 'PK'), ('context', 'texto clínico (sin identificadores)', ''), ('diag', 'text', ''), ('age_group', '6-17 | 18+', ''), ('embedding', 'vector(1024)', ''), ('updated_at', 'timestamptz', '')], LIGHT['orange'])
    vt(ax, 7.85, 3.7, 3.9, 'icf_case_codes', [('case_key', 'text', 'PK · FK'), ('item_ref', 'int (sugerencia)', 'PK'), ('component', 'b | s | d', ''), ('code', 'text (→ icf_codes)', ''), ('status', 'aceptado | editado', ''), ('qualifier', '0–4 (el del médico)', ''), ('qualifier_cn · qualifier_cl', 'int (solo s)', ''), ('qualifier_suggested', '0–4 (el del sistema)', ''), ('justification', 'text', ''), ('updated_at', 'timestamptz', '')], LIGHT['orange'])
    arrow(ax, (9.8, 4.04), (9.8, 3.7), style='-', lw=1.5)
    ax.text(9.62, 3.95, '1', ha='center', fontsize=9, fontweight='bold')
    ax.text(9.62, 3.76, 'N', ha='center', fontsize=9, fontweight='bold')
    ax.text(9.95, 3.87, 'contiene', fontsize=8, color=GRAY)
    arrow(ax, (6.0, 4.32), (6.0, 3.95), style='-', lw=1.5)
    ax.text(5.82, 4.22, '1', ha='center', fontsize=9, fontweight='bold')
    ax.text(5.82, 4.0, 'N', ha='center', fontsize=9, fontweight='bold')
    arrow(ax, (3.95, 3.7), (4.5, 3.7), style='-', lw=1.5)
    ax.text(4.07, 3.78, '1', ha='center', fontsize=9, fontweight='bold')
    ax.text(4.4, 3.78, 'N', ha='center', fontsize=9, fontweight='bold')
    nota = ['Cómo se usa', '• Búsqueda por similitud coseno (<=>) entre', '  el vector del caso nuevo y los de icf_codes', '  (candidatos) y los de icf_cases (casos', '  parecidos).', '• Los vectores los calcula bge-m3 (1.024', '  dimensiones).', '• La memoria no guarda nombre, documento,', '  edad ni género; case_key es interno.', '• Rechazar un código lo retira; un caso sin', '  códigos se borra.', '• code apunta a icf_codes por el valor', '  (relación lógica, sin clave foránea).']
    ax.text(0.25, 3.3, chr(10).join(nota), fontsize=8.2, va='top', color=INK, linespacing=1.45)
    save(fig, 'modelo-datos-vectorial.png')


erd_backend()
erd_vectorial()
