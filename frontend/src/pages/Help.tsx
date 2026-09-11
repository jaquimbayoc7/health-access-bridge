import { useState } from 'react';
import { BookOpen, Users, Activity, HelpCircle, ChevronDown, ChevronUp, Keyboard, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  useLanguage,
  icfDimensionsContent,
  predictionProfilesContent,
  helpRolesContent,
  helpShortcutsContent,
  faqContent,
} from '@/contexts/LanguageContext';

function FAQItem({ q, a }: { q: string; a: string }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="border rounded-lg overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-muted/50 transition-colors"
        aria-expanded={open}
      >
        <span className="font-medium text-sm">{q}</span>
        {open ? <ChevronUp className="h-4 w-4 text-muted-foreground flex-shrink-0" /> : <ChevronDown className="h-4 w-4 text-muted-foreground flex-shrink-0" />}
      </button>
      {open && (
        <div className="px-4 pb-4 pt-1 text-sm text-muted-foreground leading-relaxed border-t bg-muted/20">
          {a}
        </div>
      )}
    </div>
  );
}

export default function Help() {
  const { language, t } = useLanguage();
  const icfDimensions = icfDimensionsContent[language];
  const predictionProfiles = predictionProfilesContent[language];
  const roles = helpRolesContent[language];
  const shortcuts = helpShortcutsContent[language];
  const faq = faqContent[language];

  return (
    <div className="space-y-8 max-w-4xl">
      <div>
        <h1 className="text-3xl font-bold flex items-center gap-3">
          <HelpCircle className="h-8 w-8 text-primary" />
          {t('helpCenterTitle')}
        </h1>
        <p className="text-muted-foreground mt-2">
          {t('helpCenterSubtitle')}
        </p>
      </div>

      {/* Glosario ICF */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BookOpen className="h-5 w-5 text-primary" />
            {t('helpGlossaryTitle')}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg flex gap-2 text-sm text-blue-800">
            <AlertCircle className="h-4 w-4 mt-0.5 flex-shrink-0" />
            <span>
              <strong>{t('helpScaleBanner')}</strong> {t('helpScaleBannerRest')}
            </span>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            {icfDimensions.map((dim) => (
              <div key={dim.key} className="border rounded-lg p-4 space-y-2">
                <div className="flex items-center gap-2">
                  <Badge className={`${dim.color} border-0 font-bold`}>{dim.key}</Badge>
                  <span className="font-semibold text-sm">{dim.name}</span>
                </div>
                <p className="text-sm text-muted-foreground leading-relaxed">{dim.description}</p>
                <div>
                  <p className="text-xs font-medium text-muted-foreground mb-1">{t('helpExamplesLabel')}</p>
                  <ul className="text-xs text-muted-foreground space-y-0.5">
                    {dim.examples.map((ex) => (
                      <li key={ex} className="flex items-start gap-1.5">
                        <span className="text-primary mt-0.5">·</span>
                        {ex}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Perfiles de predicción */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="h-5 w-5 text-primary" />
            {t('helpPredictionProfilesTitle')}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {predictionProfiles.map((p) => (
              <div key={p.profile} className="flex items-start gap-3 p-3 border rounded-lg">
                <Badge className={`${p.color} text-white border-0 whitespace-nowrap mt-0.5`}>
                  {t('helpProfileBadge')} {p.profile}
                </Badge>
                <div>
                  <p className="font-medium text-sm">{p.label}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">{p.description}</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Guía de roles */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Users className="h-5 w-5 text-primary" />
            {t('helpRolesTitle')}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="border rounded-lg p-4 space-y-3">
              <div className="flex items-center gap-2">
                <Badge className="bg-blue-100 text-blue-800 border-0">{t('helpRoleDoctor')}</Badge>
              </div>
              <ul className="text-sm space-y-2 text-muted-foreground">
                {roles.doctor.map((item) => (
                  <li key={item} className="flex gap-2"><span className="text-green-500 font-bold">✓</span> {item}</li>
                ))}
                {roles.doctorNo.map((item) => (
                  <li key={item} className="flex gap-2"><span className="text-red-400 font-bold">✗</span> {item}</li>
                ))}
              </ul>
            </div>
            <div className="border rounded-lg p-4 space-y-3">
              <div className="flex items-center gap-2">
                <Badge className="bg-purple-100 text-purple-800 border-0">{t('helpRoleAdmin')}</Badge>
              </div>
              <ul className="text-sm space-y-2 text-muted-foreground">
                {roles.admin.map((item) => (
                  <li key={item} className="flex gap-2"><span className="text-green-500 font-bold">✓</span> {item}</li>
                ))}
                {roles.adminNo.map((item) => (
                  <li key={item} className="flex gap-2"><span className="text-red-400 font-bold">✗</span> {item}</li>
                ))}
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Atajos de teclado */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Keyboard className="h-5 w-5 text-primary" />
            {t('helpShortcutsTitle')}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-2 sm:grid-cols-2 text-sm">
            {shortcuts.map(({ key, desc }) => (
              <div key={key} className="flex items-center gap-3">
                <kbd className="px-2 py-1 bg-muted border rounded text-xs font-mono whitespace-nowrap">{key}</kbd>
                <span className="text-muted-foreground">{desc}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* FAQ */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <HelpCircle className="h-5 w-5 text-primary" />
            {t('helpFaqTitle')}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {faq.map(({ q, a }) => (
              <FAQItem key={q} q={q} a={a} />
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
