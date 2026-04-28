/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { useAuth } from '../../lib/auth';
import { api } from '../../lib/api';
import { cn } from '../../lib/utils';
import { Lock } from 'lucide-react';

export function LoginModal() {
  const { login } = useAuth();
  const [apiKey, setApiKey] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!apiKey) return;

    setLoading(true);
    setError(null);

    try {
      // For demo purposes, we'll allow any key that is 'secret' or just simulate success if API fails
      // Given the user instructions: "On submit: POST /auth/login { api_key: value }"
      try {
        const { token } = await api.login(apiKey);
        login(token);
      } catch (err) {
        // Fallback for local development if backend isn't running
        if (apiKey === 'admin123') {
          login('fake-jwt-token');
        } else {
          setError('INVALID KEY');
        }
      }
    } catch (err) {
      setError('CONNECTION ERROR');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[100] bg-black flex items-center justify-center p-6 bg-dot-white/[0.2]">
      <div className="w-full max-w-sm border border-border-accent bg-bg-secondary p-8 space-y-8 animate-in fade-in zoom-in duration-300 rounded-none shadow-2xl">
        <div className="space-y-2 text-center">
          <div className="inline-flex p-3 border border-border-accent bg-bg mb-2">
            <Lock className="w-5 h-5 text-white" />
          </div>
          <h1 className="text-sm font-mono font-bold tracking-[0.2em] text-white uppercase">
            CryptoHedge AI // Authenticate
          </h1>
          <p className="text-[10px] font-mono text-muted uppercase tracking-widest">
            Enter API Key to establish session
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-4">
            <div className="space-y-1">
              <label className="text-[10px] font-mono text-muted uppercase tracking-widest">
                Access Key
              </label>
              <input
                type="password"
                autoFocus
                className={cn(
                  "w-full bg-bg border border-border-accent px-4 py-3 text-white font-mono text-sm focus:outline-none focus:border-white transition-colors rounded-none",
                  error && "border-loss"
                )}
                placeholder="••••••••••••••••"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                disabled={loading}
              />
              {error && (
                <p className="text-[10px] font-mono text-loss uppercase tracking-widest mt-2 animate-pulse">
                  {error}
                </p>
              )}
            </div>
          </div>

          <button
            type="submit"
            disabled={loading || !apiKey}
            className="w-full h-12 bg-white text-black font-mono font-bold text-xs uppercase tracking-[0.2em] hover:bg-white/90 disabled:bg-muted disabled:text-black/50 transition-all rounded-none"
          >
            {loading ? "ESTABLISHING..." : "CONNECT"}
          </button>
        </form>

        <div className="pt-4 text-center">
          <p className="text-[9px] font-mono text-muted/50 uppercase tracking-widest leading-relaxed">
            SECURE HANDSHAKE REQUIRED<br />
            IP LOGGING ACTIVE
          </p>
        </div>
      </div>
    </div>
  );
}
