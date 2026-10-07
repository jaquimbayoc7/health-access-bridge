import { CheckCircle2, Circle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { useLanguage } from '@/contexts/LanguageContext';
import {
  GUIDE_INTRO,
  GUIDE_LIMITS,
  GUIDE_PRIVACY,
  GUIDE_SOURCES,
  GUIDE_STEPS,
  PROGRESS_ITEMS,
  PROGRESS_UPDATED,
  QUALIFIER_SCALE,
} from '@/lib/icfGuideContent';

/** Seccion «Como funciona el Perfil Funcional ICF» (Guia Predictiva). */
export function IcfGuide() {
  const { language } = useLanguage();
  const es = language === 'es';
  return (
    <div className="space-y-6" data-testid="icf-guide">
      <p className="text-lg text-muted-foreground max-w-4xl">{GUIDE_INTRO[language]}</p>

      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">{es ? 'Cómo se usa, paso a paso' : 'How to use it, step by step'}</CardTitle>
        </CardHeader>
        <CardContent>
          <ol className="space-y-3">
            {GUIDE_STEPS[language].map((step) => (
              <li key={step.title}>
                <p className="font-semibold text-primary">{step.title}</p>
                <p className="text-muted-foreground">{step.text}</p>
              </li>
            ))}
          </ol>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">{es ? 'De dónde sale cada dato' : 'Where each piece of data comes from'}</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-3">
            {GUIDE_SOURCES[language].map((s) => (
              <li key={s.title}>
                <p className="font-semibold">{s.title}</p>
                <p className="text-muted-foreground">{s.text}</p>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">{es ? 'Cómo se asigna el calificador' : 'How the qualifier is assigned'}</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>{es ? 'Nivel D (0–100)' : 'D level (0–100)'}</TableHead>
                <TableHead>{es ? 'Calificador CIF' : 'ICF qualifier'}</TableHead>
                <TableHead>{es ? 'Significado' : 'Meaning'}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {QUALIFIER_SCALE[language].map((r) => (
                <TableRow key={r.qualifier}>
                  <TableCell>{r.habLevel}</TableCell>
                  <TableCell className="font-mono">{r.qualifier}</TableCell>
                  <TableCell>{r.meaning}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">{es ? 'Límites que debe conocer' : 'Limits you should know'}</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2">
            {GUIDE_LIMITS[language].map((l) => (
              <li key={l} className="flex gap-3">
                <span className="text-primary font-bold">•</span>
                <span className="text-muted-foreground">{l}</span>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">{es ? 'Privacidad' : 'Privacy'}</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">{GUIDE_PRIVACY[language]}</p>
        </CardContent>
      </Card>
    </div>
  );
}

/** Avance del desarrollo del Perfil Funcional ICF (Ayuda). */
export function IcfProgress() {
  const { language } = useLanguage();
  return (
    <div data-testid="icf-progress">
      <p className="text-xs text-muted-foreground mb-3">
        {language === 'es' ? `Actualizado el ${PROGRESS_UPDATED}` : `Updated on ${PROGRESS_UPDATED}`}
      </p>
      <ul className="space-y-2">
        {PROGRESS_ITEMS[language].map((item) => (
          <li key={item.text} className="flex gap-3 text-sm">
            {item.state === 'done' ? (
              <CheckCircle2 className="h-4 w-4 mt-0.5 shrink-0 text-green-600" aria-label={language === 'es' ? 'Hecho' : 'Done'} />
            ) : (
              <Circle className="h-4 w-4 mt-0.5 shrink-0 text-muted-foreground" aria-label={language === 'es' ? 'Pendiente' : 'Pending'} />
            )}
            <span className="text-muted-foreground">{item.text}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
