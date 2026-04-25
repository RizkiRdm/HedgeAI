# tests/unit/test_scorers.py
import pytest
from unittest.mock import patch
from src.tools.momentum_scorer import momentum_scorer
from src.tools.rar_scorer import rar_scorer
from src.tools.onchain_scorer import onchain_scorer
from src.tools.narrative_scorer import narrative_scorer

@pytest.fixture
def mock_market_cache():
    return {
        "ticker": "SOL/USDC",
        "sector": "L1",
        "metrics_json": {
            "ohlcv_24h": [[i, 100+i, 110+i, 90+i, 105+i, 1000] for i in range(30)],
            "ohlcv_7d": [[i, 100+i, 110+i, 90+i, 105+i, 1000] for i in range(30)],
            "onchain_data": {
                "new_addresses_delta": 0.05,
                "tx_count_delta": 0.08,
                "holder_delta": 0.02
            },
            "sentiment_polarity": 0.8,
            "fear_greed_index": 70
        }
    }

def test_momentum_scorer_happy_path(mock_market_cache):
    with patch("src.state.db.get_market_cache", return_value=mock_market_cache):
        score = momentum_scorer("SOL/USDC")
        assert 0.0 <= score <= 1.0
        assert isinstance(score, float)

def test_rar_scorer_happy_path(mock_market_cache):
    with patch("src.state.db.get_market_cache", return_value=mock_market_cache):
        score = rar_scorer("SOL/USDC")
        assert 0.0 <= score <= 1.0

def test_onchain_scorer_happy_path(mock_market_cache):
    with patch("src.state.db.get_market_cache", return_value=mock_market_cache):
        score = onchain_scorer("SOL/USDC")
        assert 0.0 <= score <= 1.0

def test_narrative_scorer_happy_path(mock_market_cache):
    with patch("src.state.db.get_market_cache", return_value=mock_market_cache):
        score = narrative_scorer("SOL/USDC")
        assert 0.0 <= score <= 1.0

def test_scorers_no_data():
    with patch("src.state.db.get_market_cache", return_value=None):
        assert momentum_scorer("MISSING") == 0.0
        assert rar_scorer("MISSING") == 0.0
        assert onchain_scorer("MISSING") == 0.0
        assert narrative_scorer("MISSING") == 0.0

def test_scorers_rounding():
    # Force a score with many decimals
    with patch("src.state.db.get_market_cache", return_value={
        "metrics_json": {"sentiment_polarity": 0.333333333, "fear_greed_index": 44}
    }):
        score = narrative_scorer("SOL/USDC")
        assert len(str(score).split(".")[-1]) <= 4
