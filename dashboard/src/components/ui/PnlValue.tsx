/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { cn, formatCurrency } from '../../lib/utils';

interface PnlValueProps {
  value: number;
  className?: string;
  showSign?: boolean;
}

export function PnlValue({ value, className, showSign = true }: PnlValueProps) {
  const isPositive = value >= 0;
  
  return (
    <span className={cn(
      "font-mono tabular-nums",
      isPositive ? "text-profit" : "text-loss",
      className
    )}>
      {isPositive && showSign ? '+' : ''}{formatCurrency(value)}
    </span>
  );
}
