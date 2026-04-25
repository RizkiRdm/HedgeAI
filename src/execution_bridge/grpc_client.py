# src/execution_bridge/grpc_client.py
import grpc
import os
from typing import Any, Dict
from src.execution_bridge import execution_pb2, execution_pb2_grpc
from src.utils.logger import get_logger

log = get_logger(__name__)

GO_ENGINE_URL = os.getenv("GO_ENGINE_URL", "localhost:50051")

class GoEngineUnavailableError(Exception):
    """Raised when the Go execution engine is unreachable."""
    pass

def _get_stub() -> execution_pb2_grpc.ExecutionEngineStub:
    channel = grpc.insecure_channel(GO_ENGINE_URL)
    return execution_pb2_grpc.ExecutionEngineStub(channel)

def health_check() -> Dict[str, Any]:
    """Check health of Go engine."""
    stub = _get_stub()
    try:
        response = stub.HealthCheck(execution_pb2.Empty(), timeout=5)
        return {"ok": response.ok, "version": response.version}
    except grpc.RpcError as e:
        log.error(f"Go Engine HealthCheck failed: {e}")
        raise GoEngineUnavailableError("Go execution engine is down") from e

def dry_run_swap(ticker: str, size_usd: float, exchange: str = "okx", is_sell: bool = False) -> Dict[str, Any]:
    """Simulate a swap operation."""
    stub = _get_stub()
    request = execution_pb2.SwapRequest(
        ticker=ticker,
        size_usd=size_usd,
        exchange=exchange,
        is_sell=is_sell
    )
    try:
        res = stub.DryRunSwap(request, timeout=5)
        return {
            "estimated_slippage": res.estimated_slippage,
            "price_impact": res.price_impact,
            "estimated_output": res.estimated_output,
            "is_safe": res.is_safe,
            "rejection_reason": res.rejection_reason
        }
    except grpc.RpcError as e:
        log.error(f"DryRunSwap failed: {e}")
        raise GoEngineUnavailableError("Go execution engine is down") from e

def execute_swap(ticker: str, size_usd: float, exchange: str = "okx", is_sell: bool = False) -> Dict[str, Any]:
    """Execute a real swap operation."""
    stub = _get_stub()
    request = execution_pb2.SwapRequest(
        ticker=ticker,
        size_usd=size_usd,
        exchange=exchange,
        is_sell=is_sell
    )
    try:
        res = stub.ExecuteSwap(request, timeout=35)
        return {
            "success": res.success,
            "tx_hash": res.tx_hash,
            "executed_price": res.executed_price,
            "actual_slippage": res.actual_slippage,
            "error_message": res.error_message
        }
    except grpc.RpcError as e:
        log.error(f"ExecuteSwap failed: {e}")
        raise GoEngineUnavailableError("Go execution engine is down") from e

def get_portfolio() -> Dict[str, Any]:
    """Get current portfolio state."""
    stub = _get_stub()
    try:
        res = stub.GetPortfolio(execution_pb2.Empty(), timeout=5)
        positions = []
        for p in res.positions:
            positions.append({
                "ticker": p.ticker,
                "size": p.size,
                "entry_price": p.entry_price,
                "current_price": p.current_price,
                "unrealized_pnl": p.unrealized_pnl
            })
        return {
            "total_capital": res.total_capital,
            "available_capital": res.available_capital,
            "positions": positions
        }
    except grpc.RpcError as e:
        log.error(f"GetPortfolio failed: {e}")
        raise GoEngineUnavailableError("Go execution engine is down") from e

def liquidate(ticker: str = "", liquidate_all: bool = False) -> Dict[str, Any]:
    """Liquidate positions."""
    stub = _get_stub()
    request = execution_pb2.LiquidateRequest(
        ticker=ticker,
        liquidate_all=liquidate_all
    )
    try:
        res = stub.Liquidate(request, timeout=35)
        return {
            "success": res.success,
            "positions_closed": res.positions_closed,
            "total_pnl": res.total_pnl
        }
    except grpc.RpcError as e:
        log.error(f"Liquidate failed: {e}")
        raise GoEngineUnavailableError("Go execution engine is down") from e
