// HU-08 — exportación del dashboard de análisis a Excel y PDF.
// Una sola fuente de datos (buildSections) alimenta los dos formatos, de modo que el archivo coincide con lo que se ve.
import * as XLSX from 'xlsx';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import type { AnalyticsSummary, CountEntry } from '@/services/analytics';
import { analyticsLabels, formatNumber, formatPercent, type Labels, type Lang } from './analyticsLabels';

type Cell = string | number;

export interface ReportSection {
  id: 'summary' | 'distributions' | 'domains' | 'icf' | 'codes';
  title: string;
  /** Un bloque por tabla; en Excel se apilan en la misma hoja. */
  tables: { title?: string; head: string[]; rows: Cell[][] }[];
}

export interface ChartImage {
  title: string;
  dataUrl: string;
  /** Tamaño original en píxeles, para conservar la proporción en el PDF. */
  width?: number;
  height?: number;
  /** Leyenda en texto: la de recharts es HTML, queda fuera del SVG y no viaja en la imagen. */
  note?: string;
}

const FILTER_LABEL = (L: Labels): Record<string, string> => ({
  genero: L.gender,
  causa: L.cause,
  perfil: L.profile,
  edad_min: L.ageFrom,
  edad_max: L.ageTo,
  owner_id: L.doctor,
});

const entryRows = (entries: CountEntry[]): Cell[][] => entries.map((e) => [e.key, e.count]);

export function buildSections(summary: AnalyticsSummary, lang: Lang): ReportSection[] {
  const L = analyticsLabels(lang);
  const labels = FILTER_LABEL(L);
  const filters = Object.entries(summary.filters).map(([k, v]) => `${labels[k] ?? k}: ${v}`);
  const { totals, distributions: d, icf } = summary;

  const summaryRows: Cell[][] = [
    [L.title, summary.scope === 'global' ? L.scopeGlobal : L.scopeOwn],
    [L.generatedAt, summary.generated_at],
    [L.filters, filters.length ? filters.join(' · ') : L.all],
    [L.kpiPatients, totals.patients],
    [L.kpiPrediction, totals.with_prediction],
    [L.kpiPredictionRate, formatPercent(totals.prediction_rate)],
    [L.kpiMeanAge, formatNumber(totals.mean_age)],
    [L.kpiMeanGlobal, formatNumber(totals.mean_global_level)],
    [L.kpiWithIcf, totals.with_icf_profile],
    [L.kpiSuggestions, icf.suggestions],
    [L.kpiDecided, icf.decided],
    [L.kpiAcceptance, formatPercent(icf.acceptance_rate)],
  ];

  const header = [L.colCategory, L.colPatients];
  const distributionTables = [
    { title: L.chProfile, rows: d.profile },
    { title: L.chFisica, rows: d.cat_fisica },
    { title: L.chPsicosocial, rows: d.cat_psicosocial },
    { title: L.chGenero, rows: d.genero },
    { title: L.chAge, rows: d.age_group },
    { title: L.chCause, rows: d.cause },
  ].map((t) => ({ title: t.title, head: header, rows: entryRows(t.rows) }));

  const statusTable = {
    title: L.chStatus,
    head: [L.colComponent, L.sugerido, L.aceptado, L.editado, L.rechazado, L.colCount, L.kpiAcceptance],
    rows: (['b', 's', 'd'] as const).map((c) => {
      const s = icf.by_component[c];
      return [L[c], s.sugerido, s.aceptado, s.editado, s.rechazado, s.total, formatPercent(s.acceptance_rate)];
    }),
  };

  return [
    { id: 'summary', title: L.sheetSummary, tables: [{ head: [L.colIndicator, L.colValue], rows: summaryRows }] },
    { id: 'distributions', title: L.sheetDistributions, tables: distributionTables },
    {
      id: 'domains',
      title: L.sheetDomains,
      tables: [{
        title: L.chDomains,
        head: [L.colDomain, L.colName, L.colMean, L.colN],
        rows: summary.domains.map((x) => [x.domain, x.name, formatNumber(x.mean), x.n]),
      }],
    },
    {
      id: 'icf',
      title: L.sheetIcf,
      tables: [
        statusTable,
        { title: L.chOrigin, head: header.map((h, i) => (i ? L.colCount : h)), rows: entryRows(icf.by_origin) },
        { title: L.chModel, head: header.map((h, i) => (i ? L.colCount : h)), rows: entryRows(icf.by_model) },
      ],
    },
    {
      id: 'codes',
      title: L.sheetCodes,
      tables: [{
        title: L.chTopCodes,
        head: [L.colCode, L.colTitle, L.colComponent, L.colCount, L.colAccepted, L.colRejected],
        rows: icf.top_codes.map((c) => [c.code, c.title, L[c.component], c.count, c.accepted, c.rejected]),
      }],
    },
  ];
}

/** Excel de 5 hojas (resumen, distribuciones, dominios, ICF y códigos). */
export function buildWorkbook(summary: AnalyticsSummary, lang: Lang): XLSX.WorkBook {
  const wb = XLSX.utils.book_new();
  for (const section of buildSections(summary, lang)) {
    const aoa: Cell[][] = [];
    for (const table of section.tables) {
      if (table.title) aoa.push([table.title]);
      aoa.push(table.head, ...table.rows, []);
    }
    const ws = XLSX.utils.aoa_to_sheet(aoa);
    ws['!cols'] = section.tables[0].head.map((_, i) => ({ wch: i === 1 && section.id !== 'summary' ? 44 : 26 }));
    XLSX.utils.book_append_sheet(wb, ws, section.title.slice(0, 31));
  }
  return wb;
}

export const exportFilename = (ext: 'xlsx' | 'pdf', now: Date = new Date()): string =>
  `analisis_hab_${now.toISOString().slice(0, 10)}.${ext}`;

export function exportExcel(summary: AnalyticsSummary, lang: Lang, now: Date = new Date()): string {
  const name = exportFilename('xlsx', now);
  XLSX.writeFile(buildWorkbook(summary, lang), name);
  return name;
}

/**
 * Convierte un SVG de recharts en una imagen JPEG (data URL) para incrustarla en el PDF. Es JPEG y no PNG a propósito:
 * con PNG sin comprimir el PDF de 10 gráficos pesaba unos 19 MB; en JPEG pesa una fracción.
 */
export async function svgToImage(svg: SVGSVGElement, scale = 2, quality = 0.85): Promise<{ dataUrl: string; width: number; height: number }> {
  const box = svg.getBoundingClientRect();
  const width = Math.max(1, Math.round(box.width || Number(svg.getAttribute('width')) || 400));
  const height = Math.max(1, Math.round(box.height || Number(svg.getAttribute('height')) || 300));
  const clone = svg.cloneNode(true) as SVGSVGElement;
  clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
  clone.setAttribute('width', String(width));
  clone.setAttribute('height', String(height));
  if (!clone.getAttribute('viewBox')) clone.setAttribute('viewBox', `0 0 ${width} ${height}`);
  const xml = new XMLSerializer().serializeToString(clone);
  const url = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(xml)}`;
  const image = new Image();
  await new Promise<void>((resolve, reject) => {
    image.onload = () => resolve();
    image.onerror = () => reject(new Error('No se pudo rasterizar el gráfico'));
    image.src = url;
  });
  const canvas = document.createElement('canvas');
  canvas.width = width * scale;
  canvas.height = height * scale;
  const ctx = canvas.getContext('2d');
  if (!ctx) throw new Error('Canvas no disponible');
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
  return { dataUrl: canvas.toDataURL('image/jpeg', quality), width, height };
}

export function buildPdf(summary: AnalyticsSummary, lang: Lang, charts: ChartImage[] = []): jsPDF {
  const L = analyticsLabels(lang);
  const doc = new jsPDF({ compress: true });
  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();

  doc.setFontSize(15);
  doc.text(L.pdfTitle, pageWidth / 2, 18, { align: 'center' });
  doc.setFontSize(9);
  doc.setTextColor(100);
  doc.text(L.pdfNote, pageWidth / 2, 25, { align: 'center' });
  doc.text(L.privacy, pageWidth / 2, 30, { align: 'center' });
  doc.setTextColor(0);

  let y = 38;
  const sections = buildSections(summary, lang);
  const addTable = (title: string | undefined, head: string[], rows: Cell[][]) => {
    if (title) {
      if (y > pageHeight - 40) { doc.addPage(); y = 20; }
      doc.setFontSize(11);
      doc.text(title, 14, y);
      y += 3;
    }
    autoTable(doc, {
      head: [head],
      body: rows.map((r) => r.map(String)),
      startY: y,
      styles: { fontSize: 8 },
      headStyles: { fillColor: [59, 130, 246] },
      margin: { left: 14, right: 14 },
    });
    y = ((doc as unknown as { lastAutoTable?: { finalY: number } }).lastAutoTable?.finalY ?? y) + 8;
  };

  addTable(undefined, sections[0].tables[0].head, sections[0].tables[0].rows);

  if (charts.length) {
    doc.addPage();
    y = 20;
    const imgW = (pageWidth - 14 * 2 - 8) / 2;
    const heightOf = (c: ChartImage) => (c.width && c.height ? imgW * (c.height / c.width) : imgW * 0.7);
    for (let i = 0; i < charts.length; i += 2) {
      const row = charts.slice(i, i + 2);
      const rowH = Math.max(...row.map(heightOf)) + (row.some((c) => c.note) ? 4 : 0);
      if (y + rowH + 10 > pageHeight - 10) { doc.addPage(); y = 20; }
      row.forEach((chart, col) => {
        const x = 14 + col * (imgW + 8);
        doc.setFontSize(9);
        doc.text(chart.title, x, y);
        doc.addImage(chart.dataUrl, chart.dataUrl.startsWith('data:image/jpeg') ? 'JPEG' : 'PNG', x, y + 2, imgW, heightOf(chart));
        if (chart.note) {
          doc.setFontSize(7);
          doc.text(chart.note, x, y + heightOf(chart) + 6);
        }
      });
      y += rowH + 14;
    }
    if (y > pageHeight - 40) { doc.addPage(); y = 20; }
  }

  for (const section of sections.slice(1)) {
    for (const table of section.tables) addTable(table.title ?? section.title, table.head, table.rows);
  }
  return doc;
}

export function exportPdf(summary: AnalyticsSummary, lang: Lang, charts: ChartImage[] = [], now: Date = new Date()): string {
  const name = exportFilename('pdf', now);
  buildPdf(summary, lang, charts).save(name);
  return name;
}
