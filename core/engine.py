import logging
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AlphaMetrics:
    market_sentiment: float  # MS (0-100)
    risk_adjusted_return: float  # RAR (0-100)
    on_chain_health: float  # OCHS (0-100)
    network_strength: float  # NS (0-100)

class AlphaEngine:
    """
    Implementation of the FAS (Final Alpha Score) formula.
    FAS = (0.4 * MS) + (0.2 * RAR) + (0.3 * OCHS) + (0.1 * NS)
    """
    
    @staticmethod
    def calculate_fas(metrics: AlphaMetrics) -> float:
        try:
            fas = (
                (0.4 * metrics.market_sentiment) +
                (0.2 * metrics.risk_adjusted_return) +
                (0.3 * metrics.on_chain_health) +
                (0.1 * metrics.network_strength)
            )
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
