# src/tools/narrative_scorer.py
from typing import Any
from src.utils.logger import get_logger

log = get_logger(__name__)

def narrative_scorer(ticker: str) -> float:
    """
    Calculates Narrative Score.
    Returns: float 0.0–1.0
    """
    from src.state.db import get_market_cache
    
    try:
        cache = get_market_cache(ticker)
        if not cache:
            return 0.0

        metrics = cache.get("metrics_json", {})
        
        # CryptoPanic Sentiment Polarity (0.0 to 1.0, 0.5 neutral)
        sentiment = metrics.get("sentiment_polarity", 0.5)
        
        # Fear & Greed Index (1 to 100)
        fg_index = metrics.get("fear_greed_index", 50)
        fg_norm = float(fg_index) / 100.0

        # Weighted score
        score = (sentiment * 0.7) + (fg_norm * 0.3)
        
        return round(max(0.0, min(1.0, float(score))), 4)

    except Exception as e:
        log.error(f"narrative_scorer error for {ticker}: {e}")
        return 0.0
