/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { cn } from '../../lib/utils';

interface AgentTagProps {
  agent: string;
  className?: string;
}

export function AgentTag({ agent, className }: AgentTagProps) {
  const normalizedAgent = agent.toUpperCase();
  
  const colors: Record<string, string> = {
    'OVERSEER': 'text-muted',
    'ORACLE': 'text-cyan',
    'QUANT': 'text-yellow',
    'RISK ✓': 'text-profit',
    'RISK ✗': 'text-loss font-bold',
    'RISK': 'text-profit',
    'TRADER': 'text-white font-bold',
    'ACCOUNTANT': 'text-accent',
    'EVAL': 'text-magenta',
    'SYSTEM': 'text-muted italic',
  };

  const colorClass = colors[normalizedAgent] || colors['SYSTEM'];

  return (
    <span className={cn(
      "font-mono text-[10px] tracking-wider uppercase",
      colorClass,
      className
    )}>
      [{normalizedAgent}]
    </span>
  );
}
