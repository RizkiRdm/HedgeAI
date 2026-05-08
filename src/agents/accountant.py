# src/agents/accountant.py
import asyncio
from typing import Dict, Any, Optional
from src.utils.logger import get_logger
from src.utils import telegram_notifier
from src.state import db

log = get_logger(__name__)

# Constants from GEMINI.md
PROFIT_TAX_RATE = 0.005  # 0.5%
MONTHLY_BURN_RATE = 50.0 # Default, should ideally be in system_config

async def process_trade_result(ticker: str, entry_p: float, exit_p: float, size: float, tx_hash: str) -> None:
    """
    Handle financial recording after a trade is closed.
    Collects profit tax and updates trade history.
    """
    gross_pnl = (exit_p - entry_p) * size
    profit_tax = 0.0
    net_pnl = gross_pnl

    if gross_pnl > 0:
        profit_tax = gross_pnl * PROFIT_TAX_RATE
        net_pnl = gross_pnl - profit_tax
        
        # Update ops fund in DB (assumes db.py has these methods or we use raw SQL)
        # For now, we simulate with log and DB calls if they exist
        try:
            db.update_ops_fund(profit_tax)
            db.log_ops_transaction(amount=profit_tax, category="profit_tax", description=f"Tax from {ticker}")
        except Exception as e:
            log.error(f"Accountant: Failed to update ops fund: {e}")

    try:
        # Log to trade_history
        # Assuming schema: ticker, entry_p, exit_p, pnl, tx_hash
        db.insert_trade(ticker=ticker, entry_p=entry_p, exit_p=exit_p, pnl=net_pnl, tx_hash=tx_hash)
    except Exception as e:
        log.error(f"Accountant: Failed to log trade history: {e}")

    log.info(f"Accountant: Processed {ticker} | Gross: ${gross_pnl:.2f} | Tax: ${profit_tax:.2f} | Net: ${net_pnl:.2f}")

async def run_ops_health_check() -> None:
    """
    Periodic check of ops fund sustainability.
    """
    try:
        balance = db.get_ops_fund_balance()
        monthly_burn = float(db.get_config("monthly_burn_rate") or MONTHLY_BURN_RATE)
        
        if monthly_burn > 0:
            runway = balance / monthly_burn
        else:
            runway = 999.0

        log.info(f"Accountant: Ops Balance ${balance:.2f} | Runway {runway:.1f} months")

        if balance < monthly_burn:
            await telegram_notifier.send_ops_warning(balance, monthly_burn, runway)
            if balance < (monthly_burn * 0.5):
                log.critical("Accountant: OPS FUND CRITICAL - Below 0.5x burn")
    except Exception as e:
        log.error(f"Accountant: Health check failed: {e}")

# Helper placeholders if not in db.py - should be moved to db.py eventually
def _ensure_db_helpers():
    """Mock/ensure methods exist in db module for this agent."""
    pass
