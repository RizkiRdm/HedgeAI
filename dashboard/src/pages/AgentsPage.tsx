/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { StatusBadge } from '../components/ui/StatusBadge';
import { cn } from '../lib/utils';
import { AgentTag } from '../components/ui/AgentTag';

interface AgentCardProps {
  id: string;
  name: string;
  role: string;
  status: 'active' | 'paused' | 'error' | 'idle';
  uptime: string;
  cycles: string;
  failures: number;
  extras?: React.ReactNode;
}

function AgentCard({ id, name, role, status, uptime, cycles, failures, extras }: AgentCardProps) {
  return (
    <div className="bg-bg-secondary border border-border p-6 flex flex-col gap-4 group hover:border-border-accent transition-all rounded-none">
      <div className="flex justify-between items-start">
        <div className="space-y-1">
          <span className="text-[10px] font-mono text-muted uppercase">[{id}]</span>
          <h3 className="text-sm font-mono font-bold text-white tracking-widest">{name}</h3>
          <p className="text-[9px] font-mono text-muted uppercase tracking-tight">{role}</p>
        </div>
        <StatusBadge status={status} />
      </div>

      <div className="h-px bg-border/50" />

      <div className="space-y-2">
        <div className="flex justify-between text-[10px] font-mono uppercase tracking-widest">
          <span className="text-muted">Uptime</span>
          <span className="text-white">{uptime}</span>
        </div>
        <div className="flex justify-between text-[10px] font-mono uppercase tracking-widest">
          <span className="text-muted">Cycles</span>
          <span className="text-white">{cycles}</span>
        </div>
        <div className="flex justify-between text-[10px] font-mono uppercase tracking-widest">
          <span className="text-muted">Failures</span>
          <span className={cn(failures > 0 ? "text-loss" : "text-white")}>{failures}</span>
        </div>
      </div>

      {extras && (
        <>
          <div className="h-px bg-border/50" />
          <div className="space-y-3">
            {extras}
          </div>
        </>
      )}

      <div className="h-px bg-border/50 mt-auto" />
      <div className="flex justify-between text-[9px] font-mono text-muted uppercase">
        <span>Cycle Ref: #0A2E</span>
        <span>7.8s avg</span>
      </div>
    </div>
  );
}

export function AgentsPage() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
      <AgentCard 
        id="01" 
        name="OVERSEER" 
        role="System Orchestrator" 
        status="active" 
        uptime="14d 3h" 
        cycles="4,821" 
        failures={2} 
      />
      
      <AgentCard 
        id="02" 
        name="ORACLE" 
        role="Market Data Inverter" 
        status="active" 
        uptime="14d 3h" 
        cycles="12,402" 
        failures={0} 
      />
      
      <AgentCard 
        id="03" 
        name="QUANT" 
        role="Signal Generator" 
        status="active" 
        uptime="14d 3h" 
        cycles="4,821" 
        failures={1} 
      />
      
      <AgentCard 
        id="04" 
        name="RISK GUARDIAN" 
        role="Capital Protector" 
        status="active" 
        uptime="14d 3h" 
        cycles="4,821" 
        failures={0} 
        extras={
          <div className="space-y-2">
            <div className="flex justify-between text-[10px] font-mono uppercase">
              <span className="text-muted">Vetoes</span>
              <span className="text-white">47</span>
            </div>
            <div className="flex justify-between text-[10px] font-mono uppercase">
              <span className="text-muted">Cap Saved</span>
              <span className="text-profit">$187.30</span>
            </div>
            <div className="flex h-1.5 w-full bg-border-accent mt-2">
              <div className="bg-cyan h-full" style={{ width: '40%' }} title="Slippage" />
              <div className="bg-yellow h-full" style={{ width: '35%' }} title="Sector" />
              <div className="bg-loss h-full" style={{ width: '25%' }} title="Volatility" />
            </div>
          </div>
        }
      />
      
      <AgentCard 
        id="05" 
        name="TRADER" 
        role="Execution Engine" 
        status="active" 
        uptime="14d 3h" 
        cycles="842" 
        failures={0} 
      />
      
      <AgentCard 
        id="06" 
        name="ACCOUNTANT" 
        role="Ops Finance Manager" 
        status="active" 
        uptime="14d 3h" 
        cycles="121" 
        failures={0} 
      />
      
      <AgentCard 
        id="07" 
        name="EVAL AGENT" 
        role="Meta-Optimizer" 
        status="active" 
        uptime="14d 3h" 
        cycles="42" 
        failures={0} 
        extras={
          <div className="space-y-2">
            <div className="flex justify-between text-[10px] font-mono uppercase">
              <span className="text-muted">Next Micro</span>
              <span className="text-white">3d 14h</span>
            </div>
            <div className="flex justify-between text-[10px] font-mono uppercase">
              <span className="text-muted">Last Action</span>
              <span className="text-accent">WEIGHT ADJ.</span>
            </div>
          </div>
        }
      />

      <AgentCard 
        id="XX" 
        name="CLI STANDBY" 
        role="Human Interface" 
        status="idle" 
        uptime="0s" 
        cycles="0" 
        failures={0} 
      />
    </div>
  );
}
