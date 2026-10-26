import { render, screen, waitFor, act, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

vi.mock('@/contexts/AuthContext', () => ({ useAuth: vi.fn() }));
vi.mock('@/contexts/LanguageContext', () => ({ useLanguage: vi.fn() }));
vi.mock('@/services/analytics', () => ({
  analyticsService: { getSummary: vi.fn(), getFilterOptions: vi.fn() },
}));
vi.mock('@/services/api', () => ({ apiService: { getUsers: vi.fn() } }));
vi.mock('@/lib/analyticsExport', () => ({
  exportExcel: vi.fn(() => 'analisis.xlsx'),
  exportPdf: vi.fn(() => 'analisis.pdf'),
  svgToImage: vi.fn(async () => ({ dataUrl: 'data:image/jpeg;base64,AAAA', width: 520, height: 300 })),
}));
vi.mock('sonner', () => ({ toast: { success: vi.fn(), error: vi.fn() } }));

import Analytics from '@/pages/Analytics';
import { useAuth } from '@/contexts/AuthContext';
import { useLanguage } from '@/contexts/LanguageContext';
import { analyticsService, type AnalyticsSummary } from '@/services/analytics';
import { apiService } from '@/services/api';
import { exportExcel, exportPdf } from '@/lib/analyticsExport';
import { toast } from 'sonner';

const SUMMARY: AnalyticsSummary = {
  generated_at: '2026-10-27T15:00:00Z',
  scope: 'propio',
  filters: {},
  totals: { patients: 12, with_prediction: 10, prediction_rate: 0.8333, mean_age: 41.5, mean_global_level: 52.3, with_icf_profile: 4 },
  distributions: {
    profile: [{ key: 'Perfil 0', count: 6 }, { key: 'Perfil 1', count: 4 }],
    cat_fisica: [{ key: 'Leve', count: 5 }, { key: 'Moderada', count: 7 }],
    cat_psicosocial: [{ key: 'Leve', count: 12 }],
    genero: [{ key: 'Femenino', count: 7 }, { key: 'Masculino', count: 5 }],
    age_group: [{ key: '18-29', count: 3 }, { key: '30-44', count: 9 }],
    cause: [{ key: 'Enfermedad general', count: 8 }],
  },
  domains: [{ domain: 'D1', name: 'Aprendizaje', mean: 20, n: 12 }],
  icf: {
    patients_with_profile: 4,
    suggestions: 20,
    by_status: { sugerido: 5, aceptado: 8, editado: 3, rechazado: 4 },
    decided: 15,
    acceptance_rate: 0.7333,
    by_component: {
      b: { total: 8, aceptado: 4, editado: 1, rechazado: 1, sugerido: 2, acceptance_rate: 0.8333 },
      s: { total: 4, aceptado: 1, editado: 1, rechazado: 2, sugerido: 0, acceptance_rate: 0.5 },
      d: { total: 8, aceptado: 3, editado: 1, rechazado: 1, sugerido: 3, acceptance_rate: 0.8 },
    },
    by_origin: [{ key: 'llm', count: 12 }, { key: 'rules', count: 8 }],
    by_model: [{ key: 'gemma4:e4b', count: 20 }],
    top_codes: [{ code: 'b730', title: 'Fuerza muscular', component: 'b', count: 6, accepted: 5, rejected: 1 }],
  },
};
const EMPTY_SUMMARY: AnalyticsSummary = {
  ...SUMMARY,
  totals: { ...SUMMARY.totals, patients: 0, with_prediction: 0, prediction_rate: null, mean_age: null, mean_global_level: null, with_icf_profile: 0 },
  icf: { ...SUMMARY.icf, suggestions: 0, decided: 0, acceptance_rate: null, top_codes: [] },
};

function setup(role: 'admin' | 'médico' = 'médico', language: 'es' | 'en' = 'es') {
  vi.mocked(useAuth).mockReturnValue({ user: { id: 1, email: 'x@test.com', name: 'X', role }, login: vi.fn(), logout: vi.fn(), isLoading: false } as never);
  vi.mocked(useLanguage).mockReturnValue({ language, setLanguage: vi.fn(), t: (k: string) => k } as never);
}

beforeEach(() => {
  vi.clearAllMocks();
  vi.mocked(analyticsService.getSummary).mockResolvedValue(SUMMARY);
  vi.mocked(analyticsService.getFilterOptions).mockResolvedValue({ genero: ['Femenino', 'Masculino'], cause: ['Enfermedad general'], profile: [0, 1] });
  vi.mocked(apiService.getUsers).mockResolvedValue([
    { id: 7, email: 'a@test.com', full_name: 'Dra. Ana', is_active: true, role: 'médico' },
    { id: 1, email: 'adm@test.com', full_name: 'Admin', is_active: true, role: 'admin' },
  ]);
});
afterEach(() => { vi.useRealTimers(); });

describe('Analytics (HU-08)', () => {
  it('muestra los indicadores del resumen y avisa que los datos son agregados', async () => {
    setup();
    render(<Analytics />);
    expect(await screen.findByTestId('kpi-patients')).toHaveTextContent('12');
    expect(screen.getByTestId('kpi-prediction')).toHaveTextContent('10');
    expect(screen.getByTestId('kpi-prediction-rate')).toHaveTextContent('83.3 %');
    expect(screen.getByTestId('kpi-mean-age')).toHaveTextContent('41.5');
    expect(screen.getByText(/no incluyen nombres, documentos/i)).toBeInTheDocument();
    expect(screen.getByText(/Mis pacientes/)).toBeInTheDocument();
    expect(analyticsService.getSummary).toHaveBeenCalledWith(expect.objectContaining({ genero: '', causa: '' }));
  });

  it('cambia el idioma de la pantalla a inglés', async () => {
    setup('médico', 'en');
    render(<Analytics />);
    expect(await screen.findByText('Analytics dashboard')).toBeInTheDocument();
    expect(screen.getByText('Export Excel')).toBeInTheDocument();
  });

  it('muestra el estado vacío cuando ningún paciente coincide', async () => {
    setup();
    vi.mocked(analyticsService.getSummary).mockResolvedValue(EMPTY_SUMMARY);
    render(<Analytics />);
    expect(await screen.findByTestId('empty-patients')).toBeInTheDocument();
    expect(screen.getByTestId('kpi-mean-age')).toHaveTextContent('—');
  });

  it('un filtro de género consulta de nuevo al backend y se puede quitar', async () => {
    setup();
    const user = userEvent.setup();
    render(<Analytics />);
    await screen.findByTestId('kpi-patients');
    await user.selectOptions(screen.getByRole('combobox', { name: 'Género' }), 'Femenino');
    await waitFor(() => expect(analyticsService.getSummary).toHaveBeenLastCalledWith(expect.objectContaining({ genero: 'Femenino' })));
    await user.click(screen.getByRole('button', { name: 'Quitar filtros' }));
    await waitFor(() => expect(analyticsService.getSummary).toHaveBeenLastCalledWith(expect.objectContaining({ genero: '' })));
  });

  it('las edades se aplican con una pequeña espera, no en cada tecla', async () => {
    setup();
    render(<Analytics />);
    await screen.findByTestId('kpi-patients');
    vi.useFakeTimers();
    const calls = vi.mocked(analyticsService.getSummary).mock.calls.length;
    fireEvent.change(screen.getByLabelText('Edad desde'), { target: { value: '3' } });
    fireEvent.change(screen.getByLabelText('Edad desde'), { target: { value: '30' } });
    expect(vi.mocked(analyticsService.getSummary).mock.calls.length).toBe(calls);
    await act(async () => { await vi.advanceTimersByTimeAsync(600); });
    expect(vi.mocked(analyticsService.getSummary).mock.calls.length).toBe(calls + 1);
    expect(analyticsService.getSummary).toHaveBeenLastCalledWith(expect.objectContaining({ edad_min: '30' }));
  });

  it('muestra el error y permite reintentar', async () => {
    setup();
    vi.mocked(analyticsService.getSummary).mockRejectedValueOnce(new Error('Error temporal del servidor'));
    const user = userEvent.setup();
    render(<Analytics />);
    expect(await screen.findByRole('alert')).toHaveTextContent('Error temporal del servidor');
    await user.click(screen.getByRole('button', { name: /Reintentar/ }));
    expect(await screen.findByTestId('kpi-patients')).toHaveTextContent('12');
  });

  it('la pestaña ICF muestra la tasa de aceptación y los códigos más frecuentes', async () => {
    setup();
    const user = userEvent.setup();
    render(<Analytics />);
    await screen.findByTestId('kpi-patients');
    await user.click(screen.getByRole('tab', { name: 'Perfil funcional ICF' }));
    expect(await screen.findByTestId('kpi-acceptance')).toHaveTextContent('73.3 %');
    expect(screen.getByTestId('kpi-suggestions')).toHaveTextContent('20');
    expect(screen.getByText('b730')).toBeInTheDocument();
    expect(screen.getByText('Fuerza muscular')).toBeInTheDocument();
  });

  it('la pestaña ICF avisa cuando todavía no hay sugerencias', async () => {
    setup();
    vi.mocked(analyticsService.getSummary).mockResolvedValue({ ...SUMMARY, icf: EMPTY_SUMMARY.icf });
    const user = userEvent.setup();
    render(<Analytics />);
    await screen.findByTestId('kpi-patients');
    await user.click(screen.getByRole('tab', { name: 'Perfil funcional ICF' }));
    expect(await screen.findByTestId('empty-icf')).toBeInTheDocument();
    expect(screen.getByTestId('kpi-acceptance')).toHaveTextContent('—');
  });

  it('el administrador puede filtrar por médico; el médico no ve ese filtro', async () => {
    setup('admin');
    const user = userEvent.setup();
    const { unmount } = render(<Analytics />);
    await screen.findByTestId('kpi-patients');
    expect(await screen.findByRole('option', { name: 'Dra. Ana' })).toBeInTheDocument();
    expect(screen.queryByRole('option', { name: 'Admin' })).not.toBeInTheDocument();
    await user.selectOptions(screen.getByLabelText('Médico'), '7');
    await waitFor(() => expect(analyticsService.getSummary).toHaveBeenLastCalledWith(expect.objectContaining({ owner_id: '7' })));
    unmount();

    setup('médico');
    render(<Analytics />);
    await screen.findByTestId('kpi-patients');
    expect(screen.queryByLabelText('Médico')).not.toBeInTheDocument();
    expect(apiService.getUsers).toHaveBeenCalledTimes(1); // solo la vista del administrador
  });

  it('exporta a Excel con el resumen que se ve en pantalla', async () => {
    setup();
    const user = userEvent.setup();
    render(<Analytics />);
    await screen.findByTestId('kpi-patients');
    await user.click(screen.getByRole('button', { name: /Exportar Excel/ }));
    expect(exportExcel).toHaveBeenCalledWith(SUMMARY, 'es');
    expect(toast.success).toHaveBeenCalledWith('Archivo Excel descargado');
  });

  it('exporta a PDF y avisa si falla', async () => {
    setup();
    const user = userEvent.setup();
    render(<Analytics />);
    await screen.findByTestId('kpi-patients');
    await user.click(screen.getByRole('button', { name: /Exportar PDF/ }));
    await waitFor(() => expect(exportPdf).toHaveBeenCalledWith(SUMMARY, 'es', expect.any(Array)));
    expect(toast.success).toHaveBeenCalledWith('Archivo PDF descargado');

    vi.mocked(exportPdf).mockImplementationOnce(() => { throw new Error('boom'); });
    await user.click(screen.getByRole('button', { name: /Exportar PDF/ }));
    await waitFor(() => expect(toast.error).toHaveBeenCalledWith('No se pudo generar el archivo'));
    expect(screen.getByRole('button', { name: /Exportar PDF/ })).toBeEnabled(); // se recupera
  });

  it('los botones de exportar están desactivados mientras carga', async () => {
    setup();
    let resolve: (s: AnalyticsSummary) => void = () => undefined;
    vi.mocked(analyticsService.getSummary).mockReturnValue(new Promise((r) => { resolve = r; }));
    render(<Analytics />);
    expect(screen.getByRole('button', { name: /Exportar Excel/ })).toBeDisabled();
    await act(async () => resolve(SUMMARY));
    await waitFor(() => expect(screen.getByRole('button', { name: /Exportar Excel/ })).toBeEnabled());
  });
});
