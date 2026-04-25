# src/tools/momentum_scorer.py
import pandas as pd
import pandas_ta as ta
from typing import Any, List
from src.utils.logger import get_logger

log = get_logger(__name__)

def momentum_scorer(ticker: str) -> float:
    """
    Calculates momentum score from DuckDB cached data.
    Returns: float 0.0–1.0  (0.0 = bearish, 1.0 = bullish)
    """
    from src.state.db import get_market_cache
    
    try:
        cache = get_market_cache(ticker)
        if not cache:
            log.warning(f"momentum_scorer: no cache for {ticker}, returning 0.0")
            return 0.0

        metrics = cache.get("metrics_json", {})
        ohlcv = metrics.get("ohlcv_24h") # Expect list of [t, o, h, l, c, v]
        
        if not ohlcv or len(ohlcv) < 20: # Need enough data for MACD/RSI
            log.warning(f"momentum_scorer: insufficient data for {ticker}, returning 0.0")
            return 0.0

        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        
        # RSI (14)
        rsi = df.ta.rsi(length=14)
        current_rsi = rsi.iloc[-1] if not rsi.empty else 50.0
        rsi_norm = current_rsi / 100.0

        # MACD
        macd = df.ta.macd()
        if macd is not None and not macd.empty:
            # Safely find histogram column (contains 'MACDh')
            hist_col = [c for c in macd.columns if "MACDh" in c]
            if hist_col:
                hist = macd.iloc[-1][hist_col[0]]
                macd_signal = 1.0 if hist > 0 else 0.0
            else:
                macd_signal = 0.5
        else:
            macd_signal = 0.5

        # Price Velocity (Change over last 5 intervals)
        price_change = (df["close"].iloc[-1] - df["close"].iloc[-5]) / df["close"].iloc[-5]
        velocity_signal = 1.0 if price_change > 0 else 0.0

        # Weighted score
        score = (rsi_norm * 0.5) + (macd_signal * 0.3) + (velocity_signal * 0.2)
        
        return round(max(0.0, min(1.0, float(score))), 4)

    except Exception as e:
        log.error(f"momentum_scorer error for {ticker}: {e}")
        return 0.0
