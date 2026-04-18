import { renderHook, act, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { AuthProvider, useAuth } from '@/contexts/AuthContext';

vi.mock('@/services/api', () => ({
  apiService: {
    login: vi.fn(),
    getCurrentUser: vi.fn(),
    setToken: vi.fn(),
    clearToken: vi.fn(),
  },
}));

import { apiService } from '@/services/api';

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <MemoryRouter>
    <AuthProvider>{children}</AuthProvider>
  </MemoryRouter>
);

describe('AuthContext', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
  });

  it('returns null user when not logged in', async () => {
    const { result } = renderHook(() => useAuth(), { wrapper });
    await waitFor(() => expect(result.current.isLoading).toBe(false));
    expect(result.current.user).toBeNull();
  });

  it('login stores user in state and localStorage', async () => {
    vi.mocked(apiService.login).mockResolvedValue({
      access_token: 'test-token',
      token_type: 'bearer',
    });
    vi.mocked(apiService.getCurrentUser).mockResolvedValue({
      id: 1,
      email: 'admin@hab.co',
      full_name: 'Admin HAB',
      role: 'admin',
      is_active: true,
    });

    const { result } = renderHook(() => useAuth(), { wrapper });
    await waitFor(() => expect(result.current.isLoading).toBe(false));

    await act(async () => {
      await result.current.login('admin@hab.co', 'adminpassword');
    });

    expect(result.current.user).not.toBeNull();
    expect(result.current.user?.email).toBe('admin@hab.co');
    expect(localStorage.getItem('user')).not.toBeNull();
  });

  it('logout clears user state and removes localStorage entries', async () => {
    const storedUser = { id: 1, email: 'medico@hab.co', name: 'Medico', role: 'médico' };
    localStorage.setItem('authToken', 'tok-abc');
    localStorage.setItem('user', JSON.stringify(storedUser));

    const { result } = renderHook(() => useAuth(), { wrapper });
    await waitFor(() => expect(result.current.isLoading).toBe(false));
    expect(result.current.user?.email).toBe('medico@hab.co');

    act(() => {
      result.current.logout();
    });

    expect(result.current.user).toBeNull();
    expect(localStorage.getItem('authToken')).toBeNull();
    expect(localStorage.getItem('user')).toBeNull();
  });

  it('invalid credentials do not update user state', async () => {
    vi.mocked(apiService.login).mockRejectedValue(new Error('Unauthorized'));

    const { result } = renderHook(() => useAuth(), { wrapper });
    await waitFor(() => expect(result.current.isLoading).toBe(false));

    await expect(
      act(async () => {
        await result.current.login('bad@email.com', 'wrongpassword');
      })
    ).rejects.toThrow();

    expect(result.current.user).toBeNull();
  });
});
