# src/state/db.py
import duckdb
import os
import json
from typing import Any, Optional
from datetime import datetime, date

def get_connection() -> duckdb.DuckDBPyConnection:
    """Returns a DuckDB connection. Called at start of each function."""
    path = os.getenv("DB_PATH", "data/cryptohedge.duckdb")
    return duckdb.connect(path)

def initialize_schema() -> None:
    """Run once at startup. Creates all tables if they don't exist."""
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path) as f:
        sql = f.read()
    with get_connection() as conn:
        conn.execute(sql)

def get_config(param_name: str) -> Optional[str]:
    """Read a single config value. Returns None if not found."""
    with get_connection() as conn:
        res = conn.execute(
            "SELECT param_value FROM system_config WHERE param_name = ?", 
            [param_name]
        ).fetchone()
        return str(res[0]) if res else None

def set_config(param_name: str, param_value: str, is_locked: bool = False) -> None:
    """Upsert a config param. Raises ValueError if param is locked."""
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT is_locked FROM system_config WHERE param_name = ?", 
            [param_name]
        ).fetchone()
        
        if existing and existing[0]:
            raise ValueError(f"Config parameter '{param_name}' is locked.")
            
        conn.execute(
            """
            INSERT INTO system_config (param_name, param_value, is_locked)
            VALUES (?, ?, ?)
            ON CONFLICT (param_name) DO UPDATE SET
                param_value = excluded.param_value,
                is_locked = excluded.is_locked
            """,
            [param_name, param_value, is_locked]
        )

def insert_trade(ticker: str, entry_p: float, fas_score: float) -> str:
    """Insert open trade. Returns the new UUID."""
    with get_connection() as conn:
        res = conn.execute(
            """
            INSERT INTO trade_history (ticker, entry_p, fas_score)
            VALUES (?, ?, ?)
            RETURNING id
            """,
            [ticker, entry_p, fas_score]
        ).fetchone()
        if not res:
            raise RuntimeError("Failed to insert trade")
        return str(res[0])

def close_trade(trade_id: str, exit_p: float, pnl: float) -> None:
    """Update trade with exit price and PnL."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE trade_history SET exit_p = ?, pnl = ? WHERE id = ?",
            [exit_p, pnl, trade_id]
        )

def update_market_cache(ticker: str, sector: str, metrics_json: dict[str, Any]) -> None:
    """Upsert market_cache row."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO market_cache (ticker, sector, metrics_json, last_updated)
            VALUES (?, ?, ?, now())
            ON CONFLICT (ticker) DO UPDATE SET
                sector = excluded.sector,
                metrics_json = excluded.metrics_json,
                last_updated = now()
            """,
            [ticker, sector, json.dumps(metrics_json)]
        )

def get_market_cache(ticker: str) -> Optional[dict[str, Any]]:
    """Get cached data for ticker. Returns None if not found."""
    with get_connection() as conn:
        res = conn.execute(
            "SELECT ticker, sector, metrics_json, last_updated FROM market_cache WHERE ticker = ?",
            [ticker]
        ).fetchone()
        if res:
            return {
                "ticker": res[0],
                "sector": res[1],
                "metrics_json": json.loads(res[2]) if isinstance(res[2], str) else res[2],
                "last_updated": res[3]
            }
        return None

def insert_ops_ledger(amount: float, category: str, description: str, auto_executed: bool = False) -> None:
    """Log an ops fund transaction."""
    # Note: auto_executed column not in GEMINI.md schema, adding to description or ignoring for now
    # schema.sql matches GEMINI.md: id, amount, category, description, timestamp
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO ops_ledger (amount, category, description) VALUES (?, ?, ?)",
            [amount, category, f"{'[AUTO] ' if auto_executed else ''}{description}"]
        )

def get_ops_fund_balance() -> float:
    """Sum all ops_ledger entries to get current balance."""
    with get_connection() as conn:
        res = conn.execute("SELECT SUM(amount) FROM ops_ledger").fetchone()
        return float(res[0]) if res and res[0] is not None else 0.0

def insert_eval(period_type: str, period_start: date, period_end: date, roi_actual: float,
                roi_target: float, met_target: bool, config_snapshot: dict[str, Any], action_taken: str) -> None:
    """Log an evaluation result."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO eval_history (
                period_type, period_start, period_end, roi_actual, 
                roi_target, met_target, config_snapshot, action_taken
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                period_type, period_start, period_end, roi_actual,
                roi_target, met_target, json.dumps(config_snapshot), action_taken
            ]
        )

def checkpoint() -> None:
    """Force DuckDB WAL checkpoint. Run every hour."""
    with get_connection() as conn:
        conn.execute("PRAGMA force_checkpoint")
