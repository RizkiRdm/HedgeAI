/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  Area, 
  ComposedChart,
  ReferenceLine
} from 'recharts';
import { formatCurrency, formatNumber } from '../../lib/utils';

interface DataPoint {
  date: string;
  value: number;
  drawdown: number;
}

interface EquityCurveProps {
  data: DataPoint[];
}

export function EquityCurve({ data }: EquityCurveProps) {
  const baseline = data.length > 0 ? data[0].value : 0;

  return (
    <div className="w-full h-80 bg-bg-secondary border border-border p-6 rounded-none">
      <div className="flex justify-between items-start mb-6">
        <div>
          <h2 className="text-[10px] font-mono uppercase tracking-[0.2em] text-muted">Equity Curve / USD</h2>
          <p className="text-2xl font-mono font-bold text-white tabular-nums">
            {data.length > 0 ? formatCurrency(data[data.length - 1].value) : '--'}
          </p>
        </div>
        <div className="text-right">
          <p className="text-[10px] font-mono uppercase tracking-[0.2em] text-muted">Baseline</p>
          <p className="text-sm font-mono text-white/50">{formatCurrency(baseline)}</p>
        </div>
      </div>

      <ResponsiveContainer width="100%" height="80%">
        <ComposedChart data={data} margin={{ top: 5, right: 5, bottom: 5, left: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1a1a1a" vertical={false} />
          <XAxis 
            dataKey="date" 
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
            tickFormatter={(val) => `$${(val/1000).toFixed(1)}k`}
            domain={['auto', 'auto']}
          />
          <Tooltip
            contentStyle={{ 
              backgroundColor: '#0a0a0a', 
              border: '1px solid #333333',
              borderRadius: '0',
              fontFamily: 'IBM Plex Mono',
              fontSize: '11px'
            }}
            itemStyle={{ color: '#ffffff' }}
            formatter={(value: number) => [formatCurrency(value), 'Equity']}
            labelStyle={{ color: '#808080', marginBottom: '4px', textTransform: 'uppercase' }}
          />
          <ReferenceLine y={baseline} stroke="#333" strokeDasharray="5 5" />
          
          {/* Drawdown Area */}
          <Area 
            type="monotone" 
            dataKey="value" 
            stroke="none" 
            fill="#dc2626" 
            fillOpacity={0.1}
            baseValue={baseline}
          />
          
          <Line 
            type="monotone" 
            dataKey="value" 
            stroke="#ffffff" 
            strokeWidth={2} 
            dot={false}
            activeDot={{ r: 4, fill: '#ffffff', strokeWidth: 0 }}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
