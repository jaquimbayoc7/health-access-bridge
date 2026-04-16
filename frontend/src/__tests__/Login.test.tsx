import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';

vi.mock('@/contexts/AuthContext', () => ({ useAuth: vi.fn() }));
vi.mock('@/contexts/LanguageContext', () => ({ useLanguage: vi.fn() }));
vi.mock('sonner', () => ({ toast: { success: vi.fn(), error: vi.fn() } }));

import Login from '@/pages/Login';
import { useAuth } from '@/contexts/AuthContext';
import { useLanguage } from '@/contexts/LanguageContext';

const renderLogin = () =>
  render(
    <MemoryRouter>
      <Login />
    </MemoryRouter>
  );

describe('Login page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(useAuth).mockReturnValue({
      user: null,
      login: vi.fn(),
      logout: vi.fn(),
      isLoading: false,
    });
    vi.mocked(useLanguage).mockReturnValue({
      language: 'en',
      setLanguage: vi.fn(),
      t: (key: string) => key,
    });
  });

  it('renders email and password input fields', () => {
    renderLogin();
    expect(document.getElementById('email')).toBeInTheDocument();
    expect(document.getElementById('password')).toBeInTheDocument();
  });

  it('submit button is disabled while login request is in flight', async () => {
    vi.mocked(useAuth).mockReturnValue({
      user: null,
      login: vi.fn(() => new Promise(() => {})) as any,
      logout: vi.fn(),
      isLoading: false,
    });
    renderLogin();
    await userEvent.type(document.getElementById('email')!, 'user@test.com');
    await userEvent.type(document.getElementById('password')!, 'password123');
    await userEvent.click(screen.getByRole('button', { name: /login/i }));
    await waitFor(() => expect(screen.getByRole('button', { name: /loading/i })).toBeDisabled());
  });

  it('does not render the login form when user is already authenticated', () => {
    vi.mocked(useAuth).mockReturnValue({
      user: { id: 1, email: 'doc@hab.co', name: 'Doc', role: 'médico' },
      login: vi.fn(),
      logout: vi.fn(),
      isLoading: false,
    });
    renderLogin();
    expect(document.querySelector('form')).not.toBeInTheDocument();
  });

  it('language toggle button is rendered in the header area', () => {
    renderLogin();
    const buttons = screen.getAllByRole('button');
    expect(buttons.length).toBeGreaterThanOrEqual(2);
  });
});
