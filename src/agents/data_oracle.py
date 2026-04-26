# src/agents/data_oracle.py
"""
Data Oracle Agent — Market Data Fetcher & Cache Manager.
Owns all data ingestion. Serves clean data to other agents via DuckDB.
Never passes raw data to agents — only tickers with cached metrics.
"""
import asyncio
import time
from datetime import datetime, timezone
from typing import Optional
from src.utils.logger import get_logger
from src.state import db
from src.tools.market_fetcher import fetch_dexscreener_batch, fetch_full_metrics

log = get_logger(__name__)

# Canonical watchlist — in production, loaded from system_config
DEFAULT_WATCHLIST = [
    "SOL/USDC", "BNB/USDC", "ETH/USDC", "AVAX/USDC", "MATIC/USDC",
    "ARB/USDC", "OP/USDC", "JUP/USDC", "BONK/USDC", "WIF/USDC",
    "PYTH/USDC", "JTO/USDC", "RNDR/USDC", "HNT/USDC", "DRIFT/USDC",
    "KMNO/USDC", "CLOUD/USDC", "ZETA/USDC", "ATLAS/USDC", "SHDW/USDC",
]

# Sector classification — in production, load from system_config or external source
SECTOR_MAP: dict[str, str] = {
    "SOL": "L1", "ETH": "L1", "BNB": "L1", "AVAX": "L1", "MATIC": "L2",
    "ARB": "L2", "OP": "L2", "JUP": "DeFi", "BONK": "Meme", "WIF": "Meme",
    "PYTH": "DeFi", "JTO": "DeFi", "RNDR": "AI", "HNT": "DePIN",
    "DRIFT": "DeFi", "KMNO": "DeFi", "CLOUD": "AI", "ZETA": "DeFi",
    "ATLAS": "GameFi", "SHDW": "DePIN",
}

_CACHE_FRESHNESS_SECONDS = 15


def _is_stale(last_updated: Optional[datetime]) -> bool:
    """Check if cache entry is older than 15 seconds."""
    if last_updated is None:
        return True
    if last_updated.tzinfo is None:
        last_updated = last_updated.replace(tzinfo=timezone.utc)
    age = (datetime.now(timezone.utc) - last_updated).total_seconds()
    return age > _CACHE_FRESHNESS_SECONDS


def get_watchlist() -> list[str]:
    """Load watchlist from system_config, fallback to default."""
    raw = db.get_config("watchlist_json")
    if raw:
        import json
        try:
            return json.loads(raw)
        except Exception:
            pass
    return DEFAULT_WATCHLIST


async def run_fetch_cycle() -> list[str]:
    """
    Main fetch cycle. Called by Overseer every tick.
    1. Check which tickers need refresh (stale > 15s)
    2. Batch fetch from DexScreener first
    3. Fetch full metrics (CCXT + Covalent + CryptoPanic) for stale tickers
    4. Update DuckDB market_cache
    5. Return list of fresh ticker names for Quant Strategist
    Returns: list of tickers that are now fresh and ready to score.
    """
    watchlist = get_watchlist()
    stale_tickers: list[str] = []

    for ticker in watchlist:
        cached = db.get_market_cache(ticker)
        if cached is None or _is_stale(cached.get("last_updated")):
            stale_tickers.append(ticker)

    if not stale_tickers:
        log.info(f"data_oracle: all {len(watchlist)} tickers fresh, skipping fetch")
        return watchlist

    log.info(f"data_oracle: {len(stale_tickers)} stale tickers, fetching...")

    # Batch DexScreener first (most efficient)
    dex_batch = await fetch_dexscreener_batch(stale_tickers)

    # Full metrics per ticker (parallel, max 10 concurrent)
    sem = asyncio.Semaphore(10)

    async def _fetch_one(ticker: str) -> None:
        async with sem:
            try:
                metrics = await fetch_full_metrics(ticker)
                if metrics is None:
                    # Fallback: mark cache as STALE but keep old data
                    cached = db.get_market_cache(ticker)
                    if cached:
                        old_metrics = cached["metrics_json"]
                        old_metrics["_stale"] = True
                        db.update_market_cache(ticker, cached["sector"], old_metrics)
                    log.warning(f"data_oracle: {ticker} fetch failed, keeping cached (STALE)")
                    return

                # Inject dex data if available
                if ticker in dex_batch:
                    dex = dex_batch[ticker]
                    metrics["dex_price_usd"] = dex.get("priceUsd")
                    metrics["volume_24h"] = dex.get("volume", {}).get("h24")
                    metrics.pop("_stale", None)

                sector = SECTOR_MAP.get(ticker.split("/")[0], "Unknown")
                db.update_market_cache(ticker, sector, metrics)
                log.debug(f"data_oracle: {ticker} cached OK")

            except Exception as e:
                log.error(f"data_oracle: unhandled error for {ticker}: {e}")

    await asyncio.gather(*[_fetch_one(t) for t in stale_tickers])

    fresh_count = len(watchlist) - len(stale_tickers) + len(stale_tickers)
    log.info(f"data_oracle: fetch cycle complete. {fresh_count} tickers ready.")

    # Hourly DuckDB checkpoint
    _maybe_checkpoint()

    return watchlist


_last_checkpoint: float = 0.0


def _maybe_checkpoint() -> None:
    global _last_checkpoint
    now = time.time()
    if now - _last_checkpoint > 3600:
        try:
            db.checkpoint()
            _last_checkpoint = now
            log.info("data_oracle: DuckDB checkpoint complete")
        except Exception as e:
            log.error(f"data_oracle: checkpoint failed: {e}")
