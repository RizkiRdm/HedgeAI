/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export interface Position {
  ticker: string;
  size: number;
  entry_price: number;
  current_price: number;
  unrealized_pnl: number;
  sector?: string;
}

export interface PortfolioState {
  total_capital: number;
  available_capital: number;
  positions: Position[];
}

export interface Trade {
  id: string;
  ticker: string;
  entry_p: number | null;
  exit_p: number | null;
  fas_score: number;
  pnl: number | null;
  created_at: string;
}

export interface LedgerEntry {
  id: string;
  amount: number;
  category: "profit_tax" | "bill_payment" | "reserve";
  description: string;
  auto_executed: boolean;
  timestamp: string;
}

export interface AgentStatus {
  name: string;
  status: "active" | "paused" | "error" | "idle";
  cycles?: number;
  failures?: number;
  uptime_seconds?: number;
}

export interface EvalEntry {
  id: string;
  period_type: "micro" | "quarterly" | "annual";
  period_start: string;
  period_end: string;
  roi_actual: number;
  roi_target: number;
  met_target: boolean;
  config_snapshot: Record<string, unknown>;
  action_taken: string;
  created_at: string;
}

export type WSEvent =
  | { type: "agent_activity"; data: { agent: string; message: string } }
  | { type: "portfolio_update"; data: { total_capital: number; available_capital: number; positions: Position[] } }
  | { type: "trade_executed"; data: { ticker: string; net_pnl: number; ops_fund_balance: number } }
  | { type: "fas_signal"; data: { ticker: string; fas_score: number; ms: number; rar: number; ochs: number; ns: number } }
  | { type: "alert"; data: { level: "info" | "warning" | "critical" | "emergency"; message: string } };
