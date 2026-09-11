import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';
import { Label } from '@/components/ui/label';
import { HelpCircle } from 'lucide-react';
import { useLanguage, icfTooltipContent } from '@/contexts/LanguageContext';

type ICFDimensionKey = 'd1' | 'd2' | 'd3' | 'd4' | 'd5' | 'd6';

interface ICFTooltipLabelProps {
  dimension: ICFDimensionKey;
  htmlFor: string;
  label: string;
}

export function ICFTooltipLabel({ dimension, htmlFor, label }: ICFTooltipLabelProps) {
  const { language } = useLanguage();
  const content = icfTooltipContent[language];
  const info = content[dimension];

  return (
    <div className="flex items-center gap-1.5">
      <Label htmlFor={htmlFor}>{label}</Label>
      <Tooltip>
        <TooltipTrigger asChild>
          <button
            type="button"
            aria-label={`${language === 'es' ? 'Información sobre' : 'Information about'} ${info.name}`}
            className="text-muted-foreground hover:text-primary transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-1 rounded"
          >
            <HelpCircle className="h-3.5 w-3.5" />
          </button>
        </TooltipTrigger>
        <TooltipContent side="top" align="start" className="max-w-72 z-50">
          <div className="space-y-2 py-0.5">
            <p className="font-semibold text-xs">{info.name}</p>
            <p className="text-xs leading-relaxed">{info.description}</p>
            <p className="text-xs text-muted-foreground italic">{content.exampleLabel} {info.examples}</p>
            <div className="border-t pt-2">
              <p className="text-xs font-medium mb-0.5">{content.scaleLabel}</p>
              <p className="text-xs text-muted-foreground">
                {content.scaleText}
              </p>
            </div>
          </div>
        </TooltipContent>
      </Tooltip>
    </div>
  );
}
