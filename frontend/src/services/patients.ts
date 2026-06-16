import { ApiService } from './api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://hab-backend-dev.onrender.com';

export interface Patient {
  id: number;
  nombre_apellidos: string;
  numero_documento: string;
  fecha_nacimiento: string;
  edad: number;
  genero: string;
  orientacion_sexual: string;
  causa_deficiencia: string;
  cat_fisica: string;
  cat_psicosocial: string;
  nivel_d1: number;
  nivel_d2: number;
  nivel_d3: number;
  nivel_d4: number;
  nivel_d5: number;
  nivel_d6: number;
  nivel_global: number;
  owner_id: number;
  prediction_profile: number | null;
  prediction_description: string | null;
}

export interface PatientCreate {
  nombre_apellidos: string;
  numero_documento: string;
  fecha_nacimiento: string;
  edad: number;
  genero: string;
  orientacion_sexual: string;
  causa_deficiencia: string;
  cat_fisica: string;
  cat_psicosocial: string;
  nivel_d1: number;
  nivel_d2: number;
  nivel_d3: number;
  nivel_d4: number;
  nivel_d5: number;
  nivel_d6: number;
  nivel_global: number;
}

export interface PredictionResult {
  profile: number;
  description: string;
}

class PatientService {
  private getToken(): string {
    const token = localStorage.getItem('authToken');
    if (!token) throw new Error('No hay token de autenticación');
    return token;
  }

  private getHeaders(): HeadersInit {
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.getToken()}`,
    };
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

  async getPatients(skip: number = 0, limit: number = 100, search: string = ''): Promise<Patient[]> {
    const params = new URLSearchParams({ skip: String(skip), limit: String(limit) });
    if (search.trim()) params.append('search', search.trim());
    const response = await fetch(`${API_BASE_URL}/patients/?${params.toString()}`, {
      headers: this.getHeaders(),
    });

    return this.handleResponse<Patient[]>(response);
  }

  async getPatient(patientId: number): Promise<Patient> {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}`, {
      headers: this.getHeaders(),
    });
    return this.handleResponse<Patient>(response);
  }

  async createPatient(patient: PatientCreate): Promise<Patient> {
    const response = await fetch(`${API_BASE_URL}/patients/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(patient),
    });
    return this.handleResponse<Patient>(response);
  }

  async updatePatient(patientId: number, patient: PatientCreate): Promise<Patient> {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(patient),
    });
    return this.handleResponse<Patient>(response);
  }

  async deletePatient(patientId: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    });
    if (!response.ok) return this.handleResponse<void>(response);
  }

  async predictPatient(patientId: number): Promise<PredictionResult> {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}/predict`, {
      method: 'POST',
      headers: this.getHeaders(),
    });
    return this.handleResponse<PredictionResult>(response);
  }
}

export const patientService = new PatientService();
