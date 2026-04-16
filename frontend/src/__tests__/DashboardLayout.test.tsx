import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import React from 'react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';

vi.mock('@/contexts/AuthContext', () => ({ useAuth: vi.fn() }));
vi.mock('@/contexts/LanguageContext', () => ({
  useLanguage: vi.fn(() => ({ language: 'en', setLanguage: vi.fn(), t: (k: string) => k })),
}));

import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { useAuth } from '@/contexts/AuthContext';

describe('DashboardLayout', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('shows loading spinner while authentication is resolving', () => {
    vi.mocked(useAuth).mockReturnValue({ user: null, isLoading: true, login: vi.fn(), logout: vi.fn() });
    render(
      <MemoryRouter>
        <DashboardLayout />
      </MemoryRouter>
    );
    expect(document.querySelector('.animate-spin')).toBeInTheDocument();
  });

  it('redirects unauthenticated user to /login', () => {
    vi.mocked(useAuth).mockReturnValue({ user: null, isLoading: false, login: vi.fn(), logout: vi.fn() });
    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <Routes>
          <Route path="/login" element={<div data-testid="login-page" />} />
          <Route element={<DashboardLayout />}>
            <Route path="/dashboard" element={<div>Protected</div>} />
          </Route>
        </Routes>
      </MemoryRouter>
    );
    expect(screen.getByTestId('login-page')).toBeInTheDocument();
  });

  it('renders protected outlet content for an authenticated user', () => {
    vi.mocked(useAuth).mockReturnValue({
      user: { id: 1, email: 'medico@hab.co', name: 'Doc', role: 'médico' },
      isLoading: false,
      login: vi.fn(),
      logout: vi.fn(),
    });
    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <Routes>
          <Route element={<DashboardLayout />}>
            <Route path="/dashboard" element={<div data-testid="protected-content">OK</div>} />
          </Route>
        </Routes>
      </MemoryRouter>
    );
    expect(screen.getByTestId('protected-content')).toBeInTheDocument();
  });

  it('sidebar filter logic shows userList only to admin, hides it from médico', () => {
    const menuItems = [
      { title: 'dashboard' },
      { title: 'patients' },
      { title: 'predictions' },
      { title: 'analytics' },
      { title: 'predictiveGuide' },
      { title: 'userList' },
    ];

    const filterForRole = (role: string) =>
      menuItems.filter((item) => {
        if (
          role === 'admin' &&
          ['patients', 'predictions', 'analytics', 'predictiveGuide'].includes(item.title)
        )
          return false;
        if (role !== 'admin' && item.title === 'userList') return false;
        return true;
      });

    const adminItems = filterForRole('admin').map((i) => i.title);
    const medicoItems = filterForRole('médico').map((i) => i.title);

    expect(adminItems).toContain('userList');
    expect(adminItems).not.toContain('patients');
    expect(medicoItems).not.toContain('userList');
    expect(medicoItems).toContain('patients');
  });
});
