/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  Cell 
} from 'recharts';
import { formatCurrency } from '../../lib/utils';

interface BarData {
  name: string;
  pnl: number;
}

interface WinLossBarProps {
  data: BarData[];
  title?: string;
}

export function WinLossBar({ data, title = "PnL by Period" }: WinLossBarProps) {
  return (
    <div className="w-full h-80 bg-bg-secondary border border-border p-6 rounded-none">
      <h2 className="text-[10px] font-mono uppercase tracking-[0.2em] text-muted mb-6">{title}</h2>
      
      <ResponsiveContainer width="100%" height="80%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1a1a1a" vertical={false} />
          <XAxis 
            dataKey="name" 
            stroke="#404040" 
            fontSize={10} 
            fontFamily="IBM Plex Mono"
            tickLine={false}
            axisLine={false}
            tick={{ fill: '#808080' }}
          />
          <YAxis 
            stroke="#404040" 
            fontSize={10} 
            fontFamily="IBM Plex Mono"
            tickLine={false}
            axisLine={false}
            tick={{ fill: '#808080' }}
            tickFormatter={(val) => `$${val}`}
          />
          <Tooltip
            cursor={{ fill: 'rgba(255, 255, 255, 0.05)' }}
            contentStyle={{ 
              backgroundColor: '#0a0a0a', 
              border: '1px solid #333333',
              borderRadius: '0',
              fontFamily: 'IBM Plex Mono',
              fontSize: '11px'
            }}
            itemStyle={{ color: '#ffffff' }}
            formatter={(value: number) => [formatCurrency(value), 'PnL']}
            labelStyle={{ color: '#808080', marginBottom: '4px', textTransform: 'uppercase' }}
          />
          <Bar dataKey="pnl">
            {data.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={entry.pnl >= 0 ? '#16a34a' : '#dc2626'} 
                fillOpacity={0.8}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
