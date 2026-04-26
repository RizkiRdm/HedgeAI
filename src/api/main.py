# src/api/main.py
"""
FastAPI backend for the dashboard.
Auth: JWT Bearer token on all endpoints except /auth/login.
Rate limiting: via slowapi (100 req/min per IP).
WebSocket: JWT verified on connect via query param.
"""
import json
import asyncio
import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from src.state import db
from src.auth.auth_manager import verify_key, verify_token, issue_token
from src.utils.logger import get_logger

log = get_logger(__name__)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="CryptoHedgeAI API", docs_url=None, redoc_url=None)  # no public docs
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

security = HTTPBearer()
connected_clients: List[WebSocket] = []


# ── Auth ───────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    api_key: str


class LoginResponse(BaseModel):
    token: str
    expires_in: int


@app.post("/auth/login", response_model=LoginResponse)
@limiter.limit("10/minute")  # brute-force protection
async def login(request: Request, body: LoginRequest):
    """
    Verify API key (SHA-256 compared against AUTH_KEY_HASH in .env).
    Returns JWT on success.
    """
    if not verify_key(body.api_key):
        log.warning(f"auth: failed login attempt from {request.client.host}")
        raise HTTPException(status_code=401, detail="Invalid API key")

    token = issue_token()
    log.info(f"auth: successful login from {request.client.host}")
    return LoginResponse(token=token, expires_in=86400)


def _get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """FastAPI dependency — verify JWT on every protected endpoint."""
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload


# ── WebSocket ──────────────────────────────────────────────────────────────

@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket, token: Optional[str] = None):
    """
    WebSocket for real-time dashboard updates.
    Auth: token passed as query param ?token=<jwt>
    """
    if not token or verify_token(token) is None:
        await websocket.close(code=4001)
        log.warning("ws: rejected unauthenticated connection")
        return

    await websocket.accept()
    connected_clients.append(websocket)
    log.info(f"ws: client connected. total={len(connected_clients)}")

    try:
        while True:
            await websocket.receive_text()  # keep-alive pings from client
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        log.info(f"ws: client disconnected. remaining={len(connected_clients)}")


async def broadcast_event(event_type: str, data: Dict[str, Any]) -> None:
    """Push event to all connected dashboard clients. Non-blocking."""
    if not connected_clients:
        return
    message = json.dumps({"type": event_type, "data": data})
    dead = []
    for client in connected_clients:
        try:
            await client.send_text(message)
        except Exception:
            dead.append(client)
    for d in dead:
        connected_clients.remove(d)


# ── Protected REST endpoints ───────────────────────────────────────────────

@app.get("/api/portfolio")
@limiter.limit("60/minute")
async def get_portfolio(
    request: Request,
    _user: dict = Depends(_get_current_user),
):
    try:
        from src.execution_bridge import grpc_client
        return grpc_client.get_portfolio()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Go engine unavailable: {e}")


@app.get("/api/trades")
@limiter.limit("60/minute")
async def get_trades(
    request: Request,
    limit: int = 50,
    _user: dict = Depends(_get_current_user),
):
    with db.get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM trade_history ORDER BY created_at DESC LIMIT ?", [limit]
        ).fetchall()
        cols = [d[0] for d in conn.description]
        return [dict(zip(cols, row)) for row in rows]


@app.get("/api/ops")
@limiter.limit("30/minute")
async def get_ops(
    request: Request,
    _user: dict = Depends(_get_current_user),
):
    balance = db.get_ops_fund_balance()
    with db.get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM ops_ledger ORDER BY timestamp DESC LIMIT 20"
        ).fetchall()
        cols = [d[0] for d in conn.description]
        return {
            "balance": balance,
            "ledger": [dict(zip(cols, row)) for row in rows],
        }


@app.get("/api/agents")
@limiter.limit("60/minute")
async def get_agents(
    request: Request,
    _user: dict = Depends(_get_current_user),
):
    stop = db.get_config("EMERGENCY_STOP") or "FALSE"
    return {
        "emergency_stop": stop == "TRUE",
        "agents": {name: "active" if stop != "TRUE" else "paused"
                   for name in ["overseer", "data_oracle", "quant_strategist",
                                "risk_guardian", "execution_trader", "accountant", "eval_agent"]},
    }


@app.get("/api/eval")
@limiter.limit("30/minute")
async def get_eval(
    request: Request,
    _user: dict = Depends(_get_current_user),
):
    with db.get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM eval_history ORDER BY created_at DESC"
        ).fetchall()
        cols = [d[0] for d in conn.description]
        return [dict(zip(cols, row)) for row in rows]


@app.get("/api/status")
async def status():
    """Public health check endpoint — no auth required."""
    return {"status": "ok", "service": "cryptohedgeai"}
