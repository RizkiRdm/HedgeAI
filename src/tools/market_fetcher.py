# src/tools/market_fetcher.py
import asyncio
import httpx
import ccxt.async_support as ccxt
from typing import Dict, Any, Optional, List
from src.utils.logger import get_logger

log = get_logger(__name__)

class MarketFetcher:
    """
    Deterministic tool to fetch raw market data.
    Follows GEMINI.md rules: max 3 retries, exponential backoff.
    """
    
    def __init__(self):
        self.dex_base_url = "https://api.dexscreener.com/latest/dex/pairs"
        self.client = httpx.AsyncClient(timeout=10.0)
        self.exchanges = {
            "okx": ccxt.okx(),
            "binance": ccxt.binance()
        }

    async def _retry_request(self, func, *args, **kwargs) -> Optional[Any]:
        """Generic retry logic: 3 attempts, exponential backoff (1s, 2s, 4s)."""
        for attempt in range(3):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                wait = 2**attempt
                log.warning(f"Attempt {attempt+1} failed: {e}. Retrying in {wait}s...")
                await asyncio.sleep(wait)
        log.error(f"All 3 attempts failed for {func.__name__}")
        return None

    async def fetch_dex_screener(self, chain_id: str, pair_address: str) -> Optional[Dict[str, Any]]:
        """Fetch data from DexScreener for a specific pair."""
        url = f"{self.dex_base_url}/{chain_id}/{pair_address}"
        
        async def _do_fetch():
            resp = await self.client.get(url)
            resp.raise_for_status()
            data = resp.json()
            if not data.get("pairs"):
                raise ValueError(f"No pair data found for {chain_id}/{pair_address}")
            return data["pairs"][0]

        return await self._retry_request(_do_fetch)

    async def fetch_ccxt_price(self, ticker: str, exchange_id: str = "okx") -> Optional[float]:
        """Fetch latest price from a CEX via CCXT."""
        exchange = self.exchanges.get(exchange_id)
        if not exchange:
            log.error(f"Exchange {exchange_id} not supported")
            return None

        async def _do_fetch():
            # Ensure exchange is loaded
            ticker_data = await exchange.fetch_ticker(f"{ticker}/USDT")
            return float(ticker_data["last"])

        return await self._retry_request(_do_fetch)

    async def fetch_onchain_metrics(self, chain_id: str, pair_address: str) -> Dict[str, Any]:
        """
        Aggregates metrics for On-Chain Scorer.
        Returns normalized structure for tools to consume.
        """
        data = await self.fetch_dex_screener(chain_id, pair_address)
        if not data:
            return {}

        return {
            "liquidity": float(data.get("liquidity", {}).get("usd", 0)),
            "volume_24h": float(data.get("volume", {}).get("h24", 0)),
            "price_change_24h": float(data.get("priceChange", {}).get("h24", 0)),
            "pair_created_at": data.get("pairCreatedAt"),
            "market_cap": float(data.get("fdv", 0))  # FDV as proxy for mcap on new pairs
        }

    async def close(self):
        """Clean up connections."""
        await self.client.aclose()
        for exchange in self.exchanges.values():
            await exchange.close()

# Singleton instance for easy access
fetcher = MarketFetcher()
