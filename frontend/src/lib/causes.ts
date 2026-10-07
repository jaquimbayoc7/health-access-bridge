// Causa de la deficiencia: 21 opciones oficiales en 3 grupos, de seleccion unica
// (Anexo Tecnico de la Resolucion 1239 del 21 de julio de 2022, criterio 3 del perfil de funcionamiento).
// "Enfermedad laboral" y "Accidente de trabajo" solo deben elegirse con dictamen de origen de perdida de
// capacidad laboral y ocupacional.
export interface CauseGroup {
  label: string;
  options: string[];
}

export const CAUSE_GROUPS: CauseGroup[] = [
  {
    label: 'De nacimiento',
    options: [
      'Alteración genética o hereditaria',
      'Alteración del desarrollo embrionario',
      'Complicaciones durante el parto',
      'Condiciones de salud de la madre durante el embarazo',
    ],
  },
  {
    label: 'Adquirida',
    options: [
      'Enfermedad general',
      'Enfermedad laboral',
      'Accidente de tránsito',
      'Accidente en el hogar',
      'Accidente en el centro educativo',
      'Accidente de trabajo',
      'Accidente deportivo',
      'Desastre natural',
      'Intoxicación',
      'Envejecimiento',
      'Consumo de sustancias psicoactivas',
      'Lesión auto infligida',
      'Conflicto armado',
      'Violencia intrafamiliar',
      'Violencia por delincuencia común',
      'Otra',
    ],
  },
  { label: 'No se identifica', options: ['No se identifica causa'] },
];

export const OFFICIAL_CAUSES: string[] = CAUSE_GROUPS.flatMap((g) => g.options);

export const isOfficialCause = (value: string): boolean => OFFICIAL_CAUSES.includes(value);
