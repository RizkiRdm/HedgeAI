# Project Memory — CryptoHedgeAI

## Current State (2026-05-08)
- **Dashboard Stack:** Switched from Next.js 14 to Vite + React 19 due to development machine resource constraints.
- **Agent Progress:** 7/7 agents implemented (Eval Agent is skeleton). Pipeline imports fixed in `overseer.py`.
- **Infrastructure:** Task 1, 2, & 3 completed. Go engine now supports realistic Paper Trading with real-time price fetching from OKX and Jupiter.
- **Logic Progress:** FAS Formula and Slippage calculation currently missing dedicated modules in `src/core/`.

## Decisions & Constraints
- **Dashboard:** Stick with React 19 for MVP.
- **Architecture:** Maintain gRPC bridge between Python and Go.
- **Database:** Raw SQL with DuckDB (No ORM).

## Pending Tasks (from Review)
1. Implement missing agents to fix `overseer.py` imports.
2. Refactor math logic into `src/core/`.
3. Update ARCHITECTURE.md regarding the frontend stack.
