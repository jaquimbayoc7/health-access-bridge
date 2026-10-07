import { ApiService } from './api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://hab-backend-dev.onrender.com';

export type IcfStatus = 'sugerido' | 'aceptado' | 'editado' | 'rechazado';
export type IcfOrigin = 'llm' | 'similarity' | 'rules' | string;

export interface IcfItem {
  id: number;
  component: 'b' | 's' | 'd';
  code: string;
  title: string;
  qualifier: number | null;
  qualifier_cn: number | null;
  qualifier_cl: number | null;
  justification: string | null;
  origin: IcfOrigin;
  status: IcfStatus;
  original_code: string | null;
}

export interface IcfSuggestionSet {
  patient_id: number;
  batch_id: string | null;
  model: string | null;
  llm_used: boolean;
  created_at: string | null;
  latency_ms: number | null;
  warnings: string[];
  functions: IcfItem[];
  structures: IcfItem[];
  activities: IcfItem[];
}

export interface IcfGenerateRequest {
  diag_cie?: string;
  clinical_notes?: string;
}

export interface IcfDecision {
  status: Exclude<IcfStatus, 'sugerido'>;
  qualifier?: number;
  qualifier_cn?: number;
  qualifier_cl?: number;
}

// La sugerencia puede tardar (hasta ~15 s solo con CPU); el backend espera hasta 90 s.
class IcfServiceClient {
  private headers(): HeadersInit {
    const token = localStorage.getItem('authToken');
    if (!token) throw new Error('No hay token de autenticación');
    return { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` };
  }

  private async handle<T>(response: Response): Promise<T> {
    if (response.ok) return response.json();
    const body = await response.json().catch(() => ({}));
    if (response.status === 401) {
      ApiService.onUnauthorized?.();
      throw new Error('Sesión expirada. Por favor, inicie sesión nuevamente.');
    }
    if (response.status === 403) throw new Error('No tiene permisos para realizar esta acción.');
    const detail = body.detail;
    if (typeof detail === 'string') throw new Error(detail);
    if (Array.isArray(detail) && detail[0]?.msg) throw new Error(detail[0].msg);
    throw new Error(`Error del servidor (${response.status}). Intente de nuevo.`);
  }

  async generate(patientId: number, request: IcfGenerateRequest): Promise<IcfSuggestionSet> {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}/icf-suggestions`, {
      method: 'POST',
      headers: this.headers(),
      body: JSON.stringify(request),
    });
    return this.handle<IcfSuggestionSet>(response);
  }

  async getLatest(patientId: number): Promise<IcfSuggestionSet> {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}/icf-suggestions`, {
      headers: this.headers(),
    });
    return this.handle<IcfSuggestionSet>(response);
  }

  async decide(itemId: number, decision: IcfDecision): Promise<IcfItem> {
    const response = await fetch(`${API_BASE_URL}/icf/suggestions/${itemId}`, {
      method: 'PATCH',
      headers: this.headers(),
      body: JSON.stringify(decision),
    });
    return this.handle<IcfItem>(response);
  }
}

export const icfService = new IcfServiceClient();
