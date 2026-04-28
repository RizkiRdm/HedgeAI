/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { LiveFeed } from '../components/feed/LiveFeed';
import { ScoreBar } from '../components/ui/ScoreBar';
import { PnlValue } from '../components/ui/PnlValue';
import { cn } from '../lib/utils';
import { useGlobalState } from '../lib/store';

const DUMMY_EVENTS = [
  { id: '1', timestamp: new Date().toISOString(), agent: 'SYSTEM', message: 'Engine initialized. Awaiting market data.' },
  { id: '2', timestamp: new Date().toISOString(), agent: 'OVERSEER', message: 'Cycle #4821 started. Scanning sectors: DeFi, AI, L2.' },
  { id: '3', timestamp: new Date().toISOString(), agent: 'ORACLE', message: 'SOL/USDC volatility spike detected (+4.2%).' },
  { id: '4', timestamp: new Date().toISOString(), agent: 'QUANT', message: 'Signal generated: SOL/USDC. FAS 0.847. Momentum 0.910.' },
  { id: '5', timestamp: new Date().toISOString(), agent: 'RISK ✓', message: 'Position check PASSED. Slippage <0.2%. Sector exposure within limits.' },
  { id: '6', timestamp: new Date().toISOString(), agent: 'TRADER', message: 'EXECUTING LONG SOL/USDC @ $142.30. Size: 2.1 SOL.' },
];

export function LiveFeedPage() {
  const { lastEvents, portfolio, lastSignal } = useGlobalState();
  const events = lastEvents.length > 0 ? lastEvents : DUMMY_EVENTS;

  const positions = portfolio?.positions?.map(p => ({
    ticker: p.ticker,
    change: ((p.current_price - p.entry_price) / p.entry_price) * 100,
    value: p.size * p.current_price,
    tag: p.ticker.split('/')[0]
  })) || [
    { ticker: 'SOL/USDC', change: 2.1, value: 6.30, tag: 'SOL' },
    { ticker: 'BNB/USDC', change: -0.4, value: 6.22, tag: 'BSC' },
  ];

  return (
    <div className="grid grid-cols-12 gap-6 h-[calc(100vh-120px)]">
      {/* Left Column - Live Feed */}
      <div className="col-span-8 flex flex-col min-h-0">
        <LiveFeed events={events} />
      </div>

      {/* Right Column - Snapshot */}
      <div className="col-span-4 space-y-6 overflow-y-auto">
        {/* Active Positions */}
        <section className="bg-bg-secondary border border-border p-5">
          <h3 className="text-[10px] font-mono uppercase tracking-[0.2em] text-muted mb-4 border-b border-border pb-2">
            Active Positions
          </h3>
          <div className="space-y-4">
            {positions.map((p, i) => (
              <div key={i} className="flex items-center justify-between font-mono">
                <div className="flex flex-col">
                  <span className="text-xs text-white">{p.ticker}</span>
                  <span className="text-[9px] text-muted">{p.tag}</span>
                </div>
                <div className="flex items-center gap-4">
                  <span className={cn(
                    "text-xs tabular-nums",
                    p.change >= 0 ? "text-profit" : "text-loss"
                  )}>
                    {p.change >= 0 ? '+' : ''}{p.change}%
                  </span>
                  <span className="text-xs text-white">
                    ${p.value.toFixed(2)}
                  </span>
                </div>
              </div>
            ))}
            {positions.length === 0 && (
              <p className="text-[10px] font-mono text-muted uppercase italic text-center py-4">
                0 active positions. Capital fully available.
              </p>
            )}
          </div>
        </section>

        {/* Last Signal */}
        <section className="bg-bg-secondary border border-border p-5">
          <h3 className="text-[10px] font-mono uppercase tracking-[0.2em] text-muted mb-4 border-b border-border pb-2">
            Last Signal {lastSignal ? `/ ${lastSignal.ticker}` : ''}
          </h3>
          {!lastSignal ? (
            <p className="text-[10px] font-mono text-muted uppercase italic text-center py-4">
              Last cycle: no coins met threshold.
            </p>
          ) : (
            <div className="space-y-3">
              <ScoreBar label="FAS" value={lastSignal.fas_score} />
              <ScoreBar label="MS" value={lastSignal.ms} />
              <ScoreBar label="RAR" value={lastSignal.rar} />
              <ScoreBar label="OCHS" value={lastSignal.ochs} />
              <ScoreBar label="NS" value={lastSignal.ns} />
            </div>
          )}
        </section>

        {/* Cycle Timing */}
        <section className="bg-bg-secondary border border-border p-5">
          <h3 className="text-[10px] font-mono uppercase tracking-[0.2em] text-muted mb-4 border-b border-border pb-2">
            Cycle Metrics
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-[9px] font-mono text-muted uppercase">Latency</p>
              <p className="text-xl font-mono text-white">7.8s <span className="text-[10px] text-muted">/ 14s</span></p>
            </div>
            <div>
              <p className="text-[9px] font-mono text-muted uppercase">Iteration</p>
              <p className="text-xl font-mono text-white">#4,821</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
