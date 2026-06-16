import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';
import { Label } from '@/components/ui/label';
import { HelpCircle } from 'lucide-react';

const ICF_INFO = {
  d1: {
    name: 'D1 — Aprendizaje y conocimiento',
    description: 'Capacidad para aprender, asimilar y aplicar el conocimiento en situaciones cotidianas.',
    examples: 'Leer, calcular, resolver problemas, tomar decisiones.',
  },
  d2: {
    name: 'D2 — Tareas y demandas generales',
    description: 'Capacidad para ejecutar tareas simples o complejas y gestionar la carga de trabajo diaria.',
    examples: 'Organizar rutinas, manejar el estrés, realizar múltiples tareas.',
  },
  d3: {
    name: 'D3 — Comunicación',
    description: 'Capacidad para comunicarse mediante lenguaje verbal, no verbal o tecnológico.',
    examples: 'Hablar, escuchar, leer, escribir, usar teléfono.',
  },
  d4: {
    name: 'D4 — Movilidad',
    description: 'Capacidad para desplazarse, mantener posiciones corporales y transportar objetos.',
    examples: 'Caminar, subir escaleras, usar transporte, mover objetos.',
  },
  d5: {
    name: 'D5 — Autocuidado',
    description: 'Capacidad para cuidar el propio cuerpo: higiene, vestido y alimentación.',
    examples: 'Bañarse, vestirse, alimentarse de forma autónoma.',
  },
  d6: {
    name: 'D6 — Vida doméstica',
    description: 'Capacidad para realizar actividades del hogar de manera independiente.',
    examples: 'Cocinar, limpiar, hacer compras, cuidar el hogar.',
  },
} as const;

interface ICFTooltipLabelProps {
  dimension: keyof typeof ICF_INFO;
  htmlFor: string;
  label: string;
}

export function ICFTooltipLabel({ dimension, htmlFor, label }: ICFTooltipLabelProps) {
  const info = ICF_INFO[dimension];

  return (
    <div className="flex items-center gap-1.5">
      <Label htmlFor={htmlFor}>{label}</Label>
      <Tooltip>
        <TooltipTrigger asChild>
          <button
            type="button"
            aria-label={`Información sobre ${info.name}`}
            className="text-muted-foreground hover:text-primary transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-1 rounded"
          >
            <HelpCircle className="h-3.5 w-3.5" />
          </button>
        </TooltipTrigger>
        <TooltipContent side="top" align="start" className="max-w-72 z-50">
          <div className="space-y-2 py-0.5">
            <p className="font-semibold text-xs">{info.name}</p>
            <p className="text-xs leading-relaxed">{info.description}</p>
            <p className="text-xs text-muted-foreground italic">Ej: {info.examples}</p>
            <div className="border-t pt-2">
              <p className="text-xs font-medium mb-0.5">Escala 0 – 100</p>
              <p className="text-xs text-muted-foreground">
                0 = Sin barrera · 25 = Leve · 50 = Moderada · 75 = Grave · 100 = Barrera completa
              </p>
            </div>
          </div>
        </TooltipContent>
      </Tooltip>
    </div>
  );
}
