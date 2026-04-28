/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { cn, formatCurrency } from '../../lib/utils';
import { StatusBadge } from '../ui/StatusBadge';
import { Circle } from 'lucide-react';

export function Topbar() {
  const [tick, setTick] = useState(4821);
  const [isEmergency, setIsEmergency] = useState(false);
  const [stopConfirm, setStopConfirm] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => {
      setTick(t => t + 1);
    }, 10000);
    return () => clearInterval(timer);
  }, []);

  const handleStopClick = () => {
    if (stopConfirm) {
      setIsEmergency(true);
      setStopConfirm(false);
      // Trigger API stop here
    } else {
      setStopConfirm(true);
      setTimeout(() => setStopConfirm(false), 3000);
    }
  };

  return (
    <header className={cn(
      "h-14 fixed top-0 right-0 left-60 border-b border-border flex items-center justify-between px-6 z-40 transition-colors duration-500",
      isEmergency ? "bg-loss/20 border-loss/50" : "bg-bg"
    )}>
      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2">
          <Circle className={cn("w-2 h-2 fill-current", isEmergency ? "text-loss" : "text-profit animate-pulse-dot")} />
          <span className="font-mono text-[10px] uppercase font-bold tracking-widest">
            CryptoHedgeAI
          </span>
        </div>
        <div className="h-4 w-px bg-border-accent" />
        <span className="font-mono text-[10px] text-muted uppercase">
          Tick #{tick}
        </span>
        <div className="h-4 w-px bg-border-accent" />
        <StatusBadge status={isEmergency ? "error" : "live"} />
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-1.5 px-3 py-1 border border-border-accent bg-bg-secondary font-mono text-[10px]">
          <span className="text-muted">CAPITAL:</span>
          <span className="text-white font-bold">{formatCurrency(312.40)}</span>
        </div>
        <div className="flex items-center gap-1.5 px-3 py-1 border border-border-accent bg-bg-secondary font-mono text-[10px]">
          <span className="text-muted">OPS:</span>
          <span className="text-white font-bold">{formatCurrency(8.14)}</span>
        </div>
        
        <button
          onClick={handleStopClick}
          className={cn(
            "px-3 py-1 border font-mono text-[10px] transition-all uppercase tracking-widest",
            isEmergency 
              ? "bg-loss text-white border-loss" 
              : stopConfirm
                ? "border-loss text-loss animate-pulse bg-loss/10"
                : "border-loss text-loss hover:bg-loss hover:text-white"
          )}
        >
          {isEmergency ? "STOPPED" : stopConfirm ? "CONFIRM STOP" : "EMERGENCY STOP"}
        </button>
      </div>
    </header>
  );
}
