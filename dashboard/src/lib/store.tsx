/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { useWebSocket } from '../components/useWebSocket';
import { useAuth } from './auth';
import { WSEvent, Position, PortfolioState } from './types';

interface Alert {
  id: string;
  level: "info" | "warning" | "critical" | "emergency";
  message: string;
}

interface GlobalStateContextType {
  connected: boolean;
  portfolio: PortfolioState | null;
  lastEvents: any[];
  alerts: Alert[];
  removeAlert: (id: string) => void;
  lastSignal: { ticker: string; fas_score: number; ms: number; rar: number; ochs: number; ns: number } | null;
  addEvent: (event: any) => void;
}

const GlobalStateContext = createContext<GlobalStateContextType | undefined>(undefined);

export function GlobalStateProvider({ children }: { children: ReactNode }) {
  const { token } = useAuth();
  
  const [portfolio, setPortfolio] = useState<PortfolioState | null>(null);
  const [lastEvents, setLastEvents] = useState<any[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [lastSignal, setLastSignal] = useState<any>(null);

  const { connected, lastEvent } = useWebSocket({
    url: import.meta.env.VITE_WS_URL || "ws://localhost:8000/ws/live",
    token
  });

  const removeAlert = (id: string) => {
    setAlerts(prev => prev.filter(a => a.id !== id));
  };
  
  const addEvent = (event: any) => {
     setLastEvents(prev => [...prev.slice(-199), event]);
  }

  useEffect(() => {
    if (!lastEvent) return;

    if (lastEvent.type === 'agent_activity') {
      setLastEvents(prev => [...prev.slice(-199), {
        id: Date.now().toString() + Math.random(),
        timestamp: new Date().toISOString(),
        agent: lastEvent.data.agent,
        message: lastEvent.data.message
      }]);
    } else if (lastEvent.type === 'portfolio_update') {
      setPortfolio(lastEvent.data);
    } else if (lastEvent.type === 'fas_signal') {
      setLastSignal(lastEvent.data);
    } else if (lastEvent.type === 'alert') {
      const newAlert = { id: Date.now().toString(), ...lastEvent.data };
      setAlerts(prev => [...prev, newAlert]);
      
      if (lastEvent.data.level === 'warning') {
        setTimeout(() => removeAlert(newAlert.id), 5000);
      } else if (lastEvent.data.level === 'emergency') {
        // Flash red for 2s (handled in UI via alerts map)
        document.body.classList.add('bg-loss');
        setTimeout(() => document.body.classList.remove('bg-loss'), 2000);
      }
    }
  }, [lastEvent]);

  return (
    <GlobalStateContext.Provider value={{ connected, portfolio, lastEvents, alerts, removeAlert, lastSignal, addEvent }}>
      {children}
    </GlobalStateContext.Provider>
  );
}

export function useGlobalState() {
  const context = useContext(GlobalStateContext);
  if (context === undefined) {
    throw new Error('useGlobalState must be used within a GlobalStateProvider');
  }
  return context;
}
