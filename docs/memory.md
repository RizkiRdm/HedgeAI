# Project Memory — CryptoHedgeAI

## Current State (2026-05-08)
- **Dashboard Stack:** Switched from Next.js 14 to Vite + React 19 due to development machine resource constraints.
- **Agent Progress:** 4/7 agents implemented. Missing: Execution Trader, Accountant, Eval Agent.
- **Infrastructure:** Task 1 completed. `telegram_notifier.py` refactored to async. `market_fetcher.py` implemented with retry logic and DexScreener/CCXT support.
- **Logic Progress:** FAS Formula and Slippage calculation currently missing dedicated modules in `src/core/`.

## Decisions & Constraints
- **Dashboard:** Stick with React 19 for MVP.
- **Architecture:** Maintain gRPC bridge between Python and Go.
- **Database:** Raw SQL with DuckDB (No ORM).

## Pending Tasks (from Review)
1. Implement missing agents to fix `overseer.py` imports.
2. Refactor math logic into `src/core/`.
3. Update ARCHITECTURE.md regarding the frontend stack.
