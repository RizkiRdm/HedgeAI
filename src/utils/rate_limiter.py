# src/utils/rate_limiter.py
"""
Token bucket rate limiter per domain.
Prevents hitting free-tier API limits on DexScreener, Covalent, CryptoPanic.
Thread-safe via asyncio.Lock.
"""
import asyncio
import time
from dataclasses import dataclass, field
from typing import Dict
from src.utils.logger import get_logger

log = get_logger(__name__)

@dataclass
class TokenBucket:
    """Single token bucket for one domain."""
    capacity: float          # max tokens (burst limit)
    refill_rate: float       # tokens per second
    tokens: float = field(init=False)
    last_refill: float = field(init=False)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock, init=False)

    def __post_init__(self) -> None:
        self.tokens = self.capacity
        self.last_refill = time.monotonic()

    async def acquire(self, tokens: float = 1.0) -> None:
        """Wait until enough tokens are available, then consume them."""
        async with self.lock:
            while True:
                now = time.monotonic()
                elapsed = now - self.last_refill
                self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
                self.last_refill = now

                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return

                wait_time = (tokens - self.tokens) / self.refill_rate
                await asyncio.sleep(wait_time)


# Per-domain rate limits (empirically tuned for free tiers)
_DOMAIN_LIMITS: Dict[str, Dict[str, float]] = {
    "dexscreener": {"capacity": 5.0, "refill_rate": 2.0},    # 2 req/s, burst 5
    "covalent":    {"capacity": 3.0, "refill_rate": 0.5},    # 30 req/min
    "cryptopanic": {"capacity": 3.0, "refill_rate": 0.2},    # 12 req/min
    "alternative": {"capacity": 1.0, "refill_rate": 0.016},  # ~1 req/min
    "okx":         {"capacity": 10.0, "refill_rate": 5.0},   # 5 req/s, burst 10
}

_buckets: Dict[str, TokenBucket] = {}


def get_bucket(domain: str) -> TokenBucket:
    """Get or create a token bucket for a domain."""
    if domain not in _buckets:
        limits = _DOMAIN_LIMITS.get(domain, {"capacity": 3.0, "refill_rate": 1.0})
        _buckets[domain] = TokenBucket(**limits)
    return _buckets[domain]


async def throttle(domain: str, tokens: float = 1.0) -> None:
    """Throttle a call to the given domain. Awaitable."""
    bucket = get_bucket(domain)
    await bucket.acquire(tokens)
    log.debug(f"rate_limiter: {domain} token acquired")
