# tests/unit/test_risk_guardian.py
import pytest
from unittest.mock import patch, MagicMock
from src.agents.risk_guardian import RiskGuardian

@pytest.fixture
def guardian():
    return RiskGuardian()

@pytest.fixture
def base_signal():
    return {"ticker": "SOL/SOL", "sector": "L1", "fas_score": 0.85, "estimated_slippage": 0.005}

@pytest.fixture
def base_portfolio():
    return {
        "total_capital": 1000.0,
        "available_capital": 1000.0,
        "drawdown": 0.05,
        "positions": []
    }

def test_approve_valid_signal(guardian, base_signal, base_portfolio):
    # win_rate=0.5, avg_rr=2.0 -> Kelly = 0.5 - (0.5/2.0) = 0.25. half=0.125. capped at 0.02.
    # 1000 * 0.02 = 20.0
    with patch("src.state.db.get_config", side_effect=["0.5", "2.0"]): 
        res = guardian.evaluate_signal(base_signal, base_portfolio)
        assert res["approved"] is True
        assert res["position_size_usd"] == 20.0

def test_veto_drawdown_limit(guardian, base_signal, base_portfolio):
    base_portfolio["drawdown"] = 0.20 # 20%
    with patch("src.state.db.set_config") as mock_set_config, \
         patch("src.utils.telegram_notifier.send_emergency_alert"):
        res = guardian.evaluate_signal(base_signal, base_portfolio)
        assert res["approved"] is False
        assert res["reason"] == "drawdown_limit"
        mock_set_config.assert_called_with("EMERGENCY_STOP", "TRUE")

def test_veto_sector_cap(guardian, base_signal, base_portfolio):
    base_portfolio["positions"] = [
        {"ticker": "A/SOL", "sector": "L1"},
        {"ticker": "B/SOL", "sector": "L1"},
        {"ticker": "C/SOL", "sector": "L1"},
    ]
    res = guardian.evaluate_signal(base_signal, base_portfolio)
    assert res["approved"] is False
    assert res["reason"] == "sector_cap"

def test_veto_chain_not_eligible(guardian, base_signal, base_portfolio):
    base_signal["ticker"] = "BTC/TRX"
    res = guardian.evaluate_signal(base_signal, base_portfolio)
    assert res["approved"] is False
    assert res["reason"] == "chain_not_eligible"

def test_veto_eth_capital_low(guardian, base_signal, base_portfolio):
    base_signal["ticker"] = "PEPE/ETH"
    base_portfolio["total_capital"] = 500.0
    res = guardian.evaluate_signal(base_signal, base_portfolio)
    assert res["approved"] is False
    assert "chain_not_eligible" in res["reason"]

def test_veto_slippage(guardian, base_signal, base_portfolio):
    base_signal["estimated_slippage"] = 0.03 # 3%
    res = guardian.evaluate_signal(base_signal, base_portfolio)
    assert res["approved"] is False
    assert res["reason"] == "slippage_too_high"

def test_veto_below_minimum_size(guardian, base_signal, base_portfolio):
    base_portfolio["total_capital"] = 100.0
    # win_rate=0.1, avg_rr=1.0 -> Kelly=0.1 - (0.9/1.0) = -0.8 -> 0.0
    with patch("src.state.db.get_config", side_effect=["0.1", "1.0"]): 
        res = guardian.evaluate_signal(base_signal, base_portfolio)
        assert res["approved"] is False
        assert res["reason"] == "below_minimum_size"

def test_kelly_hard_cap(guardian, base_signal, base_portfolio):
    # win_rate=1.0, avg_rr=100.0 -> Kelly close to 1.0, but capped at 0.02
    with patch("src.state.db.get_config", side_effect=["1.0", "100.0"]):
        res = guardian.evaluate_signal(base_signal, base_portfolio)
        assert res["approved"] is True
        # 1000 * 0.02 = 20
        assert res["position_size_usd"] == 20.0
