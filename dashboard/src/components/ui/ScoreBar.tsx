/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { cn, formatNumber } from '../../lib/utils';

interface ScoreBarProps {
  label: string;
  value: number; // 0.0 - 1.0
  showValue?: boolean;
  className?: string;
}

export function ScoreBar({ label, value, showValue = true, className }: ScoreBarProps) {
  const filledCount = Math.round(value * 10);
  const emptyCount = 10 - filledCount;

  const barColor = value > 0.75 ? 'text-profit' : value > 0.5 ? 'text-yellow' : 'text-loss';

  return (
    <div className={cn("flex items-center gap-4 font-mono text-[11px]", className)}>
      <span className="w-10 text-muted uppercase tracking-wider">{label}</span>
      <div className={cn("flex gap-0.5", barColor)}>
        {Array.from({ length: filledCount }).map((_, i) => (
          <span key={`f-${i}`}>█</span>
        ))}
        {Array.from({ length: emptyCount }).map((_, i) => (
          <span key={`e-${i}`} className="text-border-accent">░</span>
        ))}
      </div>
      {showValue && (
        <span className="ml-auto tabular-nums">{formatNumber(value)}</span>
      )}
    </div>
  );
}
