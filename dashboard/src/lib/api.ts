/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { PortfolioState, Trade, LedgerEntry, AgentStatus, EvalEntry } from './types';

const API_BASE = (import.meta as any).env?.VITE_API_URL || "http://localhost:8000";

async function request<T>(endpoint: string, token: string | null, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }
  headers.set('Content-Type', 'application/json');

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    // This will be caught by the calling component to clear token
    throw new Error('UNAUTHORIZED');
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || `API Error: ${response.status}`);
  }

  return response.json();
}

export const api = {
  login: async (apiKey: string): Promise<{ token: string; expires_in: number }> => {
    return request('/auth/login', null, {
      method: 'POST',
      body: JSON.stringify({ api_key: apiKey }),
    });
  },

  getPortfolio: async (token: string): Promise<PortfolioState> => {
    return request('/api/portfolio', token);
  },

  getTrades: async (token: string, limit?: number): Promise<Trade[]> => {
    const query = limit ? `?limit=${limit}` : '';
    return request(`/api/trades${query}`, token);
  },

  getOps: async (token: string): Promise<{ balance: number; ledger: LedgerEntry[] }> => {
    return request('/api/ops', token);
  },

  getAgents: async (token: string): Promise<Record<string, AgentStatus>> => {
    return request('/api/agents', token);
  },

  getEval: async (token: string): Promise<EvalEntry[]> => {
    return request('/api/eval', token);
  },
  
  stopEngine: async (token: string): Promise<void> => {
    return request('/api/stop', token, { method: 'POST' });
  }
};
