# src/agents/risk_guardian.py
from typing import Dict, Any, List
from src.utils.logger import get_logger
from src.utils import telegram_notifier
from src.state import db
from src.core.kelly_sizer import calculate_kelly

log = get_logger(__name__)

class RiskGuardian:
    def __init__(self):
        # Configuration - following PLAN.md hardcoded rules
        self.max_drawdown = 0.15
        self.sector_cap = 3
        self.min_position_size = 5.0
        self.max_slippage = 0.02
        self.allowed_chains = ["SOL", "BSC", "BASE", "ETH"]

    def evaluate_signal(self, signal: Dict[str, Any], portfolio_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a trade signal against risk constraints.
        Returns: {"approved": bool, "reason": str, "position_size_usd": float}
        """
        ticker = signal["ticker"]
        fas_score = signal["fas_score"]
        sector = signal["sector"]
        
        total_capital = portfolio_state.get("total_capital", 0.0)
        available_capital = portfolio_state.get("available_capital", 0.0)
        drawdown = portfolio_state.get("drawdown", 0.0)
        positions = portfolio_state.get("positions", [])

        # 1. Equity Drawdown > 15%?
        if drawdown > self.max_drawdown:
            db.set_config("EMERGENCY_STOP", "TRUE")
            telegram_notifier.send_emergency_alert(f"Drawdown exceeded 15%: {drawdown:.1%}")
            log.error(f"VETO {ticker}: drawdown_limit ({drawdown:.1%})")
            return {"approved": False, "reason": "drawdown_limit", "position_size_usd": 0.0}

        # 2. Sector already has 3 active positions?
        sector_count = sum(1 for p in positions if p.get("sector") == sector)
        if sector_count >= self.sector_cap:
            log.warning(f"VETO {ticker}: sector_cap ({sector})")
            return {"approved": False, "reason": "sector_cap", "position_size_usd": 0.0}

        # 3. Chain eligible?
        chain = ticker.split("/")[1] if "/" in ticker else "unknown"
        if chain not in self.allowed_chains:
            log.warning(f"VETO {ticker}: chain_not_eligible ({chain})")
            return {"approved": False, "reason": "chain_not_eligible", "position_size_usd": 0.0}
        
        if chain == "ETH" and total_capital < 1000.0:
            log.warning(f"VETO {ticker}: eth_capital_low (${total_capital})")
            return {"approved": False, "reason": "chain_not_eligible", "position_size_usd": 0.0}

        # 4. Estimated slippage > 2.0%?
        # Note: Estimated slippage comes from signal or dry-run, 
        # here we check if signal already contains it.
        est_slippage = signal.get("estimated_slippage", 0.0)
        if est_slippage > self.max_slippage:
            log.warning(f"VETO {ticker}: slippage_too_high ({est_slippage:.1%})")
            return {"approved": False, "reason": "slippage_too_high", "position_size_usd": 0.0}

        # 5. Position Sizing
        # Kelly input: we need win_rate and avg_rr. 
        # For signal evaluation, we read these from config or use defaults.
        win_rate = float(db.get_config("win_rate") or 0.5)
        avg_rr = float(db.get_config("avg_rr") or 2.0)
        
        kelly_pct = calculate_kelly(win_rate, avg_rr)
        position_size = total_capital * kelly_pct

        # 6. Below minimum size?
        if position_size < self.min_position_size:
            log.warning(f"VETO {ticker}: below_minimum_size (${position_size:.2f})")
            return {"approved": False, "reason": "below_minimum_size", "position_size_usd": 0.0}

        # Ensure we don't exceed available capital
        position_size = min(position_size, available_capital)

        log.info(f"APPROVED {ticker}: size=${position_size:.2f} fas={fas_score}")
        return {
            "approved": True, 
            "reason": "", 
            "position_size_usd": round(position_size, 2)
        }
