/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';

export function ConfigPage() {
  const configs = [
    { key: 'ENGINE_TICK_RATE', value: '10000ms', type: 'SYSTEM' },
    { key: 'MIN_FAS_THRESHOLD', value: '0.750', type: 'QUANT' },
    { key: 'MAX_SLIPPAGE_TOLERANCE', value: '0.20%', type: 'RISK' },
    { key: 'SECTOR_AI_MAX_WEIGHT', value: '35%', type: 'OVERSEER' },
    { key: 'RPC_PRIORITY_FEE', value: '0.00005 SOL', type: 'TRADER' },
    { key: 'EMERGENCY_STOP_ENABLED', value: 'TRUE', type: 'SYSTEM' },
  ];

  return (
    <div className="space-y-8 max-w-4xl">
      <section className="bg-bg-secondary border border-border p-8">
        <h2 className="text-[10px] font-mono uppercase tracking-[0.3em] text-muted mb-8">System Configuration</h2>
        <div className="space-y-1">
          {configs.map((cfg, i) => (
            <div key={i} className="grid grid-cols-12 gap-4 py-4 border-b border-border/50 group hover:bg-white/5 px-4 transition-all">
              <div className="col-span-1">
                <span className="text-[10px] font-mono text-muted/30">{(i+1).toString().padStart(2, '0')}</span>
              </div>
              <div className="col-span-5 flex flex-col">
                <span className="text-xs font-mono font-bold text-white tracking-widest">{cfg.key}</span>
                <span className="text-[9px] font-mono text-muted uppercase mt-1">{cfg.type} DOMAIN</span>
              </div>
              <div className="col-span-4 flex items-center justify-end">
                <span className="text-xs font-mono text-cyan tabular-nums bg-cyan/5 px-3 py-1 border border-cyan/20">
                  {cfg.value}
                </span>
              </div>
              <div className="col-span-2 flex items-center justify-end">
                <span className="text-[9px] font-mono text-muted uppercase tracking-widest italic">READ_ONLY</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      <div className="p-6 border border-warn/30 bg-warn/5 text-center">
        <p className="text-[10px] font-mono text-warn uppercase tracking-[0.2em]">
          Configuration is immutable via dashboard. Use CLI: <code className="text-white bg-bg px-2 py-1 ml-2">cryptohedge set [key] [val]</code>
        </p>
      </div>
    </div>
  );
}
