import { useState } from 'react';
import { BookOpen, Users, Activity, HelpCircle, ChevronDown, ChevronUp, Keyboard, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

const ICF_DIMENSIONS = [
  {
    key: 'D1', color: 'bg-blue-100 text-blue-800',
    name: 'Aprendizaje y aplicación del conocimiento',
    description: 'Capacidad para aprender, asimilar, recordar y aplicar el conocimiento en actividades cotidianas.',
    examples: ['Leer y comprender textos', 'Calcular y razonar', 'Resolver problemas prácticos', 'Tomar decisiones informadas'],
  },
  {
    key: 'D2', color: 'bg-green-100 text-green-800',
    name: 'Tareas y demandas generales',
    description: 'Capacidad para llevar a cabo tareas cotidianas simples o complejas, gestionar rutinas y manejar el estrés.',
    examples: ['Ejecutar una tarea simple', 'Gestionar múltiples actividades', 'Manejar la presión cotidiana', 'Adaptar rutinas ante cambios'],
  },
  {
    key: 'D3', color: 'bg-purple-100 text-purple-800',
    name: 'Comunicación',
    description: 'Capacidad para comunicarse mediante lenguaje verbal, no verbal o con ayuda de tecnología.',
    examples: ['Hablar y escuchar', 'Leer y escribir', 'Usar teléfono o medios digitales', 'Comprender instrucciones'],
  },
  {
    key: 'D4', color: 'bg-orange-100 text-orange-800',
    name: 'Movilidad',
    description: 'Capacidad para desplazarse, cambiar y mantener posiciones corporales, y transportar objetos.',
    examples: ['Caminar y correr', 'Subir y bajar escaleras', 'Usar transporte público', 'Mover y cargar objetos'],
  },
  {
    key: 'D5', color: 'bg-red-100 text-red-800',
    name: 'Autocuidado',
    description: 'Capacidad para cuidar el propio cuerpo: higiene personal, vestido, alimentación y salud.',
    examples: ['Bañarse e higiene personal', 'Vestirse y desvestirse', 'Alimentarse de forma autónoma', 'Cuidar la propia salud'],
  },
  {
    key: 'D6', color: 'bg-teal-100 text-teal-800',
    name: 'Vida doméstica',
    description: 'Capacidad para realizar actividades del hogar y administrar la vida doméstica de forma independiente.',
    examples: ['Preparar alimentos', 'Limpiar y ordenar el hogar', 'Hacer compras y gestionar el dinero', 'Cuidar del hogar y objetos personales'],
  },
];

const PREDICTION_PROFILES = [
  { profile: 1, label: 'Perfil 1 — Bajo riesgo', color: 'bg-green-500', description: 'El paciente presenta barreras mínimas. Alta autonomía funcional en las 6 dimensiones ICF.' },
  { profile: 2, label: 'Perfil 2 — Riesgo leve', color: 'bg-blue-500', description: 'Barreras leves en una o más dimensiones. Requiere seguimiento periódico.' },
  { profile: 3, label: 'Perfil 3 — Riesgo moderado', color: 'bg-yellow-500', description: 'Barreras moderadas que afectan la autonomía. Se recomienda intervención terapéutica.' },
  { profile: 4, label: 'Perfil 4 — Riesgo alto', color: 'bg-orange-500', description: 'Barreras graves en múltiples dimensiones. Requiere plan de intervención prioritario.' },
  { profile: 5, label: 'Perfil 5 — Barrera severa', color: 'bg-red-500', description: 'Barrera completa o severa en la mayoría de dimensiones. Atención inmediata recomendada.' },
];

const FAQ = [
  {
    q: '¿Qué es HAB y para qué sirve?',
    a: 'Health Access Bridge (HAB) es una plataforma de gestión clínica diseñada para el seguimiento de pacientes con discapacidad. Permite registrar dimensiones funcionales ICF, ejecutar predicciones de perfil de riesgo con modelos ML y generar reportes.',
  },
  {
    q: '¿Qué significa la escala 0–100 en los campos ICF?',
    a: '0 = Sin barrera (el paciente no tiene dificultad) · 25 = Barrera leve · 50 = Barrera moderada · 75 = Barrera grave · 100 = Barrera completa (el paciente no puede realizar la actividad de forma independiente). El Nivel Global es el promedio automático de D1 a D6.',
  },
  {
    q: '¿Cómo interpreto el resultado de una predicción?',
    a: 'El modelo ML asigna un perfil del 1 al 5 basado en los niveles ICF D1–D6. El badge de color indica la severidad: verde (Perfil 1) = bajo riesgo, rojo (Perfil 5) = barrera severa. El campo "description" explica el resultado en lenguaje natural.',
  },
  {
    q: '¿Cómo exporto la lista de pacientes?',
    a: 'En la página Pacientes, usa los botones "Excel" o "PDF" en la barra de búsqueda. Se incluye la fecha, hora y nombre del médico tratante en el reporte generado.',
  },
  {
    q: '¿Qué diferencia hay entre el rol médico y el rol administrador?',
    a: 'El rol "médico" accede a Pacientes, Predicciones, Análisis y Guía Predictiva. El rol "administrador" accede al Panel de Administración para gestionar cuentas de usuarios (crear, activar, desactivar médicos).',
  },
  {
    q: '¿Puedo deshacer la eliminación de un paciente?',
    a: 'No. La eliminación de un paciente es permanente e irreversible. El sistema muestra un diálogo de confirmación con el nombre del paciente antes de proceder. Asegúrate de confirmar que es el paciente correcto.',
  },
];

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
  return (
    <div className="space-y-8 max-w-4xl">
      <div>
        <h1 className="text-3xl font-bold flex items-center gap-3">
          <HelpCircle className="h-8 w-8 text-primary" />
          Centro de Ayuda
        </h1>
        <p className="text-muted-foreground mt-2">
          Glosario ICF, guía de roles, perfiles de predicción y preguntas frecuentes sobre HAB.
        </p>
      </div>

      {/* Glosario ICF */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BookOpen className="h-5 w-5 text-primary" />
            Glosario — Dimensiones ICF (D1–D6)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg flex gap-2 text-sm text-blue-800">
            <AlertCircle className="h-4 w-4 mt-0.5 flex-shrink-0" />
            <span>
              <strong>Escala uniforme 0–100:</strong> 0 = Sin barrera · 25 = Leve · 50 = Moderada · 75 = Grave · 100 = Barrera completa.
              El <strong>Nivel Global</strong> se calcula automáticamente como el promedio de D1 a D6.
            </span>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            {ICF_DIMENSIONS.map((dim) => (
              <div key={dim.key} className="border rounded-lg p-4 space-y-2">
                <div className="flex items-center gap-2">
                  <Badge className={`${dim.color} border-0 font-bold`}>{dim.key}</Badge>
                  <span className="font-semibold text-sm">{dim.name}</span>
                </div>
                <p className="text-sm text-muted-foreground leading-relaxed">{dim.description}</p>
                <div>
                  <p className="text-xs font-medium text-muted-foreground mb-1">Ejemplos:</p>
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
            Perfiles de Predicción ML (1–5)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {PREDICTION_PROFILES.map((p) => (
              <div key={p.profile} className="flex items-start gap-3 p-3 border rounded-lg">
                <Badge className={`${p.color} text-white border-0 whitespace-nowrap mt-0.5`}>
                  Perfil {p.profile}
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
            Guía de Roles
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="border rounded-lg p-4 space-y-3">
              <div className="flex items-center gap-2">
                <Badge className="bg-blue-100 text-blue-800 border-0">Médico</Badge>
              </div>
              <ul className="text-sm space-y-2 text-muted-foreground">
                <li className="flex gap-2"><span className="text-green-500 font-bold">✓</span> Ver, crear, editar y eliminar pacientes</li>
                <li className="flex gap-2"><span className="text-green-500 font-bold">✓</span> Ejecutar predicciones ML por paciente</li>
                <li className="flex gap-2"><span className="text-green-500 font-bold">✓</span> Consultar analíticas y estadísticas</li>
                <li className="flex gap-2"><span className="text-green-500 font-bold">✓</span> Usar la Guía Predictiva ICF</li>
                <li className="flex gap-2"><span className="text-green-500 font-bold">✓</span> Exportar reportes en Excel y PDF</li>
                <li className="flex gap-2"><span className="text-red-400 font-bold">✗</span> Gestionar cuentas de usuario</li>
              </ul>
            </div>
            <div className="border rounded-lg p-4 space-y-3">
              <div className="flex items-center gap-2">
                <Badge className="bg-purple-100 text-purple-800 border-0">Administrador</Badge>
              </div>
              <ul className="text-sm space-y-2 text-muted-foreground">
                <li className="flex gap-2"><span className="text-green-500 font-bold">✓</span> Acceder al Panel de Administración</li>
                <li className="flex gap-2"><span className="text-green-500 font-bold">✓</span> Crear y registrar nuevos médicos</li>
                <li className="flex gap-2"><span className="text-green-500 font-bold">✓</span> Activar y desactivar cuentas</li>
                <li className="flex gap-2"><span className="text-green-500 font-bold">✓</span> Ver listado completo de usuarios</li>
                <li className="flex gap-2"><span className="text-red-400 font-bold">✗</span> Módulos clínicos (pacientes, predicciones)</li>
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
            Atajos útiles
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-2 sm:grid-cols-2 text-sm">
            {[
              { key: 'Tab / Shift+Tab', desc: 'Navegar entre campos del formulario' },
              { key: 'Enter', desc: 'Confirmar acción o enviar formulario' },
              { key: 'Escape', desc: 'Cerrar diálogos y modales' },
              { key: 'Ctrl + F', desc: 'Buscar en la página (nativo del navegador)' },
            ].map(({ key, desc }) => (
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
            Preguntas Frecuentes
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {FAQ.map(({ q, a }) => (
              <FAQItem key={q} q={q} a={a} />
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
