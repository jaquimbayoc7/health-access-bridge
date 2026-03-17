import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useLanguage } from '@/contexts/LanguageContext';
import profile0Image from '@/assets/profile-0.jpg';
import profile1Image from '@/assets/profile-1.jpg';
import profile2Image from '@/assets/profile-2.jpg';
import { BookOpen } from 'lucide-react';

interface ProfileData {
  title: string;
  image: string;
  clinicalInterpretation: string;
  characteristics: string[];
  suggestions: string[];
}

export default function PredictiveGuide() {
  const { language } = useLanguage();

  const profiles: Record<number, ProfileData> = {
    0: {
      title: language === 'es' ? 'Perfil 0: Percepción de Barreras Bajas o Focalizadas' : 'Profile 0: Low or Focused Barrier Perception',
      image: profile0Image,
      clinicalInterpretation: language === 'es' 
        ? 'Un paciente clasificado en el Perfil 0 tiende a reportar niveles de dificultad bajos en la mayoría de los dominios evaluados. Esto sugiere que, en general, el paciente ha desarrollado estrategias de afrontamiento efectivas, cuenta con una red de apoyo sólida, o su entorno presenta pocas barreras significativas para su desenvolvimiento. Su percepción general es de una alta funcionalidad y autonomía.'
        : 'A patient classified as Profile 0 tends to report low difficulty levels in most evaluated domains. This suggests that, in general, the patient has developed effective coping strategies, has a solid support network, or their environment presents few significant barriers to their development. Their general perception is of high functionality and autonomy.',
      characteristics: language === 'es' 
        ? [
            'Altos niveles de independencia en actividades de la vida diaria.',
            'Participación social activa.',
            'Puede que exista una o dos áreas con una dificultad leve, pero no representan un obstáculo generalizado.'
          ]
        : [
            'High levels of independence in daily living activities.',
            'Active social participation.',
            'There may be one or two areas with mild difficulty, but they do not represent a widespread obstacle.'
          ],
      suggestions: language === 'es'
        ? [
            'Reforzar y validar: Reconocer y validar las fortalezas y la resiliencia del paciente.',
            'Enfoque preventivo: Indagar sobre las áreas de dificultad leve para prevenir que se conviertan en barreras mayores.',
            'Optimización: Explorar si existen oportunidades para mejorar aún más su calidad de vida o acceso a recursos que mantengan su nivel de bienestar.'
          ]
        : [
            'Reinforce and validate: Recognize and validate the patient\'s strengths and resilience.',
            'Preventive approach: Inquire about areas of mild difficulty to prevent them from becoming major barriers.',
            'Optimization: Explore if there are opportunities to further improve their quality of life or access to resources that maintain their level of well-being.'
          ]
    },
    1: {
      title: language === 'es' ? 'Perfil 1: Percepción de Barreras Moderadas o Mixtas' : 'Profile 1: Moderate or Mixed Barrier Perception',
      image: profile1Image,
      clinicalInterpretation: language === 'es'
        ? 'El Perfil 1 representa a un paciente con una experiencia heterogénea. Típicamente, reportará niveles de dificultad bajos en algunos dominios, pero significativamente altos en otros. Este patrón mixto es clave: indica que las barreras no son generalizadas, sino contextuales y específicas. Por ejemplo, puede tener una alta funcionalidad en el hogar (nivel_d1), pero percibir barreras muy altas en el transporte o acceso a edificios (nivel_d3).'
        : 'Profile 1 represents a patient with a heterogeneous experience. Typically, they will report low difficulty levels in some domains, but significantly high in others. This mixed pattern is key: it indicates that barriers are not widespread, but contextual and specific. For example, they may have high functionality at home (level_d1), but perceive very high barriers in transportation or building access (level_d3).',
      characteristics: language === 'es'
        ? [
            'Frustración o dificultad concentrada en áreas específicas (ej. movilidad urbana, interacción social, acceso laboral).',
            'Niveles de autonomía variables dependiendo de la tarea o el entorno.',
            'Puede indicar una necesidad de adaptaciones o apoyos muy concretos.'
          ]
        : [
            'Frustration or difficulty concentrated in specific areas (e.g., urban mobility, social interaction, work access).',
            'Variable levels of autonomy depending on the task or environment.',
            'May indicate a need for very specific adaptations or supports.'
          ],
      suggestions: language === 'es'
        ? [
            'Análisis dirigido: Centrar la conversación en los dominios con puntuaciones altas para comprender la naturaleza exacta de la barrera.',
            'Intervenciones focalizadas: El plan de apoyo debe ser muy específico. Si la barrera es el transporte, las soluciones deben centrarse ahí (rutas accesibles, servicios de transporte adaptado, etc.).',
            'Desarrollo de habilidades: Trabajar con el paciente en el desarrollo de habilidades específicas para superar esas barreras concretas.'
          ]
        : [
            'Targeted analysis: Focus the conversation on domains with high scores to understand the exact nature of the barrier.',
            'Focused interventions: The support plan must be very specific. If the barrier is transportation, solutions should focus there (accessible routes, adapted transportation services, etc.).',
            'Skills development: Work with the patient on developing specific skills to overcome those specific barriers.'
          ]
    },
    2: {
      title: language === 'es' ? 'Perfil 2: Percepción de Barreras Altas y Generalizadas' : 'Profile 2: High and Generalized Barrier Perception',
      image: profile2Image,
      clinicalInterpretation: language === 'es'
        ? 'Un paciente en el Perfil 2 percibe niveles de dificultad altos en la mayoría o en todos los dominios evaluados. Esto sugiere que las barreras tienen un impacto significativo y transversal en su vida. La sensación de limitación es generalizada y puede afectar su autonomía, participación social y bienestar emocional de manera profunda.'
        : 'A patient in Profile 2 perceives high difficulty levels in most or all evaluated domains. This suggests that barriers have a significant and cross-cutting impact on their life. The sense of limitation is widespread and can deeply affect their autonomy, social participation, and emotional well-being.',
      characteristics: language === 'es'
        ? [
            'Dependencia significativa para varias actividades de la vida diaria.',
            'Aislamiento social o participación comunitaria reducida.',
            'Posible presencia de factores emocionales asociados, como frustración, ansiedad o síntomas depresivos.',
            'Puede indicar una combinación de barreras físicas, sociales y actitudinales en su entorno.'
          ]
        : [
            'Significant dependence for various daily living activities.',
            'Social isolation or reduced community participation.',
            'Possible presence of associated emotional factors, such as frustration, anxiety, or depressive symptoms.',
            'May indicate a combination of physical, social, and attitudinal barriers in their environment.'
          ],
      suggestions: language === 'es'
        ? [
            'Intervención priorizada: Es crucial identificar, junto con el paciente, cuál es la barrera más urgente o la que genera mayor malestar para abordarla primero.',
            'Enfoque multidisciplinario: Este perfil a menudo se beneficia de un plan de apoyo integral que puede incluir terapia física, terapia ocupacional, apoyo psicológico y trabajo social.',
            'Gestión de recursos: Investigar y conectar al paciente con una red de recursos comunitarios, programas de apoyo gubernamentales y adaptaciones de mayor envergadura.'
          ]
        : [
            'Prioritized intervention: It is crucial to identify, together with the patient, which is the most urgent barrier or the one that generates the most discomfort to address it first.',
            'Multidisciplinary approach: This profile often benefits from a comprehensive support plan that may include physical therapy, occupational therapy, psychological support, and social work.',
            'Resource management: Research and connect the patient with a network of community resources, government support programs, and larger-scale adaptations.'
          ]
    }
  };

  return (
    <div className="container mx-auto py-8 px-4 max-w-7xl">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <BookOpen className="h-8 w-8 text-primary" />
          <h1 className="text-4xl font-bold">
            {language === 'es' 
              ? 'Guía de Interpretación de Perfiles Predictivos' 
              : 'Predictive Profile Interpretation Guide'}
          </h1>
        </div>
        <p className="text-lg text-muted-foreground max-w-4xl">
          {language === 'es'
            ? 'El perfil predictivo generado por el sistema Health Access Bridge es una herramienta de apoyo clínico. Su objetivo es ofrecer una visión rápida y estructurada sobre cómo un paciente percibe las barreras asociadas a su discapacidad en diferentes dominios de su vida. Utilice esta información como un punto de partida para la conversación y la planificación de intervenciones, no como un sustituto del juicio clínico.'
            : 'The predictive profile generated by the Health Access Bridge system is a clinical support tool. Its objective is to offer a quick and structured view of how a patient perceives the barriers associated with their disability in different domains of their life. Use this information as a starting point for conversation and intervention planning, not as a substitute for clinical judgment.'}
        </p>
      </div>

      {/* Profiles */}
      <div className="space-y-8">
        {Object.entries(profiles).map(([key, profile]) => (
          <Card key={key} className="overflow-hidden">
            <CardHeader className="pb-4">
              <CardTitle className="text-2xl">{profile.title}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Image */}
              <div className="w-full aspect-video rounded-lg overflow-hidden">
                <img 
                  src={profile.image} 
                  alt={profile.title}
                  className="w-full h-full object-cover"
                />
              </div>

              {/* Clinical Interpretation */}
              <div>
                <h3 className="text-xl font-semibold mb-3 text-primary">
                  {language === 'es' ? 'Interpretación Clínica:' : 'Clinical Interpretation:'}
                </h3>
                <p className="text-muted-foreground leading-relaxed">
                  {profile.clinicalInterpretation}
                </p>
              </div>

              {/* Characteristics */}
              <div>
                <h3 className="text-xl font-semibold mb-3 text-primary">
                  {language === 'es' ? 'Posibles Características:' : 'Possible Characteristics:'}
                </h3>
                <ul className="space-y-2">
                  {profile.characteristics.map((char, index) => (
                    <li key={index} className="flex gap-3">
                      <span className="text-primary font-bold">•</span>
                      <span className="text-muted-foreground">{char}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Suggestions */}
              <div>
                <h3 className="text-xl font-semibold mb-3 text-primary">
                  {language === 'es' ? 'Sugerencias de Apoyo y Enfoque:' : 'Support and Approach Suggestions:'}
                </h3>
                <ul className="space-y-2">
                  {profile.suggestions.map((suggestion, index) => (
                    <li key={index} className="flex gap-3">
                      <span className="text-primary font-bold">•</span>
                      <span className="text-muted-foreground">{suggestion}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}