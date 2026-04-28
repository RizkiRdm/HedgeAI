/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { cn } from '../../lib/utils';

interface DataCardProps {
  label: string;
  value: string | number;
  delta?: string | number;
  deltaType?: 'pct' | 'usd';
  sublabel?: string;
  className?: string;
}

export function DataCard({ label, value, delta, deltaType, sublabel, className }: DataCardProps) {
  const isPositive = typeof delta === 'number' ? delta >= 0 : typeof delta === 'string' ? !delta.startsWith('-') : true;
  
  const formattedDelta = delta !== undefined ? (
    <span className={cn(
      "text-[10px] font-mono",
      isPositive ? "text-profit" : "text-loss"
    )}>
      {isPositive ? '+' : ''}{delta}{deltaType === 'pct' ? '%' : ''}
    </span>
  ) : null;

  return (
    <div className={cn(
      "p-4 border border-border bg-bg-secondary flex flex-col gap-1 rounded-none",
      className
    )}>
      <span className="text-[10px] font-mono uppercase tracking-widest text-muted">{label}</span>
      <div className="flex items-baseline gap-2">
        <span className="text-2xl font-mono font-bold text-white tabular-nums">{value}</span>
      </div>
      {(delta !== undefined || sublabel) && (
        <div className="flex items-center gap-2 mt-1">
          {formattedDelta}
          {sublabel && <span className="text-[10px] font-mono text-muted uppercase">{sublabel}</span>}
        </div>
      )}
    </div>
  );
}
