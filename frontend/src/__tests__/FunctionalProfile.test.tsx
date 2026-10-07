import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { TooltipProvider } from '@/components/ui/tooltip';

vi.mock('@/contexts/LanguageContext', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@/contexts/LanguageContext')>();
  return { ...actual, useLanguage: vi.fn() };
});
vi.mock('@/services/patients', () => ({ patientService: { getPatients: vi.fn() } }));
vi.mock('@/services/icf', () => ({
  icfService: { generate: vi.fn(), getLatest: vi.fn(), decide: vi.fn() },
}));
vi.mock('sonner', () => ({ toast: { success: vi.fn(), error: vi.fn(), warning: vi.fn() } }));

import FunctionalProfile from '@/pages/FunctionalProfile';
import { useLanguage } from '@/contexts/LanguageContext';
import { patientService } from '@/services/patients';
import { icfService } from '@/services/icf';
import { buildReportText, formatCode } from '@/lib/icfReport';
import { CAUSE_GROUPS, OFFICIAL_CAUSES, isOfficialCause } from '@/lib/causes';

const PATIENT = {
  id: 1, nombre_apellidos: 'Juan Pérez', numero_documento: '123', fecha_nacimiento: '1990-01-01', edad: 34,
  genero: 'masculino', orientacion_sexual: 'heterosexual', causa_deficiencia: 'Enfermedad general',
  cat_fisica: 'Severa', cat_psicosocial: 'Leve', nivel_d1: 70, nivel_d2: 60, nivel_d3: 80, nivel_d4: 50,
  nivel_d5: 65, nivel_d6: 75, nivel_global: 67, owner_id: 1, prediction_profile: 2,
  prediction_description: 'Perfil de Barreras Altas',
};
const CHILD = { ...PATIENT, id: 2, nombre_apellidos: 'Niña Gómez', edad: 5 };

const item = (over: Record<string, unknown>) => ({
  id: 1, component: 'b', code: 'b730', title: 'Funciones relacionadas con la fuerza muscular', qualifier: 3,
  qualifier_cn: null, qualifier_cl: null, justification: 'Debilidad', origin: 'llm', status: 'sugerido',
  original_code: null, ...over,
});

const SET = {
  patient_id: 1, batch_id: 'abc', model: 'gemma4:e4b', llm_used: true, created_at: null, latency_ms: 3400,
  warnings: [],
  functions: [item({ id: 11 })],
  structures: [item({ id: 12, component: 's', code: 's750', title: 'Estructura de la extremidad inferior', qualifier_cn: 8, qualifier_cl: 8, justification: '' })],
  activities: [item({ id: 13, component: 'd', code: 'd450', title: 'Andar', origin: 'rules', justification: '' })],
};

const EMPTY = { ...SET, batch_id: null, model: null, functions: [], structures: [], activities: [] };

const renderPage = () =>
  render(
    <MemoryRouter>
      <TooltipProvider>
        <FunctionalProfile />
      </TooltipProvider>
    </MemoryRouter>
  );

async function choosePatient(name: RegExp) {
  const user = userEvent.setup();
  await user.click(await screen.findByRole('combobox', { name: /seleccionar paciente/i }));
  await user.click(await screen.findByRole('option', { name }));
  return user;
}

beforeEach(() => {
  vi.clearAllMocks();
  (useLanguage as ReturnType<typeof vi.fn>).mockReturnValue({
    language: 'es',
    t: (k: string) => ({ functionalProfile: 'Perfil Funcional ICF', selectPatient: 'Seleccionar Paciente' }[k] ?? k),
  });
  (patientService.getPatients as ReturnType<typeof vi.fn>).mockResolvedValue([PATIENT, CHILD]);
  (icfService.getLatest as ReturnType<typeof vi.fn>).mockResolvedValue(EMPTY);
});

describe('FunctionalProfile', () => {
  it('muestra la leyenda de borrador de apoyo y la resolución', async () => {
    renderPage();
    expect((await screen.findAllByText(/Borrador de apoyo/i)).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/Resolución 1239 del 21 de julio de 2022/).length).toBeGreaterThan(0);
    expect(screen.getByText(/No sustituye el certificado de discapacidad/i)).toBeInTheDocument();
  });

  it('el botón de generar está deshabilitado sin paciente', async () => {
    renderPage();
    expect(await screen.findByRole('button', { name: /generar perfil funcional/i })).toBeDisabled();
  });

  it('genera el perfil y muestra los tres componentes con su calificador', async () => {
    (icfService.generate as ReturnType<typeof vi.fn>).mockResolvedValue(SET);
    renderPage();
    const user = await choosePatient(/Juan Pérez/);
    await user.click(screen.getByRole('button', { name: /generar perfil funcional/i }));
    expect(await screen.findByTestId('code-11')).toHaveTextContent('b730.3');
    expect(screen.getByTestId('code-12')).toHaveTextContent('s750.388');
    expect(screen.getByTestId('code-13')).toHaveTextContent('d450.3');
    expect(icfService.generate).toHaveBeenCalledWith(1, {});
  });

  it('envía el diagnóstico y las notas cuando se escriben', async () => {
    (icfService.generate as ReturnType<typeof vi.fn>).mockResolvedValue(SET);
    renderPage();
    const user = await choosePatient(/Juan Pérez/);
    await user.type(screen.getByLabelText(/Diagnóstico CIE/i), 'M54 Dorsalgia');
    await user.type(screen.getByLabelText(/Notas clínicas/i), 'Lumbalgia');
    await user.click(screen.getByRole('button', { name: /generar perfil funcional/i }));
    await waitFor(() =>
      expect(icfService.generate).toHaveBeenCalledWith(1, { diag_cie: 'M54 Dorsalgia', clinical_notes: 'Lumbalgia' })
    );
  });

  it('ofrece enlaces a la CIE que abren en pestaña nueva y un código de ejemplo rellena el diagnóstico', async () => {
    renderPage();
    const link = await screen.findByRole('link', { name: /CIE-10 en español/i });
    expect(link).toHaveAttribute('href', 'https://ais.paho.org/classifications/Chapters/');
    expect(link).toHaveAttribute('target', '_blank');
    expect(link).toHaveAttribute('rel', expect.stringContaining('noopener'));
    const user = userEvent.setup();
    await user.click(screen.getByRole('button', { name: 'G80' }));
    expect(screen.getByLabelText(/Diagnóstico CIE/i)).toHaveValue('G80 Parálisis cerebral');
  });

  it('«Usar este ejemplo» rellena el diagnóstico y las notas, y se envían al generar', async () => {
    (icfService.generate as ReturnType<typeof vi.fn>).mockResolvedValue(SET);
    renderPage();
    const user = await choosePatient(/Juan Pérez/);
    await user.click(screen.getByText('Ejemplos de notas clínicas'));
    await user.click(screen.getAllByRole('button', { name: 'Usar este ejemplo' })[0]);
    expect(screen.getByLabelText(/Diagnóstico CIE/i)).toHaveValue('G80 Parálisis cerebral');
    expect((screen.getByLabelText(/Notas clínicas/i) as HTMLTextAreaElement).value).toMatch(/Espasticidad/);
    await user.click(screen.getByRole('button', { name: /generar perfil funcional/i }));
    await waitFor(() =>
      expect(icfService.generate).toHaveBeenCalledWith(
        1,
        expect.objectContaining({ diag_cie: 'G80 Parálisis cerebral', clinical_notes: expect.stringMatching(/Espasticidad/) })
      )
    );
  });

  it('enlaza a la guía de cómo funciona el Perfil Funcional ICF', async () => {
    renderPage();
    expect(await screen.findByRole('link', { name: /Cómo funciona el Perfil Funcional ICF/i })).toHaveAttribute(
      'href',
      '/predictive-guide?section=icf'
    );
  });

  it('avisa que no aplica para menores de 6 años y no deja generar', async () => {
    renderPage();
    await choosePatient(/Niña Gómez/);
    expect(await screen.findByText(/menores de 6 años no aplica/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /generar perfil funcional/i })).toBeDisabled();
  });

  it('muestra el aviso claro cuando el servicio no responde', async () => {
    (icfService.generate as ReturnType<typeof vi.fn>).mockRejectedValue(
      new Error('El servicio de sugerencias no esta disponible en este momento')
    );
    renderPage();
    const user = await choosePatient(/Juan Pérez/);
    await user.click(screen.getByRole('button', { name: /generar perfil funcional/i }));
    const message = await screen.findByText(/no esta disponible/);
    expect(message).toHaveTextContent(/resto de la aplicación sigue funcionando/);
  });

  it('acepta y rechaza un código guardando la decisión', async () => {
    (icfService.generate as ReturnType<typeof vi.fn>).mockResolvedValue(SET);
    (icfService.decide as ReturnType<typeof vi.fn>)
      .mockResolvedValueOnce(item({ id: 11, status: 'aceptado' }))
      .mockResolvedValueOnce(item({ id: 13, component: 'd', code: 'd450', title: 'Andar', status: 'rechazado' }));
    renderPage();
    const user = await choosePatient(/Juan Pérez/);
    await user.click(screen.getByRole('button', { name: /generar perfil funcional/i }));
    await user.click(await screen.findByRole('button', { name: /aceptar b730/i }));
    expect(icfService.decide).toHaveBeenCalledWith(11, { status: 'aceptado' });
    expect(await screen.findByText('Aceptado')).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: /rechazar d450/i }));
    expect(icfService.decide).toHaveBeenCalledWith(13, { status: 'rechazado' });
    expect(await screen.findByText('Rechazado')).toBeInTheDocument();
  });

  it('edita el calificador de una función', async () => {
    (icfService.generate as ReturnType<typeof vi.fn>).mockResolvedValue(SET);
    (icfService.decide as ReturnType<typeof vi.fn>).mockResolvedValue(item({ id: 11, qualifier: 2, status: 'editado' }));
    renderPage();
    const user = await choosePatient(/Juan Pérez/);
    await user.click(screen.getByRole('button', { name: /generar perfil funcional/i }));
    await user.click(await screen.findByRole('button', { name: /editar b730/i }));
    await user.click(await screen.findByRole('combobox', { name: /calificador/i }));
    await user.click(await screen.findByRole('option', { name: /2 — Moderada/ }));
    await user.click(screen.getByRole('button', { name: /^guardar$/i }));
    await waitFor(() => expect(icfService.decide).toHaveBeenCalledWith(11, { status: 'editado', qualifier: 2 }));
    expect(await screen.findByTestId('code-11')).toHaveTextContent('b730.2');
  });

  it('carga la última sugerencia guardada al elegir el paciente', async () => {
    (icfService.getLatest as ReturnType<typeof vi.fn>).mockResolvedValue(SET);
    renderPage();
    await choosePatient(/Juan Pérez/);
    expect(await screen.findByTestId('code-11')).toBeInTheDocument();
  });
});

describe('icfReport y causas', () => {
  it('formatea los calificadores de funciones, actividades y estructuras', () => {
    expect(formatCode({ component: 'b', code: 'b730', qualifier: 3, qualifier_cn: null, qualifier_cl: null })).toBe('b730.3');
    expect(formatCode({ component: 's', code: 's750', qualifier: 3, qualifier_cn: 2, qualifier_cl: 5 })).toBe('s750.325');
    expect(formatCode({ component: 's', code: 's750', qualifier: 3, qualifier_cn: null, qualifier_cl: null })).toBe('s750.388');
  });

  it('el reporte copiado omite los rechazados e incluye la resolución y la leyenda', () => {
    const text = buildReportText(
      { ...SET, functions: [item({ id: 1 }) as never, item({ id: 2, code: 'b280', status: 'rechazado' }) as never] } as never,
      'Juan Pérez, 34 años'
    );
    expect(text).toContain('Resolución 1239 del 21 de julio de 2022');
    expect(text).toContain('b730.3');
    expect(text).not.toContain('b280');
    expect(text).toContain('No sustituye el certificado');
  });

  it('la lista de causas tiene 21 opciones oficiales en 3 grupos', () => {
    expect(OFFICIAL_CAUSES).toHaveLength(21);
    expect(CAUSE_GROUPS.map((g) => g.options.length)).toEqual([4, 16, 1]);
    expect(isOfficialCause('Accidente de trabajo')).toBe(true);
    expect(isOfficialCause('Accidente laboral')).toBe(false);
  });
});
