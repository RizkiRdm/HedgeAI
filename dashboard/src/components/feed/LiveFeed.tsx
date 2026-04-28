/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef, useMemo } from 'react';
import { AgentTag } from '../ui/AgentTag';
import { cn, formatTime } from '../../lib/utils';
import { motion, AnimatePresence } from 'motion/react';

interface Event {
  id: string;
  timestamp: string;
  agent: string;
  message: string;
}

interface LiveFeedProps {
  events: Event[];
}

const AGENTS = [
  'OVERSEER', 'ORACLE', 'QUANT', 'RISK', 'TRADER', 'ACCOUNTANT', 'EVAL', 'SYSTEM'
];

export function LiveFeed({ events }: LiveFeedProps) {
  const [filter, setFilter] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  const filteredEvents = useMemo(() => {
    if (!filter) return events;
    return events.filter(e => e.agent.startsWith(filter));
  }, [events, filter]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [filteredEvents]);

  return (
    <div className="flex flex-col h-full bg-bg border border-border">
      <div className="p-4 border-b border-border flex items-center justify-between">
        <h2 className="text-[10px] font-mono uppercase tracking-[0.2em] text-white font-bold">
          Live System Feed
        </h2>
        <div className="flex gap-2">
          <button 
            onClick={() => setFilter(null)}
            className={cn(
              "px-2 py-0.5 text-[9px] font-mono border transition-all uppercase tracking-widest",
              !filter ? "bg-white text-black border-white" : "text-muted border-border-accent hover:border-muted"
            )}
          >
            All
          </button>
          {AGENTS.map((agent) => (
            <button
              key={agent}
              onClick={() => setFilter(agent)}
              className={cn(
                "px-2 py-0.5 text-[9px] font-mono border transition-all uppercase tracking-widest",
                filter === agent ? "bg-white text-black border-white" : "text-muted border-border-accent hover:border-muted"
              )}
            >
              {agent}
            </button>
          ))}
        </div>
      </div>

      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-4 space-y-1 font-mono text-[11px]"
      >
        <AnimatePresence initial={false}>
          {filteredEvents.map((event) => (
            <motion.div
              key={event.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.15 }}
              className="flex gap-4 group"
            >
              <span className="text-muted shrink-0 w-16">[{formatTime(event.timestamp)}]</span>
              <AgentTag agent={event.agent} className="shrink-0 w-24" />
              <span className="text-text/90 group-hover:text-white transition-colors">{event.message}</span>
            </motion.div>
          ))}
        </AnimatePresence>
        
        {filteredEvents.length === 0 && (
          <div className="h-full flex items-center justify-center text-muted uppercase tracking-[0.3em] text-[10px]">
            Waiting for activity...
          </div>
        )}
      </div>
    </div>
  );
}
