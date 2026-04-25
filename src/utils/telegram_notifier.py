# src/utils/telegram_notifier.py
import os
import asyncio
from typing import Optional, Any
from telegram import Bot
from telegram.constants import ParseMode
from src.utils.logger import get_logger
from src.state import db

log = get_logger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def _send_message(text: str) -> bool:
    """Helper to send telegram message safely."""
    if not TOKEN or not CHAT_ID:
        log.warning("Telegram TOKEN or CHAT_ID not set, skipping message")
        return False
    
    try:
        bot = Bot(token=TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode=ParseMode.MARKDOWN)
        return True
    except Exception as e:
        log.error(f"Failed to send Telegram message: {e}")
        return False

def send_trade_executed(ticker: str, pnl: float, fas_score: float, tx_hash: str) -> None:
    """Notify user of executed trade."""
    emoji = "🟢" if pnl >= 0 else "🔴"
    text = (
        f"{emoji} *Trade Executed*\n"
        f"Ticker: `{ticker}`\n"
        f"PnL: `${pnl:.2f}`\n"
        f"FAS Score: `{fas_score:.2f}`\n"
        f"TX: [Hash](https://etherscan.io/tx/{tx_hash})"
    )
    asyncio.run(_send_message(text))

def send_emergency_alert(reason: str) -> None:
    """Notify user of emergency stop."""
    text = (
        f"🚨 *EMERGENCY STOP TRIGGERED*\n"
        f"Reason: {reason}\n"
        f"Bot has paused all operations."
    )
    asyncio.run(_send_message(text))

def send_formula_proposal(current: str, proposed: str, reason: str, expected_impact: str) -> None:
    """Notify user of formula change proposal."""
    text = (
        f"📊 *Formula Change Proposal*\n"
        f"Current: `{current}`\n"
        f"Proposed: `{proposed}`\n"
        f"Reason: {reason}\n"
        f"Expected Impact: {expected_impact}"
    )
    asyncio.run(_send_message(text))

def send_bill_notification(service: str, amount: float, due_date: str, days_until_due: int) -> None:
    """Notify user of upcoming bill."""
    text = (
        f"📅 *Upcoming Bill*\n"
        f"Service: `{service}`\n"
        f"Amount: `${amount:.2f}`\n"
        f"Due Date: {due_date} ({days_until_due} days left)"
    )
    asyncio.run(_send_message(text))

def send_bill_paid(service: str, amount: float, auto_executed: bool) -> None:
    """Confirm bill payment."""
    status = "Auto-paid" if auto_executed else "Paid"
    text = (
        f"✅ *Bill Paid*\n"
        f"Service: `{service}`\n"
        f"Amount: `${amount:.2f}`\n"
        f"Status: {status}"
    )
    asyncio.run(_send_message(text))

def send_ops_warning(balance: float, monthly_burn: float, runway_months: float) -> None:
    """Notify user of low ops fund balance."""
    text = (
        f"⚠️ *Ops Fund Warning*\n"
        f"Balance: `${balance:.2f}`\n"
        f"Monthly Burn: `${monthly_burn:.2f}`\n"
        f"Estimated Runway: `{runway_months:.1f} months`"
    )
    asyncio.run(_send_message(text))

# Note: Command handlers are typically in a separate bot loop, 
# but PLAN.md mentions them here. Implementation will focus on logic.

async def handle_panic_command() -> None:
    """Process /panic command."""
    db.set_config("EMERGENCY_STOP", "TRUE")
    await _send_message("😱 Panic received. EMERGENCY_STOP set to TRUE.")

async def handle_resume_command() -> None:
    """Process /resume command."""
    db.set_config("EMERGENCY_STOP", "FALSE")
    await _send_message("✅ Resume received. EMERGENCY_STOP set to FALSE.")

async def handle_status_command() -> None:
    """Process /status command."""
    stop = db.get_config("EMERGENCY_STOP")
    balance = db.get_ops_fund_balance()
    text = (
        f"🤖 *Bot Status*\n"
        f"EMERGENCY_STOP: `{stop}`\n"
        f"Ops Balance: `${balance:.2f}`"
    )
    await _send_message(text)
