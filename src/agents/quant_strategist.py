# src/agents/quant_strategist.py
from typing import List, Dict, Any
from crewai import Agent
from crewai.tools import tool
from src.utils.logger import get_logger
from src.state import db
from src.tools.momentum_scorer import momentum_scorer
from src.tools.rar_scorer import rar_scorer
from src.tools.onchain_scorer import onchain_scorer
from src.tools.narrative_scorer import narrative_scorer

log = get_logger(__name__)

@tool("momentum_scorer_tool")
def momentum_scorer_tool(ticker: str) -> float:
    """Calculates momentum score for a given ticker. Returns float 0.0-1.0."""
    return momentum_scorer(ticker)

@tool("rar_scorer_tool")
def rar_scorer_tool(ticker: str) -> float:
    """Calculates risk-adjusted return score for a given ticker. Returns float 0.0-1.0."""
    return rar_scorer(ticker)

@tool("onchain_scorer_tool")
def onchain_scorer_tool(ticker: str) -> float:
    """Calculates on-chain health score for a given ticker. Returns float 0.0-1.0."""
    return onchain_scorer(ticker)

@tool("narrative_scorer_tool")
def narrative_scorer_tool(ticker: str) -> float:
    """Calculates narrative sentiment score for a given ticker. Returns float 0.0-1.0."""
    return narrative_scorer(ticker)

class QuantStrategist:
    def __init__(self):
        self.agent = Agent(
            role="Quant Strategist",
            goal="Calculate FAS scores and identify high-quality trade signals",
            backstory=(
                "You are a top-tier quantitative researcher. You use deterministic "
                "scoring tools to evaluate market quality and generate alpha signals."
            ),
            tools=[
                momentum_scorer_tool, 
                rar_scorer_tool, 
                onchain_scorer_tool, 
                narrative_scorer_tool
            ],
            verbose=True,
            allow_delegation=False
        )

    def _get_weights(self) -> Dict[str, float]:
        """Read weights from system_config or fallback to defaults."""
        defaults = {
            "ms": 0.4,
            "rar": 0.2,
            "ochs": 0.3,
            "ns": 0.1
        }
        weights = {}
        for key, default in defaults.items():
            val = db.get_config(f"fas_weight_{key}")
            weights[key] = float(val) if val is not None else default
        return weights

    def run_analysis(self, tickers: List[str]) -> List[Dict[str, Any]]:
        """
        Analyze list of tickers and return signals with FAS >= 0.75.
        Logs every ticker analyzed.
        """
        weights = self._get_weights()
        signals = []

        for ticker in tickers:
            ms = momentum_scorer(ticker)
            rar = rar_scorer(ticker)
            ochs = onchain_scorer(ticker)
            ns = narrative_scorer(ticker)

            fas = (weights["ms"] * ms) + \
                  (weights["rar"] * rar) + \
                  (weights["ochs"] * ochs) + \
                  (weights["ns"] * ns)
            
            fas = round(fas, 4)
            
            log.info(f"ticker={ticker} ms={ms} rar={rar} ochs={ochs} ns={ns} fas={fas}")

            if fas >= 0.75:
                # Need sector info for Risk Guardian
                cache = db.get_market_cache(ticker)
                sector = cache["sector"] if cache else "unknown"
                
                signals.append({
                    "ticker": ticker,
                    "fas_score": fas,
                    "ms": ms,
                    "rar": rar,
                    "ochs": ochs,
                    "ns": ns,
                    "sector": sector
                })

        return signals
