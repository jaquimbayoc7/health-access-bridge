// Contenido de ayuda del Perfil Funcional ICF: enlaces a la CIE, ejemplos de diagnostico y de notas clinicas
// (todos SINTETICOS), guia de uso y avance del desarrollo. Lo usan la pantalla, la Guia Predictiva y la Ayuda.

type Lang = 'es' | 'en';
export type Localized<T> = Record<Lang, T>;

export const CIE_LINKS = [
  {
    key: 'oms',
    url: 'https://icd.who.int/browse10/2019/en',
    label: { es: 'Navegador CIE-10 de la OMS (inglés)', en: 'WHO ICD-10 browser (English)' },
  },
  {
    key: 'ops',
    url: 'https://ais.paho.org/classifications/Chapters/',
    label: { es: 'CIE-10 en español (OPS/OMS)', en: 'ICD-10 in Spanish (PAHO/WHO)' },
  },
] as const;

/** Diagnosticos CIE-10 frecuentes para rellenar el campo con el formato "codigo descripcion". */
export const CIE_EXAMPLES: Array<{ code: string; text: string }> = [
  { code: 'G80', text: 'Parálisis cerebral' },
  { code: 'S14', text: 'Traumatismo de nervios y de médula espinal a nivel del cuello' },
  { code: 'S78', text: 'Amputación traumática de la cadera y del muslo' },
  { code: 'G35', text: 'Esclerosis múltiple' },
  { code: 'I69', text: 'Secuelas de enfermedad cerebrovascular' },
  { code: 'F20', text: 'Esquizofrenia' },
  { code: 'F33', text: 'Trastorno depresivo recurrente' },
];

export const CIE_HELP: Localized<string> = {
  es: 'Escriba el diagnóstico de la historia clínica con su código CIE-10 (por ejemplo, «G80 Parálisis cerebral»). Un diagnóstico preciso mejora las funciones y estructuras sugeridas. Si no tiene el código, búsquelo en los enlaces y copie el que corresponda a la historia clínica: no lo adivine.',
  en: 'Enter the diagnosis from the clinical record with its ICD-10 code (for example, “G80 Cerebral palsy”). A precise diagnosis improves the suggested functions and structures. If you do not have the code, look it up with the links and copy the one from the clinical record: do not guess it.',
};

export const NOTE_TIPS: Localized<string[]> = {
  es: [
    'Describa qué función o parte del cuerpo está afectada (fuerza, tono, equilibrio, dolor, memoria, ánimo, brazo, pierna, columna…).',
    'Indique el lado (derecho, izquierdo, ambos) y la gravedad si la conoce.',
    'Mencione productos de apoyo (silla de ruedas, bastón, prótesis, audífonos) y cuándo comenzó la deficiencia.',
    'Use frases cortas basadas en la historia clínica; no copie la historia completa.',
    'No escriba nombres, documento, dirección, teléfono ni otros datos que identifiquen a la persona.',
  ],
  en: [
    'Describe which function or body part is affected (strength, tone, balance, pain, memory, mood, arm, leg, spine…).',
    'Say which side (right, left, both) and the severity if known.',
    'Mention assistive products (wheelchair, cane, prosthesis, hearing aids) and when the impairment began.',
    'Use short sentences based on the clinical record; do not paste the whole record.',
    'Do not write names, ID numbers, addresses, phone numbers or any other identifying data.',
  ],
};

export interface NoteExample {
  title: string;
  diag: string;
  note: string;
}

/** Ejemplos SINTETICOS (no son personas reales). */
export const NOTE_EXAMPLES: Localized<NoteExample[]> = {
  es: [
    {
      title: 'Parálisis cerebral espástica',
      diag: 'G80 Parálisis cerebral',
      note: 'Espasticidad en ambos miembros inferiores con marcha en tijera; usa andador. Fuerza disminuida en piernas y poco control del tronco. Dolor lumbar ocasional. Necesita ayuda para las transferencias y para vestirse. Lenguaje conservado.',
    },
    {
      title: 'Lesión medular cervical',
      diag: 'S14 Traumatismo de nervios y de médula espinal a nivel del cuello',
      note: 'Tetraparesia incompleta tras un accidente. Pérdida parcial de fuerza y de sensibilidad en las cuatro extremidades, mayor en las inferiores. Sin control de esfínteres. Se desplaza en silla de ruedas. Dolor neuropático en ambas manos.',
    },
    {
      title: 'Amputación de miembro inferior',
      diag: 'S78 Amputación traumática de la cadera y del muslo',
      note: 'Amputación transfemoral derecha por accidente de tránsito. Usa prótesis y bastón. Dolor de miembro fantasma. Limitación para subir escaleras y caminar distancias largas. Función de la mano y del miembro superior conservada.',
    },
    {
      title: 'Esclerosis múltiple',
      diag: 'G35 Esclerosis múltiple',
      note: 'Debilidad y fatiga en ambas piernas, alteración del equilibrio y de la coordinación al caminar. Visión borrosa intermitente. Los síntomas empeoran con el calor. Camina con bastón distancias cortas.',
    },
    {
      title: 'Esquizofrenia',
      diag: 'F20 Esquizofrenia',
      note: 'Alucinaciones auditivas y pensamiento desorganizado durante los episodios; aplanamiento afectivo y retraimiento social. Dificultad para concentrarse y mantener rutinas. Sin deficiencia física. Adherencia irregular al tratamiento.',
    },
    {
      title: 'Depresión recurrente',
      diag: 'F33 Trastorno depresivo recurrente',
      note: 'Ánimo bajo persistente, pérdida de interés, sueño alterado y poca energía. Dificultad para atender tareas y para relacionarse con otras personas. Sin limitación motora ni sensorial.',
    },
  ],
  en: [
    {
      title: 'Spastic cerebral palsy',
      diag: 'G80 Cerebral palsy',
      note: 'Spasticity in both legs with scissoring gait; uses a walker. Reduced leg strength and poor trunk control. Occasional low back pain. Needs help with transfers and dressing. Language preserved.',
    },
    {
      title: 'Cervical spinal cord injury',
      diag: 'S14 Injury of nerves and spinal cord at neck level',
      note: 'Incomplete tetraparesis after an accident. Partial loss of strength and sensation in all four limbs, worse in the legs. No sphincter control. Uses a wheelchair. Neuropathic pain in both hands.',
    },
    {
      title: 'Lower limb amputation',
      diag: 'S78 Traumatic amputation of hip and thigh',
      note: 'Right transfemoral amputation after a traffic accident. Uses a prosthesis and a cane. Phantom limb pain. Limited on stairs and long walking distances. Hand and upper limb function preserved.',
    },
    {
      title: 'Multiple sclerosis',
      diag: 'G35 Multiple sclerosis',
      note: 'Weakness and fatigue in both legs, impaired balance and coordination when walking. Intermittent blurred vision. Symptoms worsen with heat. Walks short distances with a cane.',
    },
    {
      title: 'Schizophrenia',
      diag: 'F20 Schizophrenia',
      note: 'Auditory hallucinations and disorganized thinking during episodes; flat affect and social withdrawal. Difficulty concentrating and keeping routines. No physical impairment. Irregular adherence to treatment.',
    },
    {
      title: 'Recurrent depression',
      diag: 'F33 Recurrent depressive disorder',
      note: 'Persistent low mood, loss of interest, disturbed sleep and low energy. Difficulty with tasks and relating to other people. No motor or sensory limitation.',
    },
  ],
};

export const NOTES_DISCLAIMER: Localized<string> = {
  es: 'Los ejemplos son sintéticos: no corresponden a personas reales. Edítelos con los datos de la historia clínica de su paciente.',
  en: 'The examples are synthetic: they do not describe real people. Edit them with the data from your patient’s clinical record.',
};

// ------------------------------------------------------------------ guia: como funciona el Perfil Funcional ICF
export interface GuideStep {
  title: string;
  text: string;
}

export const GUIDE_INTRO: Localized<string> = {
  es: 'El Perfil Funcional ICF propone, a partir de los datos del paciente, los códigos de la CIF-IA que describen su funcionamiento, tal como los pide el Anexo Técnico de la Resolución 1239 del 21 de julio de 2022. Es un borrador de apoyo: la decisión final siempre es del profesional y el certificado oficial lo emite el equipo multidisciplinario en el aplicativo RLCPD.',
  en: 'The ICF Functional Profile proposes, from the patient data, the ICF-CY codes that describe their functioning, as required by the Technical Annex of Resolution 1239 of July 21, 2022. It is a support draft: the final decision is always the professional’s, and the official certificate is issued by the multidisciplinary team in the RLCPD application.',
};

export const GUIDE_STEPS: Localized<GuideStep[]> = {
  es: [
    { title: '1. Elija al paciente', text: 'En «Perfil Funcional ICF» seleccione a su paciente. Verá sus datos, los niveles D1–D6 y la predicción de barreras. Si ya hay un perfil guardado, se muestra.' },
    { title: '2. Agregue el diagnóstico CIE y las notas (recomendado)', text: 'El Anexo identifica las funciones y estructuras desde la historia clínica. Sin diagnóstico ni notas, esas sugerencias serán genéricas. Use los enlaces a la CIE y los ejemplos de notas de la pantalla.' },
    { title: '3. Pulse «Generar Perfil Funcional»', text: 'Normalmente tarda pocos segundos; si el equipo estuvo inactivo, el primer pedido puede tardar unos 20 s. Si el servicio no responde, se muestra un aviso y el resto de la aplicación sigue funcionando.' },
    { title: '4. Revise los tres componentes', text: 'Funciones corporales (b), estructuras corporales (s) y actividades y participación (d), con máximo 3 códigos por componente, cada uno con su título oficial, calificador, justificación y origen.' },
    { title: '5. Acepte, edite o rechace cada código', text: 'Cada decisión se guarda con el modelo que sugirió. En funciones (b) y estructuras (s) la gravedad la decide usted: el sistema solo la sugiere («por confirmar») y para aceptar el código debe confirmarla o cambiarla en la propia fila, con la ayuda de gravedad a la vista. Al editar puede ajustar también el código y, en estructuras, la naturaleza del cambio y la localización.' },
    { title: '6. Copie o descargue el reporte', text: 'El reporte omite los códigos rechazados, cita la Resolución 1239 e incluye la leyenda de borrador de apoyo.' },
  ],
  en: [
    { title: '1. Choose the patient', text: 'In “Functional Profile” select your patient. You will see their data, the D1–D6 levels and the barrier prediction. If a profile was already saved, it is shown.' },
    { title: '2. Add the ICD diagnosis and notes (recommended)', text: 'The Annex identifies functions and structures from the clinical record. Without a diagnosis or notes, those suggestions will be generic. Use the ICD links and the note examples on the screen.' },
    { title: '3. Press “Generate Functional Profile”', text: 'It usually takes a few seconds; if the machine was idle, the first request may take about 20 s. If the service does not respond, a notice is shown and the rest of the application keeps working.' },
    { title: '4. Review the three components', text: 'Body functions (b), body structures (s) and activities and participation (d), with at most 3 codes per component, each with its official title, qualifier, justification and origin.' },
    { title: '5. Accept, edit or reject each code', text: 'Each decision is saved with the model that suggested it. For functions (b) and structures (s) the severity is yours to decide: the system only suggests it (“to confirm”) and to accept the code you must confirm or change it on the row itself, with the severity help in view. When editing you can also adjust the code and, for structures, the nature of the change and the location.' },
    { title: '6. Copy or download the report', text: 'The report omits rejected codes, cites Resolution 1239 and includes the support-draft notice.' },
  ],
};

export const GUIDE_SOURCES: Localized<GuideStep[]> = {
  es: [
    { title: 'Qué lo calcula el sistema con reglas fijas (no el modelo)', text: 'Qué capítulos revisar (niveles D1–D6 desde 5), el máximo de 3 códigos, los códigos de actividades (lista del Anexo) y su calificador, y la gravedad inicial de funciones y estructuras, que sale de la categoría de HAB y es solo una sugerencia que usted confirma.' },
    { title: 'Qué sugiere el modelo de lenguaje', text: 'Solo las funciones (b) y las estructuras (s), y únicamente entre los candidatos que el buscador del catálogo le entrega. No puede inventar códigos.' },
    { title: 'De dónde sale cada título', text: 'Siempre del catálogo oficial de la CIF-IA, nunca del modelo.' },
    { title: 'Qué significa el origen de cada fila', text: '«Modelo»: lo eligió el modelo entre los candidatos. «Similitud»: lo propuso el buscador (el modelo no respondió o no se usó). «Reglas»: sale de las reglas o de la lista cerrada del Anexo.' },
    { title: 'Quién decide', text: 'El profesional de la salud. Todo código queda como «sugerido» hasta que se acepta, edita o rechaza.' },
  ],
  en: [
    { title: 'What the system computes with fixed rules (not the model)', text: 'Which chapters to review (D1–D6 levels from 5), the maximum of 3 codes, the activity codes (Annex list) and their qualifier, and the initial severity of functions and structures, which comes from the HAB category and is only a suggestion you confirm.' },
    { title: 'What the language model suggests', text: 'Only functions (b) and structures (s), and only among the candidates the catalog search gives it. It cannot invent codes.' },
    { title: 'Where each title comes from', text: 'Always from the official ICF-CY catalog, never from the model.' },
    { title: 'What the origin of each row means', text: '“Model”: chosen by the model among the candidates. “Similarity”: proposed by the search (the model did not respond or was not used). “Rules”: comes from the rules or the closed Annex list.' },
    { title: 'Who decides', text: 'The health professional. Every code stays “suggested” until it is accepted, edited or rejected.' },
  ],
};

/** Escala generica de la CIF (Tabla 2 del Anexo) y como se asigna a los niveles de HAB. */
export const QUALIFIER_SCALE: Localized<{ habLevel: string; qualifier: string; meaning: string }[]> = {
  es: [
    { habLevel: '0 – 4', qualifier: '0', meaning: 'Ninguna' },
    { habLevel: '5 – 24', qualifier: '1', meaning: 'Leve' },
    { habLevel: '25 – 49', qualifier: '2', meaning: 'Moderada' },
    { habLevel: '50 – 95', qualifier: '3', meaning: 'Severa' },
    { habLevel: '96 – 100', qualifier: '4', meaning: 'Completa o no lo puede hacer' },
  ],
  en: [
    { habLevel: '0 – 4', qualifier: '0', meaning: 'None' },
    { habLevel: '5 – 24', qualifier: '1', meaning: 'Mild' },
    { habLevel: '25 – 49', qualifier: '2', meaning: 'Moderate' },
    { habLevel: '50 – 95', qualifier: '3', meaning: 'Severe' },
    { habLevel: '96 – 100', qualifier: '4', meaning: 'Complete or cannot do it' },
  ],
};

export const GUIDE_LIMITS: Localized<string[]> = {
  es: [
    'Los niveles D1–D6 de HAB son por capítulo; la CIF califica por categoría. En actividades (d), el calificador se toma del nivel de su capítulo. En funciones (b) y estructuras (s), la gravedad sugerida sale de la categoría de HAB y no está validada: en la revisión con una profesional el acuerdo con ella fue bajo (κ ponderado de 0,312 frente a la meta de 0,50), porque el sistema solo propone 2 o 3 y ella también usó 4. Por eso la gravedad de b y s la confirma usted, código por código.',
    'En funciones (b) y estructuras (s) solo cuentan calificadores desde 1 (leve). Las estructuras llevan tres calificadores: magnitud, naturaleza del cambio y localización; naturaleza y localización quedan «sin especificar» (8) hasta que usted las edite.',
    'Para menores de 6 años no aplica: el Anexo no calcula niveles por dominio entre 0 y 5 años.',
    'HAB captura la discapacidad física y la psicosocial; la sugerencia cubrirá mejor esas categorías que la visual, la auditiva o la intelectual.',
    'La causa de la deficiencia es una de las 21 opciones oficiales del Anexo. «Enfermedad laboral» y «Accidente de trabajo» solo se eligen con dictamen de origen de pérdida de capacidad laboral.',
  ],
  en: [
    'HAB’s D1–D6 levels are per chapter; the ICF qualifies per category. For activities (d) the qualifier is taken from the level of its chapter. For functions (b) and structures (s) the suggested severity comes from the HAB category and is not validated: in the review with a professional the agreement with her was low (weighted κ of 0.312 against the 0.50 target), because the system only proposes 2 or 3 and she also used 4. That is why you confirm the severity of b and s, code by code.',
    'For functions (b) and structures (s) only qualifiers from 1 (mild) count. Structures carry three qualifiers: extent, nature of change and location; nature and location stay “unspecified” (8) until you edit them.',
    'It does not apply to children under 6: the Annex does not compute domain levels between 0 and 5 years.',
    'HAB captures physical and psychosocial disability; the suggestion will cover those categories better than visual, hearing or intellectual ones.',
    'The cause of the impairment is one of the 21 official options of the Annex. “Occupational disease” and “Work accident” are chosen only with an origin ruling on loss of work capacity.',
  ],
};

export const GUIDE_PRIVACY: Localized<string> = {
  es: 'Al servicio solo viajan edad, género, causa, categorías, niveles D1–D6, la predicción y el diagnóstico y las notas que usted escriba. Nunca viajan el nombre, el documento ni la orientación sexual. El modelo corre en infraestructura propia: ningún dato clínico sale hacia servicios de terceros.',
  en: 'Only age, gender, cause, categories, D1–D6 levels, the prediction and the diagnosis and notes you write are sent to the service. Name, ID number and sexual orientation are never sent. The model runs on our own infrastructure: no clinical data goes to third-party services.',
};

// ------------------------------------------------------------------ avance del desarrollo
export type ProgressState = 'done' | 'pending';

export interface ProgressItem {
  state: ProgressState;
  text: string;
}

export const PROGRESS_TITLE: Localized<string> = {
  es: 'Perfil Funcional ICF: dónde vamos',
  en: 'ICF Functional Profile: where we are',
};

export const PROGRESS_UPDATED = '13-nov-2026';

export const PROGRESS_ITEMS: Localized<ProgressItem[]> = {
  es: [
    { state: 'done', text: 'Catálogo CIF-IA de 1.593 códigos con búsqueda por significado y lista de actividades del Anexo 1239.' },
    { state: 'done', text: 'Sugerencia de funciones, estructuras y actividades con calificador, justificación y origen; máximo 3 códigos por componente.' },
    { state: 'done', text: 'Aceptar, editar o rechazar cada código; el reporte se copia o se descarga en PDF con la leyenda de borrador de apoyo.' },
    { state: 'done', text: 'Modelo de lenguaje propio y de código abierto (Gemma 4): más preciso que la búsqueda sola en las pruebas, sin enviar datos a terceros.' },
    { state: 'done', text: 'Causas de la deficiencia con las 21 opciones oficiales del Anexo.' },
    { state: 'done', text: 'Validación con una profesional de la salud en tres rondas (24 casos nuevos en la última): precisión, cobertura y actividades cumplen las metas; la gravedad de funciones y estructuras no (κ ponderado de 0,312 frente a 0,50).' },
    { state: 'done', text: 'La gravedad de funciones y estructuras la confirma el médico en cada fila, con una ayuda que muestra los niveles D1–D6 del paciente y la escala; se registra qué sugirió el sistema y qué fijó el profesional.' },
    { state: 'pending', text: 'Operación estable en el equipo de producción (arranque automático y pruebas de extremo a extremo en todos los ambientes).' },
    { state: 'pending', text: 'Pruebas automáticas completas de la pantalla y manual de operación.' },
  ],
  en: [
    { state: 'done', text: 'ICF-CY catalog of 1,593 codes with search by meaning and the Annex 1239 activity list.' },
    { state: 'done', text: 'Suggestion of functions, structures and activities with qualifier, justification and origin; at most 3 codes per component.' },
    { state: 'done', text: 'Accept, edit or reject each code; the report can be copied or downloaded as a PDF with the support-draft notice.' },
    { state: 'done', text: 'Own open-source language model (Gemma 4): more precise than the search alone in tests, without sending data to third parties.' },
    { state: 'done', text: 'Cause of impairment with the 21 official options of the Annex.' },
    { state: 'done', text: 'Validation with a health professional in three rounds (24 new cases in the last one): precision, coverage and activities meet the targets; the severity of functions and structures does not (weighted κ of 0.312 against 0.50).' },
    { state: 'done', text: 'The severity of functions and structures is confirmed by the physician on each row, with a help panel showing the patient’s D1–D6 levels and the scale; what the system suggested and what the professional set are recorded.' },
    { state: 'pending', text: 'Stable operation on the production machine (automatic start and end-to-end tests in every environment).' },
    { state: 'pending', text: 'Complete automated tests for the screen and the operations manual.' },
  ],
};


// ------------------------------------------------------------------ ayuda para calificar la gravedad (b y s)
export const SEVERITY_HELP = {
  title: {
    es: 'Ayuda para calificar la gravedad de funciones y estructuras',
    en: 'Help for rating the severity of functions and structures',
  } as Localized<string>,
  intro: {
    es: 'La gravedad de b y s es una decisión suya: el sistema solo propone un valor inicial a partir de la categoría de discapacidad de HAB (leve = 1, moderada = 2, severa = 3, completa = 4; para las funciones mentales usa la psicosocial y para el resto la física). No está validada.',
    en: 'The severity of b and s is your decision: the system only proposes an initial value from the HAB disability category (mild = 1, moderate = 2, severe = 3, complete = 4; mental functions use the psychosocial category and the rest the physical one). It is not validated.',
  } as Localized<string>,
  how: {
    es: 'Califique cuánto se afecta la función o la estructura (porcentaje del problema) con lo que conoce del paciente: examen clínico, pruebas, historia y lo que él o su cuidador refieren. Los niveles D1–D6 miden actividades y participación, no el cuerpo: orientan, no determinan.',
    en: 'Rate how much the function or structure is affected (percentage of the problem) using what you know about the patient: clinical examination, tests, history and what they or their caregiver report. The D1–D6 levels measure activities and participation, not the body: they guide, they do not decide.',
  } as Localized<string>,
  bias: {
    es: 'Dato de la validación: el sistema solo sugirió 2 o 3, mientras la profesional que revisó también usó 4 (deficiencia completa: por ejemplo ceguera total, sordera profunda o parálisis de las piernas). Ante una pérdida completa, valore el 4.',
    en: 'Validation finding: the system only suggested 2 or 3, while the reviewing professional also used 4 (complete impairment: for example total blindness, profound deafness or paralysis of the legs). For a complete loss, consider 4.',
  } as Localized<string>,
  source: {
    es: 'Fuente: OMS, CIF (2001), escala genérica de calificadores. Validación del proyecto: una sola revisora y casos sintéticos (κ ponderado de 0,312; meta 0,50).',
    en: 'Source: WHO, ICF (2001), generic qualifier scale. Project validation: a single reviewer and synthetic cases (weighted κ of 0.312; target 0.50).',
  } as Localized<string>,
  pending: { es: 'Por confirmar', en: 'To confirm' } as Localized<string>,
  confirmed: { es: 'Confirmada', en: 'Confirmed' } as Localized<string>,
  suggested: { es: 'Sugerida por reglas', en: 'Suggested by rules' } as Localized<string>,
  mustConfirm: {
    es: 'Confirme la gravedad para poder aceptar',
    en: 'Confirm the severity to be able to accept',
  } as Localized<string>,
};
