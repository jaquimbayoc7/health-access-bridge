import type { IcfItem, IcfSuggestionSet } from '@/services/icf';

export const RESOLUTION_HEADER = 'Resolución 1239 del 21 de julio de 2022';
export const DRAFT_NOTICE =
  'Borrador de apoyo generado con ayuda de un modelo de lenguaje. No sustituye el certificado de discapacidad ' +
  'que emite el equipo multidisciplinario en el aplicativo RLCPD; cada código debe ser validado por un profesional.';

export const QUALIFIER_LABELS: Record<number, string> = {
  0: 'Ninguna',
  1: 'Leve',
  2: 'Moderada',
  3: 'Severa',
  4: 'Completa',
  8: 'Sin especificar',
  9: 'No aplicable',
};

export const NATURE_LABELS: Record<number, string> = {
  0: 'Sin cambio',
  1: 'Ausencia total',
  2: 'Ausencia parcial',
  3: 'Parte adicional',
  4: 'Dimensiones aberrantes',
  5: 'Discontinuidad',
  6: 'Posición desviada',
  7: 'Cambios cualitativos',
  8: 'Sin especificar',
  9: 'No aplicable',
};

export const LOCATION_LABELS: Record<number, string> = {
  0: 'Más de una región',
  1: 'Derecha',
  2: 'Izquierda',
  3: 'Ambos lados',
  4: 'Delante',
  5: 'Detrás',
  6: 'Proximal',
  7: 'Distal',
  8: 'Sin especificar',
  9: 'No aplicable',
};

/** Codigo con su calificador: b730.3, d450.3 o, en estructuras, s750.388 (magnitud, naturaleza, localizacion). */
export function formatCode(item: Pick<IcfItem, 'component' | 'code' | 'qualifier' | 'qualifier_cn' | 'qualifier_cl'>): string {
  if (item.qualifier === null || item.qualifier === undefined) return item.code;
  if (item.component === 's') {
    return `${item.code}.${item.qualifier}${item.qualifier_cn ?? 8}${item.qualifier_cl ?? 8}`;
  }
  return `${item.code}.${item.qualifier}`;
}

export function qualifierText(item: IcfItem): string {
  const base = item.qualifier === null ? '—' : QUALIFIER_LABELS[item.qualifier] ?? String(item.qualifier);
  if (item.component !== 's') return base;
  const nature = NATURE_LABELS[item.qualifier_cn ?? 8];
  const place = LOCATION_LABELS[item.qualifier_cl ?? 8];
  return `${base} · ${nature} · ${place}`;
}

export const ORIGIN_LABELS: Record<string, string> = {
  llm: 'Modelo',
  similarity: 'Similitud',
  rules: 'Reglas',
};

export interface ReportSection {
  title: string;
  rows: IcfItem[];
}

/** Secciones del reporte: solo los codigos que el medico no rechazo. */
export function reportSections(set: IcfSuggestionSet): ReportSection[] {
  const keep = (items: IcfItem[]) => items.filter((i) => i.status !== 'rechazado');
  return [
    { title: 'Funciones corporales (b)', rows: keep(set.functions) },
    { title: 'Estructuras corporales (s)', rows: keep(set.structures) },
    { title: 'Actividades y participación (d)', rows: keep(set.activities) },
  ];
}

export function buildReportText(set: IcfSuggestionSet, patientLabel: string): string {
  const lines = [`${RESOLUTION_HEADER} — Perfil de funcionamiento (borrador de apoyo)`, `Paciente: ${patientLabel}`, ''];
  for (const section of reportSections(set)) {
    lines.push(section.title);
    if (section.rows.length === 0) lines.push('  (sin códigos)');
    for (const row of section.rows) {
      lines.push(`  ${formatCode(row)}  ${row.title}  [${qualifierText(row)}]${row.status === 'editado' ? ' (editado)' : ''}`);
    }
    lines.push('');
  }
  lines.push(DRAFT_NOTICE);
  return lines.join('\n');
}
