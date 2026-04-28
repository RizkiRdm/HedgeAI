/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  Activity, 
  BarChart3, 
  Users, 
  Briefcase, 
  History, 
  Settings, 
  PieChart,
  Hexagon
} from 'lucide-react';
import { cn } from '../../lib/utils';
import { OpsHealthBar } from '../ui/OpsHealthBar';

const navItems = [
  { path: '/', label: 'Live Feed', icon: Activity },
  { path: '/portfolio', label: 'Portfolio', icon: PieChart },
  { path: '/analytics', label: 'Analytics', icon: BarChart3 },
  { path: '/agents', label: 'Agents', icon: Users },
  { path: '/ops', label: 'Ops & Finance', icon: Briefcase },
  { path: '/eval', label: 'Eval History', icon: History },
  { path: '/config', label: 'Config', icon: Settings },
];

export function Sidebar() {
  return (
    <aside className="w-60 h-screen fixed left-0 top-0 border-r border-border bg-bg flex flex-col shrink-0">
      <div className="p-6 flex items-center gap-3">
        <Hexagon className="w-6 h-6 text-white" />
        <span className="font-mono font-bold tracking-tighter text-lg uppercase">CryptoHedgeAI</span>
      </div>

      <nav className="flex-1 px-3 space-y-1 mt-4">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => cn(
              "flex items-center gap-3 px-3 py-2 text-xs font-mono uppercase tracking-widest transition-all",
              isActive 
                ? "bg-white text-black font-bold" 
                : "text-muted hover:border-border-accent border border-transparent"
            )}
          >
            <item.icon className="w-4 h-4" strokeWidth={1.5} />
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-border">
        <OpsHealthBar 
          balance={8.14} 
          target={25.00} 
          burnRate={2.50} 
        />
      </div>
    </aside>
  );
}
