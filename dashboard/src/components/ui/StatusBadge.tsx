/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { cn } from '../../lib/utils';

type Status = 'live' | 'veto' | 'active' | 'paused' | 'error' | 'idle';

interface StatusBadgeProps {
  status: Status;
  className?: string;
}

export function StatusBadge({ status, className }: StatusBadgeProps) {
  const configs: Record<Status, { label: string; color: string; dot: string; pulse?: boolean }> = {
    live: { label: 'LIVE', color: 'border-profit text-profit', dot: 'bg-profit', pulse: true },
    active: { label: 'ACTIVE', color: 'border-profit text-profit', dot: 'bg-profit' },
    veto: { label: 'VETO', color: 'border-loss text-loss', dot: 'bg-loss' },
    paused: { label: 'PAUSED', color: 'border-warn text-warn', dot: 'bg-warn' },
    error: { label: 'ERROR', color: 'border-loss text-loss font-bold', dot: 'bg-loss' },
    idle: { label: 'IDLE', color: 'border-muted text-muted', dot: 'bg-muted' },
  };

  const config = configs[status] || configs.idle;

  return (
    <div className={cn(
      "inline-flex items-center gap-2 px-2 py-0.5 border text-[10px] tracking-widest font-mono rounded-none uppercase",
      config.color,
      className
    )}>
      <div className={cn(
        "w-1.5 h-1.5 rounded-full",
        config.dot,
        config.pulse && "animate-pulse-dot"
      )} />
      {config.label}
    </div>
  );
}
