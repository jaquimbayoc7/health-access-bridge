const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://hab-backend-dev.onrender.com';

export interface LoginCredentials {
  username: string; // FastAPI OAuth2 uses 'username' field for email
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
  role: 'admin' | 'médico';
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  role: 'admin' | 'médico';
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export class ApiService {
  private token: string | null = null;
  static onUnauthorized: (() => void) | null = null;

  constructor() {
    // Inicializar el token desde localStorage al crear la instancia
    const storedToken = localStorage.getItem('authToken');
    if (storedToken) {
      this.token = storedToken;
    }
  }

  setToken(token: string) {
    this.token = token;
    localStorage.setItem('authToken', token);
  }

  clearToken() {
    this.token = null;
    localStorage.removeItem('authToken');
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (response.ok) return response.json();
    const body = await response.json().catch(() => ({}));
    switch (response.status) {
      case 401:
        ApiService.onUnauthorized?.();
        throw new Error('Sesión expirada. Por favor, inicie sesión nuevamente.');
      case 403:
        throw new Error('No tiene permisos para realizar esta acción.');
      case 404:
        throw new Error('El recurso solicitado no fue encontrado.');
      case 422: {
        const detail = body.detail;
        const msg = Array.isArray(detail)
          ? detail[0]?.msg || 'Datos inválidos. Verifique la información ingresada.'
          : typeof detail === 'string'
          ? detail
          : 'Datos inválidos. Verifique la información ingresada.';
        throw new Error(msg);
      }
      case 500:
        throw new Error('Error temporal del servidor. Intente de nuevo en unos momentos.');
      default:
        throw new Error(body.detail || `Error del servidor (${response.status}). Intente de nuevo.`);
    }
  }

  private getHeaders(includeAuth: boolean = true): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };
    
    if (includeAuth && this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    
    return headers;
  }

  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await fetch(`${API_BASE_URL}/users/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Error de autenticación' }));
      throw new Error(error.detail || 'Error al iniciar sesión');
    }

    return response.json();
  }

  async registerDoctor(data: RegisterData): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/admin/users/register`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    });
    return this.handleResponse<User>(response);
  }

  async getUsers(skip: number = 0, limit: number = 100): Promise<User[]> {
    const response = await fetch(`${API_BASE_URL}/admin/users?skip=${skip}&limit=${limit}`, {
      headers: this.getHeaders(),
    });
    return this.handleResponse<User[]>(response);
  }

  async getCurrentUser(): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/users/me`, {
      headers: this.getHeaders(),
    });
    return this.handleResponse<User>(response);
  }

  async updateUserStatus(userId: number, isActive: boolean): Promise<User> {
    const url = `${API_BASE_URL}/admin/users/${userId}/status`;
    const token = this.token || localStorage.getItem('authToken');
    
    try {
      const response = await fetch(url, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ is_active: isActive }),
      });

      return this.handleResponse<User>(response);
    } catch (error) {
      throw error;
    }
  }
}

export const apiService = new ApiService();
