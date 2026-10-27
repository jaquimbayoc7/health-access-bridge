import { describe, it, expect, vi } from 'vitest';
import * as XLSX from 'xlsx';

vi.mock('xlsx', async (importOriginal) => ({ ...(await importOriginal<typeof import('xlsx')>()), writeFile: vi.fn() }));
import type { AnalyticsSummary } from '@/services/analytics';
import { buildPdf, buildSections, buildWorkbook, exportFilename, exportExcel } from '@/lib/analyticsExport';
import { analyticsLabels, formatNumber, formatPercent } from '@/lib/analyticsLabels';

const SUMMARY: AnalyticsSummary = {
  generated_at: '2026-10-27T15:00:00Z',
  scope: 'global',
  filters: { genero: 'Femenino', edad_min: 18 },
  totals: { patients: 12, with_prediction: 10, prediction_rate: 0.8333, mean_age: 41.5, mean_global_level: 52.3, with_icf_profile: 4 },
  distributions: {
    profile: [{ key: 'Perfil 0', count: 6 }],
    cat_fisica: [{ key: 'Leve', count: 5 }, { key: 'Moderada', count: 7 }],
    cat_psicosocial: [{ key: 'Leve', count: 12 }],
    genero: [{ key: 'Femenino', count: 7 }],
    age_group: [{ key: '30-44', count: 9 }],
    cause: [{ key: 'Enfermedad general', count: 8 }],
  },
  domains: [{ domain: 'D1', name: 'Aprendizaje', mean: 20, n: 12 }, { domain: 'D2', name: 'Tareas', mean: null, n: 0 }],
  icf: {
    patients_with_profile: 4, suggestions: 20,
    by_status: { sugerido: 5, aceptado: 8, editado: 3, rechazado: 4 }, decided: 15, acceptance_rate: 0.7333,
    by_component: {
      b: { total: 8, aceptado: 4, editado: 1, rechazado: 1, sugerido: 2, acceptance_rate: 0.8333 },
      s: { total: 4, aceptado: 1, editado: 1, rechazado: 2, sugerido: 0, acceptance_rate: 0.5 },
      d: { total: 8, aceptado: 3, editado: 1, rechazado: 1, sugerido: 3, acceptance_rate: null },
    },
    by_origin: [{ key: 'llm', count: 12 }], by_model: [{ key: 'gemma4:e4b', count: 20 }],
    top_codes: [{ code: 'b730', title: 'Fuerza muscular', component: 'b', count: 6, accepted: 5, rejected: 1 }],
  },
};
const PNG = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';

describe('formato', () => {
  it('muestra un guion cuando no hay dato', () => {
    expect(formatPercent(null)).toBe('—');
    expect(formatPercent(0.7333)).toBe('73.3 %');
    expect(formatNumber(undefined)).toBe('—');
    expect(formatNumber(41.5)).toBe('41.5');
  });
  it('tiene los mismos textos en español e inglés', () => {
    expect(Object.keys(analyticsLabels('en')).sort()).toEqual(Object.keys(analyticsLabels('es')).sort());
  });
});

describe('buildSections', () => {
  it('arma el resumen con el alcance, los filtros y los indicadores', () => {
    const summary = buildSections(SUMMARY, 'es')[0];
    const rows = Object.fromEntries(summary.tables[0].rows.map((r) => [r[0], r[1]]));
    expect(rows['Pacientes']).toBe(12);
    expect(rows['Filtros']).toBe('Género: Femenino · Edad desde: 18');
    expect(rows['Dashboard de análisis']).toBe('Todos los pacientes');
    expect(rows['% con predicción']).toBe('83.3 %');
    expect(rows['Tasa de aceptación']).toBe('73.3 %');
  });

  it('usa «Todos» cuando no hay filtros y rotula en inglés', () => {
    const en = buildSections({ ...SUMMARY, filters: {} }, 'en')[0];
    expect(Object.fromEntries(en.tables[0].rows.map((r) => [r[0], r[1]]))['Filters']).toBe('All');
  });

  it('incluye una tabla por distribución, los dominios y las tasas por componente', () => {
    const sections = buildSections(SUMMARY, 'es');
    expect(sections.map((s) => s.id)).toEqual(['summary', 'distributions', 'domains', 'icf', 'codes']);
    expect(sections[1].tables).toHaveLength(6);
    expect(sections[2].tables[0].rows[1]).toEqual(['D2', 'Tareas', '—', 0]);
    const status = sections[3].tables[0];
    expect(status.rows[0]).toEqual(['Funciones (b)', 2, 4, 1, 1, 8, '83.3 %']);
    expect(status.rows[2][6]).toBe('—'); // sin decisiones no se inventa una tasa
    expect(sections[4].tables[0].rows[0]).toEqual(['b730', 'Fuerza muscular', 'Funciones (b)', 6, 5, 1]);
  });

  it('no contiene datos identificables', () => {
    const text = JSON.stringify(buildSections(SUMMARY, 'es'));
    expect(text).not.toMatch(/documento|nombre_apellidos|orientaci/i);
  });
});

describe('Excel', () => {
  it('genera cinco hojas con los datos del resumen', () => {
    const wb = buildWorkbook(SUMMARY, 'es');
    expect(wb.SheetNames).toEqual(['Resumen', 'Distribuciones', 'Dominios', 'ICF', 'Códigos']);
    const resumen = XLSX.utils.sheet_to_json<unknown[]>(wb.Sheets['Resumen'], { header: 1 });
    expect(resumen[0]).toEqual(['Indicador', 'Valor']);
    expect(resumen.some((r) => r[0] === 'Pacientes' && r[1] === 12)).toBe(true);
    const dist = XLSX.utils.sheet_to_json<unknown[]>(wb.Sheets['Distribuciones'], { header: 1 });
    expect(dist.some((r) => r[0] === 'Moderada' && r[1] === 7)).toBe(true);
  });

  it('nombra el archivo con la fecha y lo escribe', () => {
    expect(exportFilename('xlsx', new Date('2026-10-27T12:00:00Z'))).toBe('analisis_hab_2026-10-27.xlsx');
    expect(exportExcel(SUMMARY, 'es', new Date('2026-10-27T12:00:00Z'))).toBe('analisis_hab_2026-10-27.xlsx');
    expect(XLSX.writeFile).toHaveBeenCalledWith(expect.anything(), 'analisis_hab_2026-10-27.xlsx');
  });
});

describe('PDF', () => {
  it('genera un documento sin gráficos', () => {
    const doc = buildPdf(SUMMARY, 'es');
    expect(doc.getNumberOfPages()).toBeGreaterThanOrEqual(1);
  });

  it('agrega páginas con los gráficos incrustados', () => {
    const without = buildPdf(SUMMARY, 'es').getNumberOfPages();
    const charts = Array.from({ length: 6 }, (_, i) => ({ title: `Gráfico ${i}`, dataUrl: PNG }));
    const withCharts = buildPdf(SUMMARY, 'es', charts).getNumberOfPages();
    expect(withCharts).toBeGreaterThan(without);
  });

  it('funciona con un alcance vacío', () => {
    const empty: AnalyticsSummary = {
      ...SUMMARY,
      totals: { ...SUMMARY.totals, patients: 0, mean_age: null, prediction_rate: null },
      distributions: { profile: [], cat_fisica: [], cat_psicosocial: [], genero: [], age_group: [], cause: [] },
      icf: { ...SUMMARY.icf, suggestions: 0, top_codes: [], by_origin: [], by_model: [] },
    };
    expect(() => buildPdf(empty, 'en')).not.toThrow();
  });
});
