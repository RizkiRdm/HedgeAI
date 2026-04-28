/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './lib/auth';
import { GlobalStateProvider, useGlobalState } from './lib/store';
import { AppShell } from './components/layout/AppShell';
import { LoginModal } from './components/auth/LoginModal';
import { LiveFeedPage } from './pages/LiveFeedPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { AgentsPage } from './pages/AgentsPage';
import { OpsPage } from './pages/OpsPage';
import { EvalPage } from './pages/EvalPage';
import { ConfigPage } from './pages/ConfigPage';
import { Loader2 } from 'lucide-react';
import { cn } from './lib/utils';

function GlobalAlerts() {
  const { connected, alerts, removeAlert } = useGlobalState();
  
  return (
    <>
      {!connected && (
        <div className="fixed top-14 left-60 right-0 z-50 bg-warn text-black px-4 py-2 flex items-center justify-center gap-2 font-mono text-[11px] uppercase tracking-widest font-bold">
          <Loader2 className="w-3 h-3 animate-spin" />
          Reconnecting to engine...
        </div>
      )}
      
      <div className="fixed bottom-6 right-6 z-50 flex flex-col gap-2 pointer-events-none">
        {alerts.map(alert => (
          <div 
            key={alert.id}
            onClick={() => removeAlert(alert.id)}
            className={cn(
              "pointer-events-auto p-4 border max-w-sm font-mono text-[11px] uppercase tracking-wider backdrop-blur-md cursor-pointer",
              alert.level === 'warning' ? "bg-warn/10 border-warn text-warn" :
              alert.level === 'critical' ? "bg-loss/10 border-loss text-loss" :
              alert.level === 'emergency' ? "bg-loss border-loss text-white font-bold" :
              "bg-bg-secondary border-border text-white"
            )}
          >
            {alert.message}
          </div>
        ))}
      </div>
    </>
  );
}

function AppContent() {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <LoginModal />;
  }

  return (
    <GlobalStateProvider>
      <AppShell>
        <GlobalAlerts />
        <Routes>
          <Route path="/" element={<LiveFeedPage />} />
          <Route path="/portfolio" element={<Navigate to="/" replace />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/agents" element={<AgentsPage />} />
          <Route path="/ops" element={<OpsPage />} />
          <Route path="/eval" element={<EvalPage />} />
          <Route path="/config" element={<ConfigPage />} />
        </Routes>
      </AppShell>
    </GlobalStateProvider>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </AuthProvider>
  );
}

