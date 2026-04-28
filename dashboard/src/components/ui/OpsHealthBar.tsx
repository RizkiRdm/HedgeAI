/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { cn, formatCurrency } from '../../lib/utils';

interface OpsHealthBarProps {
  balance: number;
  target: number;
  burnRate: number; // Monthly
  className?: string;
}

export function OpsHealthBar({ balance, target, burnRate, className }: OpsHealthBarProps) {
  const percentage = Math.min((balance / target) * 100, 100);
  const runwayMonths = burnRate > 0 ? (balance / burnRate).toFixed(1) : '∞';
  
  const healthColor = percentage > 80 ? 'bg-profit' : percentage > 40 ? 'bg-warn' : 'bg-loss';

  return (
    <div className={cn("space-y-2", className)}>
      <div className="flex justify-between items-end">
        <span className="text-[10px] font-mono text-muted uppercase">Ops Health</span>
        <span className="text-[10px] font-mono text-white tracking-widest">{runwayMonths}M RUNWAY</span>
      </div>
      <div className="h-1.5 w-full bg-border-accent">
        <div 
          className={cn("h-full transition-all duration-500", healthColor)}
          style={{ width: `${percentage}%` }}
        />
      </div>
      <div className="flex justify-between text-[9px] font-mono text-muted uppercase">
        <span>{formatCurrency(balance)}</span>
        <span>Target: {formatCurrency(target)}</span>
      </div>
    </div>
  );
}
