/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { DataCard } from '../components/ui/DataCard';
import { EquityCurve } from '../components/charts/EquityCurve';
import { WinLossBar } from '../components/charts/WinLossBar';
import { cn, formatCurrency } from '../lib/utils';

const equityData = [
  { date: '04/01', value: 250.00, drawdown: 0 },
  { date: '04/05', value: 265.40, drawdown: 0 },
  { date: '04/10', value: 242.10, drawdown: 8.7 },
  { date: '04/15', value: 280.50, drawdown: 0 },
  { date: '04/20', value: 301.20, drawdown: 0 },
  { date: '04/25', value: 295.40, drawdown: 1.9 },
  { date: '04/28', value: 312.40, drawdown: 0 },
];

const pnlByWeek = [
  { name: 'W14', pnl: 15.40 },
  { name: 'W15', pnl: -23.30 },
  { name: 'W16', pnl: 38.40 },
  { name: 'W17', pnl: 20.70 },
  { name: 'W18', pnl: 11.20 },
];

export function AnalyticsPage() {
  const [period, setPeriod] = useState('Weekly');

  return (
    <div className="space-y-8">
      {/* Period Selector */}
      <div className="flex gap-1 bg-border/20 p-1 w-fit border border-border">
        {['Weekly', 'Monthly', 'Quarterly', 'Annual'].map((p) => (
          <button
            key={p}
            onClick={() => setPeriod(p)}
            className={cn(
              "px-4 py-1.5 text-[10px] font-mono uppercase tracking-[0.15em] transition-all",
              period === p 
                ? "bg-white text-black font-bold" 
                : "text-muted hover:text-white"
            )}
          >
            {p}
          </button>
        ))}
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-5 gap-4">
        <DataCard label="Sharpe Ratio" value="2.84" delta={0.12} sublabel="vs avg" />
        <DataCard label="Win Rate" value="64.2%" delta={2.1} deltaType="pct" />
        <DataCard label="Avg RR" value="1.82" delta={-0.05} />
        <DataCard label="Max Drawdown" value="12.4%" delta={-1.2} deltaType="pct" />
        <DataCard label="FAS Accuracy" value="0.892" />
      </div>

      {/* Equity Curve */}
      <div className="grid grid-cols-1">
        <EquityCurve data={equityData} />
      </div>

      {/* Detailed Analysis */}
      <div className="grid grid-cols-2 gap-6">
        <WinLossBar data={pnlByWeek} title="Weekly PnL Distribution" />
        
        {/* Sector Performance */}
        <section className="bg-bg-secondary border border-border p-6">
          <h3 className="text-[10px] font-mono uppercase tracking-[0.2em] text-muted mb-6">Sector Performance</h3>
          <table className="w-full font-mono text-xs">
            <thead>
              <tr className="border-b border-border text-muted text-[10px] tracking-widest text-left">
                <th className="pb-3 font-normal">SECTOR</th>
                <th className="pb-3 font-normal text-right">TRADES</th>
                <th className="pb-3 font-normal text-right">WIN%</th>
                <th className="pb-3 font-normal text-right">TOTAL PNL</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/50">
              {[
                  { sector: 'AI AGENTS', trades: 42, win: '68%', pnl: 42.40 },
                  { sector: 'L1 ECOSYSTEM', trades: 31, win: '61%', pnl: 18.20 },
                  { sector: 'DEFI PERPS', trades: 15, win: '53%', pnl: -12.10 },
                  { sector: 'STORAGE', trades: 8, win: '75%', pnl: 6.30 },
                ].length === 0 ? (
                <tr>
                  <td colSpan={4} className="py-8 text-center text-[10px] text-muted italic">
                    Scanning... No signals above FAS 0.75 yet.
                  </td>
                </tr>
              ) : (
                [
                  { sector: 'AI AGENTS', trades: 42, win: '68%', pnl: 42.40 },
                  { sector: 'L1 ECOSYSTEM', trades: 31, win: '61%', pnl: 18.20 },
                  { sector: 'DEFI PERPS', trades: 15, win: '53%', pnl: -12.10 },
                  { sector: 'STORAGE', trades: 8, win: '75%', pnl: 6.30 },
                ].map((row, i) => (
                  <tr key={i} className="group hover:bg-white/5">
                    <td className="py-3 text-white uppercase tracking-tight">{row.sector}</td>
                    <td className="py-3 text-right">{row.trades}</td>
                    <td className="py-3 text-right">{row.win}</td>
                    <td className={cn(
                      "py-3 text-right font-bold",
                      row.pnl >= 0 ? "text-profit" : "text-loss"
                    )}>
                      {row.pnl >= 0 ? '+' : ''}{formatCurrency(row.pnl)}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </section>
      </div>

      {/* FAS Accuracy Table */}
      <section className="bg-bg-secondary border border-border p-6">
        <h3 className="text-[10px] font-mono uppercase tracking-[0.2em] text-muted mb-6">FAS Signal Accuracy</h3>
        <table className="w-full font-mono text-xs">
          <thead>
            <tr className="border-b border-border text-muted text-[10px] tracking-widest text-left">
              <th className="pb-3 font-normal">FAS RANGE</th>
              <th className="pb-3 font-normal text-right">SIGNALS</th>
              <th className="pb-3 font-normal text-right">PROFITABLE</th>
              <th className="pb-3 font-normal text-right">WIN%</th>
              <th className="pb-3 font-normal text-right">AVG PNL</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border/50">
            {[
              { range: '0.90–1.00', signals: 142, prof: 108, win: '76.1%', pnl: 8.42 },
              { range: '0.80–0.89', signals: 384, prof: 242, win: '63.0%', pnl: 3.10 },
              { range: '0.75–0.79', signals: 112, prof: 58, win: '51.8%', pnl: 0.12 },
            ].map((row, i) => (
              <tr key={i} className="group hover:bg-white/5">
                <td className="py-3 text-white">{row.range}</td>
                <td className="py-3 text-right">{row.signals}</td>
                <td className="py-3 text-right">{row.prof}</td>
                <td className="py-3 text-right">{row.win}</td>
                <td className="py-3 text-right text-profit font-bold">+{formatCurrency(row.pnl)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
