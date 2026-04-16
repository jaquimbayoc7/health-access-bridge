import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';

vi.mock('@/contexts/AuthContext', () => ({ useAuth: vi.fn() }));
vi.mock('@/contexts/LanguageContext', () => ({ useLanguage: vi.fn() }));
vi.mock('@/services/patients', () => ({
  patientService: {
    getPatients: vi.fn(),
    createPatient: vi.fn(),
    updatePatient: vi.fn(),
    deletePatient: vi.fn(),
  },
}));
vi.mock('sonner', () => ({ toast: { success: vi.fn(), error: vi.fn() } }));

import Patients from '@/pages/Patients';
import { useAuth } from '@/contexts/AuthContext';
import { useLanguage } from '@/contexts/LanguageContext';
import { patientService } from '@/services/patients';

const MOCK_PATIENT = {
  id: 1,
  nombre_apellidos: 'Juan Pérez',
  numero_documento: '123456789',
  fecha_nacimiento: '1990-01-01',
  edad: 34,
  genero: 'masculino',
  orientacion_sexual: 'heterosexual',
  causa_deficiencia: 'Enfermedad congénita',
  cat_fisica: 'Sí',
  cat_psicosocial: 'No',
  nivel_d1: 70,
  nivel_d2: 60,
  nivel_d3: 80,
  nivel_d4: 50,
  nivel_d5: 65,
  nivel_d6: 75,
  nivel_global: 67,
  owner_id: 1,
  is_active: true,
  prediction_profile: null,
  prediction_description: null,
};

const renderPatients = () =>
  render(
    <MemoryRouter>
      <Patients />
    </MemoryRouter>
  );

describe('Patients page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(useAuth).mockReturnValue({
      user: { id: 1, email: 'medico@hab.co', name: 'Doc', role: 'médico' },
      isLoading: false,
      login: vi.fn(),
      logout: vi.fn(),
    });
    vi.mocked(useLanguage).mockReturnValue({
      language: 'en',
      setLanguage: vi.fn(),
      t: (key: string) => key,
    });
    vi.mocked(patientService.getPatients).mockResolvedValue([]);
  });

  it('renders the search input field', async () => {
    renderPatients();
    await waitFor(() => expect(patientService.getPatients).toHaveBeenCalled());
    expect(screen.getByPlaceholderText('search')).toBeInTheDocument();
  });

  it('shows empty state message when no patients are returned', async () => {
    vi.mocked(patientService.getPatients).mockResolvedValue([]);
    renderPatients();
    await waitFor(() => expect(screen.getByText('noPatientsYet')).toBeInTheDocument());
  });

  it('Add Patient button opens the create dialog', async () => {
    renderPatients();
    await waitFor(() => expect(patientService.getPatients).toHaveBeenCalled());
    const addButtons = screen.getAllByRole('button', { name: /addPatient/i });
    await userEvent.click(addButtons[0]);
    await waitFor(() => expect(screen.getByRole('dialog')).toBeInTheDocument());
  });

  it('clicking the delete icon triggers the confirmation AlertDialog', async () => {
    vi.mocked(patientService.getPatients).mockResolvedValue([MOCK_PATIENT]);

    vi.useFakeTimers();
    renderPatients();
    act(() => { vi.advanceTimersByTime(500); });
    vi.useRealTimers();

    await waitFor(() => expect(screen.getAllByText('Juan P\u00e9rez').length).toBeGreaterThan(0), {
      timeout: 2000,
    });

    const iconOnlyButtons = screen.getAllByRole('button').filter(
      (btn) => !btn.textContent?.trim() && btn.querySelector('svg')
    );
    await userEvent.click(iconOnlyButtons[iconOnlyButtons.length - 1]);

    await waitFor(() => expect(screen.getByRole('alertdialog')).toBeInTheDocument());
  });
});
