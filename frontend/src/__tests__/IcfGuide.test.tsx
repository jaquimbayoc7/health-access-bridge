import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';

vi.mock('@/contexts/LanguageContext', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@/contexts/LanguageContext')>();
  return { ...actual, useLanguage: vi.fn() };
});

import PredictiveGuide from '@/pages/PredictiveGuide';
import Help from '@/pages/Help';
import { useLanguage } from '@/contexts/LanguageContext';
import { CIE_LINKS, NOTE_EXAMPLES, PROGRESS_ITEMS, GUIDE_STEPS } from '@/lib/icfGuideContent';

const setLang = (language: 'es' | 'en') =>
  (useLanguage as ReturnType<typeof vi.fn>).mockReturnValue({ language, t: (k: string) => k });

const renderAt = (ui: React.ReactElement, url = '/') => render(<MemoryRouter initialEntries={[url]}>{ui}</MemoryRouter>);

beforeEach(() => {
  vi.clearAllMocks();
  setLang('es');
});

describe('contenido bilingüe', () => {
  it('tiene la misma cantidad de elementos en español e inglés', () => {
    expect(NOTE_EXAMPLES.es.length).toBe(NOTE_EXAMPLES.en.length);
    expect(GUIDE_STEPS.es.length).toBe(GUIDE_STEPS.en.length);
    expect(PROGRESS_ITEMS.es.length).toBe(PROGRESS_ITEMS.en.length);
  });

  it('los enlaces a la CIE son https', () => {
    CIE_LINKS.forEach((l) => expect(l.url.startsWith('https://')).toBe(true));
  });

  it('los ejemplos de notas no traen datos identificables', () => {
    NOTE_EXAMPLES.es.forEach((e) => expect(`${e.diag} ${e.note}`).not.toMatch(/\d{6,}|@/));
  });
});

describe('Guía Predictiva', () => {
  it('muestra por defecto los niveles de barrera y permite pasar al Perfil Funcional ICF', async () => {
    const user = userEvent.setup();
    renderAt(<PredictiveGuide />);
    expect(screen.getByText(/Perfil 0: Percepción de Barreras Bajas/)).toBeInTheDocument();
    expect(screen.queryByTestId('icf-guide')).not.toBeInTheDocument();
    await user.click(screen.getByRole('tab', { name: 'Perfil Funcional ICF' }));
    expect(await screen.findByTestId('icf-guide')).toBeInTheDocument();
    expect(screen.getByText('Cómo se usa, paso a paso')).toBeInTheDocument();
  });

  it('abre la sección ICF con ?section=icf', () => {
    renderAt(<PredictiveGuide />, '/predictive-guide?section=icf');
    expect(screen.getByTestId('icf-guide')).toBeInTheDocument();
    expect(screen.getByText('Límites que debe conocer')).toBeInTheDocument();
  });

  it('también está en inglés', () => {
    setLang('en');
    renderAt(<PredictiveGuide />, '/predictive-guide?section=icf');
    expect(screen.getByText('How to use it, step by step')).toBeInTheDocument();
  });
});

describe('Ayuda', () => {
  it('muestra el avance del Perfil Funcional ICF con hechos y pendientes', () => {
    renderAt(<Help />);
    const progress = screen.getByTestId('icf-progress');
    expect(within(progress).getAllByLabelText('Hecho').length).toBeGreaterThan(0);
    expect(within(progress).getAllByLabelText('Pendiente').length).toBeGreaterThan(0);
    expect(screen.getByRole('link', { name: 'Abrir el Perfil Funcional ICF' })).toHaveAttribute('href', '/functional-profile');
  });
});
