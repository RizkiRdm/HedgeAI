# src/tools/rar_scorer.py
import numpy as np
import pandas as pd
from typing import Any
from src.utils.logger import get_logger

log = get_logger(__name__)

def rar_scorer(ticker: str) -> float:
    """
    Calculates Risk-Adjusted Return score.
    Returns: float 0.0–1.0
    """
    from src.state.db import get_market_cache
    
    try:
        cache = get_market_cache(ticker)
        if not cache:
            return 0.0

        metrics = cache.get("metrics_json", {})
        ohlcv = metrics.get("ohlcv_7d") # Expect 7-day data
        
        if not ohlcv or len(ohlcv) < 10:
            return 0.0

        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        returns = df["close"].pct_change().dropna()
        
        if returns.empty:
            return 0.0

        # Sharpe-like ratio (simplified)
        mean_ret = returns.mean()
        std_ret = returns.std()
        
        sharpe = (mean_ret / std_ret) if std_ret > 0 else 0.0
        
        # Max Drawdown
        cum_ret = (1 + returns).cumprod()
        running_max = cum_ret.cummax()
        drawdown = (cum_ret - running_max) / running_max
        max_dd = abs(drawdown.min())
        
        # Normalize score
        # Sharpe typically ranges -3 to 3 for daily returns, but for short periods can vary.
        # We normalize: sharpe 0-2 -> 0.0-1.0
        sharpe_score = max(0.0, min(1.0, sharpe / 2.0))
        
        # Penalize by drawdown: 1.0 - max_dd (if dd is 0.5, score is 0.5)
        dd_score = max(0.0, 1.0 - max_dd)
        
        final_score = (sharpe_score * 0.7) + (dd_score * 0.3)
        
        return round(max(0.0, min(1.0, float(final_score))), 4)

    except Exception as e:
        log.error(f"rar_scorer error for {ticker}: {e}")
        return 0.0
