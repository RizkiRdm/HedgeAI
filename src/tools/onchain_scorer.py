# src/tools/onchain_scorer.py
from typing import Any
from src.utils.logger import get_logger

log = get_logger(__name__)

def onchain_scorer(ticker: str) -> float:
    """
    Calculates On-Chain Health Score.
    Returns: float 0.0–1.0
    """
    from src.state.db import get_market_cache
    
    try:
        cache = get_market_cache(ticker)
        if not cache:
            return 0.0

        metrics = cache.get("metrics_json", {})
        onchain = metrics.get("onchain_data") # Expect {new_addr_delta, tx_delta, holder_delta}
        
        if not onchain:
            return 0.0

        # Normalization logic: delta is usually a percentage change e.g. 0.05 for 5%
        # We assume 10% change is a strong signal (1.0)
        def normalize_delta(val: float) -> float:
            return max(0.0, min(1.0, val * 10.0))

        na_score = normalize_delta(onchain.get("new_addresses_delta", 0.0))
        tx_score = normalize_delta(onchain.get("tx_count_delta", 0.0))
        h_score = normalize_delta(onchain.get("holder_delta", 0.0))

        score = (na_score + tx_score + h_score) / 3.0
        
        return round(max(0.0, min(1.0, float(score))), 4)

    except Exception as e:
        log.error(f"onchain_scorer error for {ticker}: {e}")
        return 0.0
