import { useLanguage } from '@/contexts/LanguageContext';
import type { Patient } from '@/services/patients';
import { SEVERITY_HELP } from '@/lib/icfGuideContent';
import { QUALIFIER_LABELS, qualifierFromLevel } from '@/lib/icfReport';

const DOMAINS: Array<[keyof Patient, string, string]> = [
  ['nivel_d1', 'D1', 'Aprendizaje'],
  ['nivel_d2', 'D2', 'Tareas generales'],
  ['nivel_d3', 'D3', 'Comunicación'],
  ['nivel_d4', 'D4', 'Movilidad'],
  ['nivel_d5', 'D5', 'Autocuidado'],
  ['nivel_d6', 'D6', 'Vida doméstica'],
];

const SCALE: Array<[number, string]> = [
  [0, '0–4 %'],
  [1, '5–24 %'],
  [2, '25–49 %'],
  [3, '50–95 %'],
  [4, '96–100 %'],
];

/**
 * Ayuda para que el medico califique la gravedad (0-4) de funciones (b) y estructuras (s) (HU-07i):
 * de donde sale la sugerencia, la escala, los niveles D1-D6 del paciente y el sesgo medido en la validacion.
 * Con `compact` solo muestra la escala y los niveles (para el dialogo de edicion).
 */
export function SeverityHelp({ patient, compact = false }: { patient: Patient | null; compact?: boolean }) {
  const { language } = useLanguage();
  const es = language === 'es';
  const body = (
    <div className="space-y-3 text-sm">
      {!compact && <p className="text-muted-foreground">{SEVERITY_HELP.intro[language]}</p>}
      <ul className="grid gap-1 sm:grid-cols-3" aria-label={es ? 'Escala de gravedad' : 'Severity scale'}>
        {SCALE.map(([q, pct]) => (
          <li key={q}>
            <strong>{q} — {QUALIFIER_LABELS[q]}</strong> ({pct})
          </li>
        ))}
      </ul>
      {patient && (
        <div data-testid="severity-help-levels">
          <p className="text-xs">
            <strong>{es ? 'Categorías de HAB' : 'HAB categories'}:</strong> {es ? 'física' : 'physical'} {patient.cat_fisica} ·{' '}
            {es ? 'psicosocial' : 'psychosocial'} {patient.cat_psicosocial}
          </p>
          <div className="mt-1 grid grid-cols-2 gap-x-4 gap-y-0.5 text-xs sm:grid-cols-3">
            {DOMAINS.map(([key, id, label]) => {
              const level = Number(patient[key]);
              return (
                <span key={id}>
                  {id} {label}: {level} → {qualifierFromLevel(level)}
                </span>
              );
            })}
          </div>
        </div>
      )}
      {!compact && <p className="text-muted-foreground">{SEVERITY_HELP.how[language]}</p>}
      <p className="rounded bg-amber-100 p-2 text-amber-900 dark:bg-amber-950 dark:text-amber-100">{SEVERITY_HELP.bias[language]}</p>
      {!compact && <p className="text-xs text-muted-foreground">{SEVERITY_HELP.source[language]}</p>}
    </div>
  );
  if (compact) return <div data-testid="severity-help-compact">{body}</div>;
  return (
    <details className="rounded-md border bg-muted/40 p-3" data-testid="severity-help">
      <summary className="cursor-pointer text-sm font-medium">{SEVERITY_HELP.title[language]}</summary>
      <div className="mt-2">{body}</div>
    </details>
  );
}
