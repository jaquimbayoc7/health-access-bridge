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

class ApiService {
  private token: string | null = null;

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

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Error en el registro' }));
      throw new Error(error.detail || 'Error al registrar usuario');
    }

    return response.json();
  }

  async getUsers(skip: number = 0, limit: number = 100): Promise<User[]> {
    const response = await fetch(`${API_BASE_URL}/admin/users?skip=${skip}&limit=${limit}`, {
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      throw new Error('Error al obtener usuarios');
    }

    return response.json();
  }

  async getCurrentUser(): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/users/me`, {
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      throw new Error('Error al obtener usuario actual');
    }

    return response.json();
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

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Error al actualizar estado' }));
        throw new Error(errorData.detail || 'Error al actualizar estado del usuario');
      }

      return response.json();
    } catch (error) {
      throw error;
    }
  }
}

export const apiService = new ApiService();
