# src/agents/overseer.py
"""
Overseer Agent — System Orchestrator & Tick Controller.
Manages the 15-second cycle. Never executes trades directly.
Delegation order: Data Oracle → Quant Strategist → Risk Guardian → Execution Trader → Accountant.
"""
import asyncio
from typing import Any
from src.utils.logger import get_logger
from src.state import db
from src.utils import telegram_notifier

log = get_logger(__name__)

_agent_failure_counts: dict[str, int] = {}
MAX_AGENT_FAILURES = 3


async def run_cycle(tick_count: int) -> None:
    """
    Full pipeline for one 15-second tick.
    Checks EMERGENCY_STOP first (already checked by daemon, but double-check here).
    """
    log.info(f"overseer: tick #{tick_count} begin")

    # Double-check emergency stop
    if db.get_config("EMERGENCY_STOP") == "TRUE":
        log.warning(f"overseer: EMERGENCY_STOP — cycle aborted")
        return

    # ── Step 1: Data Oracle ────────────────────────────────────────────────
    tickers = await _delegate("data_oracle", _run_data_oracle, tick_count)
    if tickers is None:
        log.error("overseer: data_oracle failed — skipping cycle")
        return

    # ── Step 2: Quant Strategist ───────────────────────────────────────────
    signals = await _delegate("quant_strategist", _run_quant, tickers, tick_count)
    if signals is None or len(signals) == 0:
        log.info(f"overseer: no FAS signals this cycle (tick #{tick_count})")
        _push_feed_event("OVERSEER", f"Tick #{tick_count} — no signals above 0.75")
        return

    log.info(f"overseer: {len(signals)} signals → Risk Guardian")

    # ── Step 3: Portfolio state for Risk Guardian ──────────────────────────
    try:
        from src.execution_bridge import grpc_client
        portfolio = grpc_client.get_portfolio()
        portfolio["drawdown"] = _calculate_drawdown(portfolio["total_capital"])
    except Exception as e:
        log.error(f"overseer: could not get portfolio state: {e}")
        portfolio = {"total_capital": 0.0, "available_capital": 0.0,
                     "drawdown": 0.0, "positions": []}

    # ── Step 4: Risk Guardian + Execution ─────────────────────────────────
    approved_count = 0
    for signal in signals:
        result = await _delegate(
            "risk_execution",
            _run_risk_and_execute,
            signal, portfolio, tick_count,
        )
        if result and result.get("executed"):
            approved_count += 1
            # Update portfolio available capital for next signal
            portfolio["available_capital"] -= result.get("size_usd", 0)

    # ── Step 5: Accountant health check ───────────────────────────────────
    await _delegate("accountant", _run_accountant_healthcheck, tick_count)

    log.info(f"overseer: tick #{tick_count} complete. {approved_count}/{len(signals)} executed.")
    _push_feed_event(
        "OVERSEER",
        f"Cycle #{tick_count} done — {len(signals)} signals, {approved_count} executed"
    )


# ── Internal step runners ─────────────────────────────────────────────────

async def _run_data_oracle(tick_count: int) -> list[str]:
    from src.agents.data_oracle import run_fetch_cycle
    tickers = await run_fetch_cycle()
    _push_feed_event("ORACLE", f"Cache updated — {len(tickers)} tickers ready")
    return tickers


async def _run_quant(tickers: list[str], tick_count: int) -> list[dict]:
    from src.agents.quant_strategist import QuantStrategist
    qs = QuantStrategist()
    signals = qs.run_analysis(tickers)
    _push_feed_event(
        "QUANT",
        f"{len(signals)} signals FAS≥0.75 from {len(tickers)} tickers"
    )
    return signals


async def _run_risk_and_execute(
    signal: dict[str, Any],
    portfolio: dict[str, Any],
    tick_count: int,
) -> dict[str, Any]:
    from src.agents.risk_guardian import RiskGuardian
    from src.agents.execution_trader import execute_approved_order
    from src.agents.accountant import process_trade_result

    ticker = signal["ticker"]
    rg = RiskGuardian()
    eval_result = rg.evaluate_signal(signal, portfolio)

    if not eval_result["approved"]:
        _push_feed_event("RISK", f"✗ VETO {ticker} — {eval_result['reason']}")
        return {"executed": False, "reason": eval_result["reason"]}

    size_usd = eval_result["position_size_usd"]
    _push_feed_event("RISK", f"✓ Approved {ticker} size=${size_usd:.2f}")

    # Execute
    exec_result = await execute_approved_order(
        ticker=ticker,
        size_usd=size_usd,
        fas_score=signal["fas_score"],
    )

    if not exec_result["success"]:
        _push_feed_event("TRADER", f"✗ Failed {ticker} — {exec_result['error']}")
        return {"executed": False, "reason": exec_result["error"]}

    _push_feed_event(
        "TRADER",
        f"✓ TX confirmed {ticker} tx={exec_result['tx_hash'][:12]}..."
    )

    # Accountant processes the result (for paper trading, entry = exit for demo)
    # In real trading, exit is tracked separately when position is closed
    # Here we just record the entry
    _push_feed_event(
        "ACCOUNTANT",
        f"Trade #{exec_result['trade_id'][:8]} logged"
    )

    return {"executed": True, "size_usd": size_usd, "trade_id": exec_result["trade_id"]}


async def _run_accountant_healthcheck(tick_count: int) -> None:
    from src.agents.accountant import run_ops_health_check
    await run_ops_health_check()


# ── Delegation wrapper ────────────────────────────────────────────────────

async def _delegate(agent_name: str, fn, *args, **kwargs):
    """
    Run an agent function. Track failures. Alert on 3 consecutive failures.
    Returns None on failure.
    """
    try:
        result = await fn(*args, **kwargs) if asyncio.iscoroutinefunction(fn) else fn(*args, **kwargs)
        _agent_failure_counts[agent_name] = 0  # reset on success
        return result
    except Exception as e:
        count = _agent_failure_counts.get(agent_name, 0) + 1
        _agent_failure_counts[agent_name] = count
        log.error(f"overseer: {agent_name} failed (#{count}): {e}")
        if count >= MAX_AGENT_FAILURES:
            asyncio.create_task(
                telegram_notifier.async_send_emergency_alert(
                    f"Agent '{agent_name}' failed {count} consecutive times. Last: {e}"
                )
            )
        return None


# ── Dashboard feed push ───────────────────────────────────────────────────

def _push_feed_event(agent: str, message: str) -> None:
    """Non-blocking push to dashboard WebSocket clients."""
    async def _push():
        try:
            from src.api.main import broadcast_event
            await broadcast_event("agent_activity", {
                "agent": agent,
                "message": message,
            })
        except Exception:
            pass  # Dashboard not connected — non-fatal

    try:
        loop = asyncio.get_running_loop()
        loop.create_task(_push())
    except RuntimeError:
        pass


def _calculate_drawdown(current_capital: float) -> float:
    """
    Calculate drawdown from peak capital in system_config.
    Updates peak if current is higher.
    """
    peak_str = db.get_config("peak_capital")
    peak = float(peak_str) if peak_str else current_capital

    if current_capital > peak:
        db.set_config("peak_capital", str(current_capital))
        return 0.0

    if peak == 0:
        return 0.0

    return (peak - current_capital) / peak
