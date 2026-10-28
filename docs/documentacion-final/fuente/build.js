const fs = require('fs');
const path = require('path');
const D = require('docx');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun, Header, AlignmentType, HeadingLevel,
  WidthType, ShadingType, BorderStyle, TableOfContents, PageNumber, PageOrientation, LevelFormat, NumberFormat,
  SectionType, VerticalAlign, TabStopType,
} = D;

const HERE = __dirname;
const REPO = 'C:/Users/jaqui/OneDrive/Documentos/GitHub/health-access-bridge';
const OUT = path.join(REPO, 'docs/documentacion-final/Documentacion_Final_HAB_borrador_v0.2.docx');
const REFS = require('./refs.js');

// ------------------------------------------------------------------ medidas ICONTEC (NTC 1486), tamaño carta
const CM = 567; // 1 cm en DXA
const MARGIN = { top: 3 * CM, bottom: 3 * CM, left: 4 * CM, right: 2 * CM };
const PORTRAIT = { w: 12240, h: 15840 };
const TEXT_W_P = PORTRAIT.w - MARGIN.left - MARGIN.right;       // ancho útil vertical
const TEXT_W_L = PORTRAIT.h - MARGIN.left - MARGIN.right;       // ancho útil horizontal
const FONT = 'Arial';

// ------------------------------------------------------------------ lectura del contenido
const SRC = ['c1.md', 'c2.md', 'c3.md', 'c4.md', 'c5.md'].map((f) => fs.readFileSync(path.join(HERE, f), 'utf8').replace(/\r\n/g, '\n')).join('\n\n');

function imgPath(spec) {
  const [pre, name] = spec.split(':');
  if (pre === 'fig') return path.join(HERE, 'fig', name);
  if (pre === 'man') return path.join(REPO, 'docs/manuals/img', name);
  if (pre === 'mock') return path.join(REPO, 'frontend/design/images', name);
  if (pre === 'c4') return path.join(HERE, 'c4t', name);
  if (pre === 'ani') return path.join(HERE, 'ani', name);
  throw new Error('prefijo de imagen desconocido: ' + spec);
}
function imgSize(file) {
  const b = fs.readFileSync(file);
  if (b[0] === 0x89 && b[1] === 0x50) return { w: b.readUInt32BE(16), h: b.readUInt32BE(20), type: 'png' };
  let i = 2;
  while (i < b.length) {
    if (b[i] !== 0xff) { i++; continue; }
    const m = b[i + 1];
    if (m >= 0xc0 && m <= 0xcf && m !== 0xc4 && m !== 0xc8 && m !== 0xcc) return { h: b.readUInt16BE(i + 5), w: b.readUInt16BE(i + 7), type: 'jpg' };
    i += 2 + b.readUInt16BE(i + 2);
  }
  throw new Error('no se pudo leer ' + file);
}

// ------------------------------------------------------------------ primera pasada: bloques y numeración
const blocks = [];
const figIds = {}, tabIds = {};
let nFig = 0, nTab = 0, pendingTable = null;
const lines = SRC.split('\n');
for (let i = 0; i < lines.length;) {
  const ln = lines[i];
  if (!ln.trim()) { i++; continue; }
  let m;
  if ((m = ln.match(/^(#{1,3}) (.*)$/))) { blocks.push({ t: 'h', level: m[1].length, text: m[2] }); i++; continue; }
  if ((m = ln.match(/^\[\[T(?:#([\w-]+))?:\s*(.*)\]\]$/))) { nTab++; pendingTable = { n: nTab, title: m[2] }; if (m[1]) tabIds[m[1]] = nTab; i++; continue; }
  if ((m = ln.match(/^\[\[S:\s*(.*)\]\]$/))) { blocks.push({ t: 'note', text: m[1] }); i++; continue; }
  if ((m = ln.match(/^\[\[F:\s*(.*)\]\]$/))) {
    const [file, title, source, width] = m[1].split('|').map((s) => s.trim());
    nFig++;
    figIds[path.basename(file.split(':')[1], path.extname(file))] = nFig;
    blocks.push({ t: 'fig', n: nFig, file, title, source, width: parseFloat(width) });
    i++; continue;
  }
  if (ln.trim() === '[[LANDSCAPE]]') { blocks.push({ t: 'sec', orient: 'L' }); i++; continue; }
  if (ln.trim() === '[[PORTRAIT]]') { blocks.push({ t: 'sec', orient: 'P' }); i++; continue; }
  if (ln.trim() === '[[REFERENCES]]') { blocks.push({ t: 'refs' }); i++; continue; }
  if (ln.startsWith('|')) {
    const rows = [];
    while (i < lines.length && lines[i].startsWith('|')) {
      const cells = lines[i].replace(/^\||\|$/g, '').split('|').map((s) => s.trim());
      if (!cells.every((c) => /^:?-+:?$/.test(c))) rows.push(cells);
      i++;
    }
    blocks.push({ t: 'table', rows, cap: pendingTable });
    pendingTable = null;
    continue;
  }
  if (/^- /.test(ln)) {
    const items = [];
    while (i < lines.length && /^- /.test(lines[i])) { items.push(lines[i].slice(2)); i++; }
    blocks.push({ t: 'ul', items }); continue;
  }
  if (/^\d+\. /.test(ln)) {
    const items = [];
    while (i < lines.length && /^\d+\. /.test(lines[i])) { items.push(lines[i].replace(/^\d+\. /, '')); i++; }
    blocks.push({ t: 'ol', items }); continue;
  }
  const para = [ln];
  i++;
  while (i < lines.length && lines[i].trim() && !/^(#{1,3} |\[\[|\||- |\d+\. )/.test(lines[i])) { para.push(lines[i]); i++; }
  blocks.push({ t: 'p', text: para.join(' ') });
}

// ------------------------------------------------------------------ citas APA 7
const cited = new Set();
const firstUse = new Set();
function stripAcc(s) { return s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase(); }
function citeOne(key) {
  const r = REFS[key];
  if (!r) throw new Error('referencia sin definir: ' + key);
  cited.add(key);
  let a = r.s;
  if (r.sa) { if (firstUse.has(key)) a = r.sa; else firstUse.add(key); }
  return { text: `${a}, ${r.y}`, sort: stripAcc(a) + r.y };
}
function resolveText(s) {
  s = s.replace(/\[-@([\w]+)\]/g, (_, k) => { cited.add(k); if (!REFS[k]) throw new Error('ref ' + k); return `(${REFS[k].y})`; });
  s = s.replace(/\[(@[^\]]+)\]/g, (_, inner) => {
    const parts = inner.split(';').map((x) => citeOne(x.trim().replace(/^@/, '')));
    parts.sort((a, b) => a.sort.localeCompare(b.sort));
    return '(' + parts.map((p) => p.text).join('; ') + ')';
  });
  s = s.replace(/\{F:([\w-]+)\}/g, (_, id) => { if (!figIds[id]) throw new Error('figura sin id: ' + id); return `figura ${figIds[id]}`; });
  s = s.replace(/\{T:([\w-]+)\}/g, (_, id) => { if (!tabIds[id]) throw new Error('tabla sin id: ' + id); return `tabla ${tabIds[id]}`; });
  return s;
}

// ------------------------------------------------------------------ inline: **negrita**, *cursiva*, `código`
function runs(text, o = {}) {
  const base = { font: FONT, size: o.size || 24, bold: o.bold, italics: o.italics, color: o.color };
  const out = [];
  const parts = resolveText(text).split(/(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/);
  for (const p of parts) {
    if (!p) continue;
    if (p.startsWith('**')) out.push(new TextRun({ ...base, text: p.slice(2, -2), bold: true }));
    else if (p.startsWith('`')) out.push(new TextRun({ ...base, text: p.slice(1, -1), font: 'Consolas', size: (o.size || 24) - 2 }));
    else if (p.startsWith('*') && p.length > 2) out.push(new TextRun({ ...base, text: p.slice(1, -1), italics: !o.italics }));
    else out.push(new TextRun({ ...base, text: p }));
  }
  return out;
}

// ------------------------------------------------------------------ construcción
const numberingConfigs = [{ reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }];
let olCount = 0;

function widthsFor(rows, total) {
  const n = rows[0].length;
  const w = new Array(n).fill(0);
  rows.forEach((r) => r.forEach((c, i) => { w[i] = Math.max(w[i], Math.min(Math.max(c.length, 6), 70)); }));
  const weights = w.map((x) => Math.sqrt(x) + 1.5);
  const sum = weights.reduce((a, b) => a + b, 0);
  let widths = weights.map((x) => Math.max(Math.round((x / sum) * total), 850));
  const diff = total - widths.reduce((a, b) => a + b, 0);
  widths[widths.indexOf(Math.max(...widths))] += diff;
  return widths;
}

function buildTable(block, textW) {
  const widths = widthsFor(block.rows, textW);
  const border = { style: BorderStyle.SINGLE, size: 4, color: '8C9BB0' };
  const borders = { top: border, bottom: border, left: border, right: border };
  const rows = block.rows.map((r, ri) => new TableRow({
    tableHeader: ri === 0, cantSplit: true,
    children: r.map((c, ci) => new TableCell({
      width: { size: widths[ci], type: WidthType.DXA }, borders, verticalAlign: VerticalAlign.TOP,
      shading: ri === 0 ? { fill: 'D9E2F3', type: ShadingType.CLEAR, color: 'auto' } : undefined,
      margins: { top: 50, bottom: 50, left: 80, right: 80 },
      children: [new Paragraph({ spacing: { line: 240, after: 0 }, alignment: AlignmentType.LEFT, children: runs(c, { size: 19, bold: ri === 0 }) })],
    })),
  }));
  const out = [];
  if (block.cap) {
    out.push(new Paragraph({ keepNext: true, spacing: { line: 276, before: 200, after: 80 }, children: [new TextRun({ font: FONT, size: 22, bold: true, text: `Tabla ${block.cap.n}. ` }), ...runs(block.cap.title, { size: 22 })] }));
  }
  out.push(new Table({ width: { size: textW, type: WidthType.DXA }, columnWidths: widths, rows }));
  return out;
}

function buildFigure(b, textW, maxH) {
  const file = imgPath(b.file);
  const s = imgSize(file);
  let wDxa = Math.min(b.width * CM, textW);
  let hDxa = wDxa * s.h / s.w;
  if (hDxa > maxH) { hDxa = maxH; wDxa = hDxa * s.w / s.h; }
  const px = (dxa) => Math.round((dxa / 1440) * 96);
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 160, after: 60, line: 240, lineRule: D.LineRuleType.AUTO }, children: [new ImageRun({ type: s.type, data: fs.readFileSync(file), transformation: { width: px(wDxa), height: px(hDxa) }, altText: { title: b.title, description: b.title, name: path.basename(file) } })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { line: 276, after: 20 }, children: [new TextRun({ font: FONT, size: 22, bold: true, text: `Figura ${b.n}. ` }), ...runs(b.title, { size: 22 })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { line: 240, after: 200 }, children: [new TextRun({ font: FONT, size: 20, italics: true, text: 'Fuente: ' }), ...runs(b.source, { size: 20 })] }),
  ];
}

function refsBlock() {
  const keys = [...cited].sort((a, b) => stripAcc(REFS[a].a).localeCompare(stripAcc(REFS[b].a)));
  return keys.map((k) => new Paragraph({ spacing: { line: 300, after: 120 }, indent: { left: 720, hanging: 720 }, alignment: AlignmentType.LEFT, children: runs(REFS[k].a, { size: 22 }) }));
}

// secciones del cuerpo
const sections = []; // {orient, children}
let cur = { orient: 'P', children: [] };
let firstH1 = true;
const tocRows = []; // para listas
const tableList = [], figList = [];
blocks.forEach((b) => { if (b.t === 'table' && b.cap) tableList.push(b.cap); if (b.t === 'fig') figList.push(b); });

for (const b of blocks) {
  const textW = cur.orient === 'L' ? TEXT_W_L : TEXT_W_P;
  const maxH = cur.orient === 'L' ? 7600 : 9800;
  if (b.t === 'sec') { sections.push(cur); cur = { orient: b.orient, children: [] }; continue; }
  if (b.t === 'h') {
    const lvl = [HeadingLevel.HEADING_1, HeadingLevel.HEADING_2, HeadingLevel.HEADING_3][b.level - 1];
    cur.children.push(new Paragraph({ heading: lvl, pageBreakBefore: b.level === 1 && !firstH1 && cur.children.length > 0, keepNext: true, children: [new TextRun({ text: b.text })] }));
    if (b.level === 1) firstH1 = false;
    continue;
  }
  if (b.t === 'p') { cur.children.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, children: runs(b.text) })); continue; }
  if (b.t === 'ul') { b.items.forEach((it) => cur.children.push(new Paragraph({ numbering: { reference: 'bullets', level: 0 }, alignment: AlignmentType.LEFT, spacing: { line: 336, after: 80 }, children: runs(it) }))); continue; }
  if (b.t === 'ol') {
    olCount++;
    const ref = 'ol' + olCount;
    numberingConfigs.push({ reference: ref, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] });
    b.items.forEach((it) => cur.children.push(new Paragraph({ numbering: { reference: ref, level: 0 }, alignment: AlignmentType.LEFT, spacing: { line: 336, after: 80 }, children: runs(it) })));
    continue;
  }
  if (b.t === 'note') { cur.children.push(new Paragraph({ spacing: { line: 240, before: 60, after: 200 }, children: [new TextRun({ font: FONT, size: 19, italics: true, text: 'Nota. ' }), ...runs(b.text, { size: 19 })] })); continue; }
  if (b.t === 'table') { cur.children.push(...buildTable(b, textW)); continue; }
  if (b.t === 'fig') { cur.children.push(...buildFigure(b, textW, maxH)); continue; }
  if (b.t === 'refs') { cur.children.push(...refsBlock()); continue; }
}
sections.push(cur);

// ------------------------------------------------------------------ portada y preliminares
const center = (text, o = {}) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { line: 276, after: o.after ?? 120, before: o.before ?? 0 }, children: [new TextRun({ font: FONT, size: o.size || 24, bold: o.bold, text })] });
const cover = [
  center('HEALTH ACCESS BRIDGE (HAB)', { size: 30, bold: true, before: 600, after: 160 }),
  center('Plataforma web para el registro de personas con discapacidad, la predicción de barreras de acceso y la sugerencia asistida por inteligencia artificial del perfil funcional CIF', { size: 24, after: 600 }),
  center('DOCUMENTACIÓN FINAL DEL PROYECTO', { size: 26, bold: true, after: 100 }),
  center('Trabajo Integrador I, II (750128) y III (750129)', { size: 24, after: 600 }),
  center('JULIÁN ANDRÉS QUIMBAYO CASTRO', { bold: true, after: 60 }),
  center('[Código estudiantil: completar]', { after: 700 }),
  center('Docente de la asignatura', { after: 40 }),
  center('Beatriz Eugenia Florián Gaviria, Ph.D.', { bold: true, after: 200 }),
  center('Asesora del proyecto', { after: 40 }),
  center('Deisy Chaves, Ph.D.', { bold: true, after: 600 }),
  center('UNIVERSIDAD DEL VALLE', { bold: true, after: 40 }),
  center('Facultad de Ingeniería', { after: 40 }),
  center('Escuela de Ingeniería de Sistemas y Computación', { after: 40 }),
  center('Maestría para el Desarrollo de Aplicaciones Inteligentes (CODING)', { after: 40 }),
  center('Grupo 01 · Periodo agosto – diciembre de 2026', { after: 500 }),
  center('Cali, Colombia', { after: 40 }),
  center('2026', { bold: true }),
  center('Versión inicial para revisión (v0.2) · 28 de octubre de 2026', { size: 20, before: 200 }),
];

const h1Plain = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: t })] });
const listLines = (items) => items.map((t) => new Paragraph({ spacing: { line: 300, after: 80 }, indent: { left: 720, hanging: 720 }, children: runs(t, { size: 22 }) }));
const siglas = [
  ['BPMN', 'Business Process Model and Notation (notación de modelado de procesos de negocio)'],
  ['CI/CD', 'Integración continua y despliegue continuo'],
  ['CIF', 'Clasificación Internacional del Funcionamiento, de la Discapacidad y de la Salud (ICF, en inglés)'],
  ['CIF-IA', 'Versión del catálogo CIF para infancia y adolescencia usada por el sistema'],
  ['CORS', 'Intercambio de recursos de origen cruzado'],
  ['DoD', 'Definition of Done (definición de terminado)'],
  ['HAB', 'Health Access Bridge'],
  ['HCI', 'Interacción humano-computador'],
  ['HU', 'Historia de usuario'],
  ['IA', 'Inteligencia artificial'],
  ['JWT', 'JSON Web Token (token de acceso firmado)'],
  ['LLM', 'Modelo de lenguaje de gran tamaño'],
  ['RAG', 'Recuperación aumentada por generación'],
  ['RBAC', 'Control de acceso basado en roles'],
  ['RLCPD', 'Registro de Localización y Caracterización de Personas con Discapacidad'],
  ['SUS', 'Escala de Usabilidad del Sistema'],
  ['UAT', 'Pruebas de aceptación de usuario'],
  ['WCAG', 'Pautas de accesibilidad para el contenido web'],
];
const siglasRows = [['Sigla', 'Significado'], ...siglas];
const prelim = [
  new Paragraph({ children: [new TextRun({ text: 'CONTENIDO', font: FONT, size: 24, bold: true })], alignment: AlignmentType.CENTER, spacing: { after: 240 } }),
  new TableOfContents('Contenido', { hyperlink: true, headingStyleRange: '1-3' }),
  new Paragraph({ pageBreakBefore: true, alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: 'LISTA DE TABLAS', font: FONT, size: 24, bold: true })] }),
  ...listLines(tableList.map((c) => `Tabla ${c.n}. ${c.title}`)),
  new Paragraph({ pageBreakBefore: true, alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: 'LISTA DE FIGURAS', font: FONT, size: 24, bold: true })] }),
  ...listLines(figList.map((f) => `Figura ${f.n}. ${f.title}`)),
  new Paragraph({ pageBreakBefore: true, alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: 'LISTA DE SIGLAS', font: FONT, size: 24, bold: true })] }),
  ...buildTable({ rows: siglasRows, cap: null }, TEXT_W_P),
];

// ------------------------------------------------------------------ documento
const hdr = () => new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ font: FONT, size: 20, children: [PageNumber.CURRENT] })] })] });
const pageProps = (orient, extra = {}) => ({
  page: {
    size: { width: PORTRAIT.w, height: PORTRAIT.h, orientation: orient === 'L' ? PageOrientation.LANDSCAPE : PageOrientation.PORTRAIT },
    margin: { top: MARGIN.top, bottom: MARGIN.bottom, left: MARGIN.left, right: MARGIN.right, header: 850, footer: 850 },
    ...extra,
  },
});

const docSections = [
  { properties: { ...pageProps('P') }, children: cover },
  { properties: { ...pageProps('P', { pageNumbers: { start: 1, formatType: NumberFormat.LOWER_ROMAN } }), type: SectionType.NEXT_PAGE }, headers: { default: hdr() }, children: prelim },
];
sections.forEach((s, idx) => {
  docSections.push({
    properties: { ...pageProps(s.orient, idx === 0 ? { pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL } } : {}), type: SectionType.NEXT_PAGE },
    headers: { default: hdr() },
    children: s.children,
  });
});

const doc = new Document({
  creator: 'Julián Andrés Quimbayo Castro',
  title: 'Health Access Bridge: documentación final del proyecto (v0.2)',
  description: 'Documentación final de Trabajo Integrador II y III, con formato ICONTEC (NTC 1486) y citación APA 7',
  features: { updateFields: true },
  styles: {
    default: { document: { run: { font: FONT, size: 24 }, paragraph: { spacing: { line: 360, after: 160 } } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 24, bold: true, color: '000000' }, paragraph: { spacing: { before: 120, after: 240, line: 360 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 24, bold: true, color: '000000' }, paragraph: { spacing: { before: 240, after: 160, line: 360 }, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 24, bold: true, italics: true, color: '000000' }, paragraph: { spacing: { before: 200, after: 120, line: 360 }, outlineLevel: 2 } },
    ],
  },
  numbering: { config: numberingConfigs },
  sections: docSections,
});

fs.mkdirSync(path.dirname(OUT), { recursive: true });
Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log('listo', OUT, (buf.length / 1024 / 1024).toFixed(1) + ' MB', '· figuras', nFig, '· tablas', nTab, '· referencias citadas', cited.size);
});
