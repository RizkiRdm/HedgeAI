# PLAN.md — CryptoHedgeAI Development Roadmap
> **HOW TO READ THIS FILE (for AI agents):**
> This file contains GitHub Issues formatted for creation via `gh issue create`.
> Each issue is self-contained. Read ALL sections before writing any code.
> Do not skip Context, Pre-conditions, or Implementation Guide sections.
> Follow the exact file paths specified. Do not create files outside the defined structure.

---

## MILESTONES

| ID | Name | Duration | Goal |
|---|---|---|---|
| M1 | Foundation & Skeleton | Week 1, Days 1–7 | Project boots, DuckDB initialized, heartbeat ticking, gRPC bridge connected |
| M2 | Core Agents & Scoring | Week 2, Days 8–14 | All 7 agents defined, score tools working, FAS signals generating |
| M3 | Execution & Monitoring | Week 3, Days 15–21 | Trades executing via Go engine, dashboard live, PnL tracked |
| M4 | Eval, Ops & Hardening | Week 4, Days 22–30 | Eval agent running, security audited, 72h paper trading passed |

---

## GITHUB CLI SETUP (run once before creating issues)

```bash
# Create milestones
gh api repos/{owner}/{repo}/milestones --method POST -f title="M1: Foundation & Skeleton" 
gh api repos/{owner}/{repo}/milestones --method POST -f title="M2: Core Agents & Scoring" 
gh api repos/{owner}/{repo}/milestones --method POST -f title="M3: Execution & Monitoring" 
gh api repos/{owner}/{repo}/milestones --method POST -f title="M4: Eval, Ops & Hardening" 

# Create labels (run each line)
gh label create "setup"            --color "ededed" --description "Project initialization"
gh label create "backend"          --color "0075ca" --description "Python AI layer"
gh label create "go"               --color "00ADD8" --description "Go execution engine"
gh label create "frontend"         --color "7057ff" --description "Next.js dashboard"
gh label create "database"         --color "e4e669" --description "DuckDB schema and queries"
gh label create "agent"            --color "006b75" --description "CrewAI agent implementation"
gh label create "tools"            --color "fbca04" --description "Score calculator tools"
gh label create "infra"            --color "0e8a16" --description "Docker, VPS, CI/CD"
gh label create "security"         --color "b60205" --description "Security rules and audits"
gh label create "testing"          --color "c5def5" --description "Test suites and validation"
gh label create "tui"              --color "5319e7" --description "Terminal UI (Textual)"
gh label create "cli"              --color "1d76db" --description "CLI (Rich + Click)"
gh label create "priority:critical" --color "d93f0b" --description "Must complete for MVP"
gh label create "priority:high"    --color "e99695" --description "Important, not blocking"
gh label create "priority:medium"  --color "fef2c0" --description "Nice to have in timeline"
```

---

## ISSUE TEMPLATE FORMAT

Each issue below follows this structure — read every section before starting:

```
### Context         → WHY this exists and what it connects to
### Pre-conditions  → WHAT must be done first (blockers)
### Implementation  → HOW to build it (step by step, with file paths)
### File Targets    → EXACT files to create or modify
### Success Metrics → MEASURABLE outcomes that prove this is done correctly
### Verification    → COMMANDS to run to verify completion
### Expected Output → WHAT you should see when it works
### Common Mistakes → WHAT NOT to do
### Definition of Done → Final checklist
```

---

## SPRINT 1 — FOUNDATION & SKELETON
### Milestone: `M1: Foundation & Skeleton`

---

### ISSUE 001

```
title:     "Project scaffold: folder structure, Docker, env setup"
labels:    ["setup", "infra", "priority:critical"]
milestone: "M1: Foundation & Skeleton"
```

#### Context
This is the first issue. Nothing else can start until this is done. You are setting up the entire project skeleton exactly as defined in AGENTS.md. No business logic is written here — only structure, config, and Docker.

#### Pre-conditions
- None. This is issue #1.
- You need: Docker installed, Python 3.11+, Go 1.22+ on local machine.

#### Implementation Guide
**Step 1:** Create the root directory and all folders.
```bash
mkdir -p cryptohedgeai/src/{agents,core,state,heartbeat,tools,execution_bridge,utils,api,tui,cli}
mkdir -p cryptohedgeai/go_engine/{executor,proto}
mkdir -p cryptohedgeai/dashboard/{app,components}
mkdir -p cryptohedgeai/tests/{unit,integration}
mkdir -p cryptohedgeai/data
touch cryptohedgeai/data/.gitkeep
```

**Step 2:** Create `Dockerfile` at project root using `python:3.11-slim` as base. Install deps from `requirements.txt`. Set `WORKDIR /app`. Copy `src/` into container. CMD should run the heartbeat daemon.

**Step 3:** Create `docker-compose.yml` with 3 services: `python_brain`, `go_engine`, `dashboard`. Mount `./data:/data` volume for python_brain. Port 50051 for go_engine (gRPC). Port 3000 for dashboard. Port 8000 for FastAPI.

**Step 4:** Create `.env.example` with these keys (no values):
```
OKX_API_KEY=
OKX_API_SECRET=
OKX_PASSPHRASE=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
DEXSCREENER_BASE_URL=https://api.dexscreener.com
COVALENT_API_KEY=
CRYPTOPANIC_API_KEY=
JWT_SECRET=
ENVIRONMENT=development
LOG_LEVEL=INFO
```

**Step 5:** Create `requirements.txt` with:
```
crewai
duckdb
ccxt
pandas-ta
python-telegram-bot
fastapi
uvicorn[standard]
websockets
python-dotenv
grpcio
grpcio-tools
rich
click
textual
pydantic
ruff
mypy
pytest
pytest-asyncio
pytest-cov
```

**Step 6:** Create `pyproject.toml` with ruff and mypy config. Register `cryptohedge` as a CLI entrypoint pointing to `src.cli.main:cli`.

**Step 7:** Create `.gitignore` — must exclude: `.env`, `data/*.duckdb`, `__pycache__/`, `*.pyc`, `.mypy_cache/`, `.pytest_cache/`, `node_modules/`, `go_engine/bin/`.

**Step 8:** Create `README.md` with Quick Start in exactly 3 commands:
```bash
cp .env.example .env  # fill in your keys
docker-compose build
docker-compose up
```

#### File Targets
| File | Action |
|---|---|
| `Dockerfile` | CREATE |
| `docker-compose.yml` | CREATE |
| `.env.example` | CREATE |
| `requirements.txt` | CREATE |
| `pyproject.toml` | CREATE |
| `.gitignore` | CREATE |
| `README.md` | CREATE |
| All `src/` subdirs | CREATE (empty `__init__.py` in each) |

#### Success Metrics
- `docker-compose build` exits with code 0
- `docker-compose up` starts all 3 services without crash
- `.env` is NOT present in git (blocked by .gitignore)
- `find . -name "*.duckdb"` returns nothing (gitignored)
- All `src/` subdirs exist and have `__init__.py`

#### Verification Commands
```bash
docker-compose build && echo "BUILD OK"
docker-compose up -d && sleep 5 && docker-compose ps
git check-ignore -v .env                   # should output: .gitignore:.env
git check-ignore -v data/test.duckdb       # should output: .gitignore:data/*.duckdb
find src -name "__init__.py" | wc -l       # should be >= 10
```

#### Expected Output
```
✓ docker-compose ps shows 3 services: python_brain, go_engine, dashboard
✓ python_brain exits cleanly (no code yet, but no import errors)
✓ README.md exists with Quick Start section
```

#### Common Mistakes
- DO NOT put business logic in Dockerfile CMD — only `python -m src.heartbeat.daemon`
- DO NOT commit `.env` — verify with `git status` before every commit
- DO NOT use Node.js/TypeScript for anything in `src/` — Python only
- DO NOT install `SQLAlchemy` or `pandas` in `requirements.txt`

#### Definition of Done
- [ ] All folders created with `__init__.py`
- [ ] `docker-compose build` succeeds (exit 0)
- [ ] `.gitignore` verified for `.env` and `.duckdb`
- [ ] `.env.example` has all required keys
- [ ] `README.md` has 3-command Quick Start

---

### ISSUE 002

```
title:     "DuckDB: schema initialization and db.py query layer"
labels:    ["backend", "database", "priority:critical"]
milestone: "M1: Foundation & Skeleton"
```

#### Context
DuckDB is the single source of truth for the entire system. This module (`src/state/db.py`) is the ONLY place where SQL can be written. All other modules call functions from `db.py` — they never write SQL themselves. AGENTS.md strictly forbids SQLAlchemy or any ORM.

#### Pre-conditions
- Issue 001 must be completed (folder structure exists)
- `duckdb` in `requirements.txt`

#### Implementation Guide
**Step 1:** Create `src/state/schema.sql` with all 5 CREATE TABLE statements exactly as defined in AGENTS.md. Use `CREATE TABLE IF NOT EXISTS` for all tables.

**Step 2:** Create `src/state/db.py`:

```python
# src/state/db.py
import duckdb
import os
from typing import Any
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "/data/cryptohedge.duckdb")

def get_connection() -> duckdb.DuckDBPyConnection:
    """Returns a DuckDB connection. Called at start of each function."""
    return duckdb.connect(DB_PATH)

def initialize_schema() -> None:
    """Run once at startup. Creates all tables if they don't exist."""
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path) as f:
        sql = f.read()
    with get_connection() as conn:
        conn.execute(sql)

def get_config(param_name: str) -> str | None:
    """Read a single config value. Returns None if not found."""
    ...

def set_config(param_name: str, param_value: str, is_locked: bool = False) -> None:
    """Upsert a config param. Raises ValueError if param is locked."""
    ...

def insert_trade(ticker: str, entry_p: float, fas_score: float) -> str:
    """Insert open trade. Returns the new UUID."""
    ...

def close_trade(trade_id: str, exit_p: float, pnl: float) -> None:
    """Update trade with exit price and PnL."""
    ...

def update_market_cache(ticker: str, sector: str, metrics_json: dict) -> None:
    """Upsert market_cache row."""
    ...

def get_market_cache(ticker: str) -> dict | None:
    """Get cached data for ticker. Returns None if not found."""
    ...

def insert_ops_ledger(amount: float, category: str, description: str, auto_executed: bool = False) -> None:
    """Log an ops fund transaction."""
    ...

def get_ops_fund_balance() -> float:
    """Sum all ops_ledger entries to get current balance."""
    ...

def insert_eval(period_type: str, period_start, period_end, roi_actual: float,
                roi_target: float, met_target: bool, config_snapshot: dict, action_taken: str) -> None:
    """Log an evaluation result."""
    ...

def checkpoint() -> None:
    """Force DuckDB WAL checkpoint. Run every hour."""
    with get_connection() as conn:
        conn.execute("PRAGMA force_checkpoint")
```

**Step 3:** Create `tests/unit/test_db.py` with tests for every function. Use a temp file path for DB in tests — NEVER use the real `/data/` path.

**Step 4:** Register `initialize_schema()` to be called in `src/heartbeat/daemon.py` on startup (you'll create daemon.py in issue 003, just note this dependency).

#### File Targets
| File | Action |
|---|---|
| `src/state/schema.sql` | CREATE |
| `src/state/db.py` | CREATE |
| `tests/unit/test_db.py` | CREATE |

#### Success Metrics
- All 5 tables created on first `initialize_schema()` call
- `initialize_schema()` is idempotent (safe to call multiple times)
- All `db.py` functions have type hints on all parameters and return values
- No SQL strings exist outside `src/state/db.py`
- `pytest tests/unit/test_db.py -v` passes with 0 failures

#### Verification Commands
```bash
pytest tests/unit/test_db.py -v
# Expected: all tests PASS

python -c "from src.state.db import initialize_schema; initialize_schema(); print('Schema OK')"
# Expected: Schema OK (no errors)

grep -r "SELECT\|INSERT\|UPDATE\|DELETE" src/ --include="*.py" | grep -v "src/state/db.py"
# Expected: NO output (no SQL outside db.py)
```

#### Expected Output
```
tests/unit/test_db.py::test_initialize_schema PASSED
tests/unit/test_db.py::test_get_set_config PASSED
tests/unit/test_db.py::test_insert_trade PASSED
tests/unit/test_db.py::test_update_market_cache PASSED
tests/unit/test_db.py::test_ops_ledger PASSED
tests/unit/test_db.py::test_checkpoint PASSED
```

#### Common Mistakes
- DO NOT use `duckdb.connect()` without `with` statement — always use context manager to close connection
- DO NOT write `conn.execute(f"SELECT ... {user_input}")` — use parameterized queries: `conn.execute("SELECT ... WHERE param = ?", [value])`
- DO NOT import `db.py` functions and call them directly from agent files — this is a sign you're bypassing the layer correctly. Agents call `db.get_config()` not raw SQL.
- DO NOT use `/data/cryptohedge.duckdb` in tests — use `tmp_path` fixture

#### Definition of Done
- [ ] `schema.sql` has all 5 tables with IF NOT EXISTS
- [ ] `db.py` has all listed functions with complete type hints
- [ ] No raw SQL exists outside `db.py`
- [ ] Unit tests pass (0 failures, 0 errors)
- [ ] `checkpoint()` function implemented and tested

---

### ISSUE 003

```
title:     "Heartbeat daemon: 15-second async tick controller"
labels:    ["backend", "infra", "priority:critical"]
milestone: "M1: Foundation & Skeleton"
```

#### Context
The heartbeat daemon is the engine that drives the entire system. It fires every 15 seconds and delegates to the Overseer agent. It contains NO business logic itself — it only triggers. It must check `EMERGENCY_STOP` in system_config before each tick and halt if TRUE.

#### Pre-conditions
- Issue 001 (folder structure) complete
- Issue 002 (db.py with `get_config()`) complete

#### Implementation Guide
**Step 1:** Create `src/heartbeat/daemon.py`:

```python
# src/heartbeat/daemon.py
import asyncio
import signal
import logging
from datetime import datetime
from src.state.db import initialize_schema, get_config

TICK_INTERVAL_SECONDS = 15
MAX_CYCLE_SECONDS = 14

async def run_daemon() -> None:
    """
    Main daemon loop. Fires every 15 seconds.
    Checks EMERGENCY_STOP before each cycle.
    Calls overseer.run_cycle() for each tick.
    """
    initialize_schema()
    logging.info("Heartbeat daemon started")
    tick_count = 0

    while True:
        tick_start = datetime.utcnow()
        tick_count += 1

        emergency = get_config("EMERGENCY_STOP")
        if emergency == "TRUE":
            logging.warning(f"Tick #{tick_count}: EMERGENCY_STOP active — skipping cycle")
            await asyncio.sleep(TICK_INTERVAL_SECONDS)
            continue

        logging.info(f"Tick #{tick_count}: cycle start")

        try:
            # Import here to avoid circular imports
            from src.agents.overseer import run_cycle
            await asyncio.wait_for(run_cycle(tick_count), timeout=MAX_CYCLE_SECONDS)
        except asyncio.TimeoutError:
            logging.warning(f"Tick #{tick_count}: cycle exceeded {MAX_CYCLE_SECONDS}s — WARNING")
        except Exception as e:
            logging.error(f"Tick #{tick_count}: unhandled error in cycle: {e}")

        elapsed = (datetime.utcnow() - tick_start).total_seconds()
        sleep_time = max(0, TICK_INTERVAL_SECONDS - elapsed)
        await asyncio.sleep(sleep_time)

def handle_shutdown(sig, frame):
    logging.info("Shutdown signal received — stopping daemon")
    raise SystemExit(0)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)
    asyncio.run(run_daemon())
```

**Step 2:** Create a mock `src/agents/overseer.py` stub (just the function signature, implementation comes in Issue 007):
```python
async def run_cycle(tick_count: int) -> None:
    """Stub — implemented in Issue 007."""
    pass
```

**Step 3:** Create `tests/unit/test_daemon.py`. Mock `run_cycle` and verify: it gets called on each tick, EMERGENCY_STOP halts calling, timeout triggers warning log.

#### File Targets
| File | Action |
|---|---|
| `src/heartbeat/daemon.py` | CREATE |
| `src/agents/overseer.py` | CREATE (stub only) |
| `tests/unit/test_daemon.py` | CREATE |

#### Success Metrics
- Daemon logs a tick line every 15 seconds
- `EMERGENCY_STOP=TRUE` in system_config causes tick to skip without calling `run_cycle`
- A `run_cycle` that takes > 14s triggers a WARNING log but does NOT crash the daemon
- SIGTERM exits cleanly (no traceback)

#### Verification Commands
```bash
# Set EMERGENCY_STOP=TRUE and verify daemon skips
python -c "from src.state.db import set_config; set_config('EMERGENCY_STOP', 'TRUE')"
python -m src.heartbeat.daemon &
sleep 20
# Check logs — should show "EMERGENCY_STOP active" twice (two ticks in 20s)
kill %1

pytest tests/unit/test_daemon.py -v
```

#### Expected Output
```
2026-04-24 14:32:00 INFO Heartbeat daemon started
2026-04-24 14:32:00 WARNING Tick #1: EMERGENCY_STOP active — skipping cycle
2026-04-24 14:32:15 WARNING Tick #2: EMERGENCY_STOP active — skipping cycle
```

#### Common Mistakes
- DO NOT put `while True` with `time.sleep()` — use `asyncio.sleep()` for async compatibility
- DO NOT import `run_cycle` at module level — import inside the loop to avoid circular import issues
- DO NOT crash on cycle failure — catch all exceptions, log them, continue to next tick
- DO NOT call `initialize_schema()` on every tick — call ONCE at startup only

#### Definition of Done
- [ ] Daemon loops every 15 seconds
- [ ] EMERGENCY_STOP check works
- [ ] 14-second timeout on cycle works
- [ ] SIGTERM exits cleanly
- [ ] Unit tests pass

---

### ISSUE 004

```
title:     "gRPC bridge: proto definition, Python client, Go server stub"
labels:    ["backend", "go", "infra", "priority:critical"]
milestone: "M1: Foundation & Skeleton"
```

#### Context
The Go execution engine handles all latency-critical order execution. Python agents communicate with it exclusively via gRPC — never via shared memory or direct DB access. This issue sets up the communication protocol and stubs on both sides. No real trading logic yet.

#### Pre-conditions
- Issue 001 complete (folder structure)
- Go 1.22+ installed
- `grpcio` and `grpcio-tools` in requirements.txt

#### Implementation Guide
**Step 1:** Create `go_engine/proto/execution.proto`:
```protobuf
syntax = "proto3";
package execution;
option go_package = "./proto";

service ExecutionEngine {
    rpc DryRunSwap(SwapRequest) returns (DryRunResult);
    rpc ExecuteSwap(SwapRequest) returns (SwapResult);
    rpc GetPortfolio(Empty) returns (PortfolioState);
    rpc Liquidate(LiquidateRequest) returns (LiquidateResult);
    rpc HealthCheck(Empty) returns (HealthResponse);
}

message Empty {}

message SwapRequest {
    string ticker = 1;
    double size_usd = 2;
    string exchange = 3;
    bool is_sell = 4;
}

message DryRunResult {
    double estimated_slippage = 1;
    double price_impact = 2;
    double estimated_output = 3;
    bool is_safe = 4;
    string rejection_reason = 5;
}

message SwapResult {
    bool success = 1;
    string tx_hash = 2;
    double executed_price = 3;
    double actual_slippage = 4;
    string error_message = 5;
}

message PortfolioState {
    double total_capital = 1;
    double available_capital = 2;
    repeated Position positions = 3;
}

message Position {
    string ticker = 1;
    double size = 2;
    double entry_price = 3;
    double current_price = 4;
    double unrealized_pnl = 5;
}

message LiquidateRequest {
    bool liquidate_all = 1;
    string ticker = 2;
}

message LiquidateResult {
    bool success = 1;
    int32 positions_closed = 2;
    double total_pnl = 3;
}

message HealthResponse {
    bool ok = 1;
    string version = 2;
}
```

**Step 2:** Generate Python stubs:
```bash
cd src/execution_bridge
python -m grpc_tools.protoc \
  -I ../../go_engine/proto \
  --python_out=. \
  --grpc_python_out=. \
  ../../go_engine/proto/execution.proto
```

**Step 3:** Create `src/execution_bridge/grpc_client.py` with typed wrapper functions for all 5 RPC methods. Connection timeout: 5 seconds. Raise a custom `GoEngineUnavailableError` if connection fails.

**Step 4:** Create Go server stub in `go_engine/main.go` — implements all RPC methods with stub responses. `HealthCheck` must return `{ok: true, version: "0.1.0"}`. All other stubs return success=true with fake data.

**Step 5:** Add `Makefile` or `go_engine/build.sh` for compiling Go proto and building the binary.

#### File Targets
| File | Action |
|---|---|
| `go_engine/proto/execution.proto` | CREATE |
| `src/execution_bridge/execution_pb2.py` | GENERATED (via grpc_tools) |
| `src/execution_bridge/execution_pb2_grpc.py` | GENERATED (via grpc_tools) |
| `src/execution_bridge/grpc_client.py` | CREATE |
| `go_engine/main.go` | CREATE |
| `go_engine/go.mod` | CREATE |

#### Success Metrics
- Python can call `health_check()` and receive `{ok: true}`
- Proto compiles without errors for both Python and Go
- `GoEngineUnavailableError` raised (not generic exception) when Go server is down

#### Verification Commands
```bash
# Start Go server
cd go_engine && go run main.go &

# Test Python client
python -c "
from src.execution_bridge.grpc_client import health_check
result = health_check()
print('Health:', result)
assert result['ok'] == True
print('gRPC bridge OK')
"

# Stop Go server, verify error type
kill %1
python -c "
from src.execution_bridge.grpc_client import health_check, GoEngineUnavailableError
try:
    health_check()
except GoEngineUnavailableError:
    print('Correct error type raised')
except Exception as e:
    print('WRONG error type:', type(e))
"
```

#### Expected Output
```
Health: {'ok': True, 'version': '0.1.0'}
gRPC bridge OK

# After kill:
Correct error type raised
```

#### Common Mistakes
- DO NOT import gRPC stubs at module level in agents — import only in `grpc_client.py`
- DO NOT expose Go server port to internet — bind to `localhost:50051` only
- DO NOT regenerate proto stubs manually by editing `_pb2.py` files — always regenerate via `grpc_tools`
- DO NOT swallow `GoEngineUnavailableError` silently — let it propagate to calling agent

#### Definition of Done
- [ ] Proto compiles for Python and Go
- [ ] Go stub server runs and responds to HealthCheck
- [ ] Python client wrapper functions typed and working
- [ ] `GoEngineUnavailableError` raises on connection failure
- [ ] Unit test: mock gRPC, verify Python client functions

---

### ISSUE 005

```
title:     "Logger and Telegram notifier utilities"
labels:    ["backend", "utils", "priority:high"]
milestone: "M1: Foundation & Skeleton"
```

#### Context
The logger must be used everywhere in place of `print()`. It filters sensitive variable names from output. The Telegram notifier is the user's main window into what the bot is doing — it must be reliable and well-formatted.

#### Pre-conditions
- Issue 001 (folder structure)
- `python-telegram-bot` in requirements.txt
- `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`

#### Implementation Guide
**Step 1:** Create `src/utils/logger.py`:

```python
# src/utils/logger.py
import logging
import re

SENSITIVE_PATTERNS = [
    r"PRIVATE_KEY\s*[:=]\s*\S+",
    r"API_SECRET\s*[:=]\s*\S+",
    r"API_KEY\s*[:=]\s*\S+",
    r"SEED\s*[:=]\s*\S+",
    r"password\s*[:=]\s*\S+",
    r"passphrase\s*[:=]\s*\S+",
]

class SecretFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        msg = str(record.getMessage())
        for pattern in SENSITIVE_PATTERNS:
            if re.search(pattern, msg, re.IGNORECASE):
                record.msg = "[REDACTED — sensitive data blocked by SecretFilter]"
                record.args = ()
                return True
        return True

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.addFilter(SecretFilter())
    return logger
```

**Step 2:** Create `src/utils/telegram_notifier.py` with these functions:
- `send_trade_executed(ticker, pnl, fas_score, tx_hash)` — called after every trade
- `send_emergency_alert(reason)` — called on EMERGENCY_STOP trigger
- `send_formula_proposal(current, proposed, reason, expected_impact)` — for Eval Agent
- `send_bill_notification(service, amount, due_date, days_until_due)` — T-7d and T-1d
- `send_bill_paid(service, amount, auto_executed)` — confirmation after payment
- `send_ops_warning(balance, monthly_burn, runway_months)` — low ops fund alert

Each function formats a clean message and sends via `python-telegram-bot`. Add `parse_mode=ParseMode.MARKDOWN` for formatting. Errors in sending must be caught and logged — never crash the bot because Telegram is down.

**Step 3:** Create `/start`, `/stop`, `/resume`, `/panic`, `/status` command handlers in `telegram_notifier.py`. These update system_config via `db.set_config()`.

**Step 4:** Create `tests/unit/test_logger.py` — test that SecretFilter blocks: `PRIVATE_KEY=abc123`, `api_secret: xyz`, `seed: hello world`. Test that normal messages pass through.

#### File Targets
| File | Action |
|---|---|
| `src/utils/logger.py` | CREATE |
| `src/utils/telegram_notifier.py` | CREATE |
| `tests/unit/test_logger.py` | CREATE |

#### Success Metrics
- Log lines containing `PRIVATE_KEY=`, `API_SECRET=`, `SEED=` are replaced with `[REDACTED]`
- Normal log messages pass through unchanged
- Telegram send failure does NOT raise exception — caught and logged only
- All 6 send functions work and format output cleanly

#### Verification Commands
```bash
pytest tests/unit/test_logger.py -v

# Manual test secret filter
python -c "
from src.utils.logger import get_logger
log = get_logger('test')
import logging
logging.basicConfig(level=logging.DEBUG)
log.warning('Normal message — should appear')
log.warning('PRIVATE_KEY=supersecretkey123')   # should show [REDACTED]
log.warning('api_secret: mysecret456')         # should show [REDACTED]
"
```

#### Expected Output
```
WARNING test: Normal message — should appear
WARNING test: [REDACTED — sensitive data blocked by SecretFilter]
WARNING test: [REDACTED — sensitive data blocked by SecretFilter]
```

#### Common Mistakes
- DO NOT use `print()` anywhere in `src/` — always `get_logger(__name__).info()`
- DO NOT raise exceptions from Telegram send functions — wrap in try/except
- DO NOT hardcode chat IDs — always read from `os.getenv("TELEGRAM_CHAT_ID")`
- DO NOT test with real Telegram token in CI — mock the bot API in tests

#### Definition of Done
- [ ] SecretFilter blocks all sensitive patterns
- [ ] All 6 Telegram send functions implemented
- [ ] Telegram command handlers `/panic`, `/resume`, `/status` working
- [ ] Unit tests pass
- [ ] `get_logger()` used in daemon.py (replace any print statements)

---

## SPRINT 2 — CORE AGENTS & SCORING
### Milestone: `M2: Core Agents & Scoring`

---

### ISSUE 006

```
title:     "Score Tools: momentum, RAR, on-chain, narrative scorers"
labels:    ["backend", "tools", "priority:critical"]
milestone: "M2: Core Agents & Scoring"
```

#### Context
Score tools are the MOST IMPORTANT architectural boundary in this system. They are deterministic Python functions — NOT AI, NOT CrewAI agents. They receive raw data (from DuckDB cache) and return a single float 0.0–1.0. Agents receive ONLY these floats — never raw market data. This prevents hallucination and saves token costs.

#### Pre-conditions
- Issue 002 (db.py with `get_market_cache()`) complete
- `pandas-ta` in requirements.txt

#### Implementation Guide
Each scorer follows this exact pattern:
```python
# src/tools/momentum_scorer.py
from src.utils.logger import get_logger
log = get_logger(__name__)

def momentum_scorer(ticker: str) -> float:
    """
    Calculates momentum score from DuckDB cached data.
    Returns: float 0.0–1.0  (0.0 = bearish, 1.0 = bullish)
    Returns 0.0 if data unavailable (logs reason, does NOT raise).
    """
    from src.state.db import get_market_cache
    cache = get_market_cache(ticker)
    if cache is None:
        log.warning(f"momentum_scorer: no cache for {ticker}, returning 0.0")
        return 0.0

    try:
        metrics = cache.get("metrics_json", {})
        ohlcv = metrics.get("ohlcv_24h")
        if not ohlcv:
            return 0.0
        # Calculate RSI, MACD, price velocity using pandas-ta
        # Normalize result to 0.0–1.0
        score = _calculate_momentum(ohlcv)
        return round(max(0.0, min(1.0, score)), 4)
    except Exception as e:
        log.error(f"momentum_scorer: error for {ticker}: {e}")
        return 0.0
```

Build all 4 scorers with this pattern:
- `momentum_scorer(ticker)` → RSI (14), MACD crossover signal, 24h price velocity
- `rar_scorer(ticker)` → 7-day Sharpe-like ratio: mean_return / std_return, penalized by max_drawdown
- `onchain_scorer(ticker)` → from Covalent data: (new_addresses_delta + tx_count_delta + holder_delta) / 3, all normalized
- `narrative_scorer(ticker)` → (cryptopanic_polarity × 0.7) + (fear_greed_normalized × 0.3)

For Fear & Greed: the API returns integer 1–100. Normalize: `fg_norm = fear_greed_value / 100`. Values > 50 are bullish, < 50 bearish.

#### File Targets
| File | Action |
|---|---|
| `src/tools/momentum_scorer.py` | CREATE |
| `src/tools/rar_scorer.py` | CREATE |
| `src/tools/onchain_scorer.py` | CREATE |
| `src/tools/narrative_scorer.py` | CREATE |
| `tests/unit/test_scorers.py` | CREATE |

#### Success Metrics
- All scorers return float in [0.0, 1.0] — never outside this range
- All scorers return 0.0 (not raise exception) when data is unavailable
- All return values are rounded to 4 decimal places
- `pytest tests/unit/test_scorers.py` passes with 100% of scorer tests

#### Verification Commands
```bash
pytest tests/unit/test_scorers.py -v

# Test boundary — feed empty cache, verify returns 0.0 not exception
python -c "
from src.tools.momentum_scorer import momentum_scorer
result = momentum_scorer('NONEXISTENT_TICKER_XYZ')
assert isinstance(result, float), 'must return float'
assert 0.0 <= result <= 1.0, 'must be in [0, 1]'
print(f'Empty ticker returns: {result}')
"
```

#### Expected Output
```
tests/unit/test_scorers.py::test_momentum_scorer_with_data PASSED
tests/unit/test_scorers.py::test_momentum_scorer_no_data PASSED
tests/unit/test_scorers.py::test_rar_scorer_with_data PASSED
tests/unit/test_scorers.py::test_rar_scorer_no_data PASSED
tests/unit/test_scorers.py::test_onchain_scorer PASSED
tests/unit/test_scorers.py::test_narrative_scorer PASSED
tests/unit/test_scorers.py::test_all_return_bounded_floats PASSED

Empty ticker returns: 0.0
```

#### Common Mistakes
- DO NOT pass raw OHLCV arrays to agents — these tools are the wall
- DO NOT return `None` — always return `0.0` as the safe default
- DO NOT raise exceptions from scorers — always catch and return 0.0
- DO NOT use `pandas.DataFrame` in agent code — pandas-ta is only allowed inside scorer tools

#### Definition of Done
- [ ] All 4 scorers return float in [0.0, 1.0]
- [ ] All return 0.0 on missing data (no exception)
- [ ] All have complete type hints
- [ ] Unit tests: boundary test (0.0 and 1.0), happy path, missing data path
- [ ] No pandas imports outside `src/tools/`

---

### ISSUE 007

```
title:     "Quant Strategist agent: FAS formula and signal generation"
labels:    ["backend", "agent", "priority:critical"]
milestone: "M2: Core Agents & Scoring"
```

#### Context
The Quant Strategist is the first full CrewAI agent implementation. It receives a list of tickers from Data Oracle, calls all 4 scorer tools per coin, applies the FAS formula, filters for FAS >= 0.75, and passes signals to Risk Guardian. It logs every score for every coin — this log is critical for evaluation.

#### Pre-conditions
- Issue 006 (all 4 scorer tools) complete
- Issue 002 (db.py) complete
- `crewai` installed

#### Implementation Guide
**Step 1:** Understand CrewAI agent structure:
```python
from crewai import Agent, Task, Crew

agent = Agent(
    role="Quant Strategist",
    goal="Calculate FAS scores for all coins and identify signals above 0.75",
    backstory="...",
    tools=[momentum_scorer_tool, rar_scorer_tool, onchain_scorer_tool, narrative_scorer_tool],
    verbose=True
)
```

**Step 2:** Wrap scorer functions as CrewAI tools using `@tool` decorator:
```python
from crewai.tools import tool

@tool("momentum_scorer")
def momentum_scorer_tool(ticker: str) -> float:
    """Calculates momentum score for a given ticker. Returns float 0.0-1.0."""
    from src.tools.momentum_scorer import momentum_scorer
    return momentum_scorer(ticker)
```

**Step 3:** Implement `src/agents/quant_strategist.py` with:
- `run_analysis(tickers: list[str]) -> list[dict]` function
- Each dict in result: `{"ticker": str, "fas_score": float, "ms": float, "rar": float, "ochs": float, "ns": float, "sector": str}`
- FAS formula MUST be: `fas = (0.4 * ms) + (0.2 * rar) + (0.3 * ochs) + (0.1 * ns)`
- Filter: only include where `fas >= 0.75`
- Log every ticker analyzed with all 4 component scores

**Step 4:** Read FAS weights from `system_config` table (param names: `fas_weight_ms`, `fas_weight_rar`, `fas_weight_ochs`, `fas_weight_ns`). Fall back to defaults (0.4, 0.2, 0.3, 0.1) if not found. This allows Eval Agent to adjust weights.

#### File Targets
| File | Action |
|---|---|
| `src/agents/quant_strategist.py` | CREATE |
| `tests/unit/test_quant_strategist.py` | CREATE |

#### Success Metrics
- FAS formula matches: `(0.4×MS) + (0.2×RAR) + (0.3×OCHS) + (0.1×NS)` exactly
- Only tickers with FAS >= 0.75 appear in output
- Log line per ticker: `ticker=SOL ms=0.91 rar=0.74 ochs=0.88 ns=0.79 fas=0.847`
- Throughput: 300 tickers analyzed in under 8 seconds (measure with `time.perf_counter()`)
- Reads weights from system_config if present

#### Verification Commands
```bash
pytest tests/unit/test_quant_strategist.py -v

# Throughput test
python -c "
import time
from src.agents.quant_strategist import run_analysis
tickers = [f'COIN{i}/USDC' for i in range(300)]
start = time.perf_counter()
signals = run_analysis(tickers)
elapsed = time.perf_counter() - start
print(f'300 coins analyzed in {elapsed:.2f}s')
assert elapsed < 8.0, f'Too slow: {elapsed:.2f}s > 8s'
print(f'Signals found: {len(signals)}')
"
```

#### Expected Output
```
tests/unit/test_quant_strategist.py::test_fas_formula_correct PASSED
tests/unit/test_quant_strategist.py::test_filters_below_threshold PASSED
tests/unit/test_quant_strategist.py::test_reads_weights_from_config PASSED
tests/unit/test_quant_strategist.py::test_logs_all_tickers PASSED

300 coins analyzed in 4.31s
Signals found: 3
```

#### Common Mistakes
- DO NOT change FAS formula coefficients from defaults without reading system_config first
- DO NOT skip tickers — every ticker must be analyzed and logged, even if FAS < 0.75
- DO NOT hardcode weights as literals — always read from system_config with fallback
- DO NOT estimate scores when data missing — if scorer returns 0.0 for all 4, FAS = 0.0, coin is skipped

#### Definition of Done
- [ ] FAS formula implemented exactly
- [ ] Weights read from system_config
- [ ] All tickers logged with component scores
- [ ] Only FAS >= 0.75 returned
- [ ] Throughput: 300 coins < 8s
- [ ] Unit tests pass

---

### ISSUE 008

```
title:     "Risk Guardian agent: veto logic, position sizing, emergency stop"
labels:    ["backend", "agent", "priority:critical"]
milestone: "M2: Core Agents & Scoring"
```

#### Context
Risk Guardian has absolute veto power. No trade executes without its approval. It enforces every hard constraint in the system. Its veto cannot be overridden by any other agent. Every veto must be logged permanently.

#### Pre-conditions
- Issue 007 (Quant Strategist — signals format) complete
- Issue 002 (db.py) complete

#### Implementation Guide
**Step 1:** Create `src/core/kelly_sizer.py`:
```python
def calculate_kelly(win_rate: float, avg_rr: float) -> float:
    """
    Kelly Criterion: f = W - (1-W)/R
    W = win_rate (0.0-1.0), R = avg risk/reward ratio
    Returns half-Kelly: result * 0.5
    Hard cap: 0.02 (2% max of equity) — HARDCODED, never change
    """
    if avg_rr <= 0 or win_rate <= 0:
        return 0.0
    kelly = win_rate - ((1 - win_rate) / avg_rr)
    half_kelly = kelly * 0.5
    return max(0.0, min(0.02, half_kelly))  # 0.02 = 2% HARDCODED
```

**Step 2:** Create `src/agents/risk_guardian.py` with `evaluate_signal(signal: dict, portfolio_state: dict) -> dict`:
- Returns `{"approved": bool, "reason": str, "position_size_usd": float}`
- Check order (stop at first VETO):
  1. `equity_drawdown > 0.15` → VETO: "drawdown_limit" + trigger emergency
  2. `sector_count[signal.sector] >= 3` → VETO: "sector_cap"
  3. `chain not in allowed_chains` → VETO: "chain_not_eligible"
  4. `estimated_slippage > 0.02` → VETO: "slippage_too_high"
  5. Calculate position size. If `< 5.0` USD → VETO: "below_minimum_size"
  6. APPROVE

**Step 3:** Log every evaluation to a structured log line. Log VETOs to `system_config` as a running veto count.

**Step 4:** Emergency stop trigger — when drawdown > 15%, call:
```python
db.set_config("EMERGENCY_STOP", "TRUE")
telegram_notifier.send_emergency_alert(f"Drawdown exceeded 15%: {drawdown:.1%}")
```

#### File Targets
| File | Action |
|---|---|
| `src/core/kelly_sizer.py` | CREATE |
| `src/agents/risk_guardian.py` | CREATE |
| `tests/unit/test_risk_guardian.py` | CREATE |

#### Success Metrics
- All 5 veto conditions independently tested and working
- Position size never exceeds 2% of total equity in any scenario
- Veto logged with: ticker, veto_reason, fas_score, timestamp
- EMERGENCY_STOP set in system_config when drawdown > 15%
- Minimum position $5 enforced

#### Verification Commands
```bash
pytest tests/unit/test_risk_guardian.py -v

# Verify hard cap
python -c "
from src.core.kelly_sizer import calculate_kelly
# Even with perfect win rate and high RR, must not exceed 0.02
result = calculate_kelly(win_rate=1.0, avg_rr=100.0)
assert result <= 0.02, f'Hard cap violated: {result}'
print(f'Kelly capped at: {result}')
"
```

#### Expected Output
```
test_veto_drawdown_limit PASSED
test_veto_sector_cap PASSED
test_veto_chain_not_eligible PASSED
test_veto_slippage PASSED
test_veto_below_minimum_size PASSED
test_approve_valid_signal PASSED
test_emergency_stop_on_drawdown PASSED

Kelly capped at: 0.02
```

#### Common Mistakes
- DO NOT allow position size > 2% under any circumstance — this is a hard cap
- DO NOT forget to log VETOs permanently — silent vetos are a bug
- DO NOT allow ETH trades when capital < $1000 — check from system_config `total_capital`
- DO NOT let Risk Guardian approve and then second-guess — decision is final once returned

#### Definition of Done
- [ ] All 5 veto conditions implemented and tested
- [ ] Kelly sizer hard-capped at 2%
- [ ] Emergency stop triggers on >15% drawdown
- [ ] All vetoes logged with full context
- [ ] Unit tests cover every veto path

---

## SPRINT 3 — EXECUTION & MONITORING
### Milestone: `M3: Execution & Monitoring`

---

### ISSUE 009

```
title:     "Go execution engine: real order execution and dry-run"
labels:    ["go", "backend", "priority:critical"]
milestone: "M3: Execution & Monitoring"
```

#### Context
The Go engine is the only component that touches real money. It receives swap requests from Python via gRPC, simulates them first (dry-run), then executes if safe. It connects to OKX for CEX and Jupiter for Solana DEX. Sub-100ms execution is required after dry-run passes.

#### Pre-conditions
- Issue 004 (gRPC proto + stubs) complete
- OKX API credentials available in environment

#### Implementation Guide
**Step 1:** Implement `go_engine/executor/order.go`:
```go
// DryRunSwap simulates the swap and returns risk metrics
func DryRunSwap(ctx context.Context, req *proto.SwapRequest) (*proto.DryRunResult, error) {
    // 1. Fetch current orderbook from OKX
    // 2. Calculate estimated slippage based on order size vs liquidity
    // 3. Calculate price impact
    // 4. Return is_safe = (estimated_slippage < 0.02)  ← 0.02 = 2% HARDCODED
}

// ExecuteSwap places the real order after dry-run passes
func ExecuteSwap(ctx context.Context, req *proto.SwapRequest) (*proto.SwapResult, error) {
    // 1. Place market order via OKX REST API
    // 2. Wait for fill confirmation, max 30 seconds
    // 3. Return tx_hash, executed_price, actual_slippage
}
```

**Step 2:** OKX integration using their REST API (not a Go library — use `net/http` with HMAC-SHA256 signing). OKX requires: timestamp, method, path, body in signature.

**Step 3:** Jupiter DEX integration for Solana — use Jupiter Quote API (`https://quote-api.jup.ag/v6/quote`) and Swap API. For paper trading mode, skip actual signing.

**Step 4:** 30-second confirmation timeout — if order placed but not confirmed in 30s, return `success=false, error_message="timeout"`. Do NOT retry automatically.

#### File Targets
| File | Action |
|---|---|
| `go_engine/executor/order.go` | CREATE |
| `go_engine/executor/okx_client.go` | CREATE |
| `go_engine/executor/jupiter_client.go` | CREATE |
| `go_engine/main.go` | UPDATE (from stub to real) |

#### Success Metrics
- DryRunSwap returns slippage estimate within 500ms
- `is_safe=false` when estimated slippage > 2.0%
- ExecuteSwap completes or times out within 31 seconds (max)
- Paper trading mode (env: `PAPER_TRADING=true`) skips real execution

#### Verification Commands
```bash
# Paper trading mode test
PAPER_TRADING=true go run go_engine/main.go &

python -c "
from src.execution_bridge.grpc_client import dry_run_swap, execute_swap
result = dry_run_swap('SOL/USDC', 10.0, 'okx', False)
print('Dry run:', result)
assert 'estimated_slippage' in result
assert 'is_safe' in result
"
```

#### Expected Output
```
Dry run: {'estimated_slippage': 0.0031, 'price_impact': 0.0028, 'estimated_output': 9.969, 'is_safe': True, 'rejection_reason': ''}
```

#### Common Mistakes
- DO NOT execute real swaps when `PAPER_TRADING=true`
- DO NOT log OKX API secret or private key anywhere in Go logs
- DO NOT retry ExecuteSwap automatically — one attempt only
- DO NOT bind gRPC to `0.0.0.0` in production — use `127.0.0.1:50051`

#### Definition of Done
- [ ] DryRunSwap returns correct slippage estimate
- [ ] `is_safe` false when slippage > 2%
- [ ] ExecuteSwap has 30s timeout
- [ ] Paper trading mode implemented
- [ ] OKX and Jupiter clients working

---

### ISSUE 010

```
title:     "FastAPI WebSocket server + Next.js dashboard"
labels:    ["backend", "frontend", "dashboard", "priority:high"]
milestone: "M3: Execution & Monitoring"
```

#### Context
The dashboard is read-only. No trading controls live here — everything is via Telegram or CLI. The FastAPI backend pushes real-time events via WebSocket. The frontend connects and displays live data in the 5 views defined in DESIGN.md.

#### Pre-conditions
- Issue 002 (db.py) complete — REST endpoints read from DuckDB
- Issues 007–009 complete (agents generating events to push)
- Node.js 18+ installed for Next.js

#### Implementation Guide
**Step 1:** Create `src/api/main.py` (FastAPI):
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()
connected_clients: list[WebSocket] = []

@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep-alive ping from client
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

async def broadcast_event(event_type: str, data: dict):
    """Call this from agents to push events to dashboard."""
    message = json.dumps({"type": event_type, "data": data})
    for client in connected_clients.copy():
        try:
            await client.send_text(message)
        except Exception:
            connected_clients.remove(client)
```

**Step 2:** Add REST endpoints:
- `GET /api/portfolio` → calls Go engine gRPC `GetPortfolio()`
- `GET /api/trades?limit=50` → calls `db.get_recent_trades(limit)`
- `GET /api/ops` → ops fund balance + upcoming bills from `ops_ledger`
- `GET /api/agents` → agent status from `system_config` table
- `GET /api/eval` → evaluation history from `eval_history`

**Step 3:** Next.js dashboard — create 5 pages matching DESIGN.md layouts:
- `/` → Live Feed + Portfolio Snapshot
- `/analytics` → Charts page
- `/agents` → Agent cards
- `/ops` → Ops & Finance
- `/eval` → Evaluation history

Follow the component list in DESIGN.md section 3.11 (build Priority 1 components first).

**Step 4:** Install fonts: `@fontsource/ibm-plex-mono` and `@fontsource/ibm-plex-sans` in dashboard package.json.

#### File Targets
| File | Action |
|---|---|
| `src/api/main.py` | CREATE |
| `dashboard/app/page.tsx` | CREATE (Live Feed view) |
| `dashboard/app/analytics/page.tsx` | CREATE |
| `dashboard/app/agents/page.tsx` | CREATE |
| `dashboard/app/ops/page.tsx` | CREATE |
| `dashboard/components/` | CREATE (StatusBadge, DataCard, FeedRow, ScoreBar, PnlValue) |

#### Success Metrics
- WebSocket events appear in dashboard within 500ms of agent action
- All 5 REST endpoints return correct data from DuckDB
- Dashboard renders on mobile (test at 375px width)
- JWT rejects unauthenticated WebSocket connections

#### Verification Commands
```bash
# Start API
uvicorn src.api.main:app --port 8000 &

# Test WebSocket
python -c "
import asyncio, websockets, json
async def test():
    async with websockets.connect('ws://localhost:8000/ws/live') as ws:
        print('Connected to WebSocket')
        # Send test event
        from src.api.main import broadcast_event
        await broadcast_event('test', {'message': 'hello'})
        msg = await asyncio.wait_for(ws.recv(), timeout=2)
        print('Received:', json.loads(msg))
asyncio.run(test())
"

# Test REST
curl http://localhost:8000/api/portfolio
curl http://localhost:8000/api/trades?limit=5
```

#### Expected Output
```
Connected to WebSocket
Received: {'type': 'test', 'data': {'message': 'hello'}}

# Portfolio endpoint
{"total_capital": 312.40, "available_capital": 299.93, "positions": [...]}
```

#### Common Mistakes
- DO NOT add trading controls (buy/sell buttons) to dashboard — read-only only
- DO NOT use `localStorage` in Next.js for JWT — use httpOnly cookie
- DO NOT block WebSocket on DB query — use async DB wrapper
- DO NOT hardcode `localhost` in Next.js — use `NEXT_PUBLIC_API_URL` env var

#### Definition of Done
- [ ] WebSocket endpoint working
- [ ] `broadcast_event()` callable from agent code
- [ ] All 5 REST endpoints working
- [ ] All 5 Next.js pages built
- [ ] Priority 1 components built (StatusBadge, DataCard, FeedRow, ScoreBar, PnlValue)
- [ ] Mobile responsive

---

## SPRINT 4 — EVAL, OPS HARDENING & LAUNCH
### Milestone: `M4: Eval, Ops & Hardening`

---

### ISSUE 011

```
title:     "TUI: Python Textual terminal interface"
labels:    ["backend", "tui", "priority:medium"]
milestone: "M4: Eval, Ops & Hardening"
```

#### Context
The TUI is an alternative to the web dashboard for users on terminal-only servers. It uses Python Textual and connects to the same WebSocket as the dashboard. It follows the layout in DESIGN.md section 4.

#### Pre-conditions
- Issue 010 (FastAPI WebSocket) complete
- `textual` and `websockets` in requirements.txt

#### Implementation Guide
Follow DESIGN.md section 4 exactly:
- 4-panel layout: LiveFeed (left), PortfolioSnapshot (right-top), OpsHealthBar (right-mid), ActivePositions (right-bottom)
- AgentStrip at bottom
- 6-tab navigation (1–6 keys)
- Keyboard shortcuts as specified in DESIGN.md section 4.6
- Connect to `ws://localhost:8000/ws/live` using `websockets` library inside async Textual task

Create: `src/tui/app.py`, `src/tui/widgets.py`, `src/tui/styles/app.tcss`

Register CLI command: `cryptohedge tui` launches `textual run src/tui/app.py`

#### File Targets
| File | Action |
|---|---|
| `src/tui/app.py` | CREATE |
| `src/tui/widgets.py` | CREATE (LiveFeed, PortfolioSnapshot, AgentStrip, ScoreBar, OpsHealthBar, TradeTable) |
| `src/tui/styles/app.tcss` | CREATE |

#### Success Metrics
- TUI launches with `cryptohedge tui`
- Live feed updates in real-time from WebSocket
- All 6 keyboard shortcuts work
- Emergency stop (`e` key) requires typing "STOP" to confirm
- Renders correctly in 80×24 minimum terminal size

#### Verification Commands
```bash
# Launch TUI
cryptohedge tui

# Check min terminal size
resize -s 24 80 && cryptohedge tui
```

#### Expected Output
```
TUI renders 4-panel layout
AgentStrip shows 7 agent status dots
LiveFeed auto-scrolls on new events
```

#### Common Mistakes
- DO NOT use `time.sleep()` inside Textual app — use `asyncio.sleep()` or Textual timers
- DO NOT block the main thread with WebSocket recv — run in background worker
- DO NOT hardcode colors — use Textual CSS variables for light/dark compatibility

#### Definition of Done
- [ ] TUI launches via `cryptohedge tui`
- [ ] 6 panels render correctly
- [ ] WebSocket connected and live feed updating
- [ ] All keyboard shortcuts working
- [ ] Emergency stop confirmation flow working

---

### ISSUE 012

```
title:     "CLI: Rich + Click command interface"
labels:    ["backend", "cli", "priority:medium"]
milestone: "M4: Eval, Ops & Hardening"
```

#### Context
The CLI provides quick terminal access to bot status without launching the full TUI. Follows DESIGN.md section 5 exactly. Every command must support `--json` flag for automation.

#### Pre-conditions
- Issue 002 (db.py) complete
- Issue 010 (REST endpoints) complete
- `rich` and `click` in requirements.txt

#### Implementation Guide
Create `src/cli/main.py` with all commands from DESIGN.md section 5.2. Use Rich `Console`, `Table`, `Panel`, `Progress` for formatting. Output must match the examples in DESIGN.md section 5.3 exactly (same column headers, same alignment).

Register in `pyproject.toml`:
```toml
[project.scripts]
cryptohedge = "src.cli.main:cli"
```

#### File Targets
| File | Action |
|---|---|
| `src/cli/main.py` | CREATE |
| `src/cli/formatters.py` | CREATE (Rich table/panel builders) |
| `tests/unit/test_cli.py` | CREATE |

#### Success Metrics
- `cryptohedge status` renders in < 1 second
- `cryptohedge stop` requires typing "STOP" to confirm
- `cryptohedge trades --json` outputs valid JSON
- All commands exit 0 on success, exit 1 on error

#### Verification Commands
```bash
cryptohedge status
cryptohedge trades --limit 5
cryptohedge agents
cryptohedge ops
cryptohedge trades --json --limit 3 | python -m json.tool   # validate JSON
echo $?   # should be 0
```

#### Common Mistakes
- DO NOT use `input()` for confirmation — use `click.prompt()` or `click.confirm()`
- DO NOT use `print()` — use `rich.console.Console().print()`

#### Definition of Done
- [ ] All 8 commands implemented
- [ ] `--json` flag works on all commands
- [ ] Error format follows DESIGN.md section 5.4
- [ ] `cryptohedge stop` requires "STOP" confirmation
- [ ] Unit tests for CLI output format

---

### ISSUE 013

```
title:     "Security hardening: secret filter, whitelist, veto audit"
labels:    ["security", "backend", "priority:critical"]
milestone: "M4: Eval, Ops & Hardening"
```

#### Context
Security audit before paper trading. This issue does NOT add new features — it verifies that every security rule in AGENTS.md is actually implemented and cannot be bypassed.

#### Pre-conditions
- All previous issues in M1–M3 complete

#### Implementation Guide
**Step 1:** Secret filter audit — grep entire `src/` for any `print()` call. Every `print()` is a bug. Replace with logger.

**Step 2:** Whitelist enforcement — verify `Accountant` checks `whitelist_addresses` from system_config before every payment. Write integration test that attempts payment to non-whitelisted address and verifies it raises `PaymentNotWhitelistedError`.

**Step 3:** Dry-run gate — verify `ExecutionTrader` cannot call `execute_swap` without a preceding successful `dry_run_swap` result in the same cycle. Add a session token pattern: `dry_run_swap` returns a `run_token`, `execute_swap` requires that token.

**Step 4:** Hardcoded values test — write a test that reads every hardcoded value from running config and asserts they match expected:
```python
def test_hardcoded_values_unchanged():
    assert get_config("fas_threshold") == "0.75"       # or default
    assert MAX_DRAWDOWN_PCT == 0.15
    assert PROFIT_TAX_RATE == 0.005
    assert MAX_POSITION_PCT == 0.02
    assert MAX_SLIPPAGE_PCT == 0.02
    assert SECTOR_CAP == 3
```

#### File Targets
| File | Action |
|---|---|
| `tests/security/test_secret_filter.py` | CREATE |
| `tests/security/test_payment_whitelist.py` | CREATE |
| `tests/security/test_dryrun_gate.py` | CREATE |
| `tests/security/test_hardcoded_values.py` | CREATE |

#### Success Metrics
- Zero `print()` calls in `src/` (verified by grep)
- Payment to non-whitelisted address raises `PaymentNotWhitelistedError`
- `execute_swap` without prior dry-run raises `DryRunRequiredError`
- All hardcoded values match expected in test

#### Verification Commands
```bash
# Check for print() (should return nothing)
grep -rn "^[^#]*print(" src/ --include="*.py" | grep -v "test_"
echo "print() count above should be 0"

# Run security tests
pytest tests/security/ -v

# Verify no secrets in any log output
python -m src.heartbeat.daemon &
sleep 20 && kill %1
grep -i "secret\|private_key\|seed\|passphrase" daemon.log | grep -v "REDACTED"
echo "Any output above is a security violation"
```

#### Expected Output
```
# print() check
(no output)

# Security tests
test_secret_filter_blocks_private_key PASSED
test_secret_filter_blocks_api_secret PASSED
test_payment_to_nonwhitelisted_raises PASSED
test_execute_without_dryrun_raises PASSED
test_hardcoded_values_unchanged PASSED

# Log grep
(no output — all sensitive terms REDACTED)
```

#### Common Mistakes
- DO NOT only grep for `PRIVATE_KEY` — also check `api_secret`, `seed`, `passphrase`, `password`
- DO NOT skip the dry-run gate test — this is the most critical safety check
- DO NOT mark test as passing if it only tests the happy path

#### Definition of Done
- [ ] Zero `print()` in `src/`
- [ ] All 4 security test files pass
- [ ] Whitelist enforcement verified by test
- [ ] Dry-run gate verified by test
- [ ] Hardcoded values test passes

---

### ISSUE 014

```
title:     "Paper trading: 72-hour dry-run validation on live market data"
labels:    ["testing", "priority:critical"]
milestone: "M4: Eval, Ops & Hardening"
```

#### Context
Final validation before any real money goes in. The entire system runs with `PAPER_TRADING=true` for 72 hours. All logic runs for real — only the actual on-chain transaction is skipped. This proves the system works end-to-end.

#### Pre-conditions
- ALL previous issues complete
- `PAPER_TRADING=true` in `.env`
- All API keys configured (OKX, Telegram, CryptoPanic, Covalent)

#### Implementation Guide
**Step 1:** Set `PAPER_TRADING=true` in `.env`. This flag makes the Go engine return fake tx_hash without executing real orders.

**Step 2:** Start full stack: `docker-compose up`

**Step 3:** Monitor for 72 hours via TUI or dashboard. Document:
- How many ticks completed
- How many FAS signals generated
- How many approved vs vetoed
- How many simulated trades executed
- Whether ops_ledger updated correctly for each simulated profit

**Step 4:** Create `tests/integration/test_paper_trading.py` that runs a single tick cycle end-to-end with mocked APIs and real DuckDB.

#### Success Metrics
- System runs 72 hours without crash (4,320 ticks)
- At least 5 FAS >= 0.75 signals generated
- At least 1 Risk Guardian veto triggered (verify with logs)
- ops_ledger updated after each simulated profitable trade
- Dashboard shows correct data throughout
- Telegram notifications delivered for all events
- No sensitive data in any log file from 72h run

#### Verification Commands
```bash
# Start 72h paper trading
PAPER_TRADING=true docker-compose up -d

# Monitor ticks
docker-compose logs python_brain -f | grep "Tick #"

# After 72h, check counts
docker-compose exec python_brain python -c "
from src.state.db import get_connection
with get_connection() as conn:
    trades = conn.execute('SELECT COUNT(*) FROM trade_history').fetchone()[0]
    ops = conn.execute('SELECT COUNT(*) FROM ops_ledger').fetchone()[0]
    evals = conn.execute('SELECT COUNT(*) FROM eval_history').fetchone()[0]
    print(f'Trades: {trades}')
    print(f'Ops entries: {ops}')
    print(f'Eval entries: {evals}')
"

# Security: no secrets in logs
docker-compose logs | grep -i "secret\|private_key\|seed" | grep -v "REDACTED"
# Expected: no output
```

#### Expected Output
```
Trades: 12              (at least 5)
Ops entries: 8          (at least 1 per profitable trade)
Eval entries: 0–1       (micro eval may trigger in 72h)
(no sensitive data in logs)
```

#### Common Mistakes
- DO NOT run with real money before 72h paper trading passes
- DO NOT count the test as passing if the system crashed at any point
- DO NOT disable logging during paper trading — you need the full log for audit

#### Definition of Done
- [ ] 72 hours continuous operation without crash
- [ ] At least 5 signals processed
- [ ] ops_ledger correctly updated
- [ ] Dashboard functional throughout
- [ ] No secrets in logs
- [ ] Integration test passes

---

## ISSUE LABELS REFERENCE

```
setup           → Project initialization tasks
backend         → Python AI layer
go              → Go execution engine
frontend        → Next.js dashboard
database        → DuckDB schema/queries
agent           → CrewAI agent implementation
tools           → Score calculator tools (deterministic, not AI)
infra           → Docker, VPS, CI/CD
security        → Security rules and audits
testing         → Test suites and validation
tui             → Terminal UI (Textual)
cli             → CLI (Rich + Click)
priority:critical → Must complete for MVP
priority:high     → Important, not blocking
priority:medium   → Nice to have in timeline
```

---

*Version: 4.0 | Last Updated: 2026-04-24 | Total Issues: 14 | For AI agents: read every section of every issue before writing code*
