/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { cn, formatPercent } from '../lib/utils';
import { Check, X } from 'lucide-react';

export function EvalPage() {
  const evalRuns = [
    { period: 'MICRO-14', start: '2026-04-20', end: '2026-04-23', actual: 4.2, target: 3.5, met: true, action: 'WEIGHT ADJ.' },
    { period: 'QUARTERLY-Q1', start: '2026-01-01', end: '2026-03-31', actual: 18.2, target: 15.0, met: true, action: 'RESERVE INC.' },
    { period: 'MICRO-13', start: '2026-04-10', end: '2026-04-13', actual: 2.1, target: 3.5, met: false, action: 'RE-SCAN' },
  ];

  const configSnapshot = {
    agents: {
      overseer_v: "1.4.2",
      risk_multiplier: 1.25,
      max_slippage: "0.2%",
      vol_threshold: 0.85
    },
    engine: {
      tick_delay_ms: 10000,
      min_fas_signal: 0.75,
      profit_split_tax: "2.5%"
    }
  };

  return (
    <div className="space-y-8">
      <section className="bg-bg-secondary border border-border p-6">
        <h3 className="text-[10px] font-mono uppercase tracking-[0.2em] text-muted mb-6">Evaluation Logs</h3>
        <table className="w-full font-mono text-xs">
          <thead>
            <tr className="border-b border-border text-muted text-[10px] tracking-widest text-left">
              <th className="pb-3 font-normal">PERIOD</th>
              <th className="pb-3 font-normal">START</th>
              <th className="pb-3 font-normal">END</th>
              <th className="pb-3 font-normal text-right">ROI ACTUAL</th>
              <th className="pb-3 font-normal text-right">ROI TARGET</th>
              <th className="pb-3 font-normal text-center">MET</th>
              <th className="pb-3 font-normal text-right">ACTION TAKEN</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border/50">
            {evalRuns.map((run, i) => (
              <tr key={i} className="group hover:bg-white/5">
                <td className="py-4 text-white font-bold tracking-widest">{run.period}</td>
                <td className="py-4 tabular-nums">{run.start}</td>
                <td className="py-4 tabular-nums">{run.end}</td>
                <td className={cn("py-4 text-right font-bold", run.met ? "text-profit" : "text-loss")}>
                  {formatPercent(run.actual)}
                </td>
                <td className="py-4 text-right text-muted">{formatPercent(run.target)}</td>
                <td className="py-4 text-center flex justify-center">
                  {run.met ? <Check className="w-4 h-4 text-profit" /> : <X className="w-4 h-4 text-loss" />}
                </td>
                <td className="py-4 text-right">
                  <span className="px-2 py-0.5 border border-border-accent text-[9px] uppercase text-accent tracking-tighter">
                    {run.action}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <section className="bg-bg-secondary border border-border p-6">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-[10px] font-mono uppercase tracking-[0.2em] text-muted">Config Snapshot / Current</h3>
            <span className="px-2 py-0.5 bg-border text-[9px] font-mono text-white">#0428-A</span>
          </div>
          <pre className="bg-bg p-6 text-[11px] font-mono text-cyan/80 overflow-x-auto border border-border-accent leading-relaxed">
            {JSON.stringify(configSnapshot, null, 2)}
          </pre>
        </section>

        <section className="bg-bg-secondary border border-border p-8 flex flex-col items-center justify-center space-y-6 text-center">
          <h3 className="text-[10px] font-mono uppercase tracking-[0.3em] text-muted mb-2">Last Evaluation Outcome</h3>
          <div className="w-24 h-24 border-2 border-profit rounded-full flex items-center justify-center bg-profit/5 shadow-[0_0_40px_rgba(22,163,74,0.1)]">
            <Check className="w-12 h-12 text-profit" strokeWidth={3} />
          </div>
          <div className="space-y-1">
            <p className="text-2xl font-mono font-bold text-white tracking-widest">DRIVE MET</p>
            <p className="text-[10px] font-mono text-muted uppercase tracking-wider">Target: 3.5% / Actual: 4.2%</p>
          </div>
          <p className="text-xs font-mono text-muted max-w-xs uppercase leading-loose border-t border-border pt-4">
            Autonomous weight adjustments applied to Oracles 2 and 4. Evaluation session closed.
          </p>
        </section>
      </div>
    </div>
  );
}
