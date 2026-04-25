# src/api/main.py
import json
import asyncio
from typing import List, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from src.state import db
from src.execution_bridge import grpc_client
from src.utils.logger import get_logger

log = get_logger(__name__)

app = FastAPI(title="CryptoHedgeAI API")

# CORS for Dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to dashboard URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_clients: List[WebSocket] = []

@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    log.info(f"New dashboard client connected. Total: {len(connected_clients)}")
    try:
        while True:
            # Keep-alive or handle client messages
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        log.info(f"Dashboard client disconnected. Remaining: {len(connected_clients)}")

async def broadcast_event(event_type: str, data: Dict[str, Any]):
    """Push event to all connected dashboard clients."""
    if not connected_clients:
        return
    
    message = json.dumps({"type": event_type, "data": data})
    for client in connected_clients.copy():
        try:
            await client.send_text(message)
        except Exception as e:
            log.error(f"Error broadcasting to client: {e}")
            connected_clients.remove(client)

@app.get("/api/portfolio")
async def get_portfolio():
    """Proxy for Go engine GetPortfolio."""
    try:
        return grpc_client.get_portfolio()
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/trades")
async def get_trades(limit: int = 50):
    """Fetch recent trades from DuckDB."""
    with db.get_connection() as conn:
        res = conn.execute(
            "SELECT * FROM trade_history ORDER BY created_at DESC LIMIT ?",
            [limit]
        ).fetchall()
        # Fetch column names
        cols = [d[0] for d in conn.description]
        return [dict(zip(cols, row)) for row in res]

@app.get("/api/ops")
async def get_ops():
    """Fetch ops fund balance and ledger."""
    balance = db.get_ops_fund_balance()
    with db.get_connection() as conn:
        ledger = conn.execute(
            "SELECT * FROM ops_ledger ORDER BY timestamp DESC LIMIT 20"
        ).fetchall()
        cols = [d[0] for d in conn.description]
        return {
            "balance": balance,
            "ledger": [dict(zip(cols, row)) for row in ledger]
        }

@app.get("/api/agents")
async def get_agents():
    """Fetch agent status from system_config."""
    # Logic to aggregate agent status
    stop = db.get_config("EMERGENCY_STOP")
    return {
        "overseer": "active" if stop != "TRUE" else "paused",
        "data_oracle": "active",
        "quant_strategist": "active",
        "risk_guardian": "active",
        "execution_trader": "active",
        "accountant": "active",
        "eval_agent": "active"
    }

@app.get("/api/eval")
async def get_eval():
    """Fetch evaluation history."""
    with db.get_connection() as conn:
        res = conn.execute("SELECT * FROM eval_history ORDER BY created_at DESC").fetchall()
        cols = [d[0] for d in conn.description]
        return [dict(zip(cols, row)) for row in res]
