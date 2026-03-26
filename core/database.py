import duckdb
import logging
import threading
from pathlib import Path
from typing import Optional, Any


class DatabaseManager:
    _instance: Optional["DatabaseManager"] = None
    _lock = threading.Lock()

    def __new__(cls, db_path: str = "data/state.duckdb"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseManager, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_path: str = "data/state.duckdb"):
        if self._initialized:
            return

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(str(self.db_path))
        self._init_db()
        self._initialized = True
        logging.info(f"Database initialized at {self.db_path}")

    def _init_db(self):
        """Initialize database schema based on BLUEPRINT.md"""
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS market_cache (
                ticker VARCHAR PRIMARY KEY,
                metrics JSON,
                sector_tag VARCHAR,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS trade_history (
                id INTEGER PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ticker VARCHAR,
                chain VARCHAR,
                side VARCHAR,
                amount DOUBLE,
                price DOUBLE,
                slippage DOUBLE,
                gas_fee DOUBLE,
                pnl DOUBLE,
                status VARCHAR
            );
            
            CREATE TABLE IF NOT EXISTS system_config (
                key VARCHAR PRIMARY KEY,
                value VARCHAR,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS pending_expenses (
                id INTEGER PRIMARY KEY,
                description VARCHAR,
                amount DOUBLE,
                status VARCHAR,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        )
        # Initialize default config if not exists
        self.conn.execute(
            "INSERT OR IGNORE INTO system_config (key, value) VALUES ('emergency_stop', 'false')"
        )
        self.conn.execute(
            "INSERT OR IGNORE INTO system_config (key, value) VALUES ('fas_threshold', '75')"
        )

    def get_cache(self, ticker: str) -> Optional[dict]:
        result = self.conn.execute(
            "SELECT metrics FROM market_cache WHERE ticker = ?", [ticker]
        ).fetchone()
        return result[0] if result else None

    def update_state(self, table: str, data: dict, where_clause: str = ""):
        # In production, use parameterized queries for security
        keys = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        values = list(data.values())

        if where_clause:
            set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
            self.conn.execute(
                f"UPDATE {table} SET {set_clause} WHERE {where_clause}", values
            )
        else:
            self.conn.execute(
                f"INSERT OR REPLACE INTO {table} ({keys}) VALUES ({placeholders})",
                values,
            )

    def close(self):
        self.conn.close()


# Singleton Accessor
def get_db() -> DatabaseManager:
    return DatabaseManager()
