/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { ReactNode, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Topbar } from './Topbar';

interface AppShellProps {
  children: ReactNode;
}

export function AppShell({ children }: AppShellProps) {
  const navigate = useNavigate();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
      
      const routes: Record<string, string> = {
        '1': '/',
        '2': '/portfolio',
        '3': '/analytics',
        '4': '/agents',
        '5': '/ops',
        '6': '/eval',
        '7': '/config'
      };

      if (routes[e.key]) {
        navigate(routes[e.key]);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [navigate]);

  return (
    <div className="min-h-screen bg-bg text-text selection:bg-accent selection:text-white">
      <Sidebar />
      <div className="pl-60">
        <Topbar />
        <main className="pt-14 p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
