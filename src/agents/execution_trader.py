# src/agents/execution_trader.py
import asyncio
from typing import Dict, Any, Optional
from src.utils.logger import get_logger
from src.utils import telegram_notifier
from src.execution_bridge import grpc_client

log = get_logger(__name__)

async def execute_approved_order(ticker: str, size_usd: float, fas_score: float) -> Dict[str, Any]:
    """
    Final gate before money moves.
    Mandatory dry-run check before execution.
    """
    log.info(f"ExecutionTrader: Processing {ticker} size=${size_usd:.2f}")

    try:
        # 1. Mandatory Dry-Run via gRPC
        # We assume size_usd is converted to native amount if needed by Go engine, 
        # or Go engine handles USD sizes.
        dry_run = grpc_client.dry_run_swap(ticker, size_usd)
        
        if not dry_run.get("success"):
            log.error(f"Dry-run failed for {ticker}: {dry_run.get('error')}")
            return {"success": False, "error": f"dry_run_failed: {dry_run.get('error')}"}

        est_slippage = dry_run.get("estimated_slippage", 0.0)
        
        # 2. Final Slippage Check (Hardcoded 2.0% as per GEMINI.md)
        if est_slippage > 0.02:
            log.warning(f"Execution aborted: slippage {est_slippage:.2%} > 2.0%")
            await telegram_notifier.send_emergency_alert(
                f"Execution ABORTED for {ticker}: Slippage {est_slippage:.2%} exceeds 2% limit"
            )
            return {"success": False, "error": "slippage_too_high"}

        # 3. Real Execution via gRPC
        log.info(f"ExecutionTrader: Executing swap for {ticker}...")
        exec_result = grpc_client.execute_swap(ticker, size_usd)
        
        if not exec_result.get("success"):
            # Retry once if specified in GEMINI.md (Step 8 of Execution Protocol)
            log.warning(f"Execution failed, retrying once: {exec_result.get('error')}")
            await asyncio.sleep(2)
            exec_result = grpc_client.execute_swap(ticker, size_usd)

        if exec_result.get("success"):
            tx_hash = exec_result.get("tx_hash", "unknown")
            trade_id = exec_result.get("trade_id", "unknown")
            log.info(f"ExecutionTrader: SUCCESS {ticker} tx={tx_hash}")
            
            # Notify on success
            # Note: Accountant will handle PnL and trade_history logging in the pipeline
            await telegram_notifier.send_trade_executed(ticker, 0.0, fas_score, tx_hash)
            
            return {
                "success": True, 
                "tx_hash": tx_hash, 
                "trade_id": trade_id,
                "error": ""
            }
        else:
            log.error(f"ExecutionTrader: FAILED {ticker} after retry: {exec_result.get('error')}")
            return {"success": False, "error": exec_result.get("error")}

    except Exception as e:
        log.error(f"ExecutionTrader: unexpected error during execution: {e}")
        return {"success": False, "error": str(e)}
