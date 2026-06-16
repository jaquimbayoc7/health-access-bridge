import { useState, useEffect } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Users, Activity, HelpCircle, CheckCircle2 } from 'lucide-react';

export const ONBOARDING_KEY = 'hab_onboarding_done';

const STEPS = [
  {
    icon: CheckCircle2,
    iconColor: 'text-green-500',
    title: '¡Bienvenido a Health Access Bridge!',
    description:
      'HAB es la plataforma de gestión clínica para pacientes con discapacidad. Te guiaremos en 3 pasos para que puedas empezar a usarla de inmediato.',
    hint: null,
  },
  {
    icon: Users,
    iconColor: 'text-primary',
    title: 'Módulo de Pacientes',
    description:
      'Registra y gestiona el historial de tus pacientes. Completa los campos ICF (D1–D6) para medir las barreras funcionales en 6 dimensiones clave.',
    hint: '💡 Cada campo ICF tiene un ícono "?" que explica qué mide la dimensión y cómo calificar en la escala de 0 a 100.',
  },
  {
    icon: Activity,
    iconColor: 'text-blue-500',
    title: 'Módulo de Predicciones ML',
    description:
      'Selecciona un paciente y ejecuta una predicción de perfil de riesgo. El modelo asigna uno de 3 perfiles: Perfil 0 (barreras bajas), Perfil 1 (barreras mixtas) o Perfil 2 (barreras altas y generalizadas).',
    hint: '💡 El badge de color indica el perfil: gris = Perfil 0 (bajas) · verde = Perfil 1 (mixtas) · azul = Perfil 2 (altas). Consulta la Guía Predictiva para la interpretación clínica completa.',
  },
  {
    icon: HelpCircle,
    iconColor: 'text-orange-500',
    title: 'Centro de Ayuda',
    description:
      'Accede en cualquier momento al Centro de Ayuda desde el menú lateral. Encontrarás el glosario ICF completo, la guía de roles y preguntas frecuentes.',
    hint: '💡 Si tienes dudas sobre la terminología ICF o el funcionamiento del sistema, la sección Ayuda te orienta paso a paso.',
  },
];

export function OnboardingModal() {
  const [open, setOpen] = useState(false);
  const [step, setStep] = useState(0);

  useEffect(() => {
    const done = localStorage.getItem(ONBOARDING_KEY);
    if (!done) {
      const timer = setTimeout(() => setOpen(true), 600);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleNext = () => {
    if (step < STEPS.length - 1) {
      setStep((s) => s + 1);
    } else {
      handleClose();
    }
  };

  const handleBack = () => {
    if (step > 0) setStep((s) => s - 1);
  };

  const handleClose = () => {
    localStorage.setItem(ONBOARDING_KEY, 'true');
    setOpen(false);
  };

  const current = STEPS[step];
  const Icon = current.icon;
  const isLast = step === STEPS.length - 1;
  const progress = ((step + 1) / STEPS.length) * 100;

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="max-w-md">
        <DialogHeader className="space-y-4 text-center">
          <div className="pt-4 flex justify-center">
            <Icon className={`h-14 w-14 ${current.iconColor}`} />
          </div>
          <DialogTitle className="text-xl text-center">{current.title}</DialogTitle>
          <DialogDescription className="text-sm leading-relaxed text-center">
            {current.description}
          </DialogDescription>
          {current.hint && (
            <div className="bg-muted rounded-lg px-4 py-3 text-sm text-left text-muted-foreground">
              {current.hint}
            </div>
          )}
        </DialogHeader>

        <div className="flex items-center gap-3 mt-2">
          <Progress value={progress} className="flex-1" />
          <span className="text-xs text-muted-foreground whitespace-nowrap">
            {step + 1} / {STEPS.length}
          </span>
        </div>

        <DialogFooter className="mt-2">
          <div className="flex w-full items-center justify-between gap-2">
            <div>
              {step > 0 && (
                <Button variant="outline" size="sm" onClick={handleBack}>
                  Anterior
                </Button>
              )}
            </div>
            <div className="flex gap-2">
              <Button variant="ghost" size="sm" onClick={handleClose}>
                Omitir
              </Button>
              <Button size="sm" onClick={handleNext}>
                {isLast ? 'Comenzar' : 'Siguiente'}
              </Button>
            </div>
          </div>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
