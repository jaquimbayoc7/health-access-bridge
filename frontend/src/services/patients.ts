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

  async getPatients(skip: number = 0, limit: number = 100, search: string = ''): Promise<Patient[]> {
    const params = new URLSearchParams({ skip: String(skip), limit: String(limit) });
    if (search.trim()) params.append('search', search.trim());
    const response = await fetch(`${API_BASE_URL}/patients/?${params.toString()}`, {
      headers: this.getHeaders(),
    });

    if (response.status === 401) {
      localStorage.removeItem('authToken');
      localStorage.removeItem('userRole');
      window.location.href = '/login';
      throw new Error('Sesión expirada. Por favor, inicia sesión nuevamente.');
    }

    if (!response.ok) {
      throw new Error('Error al obtener pacientes');
    }

    return response.json();
  }

  async getPatient(patientId: number): Promise<Patient> {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}`, {
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      throw new Error('Error al obtener paciente');
    }

    return response.json();
  }

  async createPatient(patient: PatientCreate): Promise<Patient> {
    const response = await fetch(`${API_BASE_URL}/patients/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(patient),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Error al crear paciente' }));
      throw new Error(error.detail || 'Error al crear paciente');
    }

    return response.json();
  }

  async updatePatient(patientId: number, patient: PatientCreate): Promise<Patient> {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(patient),
    });

    if (response.status === 401) {
      localStorage.removeItem('authToken');
      localStorage.removeItem('userRole');
      window.location.href = '/login';
      throw new Error('Sesión expirada. Por favor, inicia sesión nuevamente.');
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Error al actualizar paciente' }));
      throw new Error(error.detail || 'Error al actualizar paciente');
    }

    return response.json();
  }

  async deletePatient(patientId: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    });

    if (response.status === 401) {
      localStorage.removeItem('authToken');
      localStorage.removeItem('userRole');
      window.location.href = '/login';
      throw new Error('Sesión expirada. Por favor, inicia sesión nuevamente.');
    }

    if (!response.ok) {
      throw new Error('Error al eliminar paciente');
    }
  }

  async predictPatient(patientId: number): Promise<PredictionResult> {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}/predict`, {
      method: 'POST',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Error en la predicción' }));
      throw new Error(error.detail || 'Error al realizar predicción');
    }

    return response.json();
  }
}

export const patientService = new PatientService();
