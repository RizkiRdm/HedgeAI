# tests/unit/test_db.py
import pytest
import os
from datetime import date
from src.state.db import (
    initialize_schema, get_config, set_config, insert_trade, 
    close_trade, update_market_cache, get_market_cache, 
    insert_ops_ledger, get_ops_fund_balance, checkpoint, get_connection
)

@pytest.fixture(autouse=True)
def test_db(tmp_path, monkeypatch):
    """Setup temporary database for each test."""
    db_file = tmp_path / "test_cryptohedge.duckdb"
    monkeypatch.setenv("DB_PATH", str(db_file))
    
    # Need to copy schema.sql relative to db.py or mock it
    # Implementation of initialize_schema reads schema.sql relative to db.py
    # So we ensure the test environment can find it.
    initialize_schema()
    return db_file

def test_initialize_schema():
    """Verify all tables created."""
    with get_connection() as conn:
        tables = conn.execute("SHOW TABLES").fetchall()
        table_names = [t[0] for t in tables]
        assert "market_cache" in table_names
        assert "trade_history" in table_names
        assert "system_config" in table_names
        assert "ops_ledger" in table_names
        assert "eval_history" in table_names

def test_config_crud():
    """Test system_config operations."""
    set_config("key", "val")
    assert get_config("key") == "val"
    
    set_config("key", "new_val")
    assert get_config("key") == "new_val"
    
    set_config("locked", "secret", is_locked=True)
    with pytest.raises(ValueError, match="is locked"):
        set_config("locked", "hacked")

def test_trade_lifecycle():
    """Test trade insertion and closing."""
    trade_id = insert_trade("SOL/USDC", 100.5, 0.88)
    assert trade_id is not None
    
    close_trade(trade_id, 105.0, 4.5)
    
    with get_connection() as conn:
        res = conn.execute("SELECT exit_p, pnl FROM trade_history WHERE id = ?", [trade_id]).fetchone()
        assert res[0] == 105.0
        assert res[1] == 4.5

def test_market_cache_upsert():
    """Test market data caching."""
    data = {"ms": 0.9, "rar": 0.8}
    update_market_cache("BTC/USDC", "Majors", data)
    
    cached = get_market_cache("BTC/USDC")
    assert cached is not None
    assert cached["sector"] == "Majors"
    assert cached["metrics_json"] == data

def test_ops_ledger():
    """Test fund balance calculation."""
    insert_ops_ledger(100.0, "profit_tax", "win")
    insert_ops_ledger(-20.0, "bill_payment", "hosting")
    
    assert get_ops_fund_balance() == 80.0

def test_checkpoint():
    """Verify PRAGMA runs."""
    checkpoint()
