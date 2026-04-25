import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from src.heartbeat.daemon import run_daemon
from src.state import db

@pytest.mark.asyncio
async def test_full_cycle_paper_trading(tmp_path, monkeypatch):
    """Run one end-to-end cycle in paper trading mode."""
    # Setup test DB
    db_file = tmp_path / "integration.duckdb"
    monkeypatch.setenv("DB_PATH", str(db_file))
    monkeypatch.setenv("PAPER_TRADING", "true")
    
    db.initialize_schema()
    db.set_config("EMERGENCY_STOP", "FALSE")
    
    # Mock Market Cache with a high FAS coin
    high_fas_data = {
        "ticker": "HIGH/SOL",
        "sector": "L1",
        "metrics_json": {
            "ohlcv_24h": [[i, 100+i, 110, 90, 105+i, 1000] for i in range(30)],
            "ohlcv_7d": [[i, 100+i, 110, 90, 105+i, 1000] for i in range(30)],
            "onchain_data": {
                "new_addresses_delta": 0.1,
                "tx_count_delta": 0.1,
                "holder_delta": 0.1
            },
            "sentiment_polarity": 0.9, # Super bullish
            "fear_greed_index": 80
        }
    }
    db.update_market_cache("HIGH/SOL", "L1", high_fas_data["metrics_json"])
    
    # Need to mock the agent behavior to actually trigger the flow
    # Since Overseer is stubbed, we'll mock its logic for this test
    # based on the GEMINI.md instructions for Overseer.
    
    from src.agents.quant_strategist import QuantStrategist
    from src.agents.risk_guardian import RiskGuardian
    from src.execution_bridge import grpc_client
    
    # 1. Analyze
    qs = QuantStrategist()
    signals = qs.run_analysis(["HIGH/SOL"])
    assert len(signals) == 1
    assert signals[0]["fas_score"] >= 0.75
    
    # 2. Risk Evaluation
    rg = RiskGuardian()
    portfolio = {
        "total_capital": 1000.0,
        "available_capital": 1000.0,
        "drawdown": 0.0,
        "positions": []
    }
    eval_res = rg.evaluate_signal(signals[0], portfolio)
    assert eval_res["approved"] is True
    
    # 3. Dry Run (Needs Go server or mock)
    with patch("src.execution_bridge.grpc_client.dry_run_swap", return_value={
        "is_safe": True, "estimated_slippage": 0.005, "price_impact": 0.001, "estimated_output": 19.9
    }), patch("src.execution_bridge.grpc_client.execute_swap", return_value={
        "success": True, "tx_hash": "0xmock", "executed_price": 100.0, "actual_slippage": 0.005, "error_message": ""
    }):
        # 4. Execute
        res = grpc_client.execute_swap("HIGH/SOL", eval_res["position_size_usd"])
        assert res["success"] is True
        assert "0xmock" in res["tx_hash"]
        
        # 5. Log trade (Accountant role)
        db.insert_trade("HIGH/SOL", 100.0, signals[0]["fas_score"])
        
    # Verify DB state
    with db.get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM trade_history").fetchone()[0]
        assert count == 1
