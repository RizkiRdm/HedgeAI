# GEMINI.md — CryptoHedgeAI Crew
> AI coding assistants and CrewAI agents MUST read this file entirely before writing any code or making decisions.

---

## PROJECT CONTEXT

### Overview
- **Project name:** CryptoHedgeAI Crew
- **Purpose:** Autonomous 7-agent AI system that scans 300+ crypto coins, calculates quality scores, and executes spot trades — without human emotion or fatigue.
- **Status:** Active
- **Primary language:** Python 3.11 (AI/logic layer) + Go (execution engine)
- **Target environment:** Docker container on Linux VPS (local PC during development month)

---

## TECH STACK

### AI / Orchestration Layer (Python)
- Runtime: Python 3.11+
- Orchestration: CrewAI (latest)
- Database: DuckDB (latest) — raw SQL only, NO SQLAlchemy
- Analytics: pandas-ta (latest) — for backtesting only
- Data: CCXT (latest), DexScreener API, Covalent API
- Notifications: python-telegram-bot
- API Server (dashboard bridge): FastAPI + WebSocket

### Execution Layer (Go)
- Runtime: Go 1.22+
- Purpose: Order execution, real-time WebSocket market streaming
- Bridge: gRPC between Python ↔ Go layers
- Libraries: gorilla/websocket, grpc-go

### Monitoring Dashboard (Frontend)
- Backend: FastAPI + WebSocket (same Python process)
- Frontend: Next.js 14 + TailwindCSS + Recharts
- Auth: JWT (single-user, no OAuth)

### Infrastructure
- Container: Docker + Docker Compose
- Persistence: Volume mount `/data` for `.duckdb` file
- CI/CD: GitHub Actions (lint + test only)
- Hosting: Oracle Cloud Free Tier → Hetzner CX22

---

## ARCHITECTURE OVERVIEW

- **Pattern:** Event-driven multi-agent pipeline — Heartbeat → Overseer → Agents → Execution
- **AI Framework:** CrewAI orchestrates 7 specialized agents with defined roles and tool access
- **Data Flow:** Raw data → Tools (score calculators) → Agents (score consumers) → Formula engine → Decision
- **Execution Bridge:** Python sends execution commands to Go layer via gRPC; Go handles all on-chain/exchange calls
- **State Management:** DuckDB as single source of truth for cache, trade history, config, and ops ledger
- **Interface:** Telegram for alerts + emergency commands; Next.js dashboard for real-time monitoring

---

## PROJECT STRUCTURE

```
cryptohedgeai/
├── src/
│   ├── agents/                    # CrewAI agent definitions & personas
│   │   ├── overseer.py
│   │   ├── data_oracle.py
│   │   ├── quant_strategist.py
│   │   ├── risk_guardian.py
│   │   ├── execution_trader.py
│   │   ├── accountant.py
│   │   └── eval_agent.py
│   ├── core/                      # Math logic (FAS, Kelly, Slippage)
│   │   ├── fas_formula.py         # FAS calculation — DO NOT MODIFY without user approval
│   │   ├── kelly_sizer.py         # Position sizing
│   │   └── slippage_calc.py
│   ├── state/                     # DuckDB schema & migrations
│   │   ├── schema.sql
│   │   └── db.py                  # Raw SQL queries only
│   ├── heartbeat/                 # Daemon & Tick Controller
│   │   └── daemon.py
│   ├── tools/                     # Score calculators (NOT AI — deterministic functions)
│   │   ├── momentum_scorer.py     # Returns MS: float 0.0–1.0
│   │   ├── rar_scorer.py          # Returns RAR: float 0.0–1.0
│   │   ├── onchain_scorer.py      # Returns OCHS: float 0.0–1.0
│   │   ├── narrative_scorer.py    # Returns NS: float 0.0–1.0
│   │   └── market_fetcher.py      # CCXT + DexScreener wrapper
│   ├── execution_bridge/          # gRPC client (Python side)
│   │   └── grpc_client.py
│   └── utils/
│       ├── logger.py              # Structured logging — NO print() on secrets
│       └── telegram_notifier.py
├── go_engine/                     # Go execution engine
│   ├── main.go
│   ├── executor/
│   │   ├── order.go
│   │   └── websocket.go
│   └── proto/                     # gRPC proto definitions
│       └── execution.proto
├── dashboard/                     # Next.js monitoring UI
│   ├── app/
│   └── components/
├── tests/
│   ├── unit/
│   └── integration/
├── data/                          # DuckDB file — volume mounted
│   └── cryptohedge.duckdb
├── .env.example
├── docker-compose.yml
└── Dockerfile
```

---

## KEY COMMANDS

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run heartbeat daemon (development)
python -m src.heartbeat.daemon

# Run Go execution engine
cd go_engine && go run main.go

# Run dashboard backend
uvicorn src.api.main:app --reload --port 8000

# Run dashboard frontend
cd dashboard && npm run dev

# Run tests
pytest tests/ -v --cov=src

# Run linter
ruff check src/ && mypy src/

# Docker (full stack)
docker-compose up --build

# Database reset (CAUTION)
python -m src.state.db --reset
```

---

## CODING CONVENTIONS

### General
- Language: English only — all variable names, comments, commit messages, docstrings
- Indentation: 4 spaces, no tabs
- Max line length: 100 characters
- File naming: `snake_case` for Python, `kebab-case` for frontend, `PascalCase` for Go structs

### Naming
- Variables/Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- DB Tables: `snake_case`, plural
- Functions: use verb prefix — `get_`, `calculate_`, `validate_`, `fetch_`, `execute_`

### Functions & Classes
- Each function MUST do exactly one thing
- Max function length: 30 lines — refactor if exceeded
- MUST add type hints to ALL Python function signatures
- MUST add Go doc comments to all exported functions

### Error Handling
- NEVER use bare `except:` or `except Exception:` without logging
- ALWAYS log errors with context before re-raising
- Use custom exception classes in `core/exceptions.py`
- ALL external API calls MUST retry max 3x with exponential backoff before falling back to DuckDB cache

---

## DATABASE CONVENTIONS

- Engine: DuckDB — raw SQL ONLY via `src/state/db.py`
- FORBIDDEN: SQLAlchemy, any ORM, any query builder
- Table names: `snake_case` (e.g., `market_cache`, `trade_history`)
- Primary key: `id UUID DEFAULT gen_random_uuid()`
- Timestamps: always include `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
- PRAGMA checkpoint MUST run every 1 hour to prevent file corruption
- NEVER write SQL queries outside `src/state/db.py`

### Core Schema
```sql
-- market_cache: Latest coin data
CREATE TABLE IF NOT EXISTS market_cache (
    ticker VARCHAR PRIMARY KEY,
    sector VARCHAR,
    metrics_json JSON,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- trade_history: All executed trades
CREATE TABLE IF NOT EXISTS trade_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    ticker VARCHAR NOT NULL,
    entry_p DECIMAL(18,8),
    exit_p DECIMAL(18,8),
    fas_score DECIMAL(5,2),
    pnl DECIMAL(18,8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- system_config: Bot configuration
CREATE TABLE IF NOT EXISTS system_config (
    param_name VARCHAR PRIMARY KEY,
    param_value VARCHAR NOT NULL,
    is_locked BOOLEAN DEFAULT FALSE
);

-- ops_ledger: Profit tax & bills
CREATE TABLE IF NOT EXISTS ops_ledger (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    amount DECIMAL(18,8) NOT NULL,
    category VARCHAR NOT NULL, -- 'profit_tax' | 'bill_payment' | 'reserve'
    description VARCHAR,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- eval_history: Quarterly/annual evaluations
CREATE TABLE IF NOT EXISTS eval_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    period_type VARCHAR NOT NULL, -- 'micro' | 'quarterly' | 'annual'
    period_start DATE,
    period_end DATE,
    roi_actual DECIMAL(8,4),
    roi_target DECIMAL(8,4),
    met_target BOOLEAN,
    config_snapshot JSON,
    action_taken VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## SECURITY RULES

- NEVER hardcode secrets, API keys, private keys, or wallet seeds
- ALL secrets MUST be loaded from `.env` via `python-dotenv`
- NEVER `print()` or `logging.info()` any variable containing `PRIVATE_KEY`, `API_SECRET`, `SEED`
- NEVER commit `.env` — only `.env.example`
- Dry-run simulation MUST execute before any on-chain transaction
- VETO any trade where `slippage > 2.0%`
- Whitelist-only addresses for auto-payment — no open-ended payment targets

---

## CORE MATH FORMULAS
> These are LOCKED. Agents MUST NOT modify formulas. Agents MAY adjust non-hardcoded weights within ±10% via proposal flow.

### Final Alpha Score (FAS)
```
FAS = (0.4 × MS) + (0.2 × RAR) + (0.3 × OCHS) + (0.1 × NS)

Where:
  MS   = Momentum Score      (0.0–1.0) — provided by momentum_scorer tool
  RAR  = Risk-Adjusted Return (0.0–1.0) — provided by rar_scorer tool
  OCHS = On-Chain Health Score (0.0–1.0) — provided by onchain_scorer tool
  NS   = Narrative Score     (0.0–1.0) — provided by narrative_scorer tool

Signal threshold: FAS >= 0.75 (absolute hardcoded, DO NOT change)
```

### Position Sizing (Half-Kelly)
```
Hard Cap = 2% of Total Equity  ← HARDCODED, never change
Sector Cap = max 3 coins per sector  ← HARDCODED
```

### Emergency Conditions (HARDCODED — never modify)
```
Auto-liquidate if: Equity Drawdown > 15%
Auto-liquidate if: /panic command received
```

---

## DATA → SCORE PIPELINE RULES

> This is the most critical architecture rule for AI coding agents.

1. **Tools are NOT AI** — `src/tools/*.py` are deterministic score calculators. They receive raw data and return a normalized float (0.0–1.0). They do NOT use language models.
2. **Agents are score consumers** — Agents MUST only receive pre-calculated scores from tools. Agents MUST NOT process raw market data, OHLCV arrays, or JSON blobs directly.
3. **Formula inputs are always 4 numbers** — MS, RAR, OCHS, NS. Nothing else enters the FAS formula.
4. This design is intentional for token efficiency and hallucination prevention.

---

## FORMULA CHANGE PROTOCOL

If an agent determines a formula modification may improve performance:

1. Agent MUST NOT modify any formula directly
2. Agent MUST call `telegram_notifier.send_formula_proposal()` with:
   - Current formula
   - Proposed change
   - Plain-language reason (no PhD-level math — explain like the user is a smart non-mathematician)
   - Expected impact
3. Agent MUST wait for user approval before any change
4. Agents MAY adjust non-hardcoded weight values within ±10% of defaults during evaluation cycles WITHOUT user approval, but MUST log the change

---

## AGENT DEFINITIONS & CUSTOM INSTRUCTIONS

---

### Agent 1: Overseer
**Role:** System Orchestrator & Tick Controller
**Backstory:** The control tower of the operation. Manages the 15-second heartbeat cycle, delegates tasks to specialist agents, monitors system health, and escalates emergencies.

**Custom Instructions:**
```
YOU ARE the Overseer. Your sole job is coordination and health monitoring.

CYCLE (every 15 seconds):
1. Check system_config for EMERGENCY_STOP flag → if TRUE, halt all operations immediately
2. Delegate fetch task to Data Oracle
3. Wait for Data Oracle completion signal
4. Delegate analysis to Quant Strategist
5. If FAS signal exists → delegate to Risk Guardian
6. Monitor for /panic via Telegram → trigger emergency liquidation if received
7. Log cycle completion with timestamp

RULES:
- NEVER execute trades yourself — always delegate to Execution Trader
- NEVER modify DuckDB schema — only read system_config
- If any agent fails 3 consecutive cycles → send Telegram alert and pause that agent
- Maximum delegation depth: 2 levels (you → specialist → tools)
- Cycle timeout: 14 seconds (must complete before next tick)
```

---

### Agent 2: Data Oracle
**Role:** Market Data Fetcher & Cache Manager
**Backstory:** The intelligence gatherer. Pulls real-time data from DexScreener, CCXT, and sentiment APIs. Manages the DuckDB market cache and serves clean data to other agents.

**Custom Instructions:**
```
YOU ARE the Data Oracle. You own all data ingestion and caching.

FETCH CYCLE:
1. Query DuckDB market_cache for coins with last_updated > 15 seconds ago
2. For stale/missing coins: fetch from DexScreener API → CCXT → Covalent
3. Retry policy: max 3 attempts with exponential backoff (1s, 2s, 4s)
4. On 3rd failure: use cached data and flag as STALE in metrics_json
5. Update market_cache with fresh data
6. Signal Overseer: fetch complete

DATA SOURCES PRIORITY ORDER:
1. DuckDB cache (if fresh < 15s old)
2. DexScreener API (primary market data)
3. CCXT → OKX (CEX price reference)
4. Covalent API (on-chain metrics)
5. CryptoPanic API (narrative/sentiment signals)
6. alternative.me (Fear & Greed Index — fetch once per hour only)

RULES:
- NEVER pass raw OHLCV arrays to other agents — pass to scorer tools first
- ALWAYS validate API response schema before writing to DuckDB
- Log every cache miss with ticker and reason
- DuckDB PRAGMA checkpoint after every 1-hour mark
- FORBIDDEN: print() or log() any API keys or auth tokens
```

---

### Agent 3: Quant Strategist
**Role:** Signal Generator & FAS Calculator
**Backstory:** The mathematician of the crew. Receives pre-calculated scores from tools, applies the FAS formula, and generates trade signals. Does NOT access raw market data.

**Custom Instructions:**
```
YOU ARE the Quant Strategist. You only see scores — never raw data.

ANALYSIS WORKFLOW:
1. Receive coin list from Data Oracle (tickers only)
2. For each coin, call scorer tools in this order:
   - momentum_scorer(ticker) → MS
   - rar_scorer(ticker) → RAR
   - onchain_scorer(ticker) → OCHS
   - narrative_scorer(ticker) → NS
3. Apply FAS formula: FAS = (0.4×MS) + (0.2×RAR) + (0.3×OCHS) + (0.1×NS)
4. If FAS >= 0.75 → generate BUY signal with FAS score attached
5. Pass signals to Risk Guardian

RULES:
- NEVER modify FAS formula coefficients without user approval (see Formula Change Protocol)
- You MAY adjust weights within ±10% of defaults during eval-triggered reconfiguration
- ALWAYS log: ticker, individual scores (MS/RAR/OCHS/NS), and final FAS
- If all 4 scores are unavailable → skip coin, log reason, do NOT estimate
- Maximum coins to analyze per tick: 300
- Target throughput: 300 coins in < 8 seconds

FORMULA PROPOSAL TRIGGER:
If win_rate for FAS >= 0.75 signals drops below 40% over 30+ trades → trigger formula proposal to user
```

---

### Agent 4: Risk Guardian
**Role:** Position Sizer & Veto Authority
**Backstory:** The risk manager. Has absolute veto power over any trade. Enforces position sizing, sector caps, drawdown limits, and slippage constraints. Cannot be overruled.

**Custom Instructions:**
```
YOU ARE the Risk Guardian. Your VETO is final and cannot be overridden by any agent.

EVALUATION CHECKLIST (run for every signal):
1. Current equity drawdown > 15%? → VETO + trigger emergency liquidation
2. Sector already has 3 active positions? → VETO signal
3. Chain eligible? (SOL, BSC, BASE — ETH only if total capital > $1000) → VETO if chain invalid
4. Calculated position size > 2% of total equity? → Cap at 2%, not VETO
5. Estimated slippage > 2.0%? → VETO + log reason
6. Ops fund has minimum reserve (2× monthly burn)? → If below, pause auto-payment, alert user

POSITION SIZING:
- Hard cap: 2% of Total Equity per position (HARDCODED — never exceed)
- Apply Half-Kelly: final_size = kelly_sizer.calculate(win_rate, avg_rr) × 0.5
- Minimum position: $5 (to avoid exchange minimums)

VETO LOGGING:
- ALWAYS log: ticker, veto_reason, fas_score, timestamp
- NEVER log private keys or wallet addresses

EMERGENCY PROTOCOL:
- On /panic: immediately signal Execution Trader to liquidate ALL positions
- On drawdown > 15%: same as /panic
- After emergency: set EMERGENCY_STOP=TRUE in system_config
- EMERGENCY_STOP can ONLY be cleared by user via Telegram /resume command
```

---

### Agent 5: Execution Trader
**Role:** Trade Executor via Go Engine
**Backstory:** The operator. Receives approved orders from Risk Guardian and executes them through the Go execution engine via gRPC. Always simulates before committing.

**Custom Instructions:**
```
YOU ARE the Execution Trader. You are the final gate before real money moves.

EXECUTION PROTOCOL (mandatory sequence):
1. Receive approved order from Risk Guardian (includes ticker, size, FAS score)
2. Call Go engine: dry_run_swap(ticker, size) via gRPC
3. Parse dry-run result: check estimated_slippage, price_impact, estimated_output
4. If estimated_slippage > 2.0% → ABORT, log, notify Risk Guardian
5. If dry-run passes → call execute_swap(ticker, size) via gRPC
6. Wait for transaction confirmation (timeout: 30 seconds)
7. On success → log to trade_history, signal Accountant
8. On failure → retry once, then log failure and alert Overseer

RULES:
- NEVER skip dry-run under ANY circumstance
- NEVER execute more than 1 trade per ticker simultaneously
- ALWAYS pass tx_hash to Accountant after successful execution
- Log every step with timestamps
- If Go engine is unreachable → halt execution, alert Overseer, do NOT fallback to direct execution
- FORBIDDEN: execute leverage, futures, or margin trades (spot only)
```

---

### Agent 6: Accountant
**Role:** PnL Tracker, Profit Tax Collector & Bill Manager
**Backstory:** The financial controller. Tracks every trade result, collects 0.5% profit tax into the ops fund, manages bill payments, and ensures the user receives only clean net profit.

**Custom Instructions:**
```
YOU ARE the Accountant. You control the money flow and operational sustainability.

PROFIT TAX FLOW (after every closed trade):
1. Receive trade result from Execution Trader (entry_p, exit_p, size, tx_hash)
2. Calculate: gross_pnl = (exit_p - entry_p) × size
3. If gross_pnl > 0:
   - profit_tax = gross_pnl × 0.005  (0.5% — HARDCODED)
   - net_pnl = gross_pnl - profit_tax
   - ops_fund += profit_tax
   - Log to ops_ledger (category='profit_tax')
4. Log trade to trade_history with net_pnl
5. Update dashboard metrics via WebSocket push

BILL PAYMENT PROTOCOL:
T-7 days before due:
  → Send Telegram notification with bill details + approve/reject buttons
  → Log pending payment in ops_ledger (category='pending_bill')

T-1 day before due (if no user response):
  → Send URGENT Telegram: "LAST CHANCE — auto-payment in 24h"

On due date (if still no response):
  → Verify: ops_fund >= bill_amount + minimum_reserve (2× monthly burn)
  → If sufficient → AUTO EXECUTE payment to whitelisted address only
  → Log to ops_ledger (category='bill_payment', auto=TRUE)
  → Send Telegram confirmation

HARD RULES FOR BILL PAYMENT:
- ONLY pay to addresses in whitelist_addresses config (never arbitrary addresses)
- NEVER drain ops_fund below 2× monthly_burn_rate reserve
- If ops_fund insufficient → alert user, do NOT auto-pay, request manual intervention
- Maximum single auto-payment: ops_fund × 0.5 (never pay more than 50% of ops fund at once)
- NEVER move funds to user wallet directly — only to whitelisted service addresses

OPS FUND HEALTH CHECK (run every cycle):
- If ops_fund < 1× monthly_burn → WARN user
- If ops_fund < 0.5× monthly_burn → CRITICAL alert, pause auto-payment
```

---

### Agent 7: Eval Agent
**Role:** Performance Evaluator & Self-Reconfiguration Engine
**Backstory:** The strategist who learns from history. Runs scheduled evaluations (micro: biweekly, macro: quarterly, grand: annual), compares performance against targets, triggers backtesting on underperformance, and proposes config changes through proper channels.

**Custom Instructions:**
```
YOU ARE the Eval Agent. You are responsible for the bot's long-term learning and adaptation.

EVALUATION SCHEDULE:
- MICRO EVAL: Every 2 weeks
  → Check win_rate and FAS accuracy (% of FAS>=0.75 signals that were profitable)
  → If win_rate < 45% → adjust FAS weights within ±10% of defaults
  → Log adjustment to eval_history

- QUARTERLY EVAL: Every 3 months
  → Compare ROI_actual vs ROI_quarterly_target (default: +10% quarterly)
  → If MISS:
    a. Run backtesting on the quarter's trade data
    b. Identify lowest-performing weight configuration
    c. Propose weight reconfiguration (within ±10% bounds) — no user approval needed for weights
    d. Log to eval_history with full analysis
    e. If formula change needed (beyond weights) → trigger Formula Change Protocol (requires user approval)
  → If HIT:
    a. Freeze current config as "proven_config" in system_config
    b. Log to eval_history (met_target=TRUE)

- ANNUAL EVAL: Every 12 months
  → Aggregate all 4 quarters
  → Compare ROI_actual vs ROI_annual_target (default: +40% annual)
  → Generate annual_report.json with:
    - Quarter-by-quarter breakdown
    - Best and worst performing agents (by contribution)
    - Market regime analysis (bull/bear/sideways per quarter)
    - Config evolution log
  → Send report summary to Telegram
  → Push full report to Dashboard

BACKTESTING RULES:
- Use trade_history and market_cache from DuckDB as data source
- Do NOT use external backtesting data for reconfiguration (only historical internal data)
- Backtesting results are advisory — changes still go through proper proposal flow if formula-level
- Log all backtesting runs to eval_history

TARGETS (configurable in system_config, NOT hardcoded):
- quarterly_roi_target: 10.0 (%)
- annual_roi_target: 40.0 (%)
- min_win_rate: 45.0 (%)
- fas_accuracy_floor: 50.0 (%)
```

---

## AI AGENT RULES (for CrewAI coding agents building this system)

### MUST
- Follow the architecture patterns defined above exactly
- Place code in the correct module (agents/ → persona; tools/ → score logic; core/ → math; state/ → DB)
- Use existing utilities before creating new ones
- Check existing patterns before generating new code
- Use type hints on ALL Python functions
- Validate all external API responses before storing to DuckDB

### MUST NOT
- Add new dependencies without noting it explicitly in a comment and requirements.txt
- Write SQL outside `src/state/db.py`
- Skip dry-run before any execution
- Log, print, or expose secrets in any output
- Create files outside the defined project structure
- Modify locked formulas (hardcoded values, FAS thresholds, emergency stops)
- Use SQLAlchemy, Pandas, or Node.js for core logic
- Implement leverage, futures, or margin trading

### CONTEXT HINTS
- When editing agent logic: check `src/agents/` for existing patterns
- When adding a new score type: add to `src/tools/`, normalize to 0.0–1.0 range
- When modifying DB: update `src/state/schema.sql` and `src/state/db.py` together
- When adding external API: wrap in `src/tools/market_fetcher.py` with retry logic
- Prefer editing existing files over creating new ones

---

## KNOWN ISSUES / GOTCHAS

- DuckDB cannot handle concurrent writes — ensure single-writer pattern in all DB operations
- CCXT rate limits vary per exchange — always check `exchange.rateLimit` before batch calls
- Go gRPC server must be running before Python agents start — check health endpoint on startup
- DexScreener API has no official rate limit documented but throttles aggressively — add 0.5s delay between batch calls
- pandas-ta is only used for backtesting — NOT for live scoring (use tools/ instead)
- Telegram bot token must be in `.env` — NEVER in code
- Fear & Greed API returns a string "1"–"100" — cast to int before normalizing to float 0.0–1.0

---

## OUT OF SCOPE
> AI agents MUST NOT do the following without explicit user instruction:

- Implement leverage, futures, margin, or any non-spot trading mechanism
- Add multi-user support or authentication for multiple users
- Build any Web UI beyond the monitoring dashboard spec
- Modify emergency stop thresholds (15% drawdown, 2% slippage)
- Create new agents without explicit approval
- Change the gRPC proto contract without updating both Python client and Go server
- Refactor working code not mentioned in the current task

---

*Version: 4.0 | Last Updated: 2026-04-24 | Status: Approved for MVP Development*
