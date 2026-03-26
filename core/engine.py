import logging
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AlphaMetrics:
    # Screening Layer (8 metrics)
    liquidity_usd: float
    pair_age_hours: float
    volume_24h_usd: float
    top10_holder_pct: float
    buy_tax_pct: float
    sell_tax_pct: float
    holder_count: int
    has_social_links: bool

    # Quantitative Analysis (14 metrics - simplified for scoring)
    momentum_score: float  # RSI, MACD, etc.
    volume_score: float    # OBV, Vol Change, etc.
    volatility_score: float # ATR, BB, etc.

    # Contextual Intelligence (6 metrics)
    smart_money_flow: float
    cex_announcement: bool
    social_volume_24h: float
    kol_mentions_count: int
    github_commits_30d: int
    funding_rate: float

class AlphaEngine:
    """
    Implementation of the FAS (Final Alpha Score) formula.
    FAS = (0.4 * MS) + (0.2 * RAR) + (0.3 * OCHS) + (0.1 * NS)
    """
    
    @staticmethod
    def calculate_fas(metrics: AlphaMetrics) -> float:
        try:
            # 1. Momentum Score (MS)
            ms = metrics.momentum_score
            
            # 2. Risk-Adjusted Return (RAR)
            # Simplified: Expected Return / Volatility
            rar = metrics.volume_score / (metrics.volatility_score + 0.001)
            
            # 3. On-Chain Health Score (OCHS)
            # Simplified: Liquidity + Holder Growth - Concentration
            ochs = (metrics.liquidity_usd / 1000000) + (metrics.holder_count / 1000) - (metrics.top10_holder_pct / 100)
            
            # 4. Sentiment / Narrative Score (NS)
            ns = (metrics.social_volume_24h / 1000) + (metrics.kol_mentions_count / 10)

            # Normalize components to 0-100 (simplified)
            ms = min(max(ms, 0), 100)
            rar = min(max(rar * 10, 0), 100)
            ochs = min(max(ochs * 20, 0), 100)
            ns = min(max(ns * 5, 0), 100)

            fas = (0.4 * ms) + (0.2 * rar) + (0.3 * ochs) + (0.1 * ns)
            return round(fas, 2)
        except Exception as e:
            logging.error(f"Error calculating FAS: {e}")
            return 0.0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> float:
        """Helper to calculate FAS from raw dictionary data"""
        metrics = AlphaMetrics(
            market_sentiment=data.get('ms', 0.0),
            risk_adjusted_return=data.get('rar', 0.0),
            on_chain_health=data.get('ochs', 0.0),
            network_strength=data.get('ns', 0.0)
        )
        return cls.calculate_fas(metrics)
