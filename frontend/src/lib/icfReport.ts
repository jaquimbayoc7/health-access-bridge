import type { IcfItem, IcfSuggestionSet } from '@/services/icf';

export const RESOLUTION_HEADER = 'Resolución 1239 del 21 de julio de 2022';
export const DRAFT_NOTICE =
  'Borrador de apoyo generado con ayuda de un modelo de lenguaje. No sustituye el certificado de discapacidad ' +
  'que emite el equipo multidisciplinario en el aplicativo RLCPD; cada código debe ser validado por un profesional.';

export const SEVERITY_NOTICE =
  'La gravedad de funciones y estructuras es una sugerencia por reglas sin validación clínica suficiente ' +
  '(κ ponderado de 0,312 frente a la meta de 0,50): solo vale cuando el profesional la confirma.';

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

/** Gravedad de una funcion o estructura que el medico aun no confirmo (HU-07i): en el reporte se marca como sugerida. */
export function severityUnconfirmed(item: IcfItem): boolean {
  return item.component !== 'd' && item.qualifier !== null && item.qualifier_confirmed !== true;
}

/** Texto de la columna Calificador del reporte: agrega «(gravedad sugerida)» si el medico no la confirmo. */
export function reportQualifierText(item: IcfItem): string {
  return severityUnconfirmed(item) ? `${qualifierText(item)} (gravedad sugerida, sin confirmar)` : qualifierText(item);
}

/** Calificador de la CIF (0-4) que corresponde a un nivel de HAB 0-100 (escala generica de la OMS). */
export function qualifierFromLevel(level: number): number {
  if (level <= 4) return 0;
  if (level <= 24) return 1;
  if (level <= 49) return 2;
  if (level <= 95) return 3;
  return 4;
}

/** Justificacion que se muestra y se imprime: la del medico si la escribio o corrigio; si no, la del modelo. */
export function justificationText(item: Pick<IcfItem, 'justification' | 'justification_medico'>): string {
  return (item.justification_medico || item.justification || '').trim();
}

/** Que cambio el medico respecto de lo sugerido (HU-07j), para el reporte y la tabla; vacio si no cambio nada. */
export function decisionNote(item: IcfItem, lang: 'es' | 'en' = 'es'): string {
  if (item.status !== 'aceptado' && item.status !== 'editado') return '';
  const es = lang === 'es';
  const parts: string[] = [];
  if (item.component !== 'd' && item.qualifier_confirmed && item.qualifier !== null) {
    const suggested = item.qualifier_suggested;
    parts.push(
      suggested !== null && suggested !== undefined && suggested !== item.qualifier
        ? es
          ? `Gravedad ajustada por el médico: ${suggested} → ${item.qualifier}`
          : `Severity adjusted by the physician: ${suggested} → ${item.qualifier}`
        : es
          ? `Gravedad confirmada por el médico: ${item.qualifier}`
          : `Severity confirmed by the physician: ${item.qualifier}`
    );
  }
  if (item.original_code) {
    parts.push(
      es ? `Código ajustado por el médico (sugerido: ${item.original_code})` : `Code adjusted by the physician (suggested: ${item.original_code})`
    );
  }
  return parts.join('. ');
}

/**
 * Texto apto para el PDF. jsPDF usa fuentes estandar (WinAnsi): un caracter fuera de ese juego, como la κ o la flecha →,
 * no se dibuja y descompone todo el texto de la celda o del parrafo (letras separadas, texto cortado). Se sustituyen los
 * que usa el reporte y cualquier otro fuera de WinAnsi pasa a «?».
 */
export function pdfSafe(text: string): string {
  const winAnsiExtras = '€‚ƒ„…†‡ˆ‰Š‹ŒŽ‘’“”•–—˜™š›œžŸ';
  const mapped = text.replace(/κ/g, 'kappa').replace(/\s*→\s*/g, ' a ').replace(/≥/g, '>=').replace(/≤/g, '<=');
  // Array.from recorre por caracter (un emoji cuenta como uno, no como dos mitades)
  return Array.from(mapped)
    .map((ch) => ((ch.codePointAt(0) ?? 0) <= 0xff || winAnsiExtras.includes(ch) ? ch : '?'))
    .join('');
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
      lines.push(`  ${formatCode(row)}  ${row.title}  [${reportQualifierText(row)}]${row.status === 'editado' ? ' (editado)' : ''}`);
      const why = justificationText(row);
      if (why) lines.push(`      Justificación${row.justification_medico ? ' (del médico)' : ''}: ${why}`);
      const note = decisionNote(row);
      if (note) lines.push(`      ${note}`);
    }
    lines.push('');
  }
  lines.push(DRAFT_NOTICE);
  lines.push(SEVERITY_NOTICE);
  return lines.join('\n');
}
