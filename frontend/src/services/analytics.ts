import { ApiService } from './api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://hab-backend-dev.onrender.com';

export interface CountEntry {
  key: string;
  count: number;
}

export interface DomainMean {
  domain: string;
  name: string;
  mean: number | null;
  n: number;
}

export interface ComponentStats {
  total: number;
  aceptado: number;
  editado: number;
  rechazado: number;
  sugerido: number;
  acceptance_rate: number | null;
}

export interface TopCode {
  code: string;
  title: string;
  component: 'b' | 's' | 'd';
  count: number;
  accepted: number;
  rejected: number;
}

export interface IcfSummary {
  patients_with_profile: number;
  suggestions: number;
  by_status: { sugerido: number; aceptado: number; editado: number; rechazado: number };
  decided: number;
  acceptance_rate: number | null;
  by_component: Record<'b' | 's' | 'd', ComponentStats>;
  by_origin: CountEntry[];
  by_model: CountEntry[];
  top_codes: TopCode[];
}

export interface AnalyticsSummary {
  generated_at: string;
  scope: 'global' | 'propio';
  filters: Record<string, string | number>;
  totals: {
    patients: number;
    with_prediction: number;
    prediction_rate: number | null;
    mean_age: number | null;
    mean_global_level: number | null;
    with_icf_profile: number;
  };
  distributions: {
    profile: CountEntry[];
    cat_fisica: CountEntry[];
    cat_psicosocial: CountEntry[];
    genero: CountEntry[];
    age_group: CountEntry[];
    cause: CountEntry[];
  };
  domains: DomainMean[];
  icf: IcfSummary;
}

export interface AnalyticsFilterOptions {
  genero: string[];
  cause: string[];
  profile: number[];
}

/** Filtros del dashboard; un valor vacío o indefinido no se envía. */
export interface AnalyticsFilters {
  genero?: string;
  causa?: string;
  perfil?: string;
  edad_min?: string;
  edad_max?: string;
  owner_id?: string;
}

class AnalyticsService {
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
    if (response.status === 403) throw new Error('No tiene permisos para ver estas estadísticas.');
    const detail = body.detail;
    if (response.status === 422) {
      throw new Error(typeof detail === 'string' ? detail : detail?.[0]?.msg || 'Filtros inválidos.');
    }
    throw new Error(typeof detail === 'string' ? detail : `Error del servidor (${response.status}). Intente de nuevo.`);
  }

  async getSummary(filters: AnalyticsFilters = {}): Promise<AnalyticsSummary> {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && String(value).trim() !== '') params.append(key, String(value).trim());
    });
    const query = params.toString();
    const response = await fetch(`${API_BASE_URL}/analytics/summary${query ? `?${query}` : ''}`, {
      headers: this.headers(),
    });
    return this.handle<AnalyticsSummary>(response);
  }

  async getFilterOptions(): Promise<AnalyticsFilterOptions> {
    const response = await fetch(`${API_BASE_URL}/analytics/filters`, { headers: this.headers() });
    return this.handle<AnalyticsFilterOptions>(response);
  }
}

export const analyticsService = new AnalyticsService();
