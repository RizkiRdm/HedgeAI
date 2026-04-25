# tests/unit/test_quant_strategist.py
import pytest
from unittest.mock import patch, MagicMock
from src.agents.quant_strategist import QuantStrategist

@pytest.fixture
def strategist():
    return QuantStrategist()

def test_fas_formula_defaults(strategist):
    """Verify FAS formula matches requirements with default weights."""
    # (0.4 * 0.9) + (0.2 * 0.8) + (0.3 * 0.7) + (0.1 * 0.6)
    # 0.36 + 0.16 + 0.21 + 0.06 = 0.79
    with patch("src.agents.quant_strategist.momentum_scorer", return_value=0.9), \
         patch("src.agents.quant_strategist.rar_scorer", return_value=0.8), \
         patch("src.agents.quant_strategist.onchain_scorer", return_value=0.7), \
         patch("src.agents.quant_strategist.narrative_scorer", return_value=0.6), \
         patch("src.state.db.get_config", return_value=None), \
         patch("src.state.db.get_market_cache", return_value={"sector": "L1"}):
        
        signals = strategist.run_analysis(["SOL/USDC"])
        assert len(signals) == 1
        assert signals[0]["fas_score"] == 0.79

def test_filters_below_threshold(strategist):
    """Verify signals below 0.75 are excluded."""
    # (0.4 * 0.1) + (0.2 * 0.1) + (0.3 * 0.1) + (0.1 * 0.1) = 0.1
    with patch("src.agents.quant_strategist.momentum_scorer", return_value=0.1), \
         patch("src.agents.quant_strategist.rar_scorer", return_value=0.1), \
         patch("src.agents.quant_strategist.onchain_scorer", return_value=0.1), \
         patch("src.agents.quant_strategist.narrative_scorer", return_value=0.1), \
         patch("src.state.db.get_config", return_value=None):
        
        signals = strategist.run_analysis(["DUMP/USDC"])
        assert len(signals) == 0

def test_reads_weights_from_config(strategist):
    """Verify weights are read from system_config."""
    # Custom weights: ms=1.0, others=0.0
    def mock_get_config(param):
        if param == "fas_weight_ms": return "1.0"
        return "0.0"
        
    with patch("src.agents.quant_strategist.momentum_scorer", return_value=0.95), \
         patch("src.agents.quant_strategist.rar_scorer", return_value=0.1), \
         patch("src.agents.quant_strategist.onchain_scorer", return_value=0.1), \
         patch("src.agents.quant_strategist.narrative_scorer", return_value=0.1), \
         patch("src.state.db.get_config", side_effect=mock_get_config), \
         patch("src.state.db.get_market_cache", return_value={"sector": "L1"}):
        
        signals = strategist.run_analysis(["SOL/USDC"])
        assert len(signals) == 1
        assert signals[0]["fas_score"] == 0.95
