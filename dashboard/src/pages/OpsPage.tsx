/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { DataCard } from '../components/ui/DataCard';
import { OpsHealthBar } from '../components/ui/OpsHealthBar';
import { cn, formatCurrency } from '../lib/utils';

export function OpsPage() {
  return (
    <div className="space-y-8">
      {/* Top: Ops Fund status card */}
      <section className="bg-bg-secondary border border-border p-8 grid grid-cols-1 md:grid-cols-3 gap-8 items-center">
        <div className="md:col-span-1 space-y-1">
          <h2 className="text-[10px] font-mono uppercase tracking-[0.3em] text-muted mb-4">Operations Fund</h2>
          <p className="text-4xl font-mono font-bold text-white tracking-widest">{formatCurrency(8.14)}</p>
          <p className="text-[10px] font-mono text-muted uppercase mt-2">SOL/USDC Balance</p>
        </div>
        <div className="md:col-span-2 space-y-6">
          <OpsHealthBar balance={8.14} target={25.0} burnRate={2.50} className="max-w-md" />
          <div className="grid grid-cols-2 gap-8 pt-4 border-t border-border/50">
            <div>
              <p className="text-[9px] font-mono text-muted uppercase">Monthly Burn</p>
              <p className="text-lg font-mono text-white">{formatCurrency(2.50)}</p>
            </div>
            <div>
              <p className="text-[9px] font-mono text-muted uppercase">Auto-Pay</p>
              <p className="text-lg font-mono text-profit uppercase">ENABLED</p>
            </div>
          </div>
        </div>
      </section>

      {/* Middle: Upcoming Bills */}
      <section className="bg-bg-secondary border border-border p-6">
        <h3 className="text-[10px] font-mono uppercase tracking-[0.2em] text-muted mb-6">Upcoming Service Obligations</h3>
        <table className="w-full font-mono text-xs">
          <thead>
            <tr className="border-b border-border text-muted text-[10px] tracking-widest text-left">
              <th className="pb-3 font-normal">SERVICE</th>
              <th className="pb-3 font-normal text-right">AMOUNT</th>
              <th className="pb-3 font-normal text-right">DUE DATE</th>
              <th className="pb-3 font-normal text-right">STATUS</th>
              <th className="pb-3 font-normal text-right">ACTION</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border/50">
            {[
              { svc: 'RPC ENDPOINT (HELIUS)', amt: 0.50, due: '2026-05-01', status: 'PENDING', color: 'text-warn' },
              { svc: 'COMPUTE (CLOUDFLARE)', amt: 0.12, due: '2026-05-12', status: 'PENDING', color: 'text-warn' },
              { svc: 'DATA INDEXER (QUICKNODE)', amt: 0.75, due: '2026-05-15', status: 'QUEUED', color: 'text-muted' },
              { svc: 'OPS OVERHEAD (RESERVE)', amt: 1.13, due: '2026-05-20', status: 'PAID', color: 'text-profit' },
            ].map((row, i) => (
              <tr key={i} className="group hover:bg-white/5">
                <td className="py-4 text-white uppercase tracking-wider">{row.svc}</td>
                <td className="py-4 text-right text-white font-bold">{formatCurrency(row.amt)}</td>
                <td className="py-4 text-right tabular-nums">{row.due}</td>
                <td className={cn("py-4 text-right text-[10px] font-bold tracking-widest", row.color)}>{row.status}</td>
                <td className="py-4 text-right">
                  <button className="px-3 py-1 border border-border-accent text-[9px] uppercase tracking-widest hover:border-white transition-all">Manual</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {/* Bottom: Ledger */}
      <section className="bg-bg-secondary border border-border p-6">
        <h3 className="text-[10px] font-mono uppercase tracking-[0.2em] text-muted mb-6">Operational Ledger</h3>
        <table className="w-full font-mono text-xs">
          <thead>
            <tr className="border-b border-border text-muted text-[10px] tracking-widest text-left">
              <th className="pb-3 font-normal">TYPE</th>
              <th className="pb-3 font-normal text-right">AMOUNT</th>
              <th className="pb-3 font-normal text-center">CATEGORY</th>
              <th className="pb-3 font-normal text-right">DATE</th>
              <th className="pb-3 font-normal">NOTE</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border/50">
            {[
              { type: 'IN', amt: 0.84, cat: 'PROFIT_TAX', date: '2026-04-27 14:32', note: 'Cycle #4820 Trade Fee' },
              { type: 'OUT', amt: 0.15, cat: 'RPC_FEE', date: '2026-04-27 09:12', note: 'Batch execution signatures' },
              { type: 'IN', amt: 1.21, cat: 'PROFIT_TAX', date: '2026-04-26 22:58', note: 'Cycle #4812 Trade Fee' },
              { type: 'OUT', amt: 0.50, cat: 'BILL_PAY', date: '2026-04-26 12:00', note: 'Weekly API subscription' },
            ].map((row, i) => (
              <tr key={i} className="group hover:bg-white/5">
                <td className={cn("py-3 text-[10px] font-bold", row.type === 'IN' ? 'text-profit' : 'text-loss')}>{row.type}</td>
                <td className={cn("py-3 text-right font-bold tabular-nums", row.type === 'IN' ? 'text-profit' : 'text-loss')}>
                  {row.type === 'IN' ? '+' : '-'}{formatCurrency(row.amt)}
                </td>
                <td className="py-3 text-center">
                  <span className="px-2 py-0.5 border border-border-accent text-[9px] uppercase text-muted tracking-tighter">{row.cat}</span>
                </td>
                <td className="py-3 text-right tabular-nums text-muted">{row.date}</td>
                <td className="py-3 pl-4 text-white/70 italic text-[10px]">{row.note}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="flex justify-center mt-6">
          <div className="flex gap-2">
            <button className="px-3 py-1 border border-border text-[10px] text-muted uppercase">Prev</button>
            <span className="px-3 py-1 border border-border bg-white text-black font-bold text-[10px]">1</span>
            <button className="px-3 py-1 border border-border text-[10px] text-muted uppercase">Next</button>
          </div>
        </div>
      </section>
    </div>
  );
}
