import React, { createContext, useContext, useState, useEffect } from 'react';

type Language = 'en' | 'es';

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: string) => string;
}

const translations = {
  en: {
    // Navigation
    dashboard: 'Dashboard',
    patients: 'Patients',
    predictions: 'Predictions',
    analytics: 'Analytics',
    predictiveGuide: 'Predictive Guide',
    userList: 'User List',
    help: 'Help',
    settings: 'Settings',
    logout: 'Logout',
    
    // Auth
    login: 'Login',
    email: 'Email',
    password: 'Password',
    welcomeBack: 'Welcome Back',
    loginSubtitle: 'Enter your credentials to access your account',
    forgotPasswordText: 'Forgot your password?',
    passwordRecoveryDisclaimer: 'For security reasons, passwords cannot be reset from this page. Please contact your corresponding administrator, who will send you a recovery email.',
    
    // Dashboard
    totalPatients: 'Total Patients',
    activeCases: 'Active Cases',
    predictionsToday: 'Predictions Today',
    successRate: 'Success Rate',
    recentPatients: 'Recent Patients',
    viewAll: 'View All',
    noPatientsYet: 'No patients yet',
    addFirstPatient: 'Add your first patient to get started',
    
    // Patients
    addPatient: 'Add Patient',
    patientList: 'Patient List',
    patientName: 'Patient Name',
    age: 'Age',
    gender: 'Gender',
    status: 'Status',
    actions: 'Actions',
    edit: 'Edit',
    delete: 'Delete',
    viewDetails: 'View Details',
    male: 'Male',
    female: 'Female',
    other: 'Other',
    createPatient: 'Create Patient',
    editPatient: 'Edit Patient',
    fullName: 'Full Name',
    birthDate: 'Birth Date',
    sexualOrientation: 'Sexual Orientation',
    deficiencyCause: 'Cause of Deficiency',
    physicalCategory: 'Physical Category',
    psychosocialCategory: 'Psychosocial Category',
    levelD1: 'Level D1 (Learning)',
    levelD2: 'Level D2 (General Tasks)',
    levelD3: 'Level D3 (Communication)',
    levelD4: 'Level D4 (Mobility)',
    levelD5: 'Level D5 (Self-Care)',
    levelD6: 'Level D6 (Domestic Life)',
    globalLevel: 'Global Level',
    confirmDelete: 'Are you sure you want to delete this patient?',
    deleteWarning: 'This action cannot be undone.',
    patientCreated: 'Patient created successfully',
    patientUpdated: 'Patient updated successfully',
    patientDeleted: 'Patient deleted successfully',
    errorLoadingPatients: 'Error loading patients',
    errorCreatingPatient: 'Error creating patient',
    errorUpdatingPatient: 'Error updating patient',
    errorDeletingPatient: 'Error deleting patient',
    
    // Predictions
    newPrediction: 'New Prediction',
    selectPatient: 'Select Patient',
    predictionHistory: 'Prediction History',
    runPrediction: 'Run Prediction',
    barrierType: 'Barrier Type',
    confidence: 'Confidence',
    date: 'Date',
    
    // Common
    save: 'Save',
    cancel: 'Cancel',
    search: 'Search',
    filter: 'Filter',
    export: 'Export',
    loading: 'Loading...',
    error: 'Error',
    success: 'Success',

    // Help Center
    helpCenterTitle: 'Help Center',
    helpCenterSubtitle: 'ICF glossary, role guide, prediction profiles and frequently asked questions about HAB.',
    helpDisclaimerTitle: 'Important notice',
    helpDisclaimerText: 'Health Access Bridge (HAB) uses an adaptation of the International Classification of Functioning, Disability and Health (ICF) model developed by the World Health Organization (WHO). This platform is NOT an official WHO application, nor is it endorsed or certified by that organization. The predictions and functional profiles generated are decision-support tools intended to assist the treating physician — they do not replace clinical judgment, a formal diagnosis, or professional medical evaluation.',
    helpGlossaryTitle: 'Glossary — ICF Dimensions (D1–D6)',
    helpScaleBanner: 'Uniform 0–100 scale:',
    helpScaleBannerRest: '0 = No barrier · 25 = Mild · 50 = Moderate · 75 = Severe · 100 = Complete barrier. The Global Level is automatically calculated as the average of D1 to D6.',
    helpExamplesLabel: 'Examples:',
    helpPredictionProfilesTitle: 'ML Prediction Profiles (1–5)',
    helpProfileBadge: 'Profile',
    helpRolesTitle: 'Role Guide',
    helpRoleDoctor: 'Doctor',
    helpRoleAdmin: 'Administrator',
    helpShortcutsTitle: 'Useful Shortcuts',
    helpFaqTitle: 'Frequently Asked Questions',
  },
  es: {
    // Navegación
    dashboard: 'Panel',
    patients: 'Pacientes',
    predictions: 'Predicciones',
    analytics: 'Análisis',
    predictiveGuide: 'Guía Predictiva',
    userList: 'Listado de Usuarios',
    help: 'Ayuda',
    settings: 'Configuración',
    logout: 'Cerrar Sesión',
    
    // Autenticación
    login: 'Iniciar Sesión',
    email: 'Correo Electrónico',
    password: 'Contraseña',
    welcomeBack: 'Bienvenido de Nuevo',
    loginSubtitle: 'Ingresa tus credenciales para acceder a tu cuenta',
    forgotPasswordText: '¿Olvidó su contraseña?',
    passwordRecoveryDisclaimer: 'Por seguridad, la contraseña no se puede restablecer desde esta página. Comuníquese con el administrador correspondiente, quien le enviará un correo de recuperación.',
    
    // Panel
    totalPatients: 'Total de Pacientes',
    activeCases: 'Casos Activos',
    predictionsToday: 'Predicciones Hoy',
    successRate: 'Tasa de Éxito',
    recentPatients: 'Pacientes Recientes',
    viewAll: 'Ver Todo',
    noPatientsYet: 'Aún no hay pacientes',
    addFirstPatient: 'Agrega tu primer paciente para comenzar',
    
    // Pacientes
    addPatient: 'Agregar Paciente',
    patientList: 'Lista de Pacientes',
    patientName: 'Nombre del Paciente',
    age: 'Edad',
    gender: 'Género',
    status: 'Estado',
    actions: 'Acciones',
    edit: 'Editar',
    delete: 'Eliminar',
    viewDetails: 'Ver Detalles',
    male: 'Masculino',
    female: 'Femenino',
    other: 'Otro',
    createPatient: 'Crear Paciente',
    editPatient: 'Editar Paciente',
    fullName: 'Nombre Completo',
    birthDate: 'Fecha de Nacimiento',
    sexualOrientation: 'Orientación Sexual',
    deficiencyCause: 'Causa de la Deficiencia',
    physicalCategory: 'Categoría Física',
    psychosocialCategory: 'Categoría Psicosocial',
    levelD1: 'Nivel D1 (Aprendizaje)',
    levelD2: 'Nivel D2 (Tareas Generales)',
    levelD3: 'Nivel D3 (Comunicación)',
    levelD4: 'Nivel D4 (Movilidad)',
    levelD5: 'Nivel D5 (Autocuidado)',
    levelD6: 'Nivel D6 (Vida Doméstica)',
    globalLevel: 'Nivel Global',
    confirmDelete: '¿Está seguro que desea eliminar este paciente?',
    deleteWarning: 'Esta acción no se puede deshacer.',
    patientCreated: 'Paciente creado exitosamente',
    patientUpdated: 'Paciente actualizado exitosamente',
    patientDeleted: 'Paciente eliminado exitosamente',
    errorLoadingPatients: 'Error al cargar pacientes',
    errorCreatingPatient: 'Error al crear paciente',
    errorUpdatingPatient: 'Error al actualizar paciente',
    errorDeletingPatient: 'Error al eliminar paciente',
    
    // Predicciones
    newPrediction: 'Nueva Predicción',
    selectPatient: 'Seleccionar Paciente',
    predictionHistory: 'Historial de Predicciones',
    runPrediction: 'Ejecutar Predicción',
    barrierType: 'Tipo de Barrera',
    confidence: 'Confianza',
    date: 'Fecha',
    
    // Común
    save: 'Guardar',
    cancel: 'Cancelar',
    search: 'Buscar',
    filter: 'Filtrar',
    export: 'Exportar',
    loading: 'Cargando...',
    error: 'Error',
    success: 'Éxito',

    // Centro de Ayuda
    helpCenterTitle: 'Centro de Ayuda',
    helpCenterSubtitle: 'Glosario ICF, guía de roles, perfiles de predicción y preguntas frecuentes sobre HAB.',
    helpDisclaimerTitle: 'Aviso importante',
    helpDisclaimerText: 'Health Access Bridge (HAB) utiliza una adaptación del modelo de la Clasificación Internacional del Funcionamiento, de la Discapacidad y de la Salud (CIF/ICF) desarrollado por la Organización Mundial de la Salud (OMS). Esta plataforma NO es una aplicación oficial de la OMS, ni está avalada ni certificada por dicha organización. Las predicciones y perfiles funcionales generados son herramientas de apoyo a la decisión, pensadas para asistir al médico tratante — no reemplazan el criterio clínico, un diagnóstico formal ni la evaluación médica profesional.',
    helpGlossaryTitle: 'Glosario — Dimensiones ICF (D1–D6)',
    helpScaleBanner: 'Escala uniforme 0–100:',
    helpScaleBannerRest: '0 = Sin barrera · 25 = Leve · 50 = Moderada · 75 = Grave · 100 = Barrera completa. El Nivel Global se calcula automáticamente como el promedio de D1 a D6.',
    helpExamplesLabel: 'Ejemplos:',
    helpPredictionProfilesTitle: 'Perfiles de Predicción ML (1–5)',
    helpProfileBadge: 'Perfil',
    helpRolesTitle: 'Guía de Roles',
    helpRoleDoctor: 'Médico',
    helpRoleAdmin: 'Administrador',
    helpShortcutsTitle: 'Atajos útiles',
    helpFaqTitle: 'Preguntas Frecuentes',
  },
};

// --- Contenido estructurado de Ayuda (ICF Tooltip + Centro de Ayuda) ---
// Estos diccionarios responden al idioma activo, a diferencia del contenido
// previo que estaba hardcodeado en español dentro de los componentes.

export const icfTooltipContent = {
  en: {
    d1: { name: 'D1 — Learning and applying knowledge', description: 'Ability to learn, absorb and apply knowledge in everyday situations.', examples: 'Reading, calculating, solving problems, making decisions.' },
    d2: { name: 'D2 — General tasks and demands', description: 'Ability to carry out simple or complex tasks and manage daily workload.', examples: 'Organizing routines, managing stress, multitasking.' },
    d3: { name: 'D3 — Communication', description: 'Ability to communicate through verbal, non-verbal or assistive technology.', examples: 'Speaking, listening, reading, writing, using a phone.' },
    d4: { name: 'D4 — Mobility', description: 'Ability to move around, maintain body positions and carry objects.', examples: 'Walking, climbing stairs, using transport, moving objects.' },
    d5: { name: 'D5 — Self-care', description: 'Ability to care for one\'s own body: hygiene, dressing and eating.', examples: 'Bathing, dressing, eating independently.' },
    d6: { name: 'D6 — Domestic life', description: 'Ability to independently carry out household activities.', examples: 'Cooking, cleaning, shopping, caring for the home.' },
    scaleLabel: 'Scale 0 – 100',
    scaleText: '0 = No barrier · 25 = Mild · 50 = Moderate · 75 = Severe · 100 = Complete barrier',
    exampleLabel: 'E.g.',
  },
  es: {
    d1: { name: 'D1 — Aprendizaje y conocimiento', description: 'Capacidad para aprender, asimilar y aplicar el conocimiento en situaciones cotidianas.', examples: 'Leer, calcular, resolver problemas, tomar decisiones.' },
    d2: { name: 'D2 — Tareas y demandas generales', description: 'Capacidad para ejecutar tareas simples o complejas y gestionar la carga de trabajo diaria.', examples: 'Organizar rutinas, manejar el estrés, realizar múltiples tareas.' },
    d3: { name: 'D3 — Comunicación', description: 'Capacidad para comunicarse mediante lenguaje verbal, no verbal o tecnológico.', examples: 'Hablar, escuchar, leer, escribir, usar teléfono.' },
    d4: { name: 'D4 — Movilidad', description: 'Capacidad para desplazarse, mantener posiciones corporales y transportar objetos.', examples: 'Caminar, subir escaleras, usar transporte, mover objetos.' },
    d5: { name: 'D5 — Autocuidado', description: 'Capacidad para cuidar el propio cuerpo: higiene, vestido y alimentación.', examples: 'Bañarse, vestirse, alimentarse de forma autónoma.' },
    d6: { name: 'D6 — Vida doméstica', description: 'Capacidad para realizar actividades del hogar de manera independiente.', examples: 'Cocinar, limpiar, hacer compras, cuidar el hogar.' },
    scaleLabel: 'Escala 0 – 100',
    scaleText: '0 = Sin barrera · 25 = Leve · 50 = Moderada · 75 = Grave · 100 = Barrera completa',
    exampleLabel: 'Ej:',
  },
} as const;

export const icfDimensionsContent = {
  en: [
    { key: 'D1', color: 'bg-blue-100 text-blue-800', name: 'Learning and applying knowledge', description: 'Ability to learn, absorb, remember and apply knowledge in everyday activities.', examples: ['Reading and understanding texts', 'Calculating and reasoning', 'Solving practical problems', 'Making informed decisions'] },
    { key: 'D2', color: 'bg-green-100 text-green-800', name: 'General tasks and demands', description: 'Ability to carry out simple or complex daily tasks, manage routines and handle stress.', examples: ['Carrying out a simple task', 'Managing multiple activities', 'Handling daily pressure', 'Adapting routines to change'] },
    { key: 'D3', color: 'bg-purple-100 text-purple-800', name: 'Communication', description: 'Ability to communicate through verbal, non-verbal language or with the help of technology.', examples: ['Speaking and listening', 'Reading and writing', 'Using a phone or digital media', 'Understanding instructions'] },
    { key: 'D4', color: 'bg-orange-100 text-orange-800', name: 'Mobility', description: 'Ability to move around, change and maintain body positions, and carry objects.', examples: ['Walking and running', 'Going up and down stairs', 'Using public transport', 'Moving and carrying objects'] },
    { key: 'D5', color: 'bg-red-100 text-red-800', name: 'Self-care', description: 'Ability to care for one\'s own body: personal hygiene, dressing, eating and health.', examples: ['Bathing and personal hygiene', 'Dressing and undressing', 'Eating independently', 'Taking care of one\'s own health'] },
    { key: 'D6', color: 'bg-teal-100 text-teal-800', name: 'Domestic life', description: 'Ability to carry out household activities and manage domestic life independently.', examples: ['Preparing food', 'Cleaning and tidying the home', 'Shopping and managing money', 'Caring for the home and personal items'] },
  ],
  es: [
    { key: 'D1', color: 'bg-blue-100 text-blue-800', name: 'Aprendizaje y aplicación del conocimiento', description: 'Capacidad para aprender, asimilar, recordar y aplicar el conocimiento en actividades cotidianas.', examples: ['Leer y comprender textos', 'Calcular y razonar', 'Resolver problemas prácticos', 'Tomar decisiones informadas'] },
    { key: 'D2', color: 'bg-green-100 text-green-800', name: 'Tareas y demandas generales', description: 'Capacidad para llevar a cabo tareas cotidianas simples o complejas, gestionar rutinas y manejar el estrés.', examples: ['Ejecutar una tarea simple', 'Gestionar múltiples actividades', 'Manejar la presión cotidiana', 'Adaptar rutinas ante cambios'] },
    { key: 'D3', color: 'bg-purple-100 text-purple-800', name: 'Comunicación', description: 'Capacidad para comunicarse mediante lenguaje verbal, no verbal o con ayuda de tecnología.', examples: ['Hablar y escuchar', 'Leer y escribir', 'Usar teléfono o medios digitales', 'Comprender instrucciones'] },
    { key: 'D4', color: 'bg-orange-100 text-orange-800', name: 'Movilidad', description: 'Capacidad para desplazarse, cambiar y mantener posiciones corporales, y transportar objetos.', examples: ['Caminar y correr', 'Subir y bajar escaleras', 'Usar transporte público', 'Mover y cargar objetos'] },
    { key: 'D5', color: 'bg-red-100 text-red-800', name: 'Autocuidado', description: 'Capacidad para cuidar el propio cuerpo: higiene personal, vestido, alimentación y salud.', examples: ['Bañarse e higiene personal', 'Vestirse y desvestirse', 'Alimentarse de forma autónoma', 'Cuidar la propia salud'] },
    { key: 'D6', color: 'bg-teal-100 text-teal-800', name: 'Vida doméstica', description: 'Capacidad para realizar actividades del hogar y administrar la vida doméstica de forma independiente.', examples: ['Preparar alimentos', 'Limpiar y ordenar el hogar', 'Hacer compras y gestionar el dinero', 'Cuidar del hogar y objetos personales'] },
  ],
} as const;

export const predictionProfilesContent = {
  en: [
    { profile: 0, label: 'Profile 0 — Low or Focused Barriers', color: 'bg-gray-500', description: 'The patient reports low difficulty levels in most domains. They have developed effective coping strategies or have an environment with few significant barriers. High autonomy and overall functionality.' },
    { profile: 1, label: 'Profile 1 — Moderate or Mixed Barriers', color: 'bg-green-500', description: 'The patient shows a heterogeneous experience: low levels in some domains and significantly high in others. Barriers are contextual and specific, not generalized. Requires targeted interventions.' },
    { profile: 2, label: 'Profile 2 — High and Generalized Barriers', color: 'bg-blue-500', description: 'The patient perceives high difficulty levels in most or all evaluated domains. Barriers have a significant cross-cutting impact on their life, autonomy and social participation. Requires priority, multidisciplinary intervention.' },
  ],
  es: [
    { profile: 0, label: 'Perfil 0 — Barreras Bajas o Focalizadas', color: 'bg-gray-500', description: 'El paciente reporta niveles de dificultad bajos en la mayoría de dominios. Ha desarrollado estrategias de afrontamiento efectivas o cuenta con un entorno con pocas barreras significativas. Alta autonomía y funcionalidad general.' },
    { profile: 1, label: 'Perfil 1 — Barreras Moderadas o Mixtas', color: 'bg-green-500', description: 'El paciente presenta una experiencia heterogénea: niveles bajos en algunos dominios y significativamente altos en otros. Las barreras son contextuales y específicas, no generalizadas. Requiere intervenciones focalizadas.' },
    { profile: 2, label: 'Perfil 2 — Barreras Altas y Generalizadas', color: 'bg-blue-500', description: 'El paciente percibe niveles de dificultad altos en la mayoría o todos los dominios evaluados. Las barreras tienen un impacto transversal significativo en su vida, autonomía y participación social. Requiere intervención prioritaria y enfoque multidisciplinario.' },
  ],
} as const;

export const helpRolesContent = {
  en: {
    doctor: ['View, create, edit and delete patients', 'Run ML predictions per patient', 'Check analytics and statistics', 'Use the Predictive ICF Guide', 'Export reports in Excel and PDF'],
    doctorNo: ['Manage user accounts'],
    admin: ['Access the Admin Panel', 'Create and register new doctors', 'Activate and deactivate accounts', 'View the full user list'],
    adminNo: ['Clinical modules (patients, predictions)'],
  },
  es: {
    doctor: ['Ver, crear, editar y eliminar pacientes', 'Ejecutar predicciones ML por paciente', 'Consultar analíticas y estadísticas', 'Usar la Guía Predictiva ICF', 'Exportar reportes en Excel y PDF'],
    doctorNo: ['Gestionar cuentas de usuario'],
    admin: ['Acceder al Panel de Administración', 'Crear y registrar nuevos médicos', 'Activar y desactivar cuentas', 'Ver listado completo de usuarios'],
    adminNo: ['Módulos clínicos (pacientes, predicciones)'],
  },
} as const;

export const helpShortcutsContent = {
  en: [
    { key: 'Tab / Shift+Tab', desc: 'Navigate between form fields' },
    { key: 'Enter', desc: 'Confirm action or submit form' },
    { key: 'Escape', desc: 'Close dialogs and modals' },
    { key: 'Ctrl + F', desc: 'Search on the page (native browser feature)' },
  ],
  es: [
    { key: 'Tab / Shift+Tab', desc: 'Navegar entre campos del formulario' },
    { key: 'Enter', desc: 'Confirmar acción o enviar formulario' },
    { key: 'Escape', desc: 'Cerrar diálogos y modales' },
    { key: 'Ctrl + F', desc: 'Buscar en la página (nativo del navegador)' },
  ],
} as const;

export const faqContent = {
  en: [
    { q: 'What is HAB and what is it for?', a: 'Health Access Bridge (HAB) is a clinical management platform designed to track patients with disabilities. It allows recording ICF functional dimensions, running ML risk profile predictions and generating reports.' },
    { q: 'What does the 0–100 scale mean in ICF fields?', a: '0 = No barrier (the patient has no difficulty) · 25 = Mild barrier · 50 = Moderate barrier · 75 = Severe barrier · 100 = Complete barrier (the patient cannot perform the activity independently). The Global Level is the automatic average of D1 to D6.' },
    { q: 'How do I interpret a prediction result?', a: 'The ML model assigns a profile from 0 to 2 based on the ICF D1–D6 levels. Profile 0 (gray) = low or focused barriers · Profile 1 (green) = moderate or mixed barriers · Profile 2 (blue) = high and generalized barriers. The description field explains the result in natural clinical language.' },
    { q: 'How do I export the patient list?', a: 'On the Patients page, use the "Excel" or "PDF" buttons in the search bar. The generated report includes the date, time and name of the attending doctor.' },
    { q: 'What is the difference between the doctor and administrator roles?', a: 'The "doctor" role accesses Patients, Predictions, Analytics and Predictive Guide. The "administrator" role accesses the Admin Panel to manage user accounts (create, activate, deactivate doctors).' },
    { q: 'Can I undo the deletion of a patient?', a: 'No. Deleting a patient is permanent and irreversible. The system shows a confirmation dialog with the patient\'s name before proceeding. Make sure to confirm it is the correct patient.' },
  ],
  es: [
    { q: '¿Qué es HAB y para qué sirve?', a: 'Health Access Bridge (HAB) es una plataforma de gestión clínica diseñada para el seguimiento de pacientes con discapacidad. Permite registrar dimensiones funcionales ICF, ejecutar predicciones de perfil de riesgo con modelos ML y generar reportes.' },
    { q: '¿Qué significa la escala 0–100 en los campos ICF?', a: '0 = Sin barrera (el paciente no tiene dificultad) · 25 = Barrera leve · 50 = Barrera moderada · 75 = Barrera grave · 100 = Barrera completa (el paciente no puede realizar la actividad de forma independiente). El Nivel Global es el promedio automático de D1 a D6.' },
    { q: '¿Cómo interpreto el resultado de una predicción?', a: 'El modelo ML asigna un perfil del 0 al 2 basado en los niveles ICF D1–D6. Perfil 0 (gris) = barreras bajas o focalizadas · Perfil 1 (verde) = barreras moderadas o mixtas · Perfil 2 (azul) = barreras altas y generalizadas. El campo de descripción explica el resultado en lenguaje clínico natural.' },
    { q: '¿Cómo exporto la lista de pacientes?', a: 'En la página Pacientes, usa los botones "Excel" o "PDF" en la barra de búsqueda. Se incluye la fecha, hora y nombre del médico tratante en el reporte generado.' },
    { q: '¿Qué diferencia hay entre el rol médico y el rol administrador?', a: 'El rol "médico" accede a Pacientes, Predicciones, Análisis y Guía Predictiva. El rol "administrador" accede al Panel de Administración para gestionar cuentas de usuarios (crear, activar, desactivar médicos).' },
    { q: '¿Puedo deshacer la eliminación de un paciente?', a: 'No. La eliminación de un paciente es permanente e irreversible. El sistema muestra un diálogo de confirmación con el nombre del paciente antes de proceder. Asegúrate de confirmar que es el paciente correcto.' },
  ],
} as const;

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [language, setLanguage] = useState<Language>(() => {
    const saved = localStorage.getItem('language');
    return (saved as Language) || 'en';
  });

  useEffect(() => {
    localStorage.setItem('language', language);
  }, [language]);

  const t = (key: string): string => {
    return translations[language][key as keyof typeof translations.en] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within LanguageProvider');
  }
  return context;
};
