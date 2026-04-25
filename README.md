# CryptoHedgeAI Crew

Autonomous 7-agent AI system that scans 300+ crypto coins, calculates quality scores, and executes spot trades — without human emotion or fatigue.

## Overview

CryptoHedgeAI is an event-driven multi-agent pipeline designed for autonomous crypto trading. It leverages CrewAI for agent orchestration, DuckDB for high-performance data persistence, and a Go-based execution engine for real-time order processing.

## Tech Stack

- **AI Layer:** Python 3.11+, CrewAI, DuckDB, FastAPI
- **Execution Layer:** Go 1.22+, gRPC, WebSocket
- **Dashboard:** Next.js 14, TailwindCSS, Recharts
- **Infrastructure:** Docker, Docker Compose

## 7-Agent Architecture

1.  **Overseer:** System Orchestrator & Tick Controller.
2.  **Data Oracle:** Market Data Fetcher & Cache Manager.
3.  **Quant Strategist:** Signal Generator & FAS Calculator.
4.  **Risk Guardian:** Position Sizer & Veto Authority.
5.  **Execution Trader:** Trade Executor via Go Engine.
6.  **Accountant:** PnL Tracker & Financial Controller.
7.  **Eval Agent:** Performance Evaluator & Self-Reconfiguration Engine.

## Core Math: Final Alpha Score (FAS)

The system uses a deterministic formula to evaluate trade signals:

`FAS = (0.4 × MS) + (0.2 × RAR) + (0.3 × OCHS) + (0.1 × NS)`

- **MS:** Momentum Score
- **RAR:** Risk-Adjusted Return
- **OCHS:** On-Chain Health Score
- **NS:** Narrative Score

**Signal Threshold:** `FAS >= 0.75`

## Quick Start

```bash
# Setup environment
cp .env.example .env  # fill in your keys

# Build and run with Docker
docker-compose up --build
```

## Structure

- `src/`: Python AI/logic layer
- `go_engine/`: Go execution engine
- `dashboard/`: Next.js monitoring UI
- `tests/`: Unit and integration tests
- `data/`: DuckDB persistence volume
- `core/`: Shared math and configuration logic
- `state/`: Database schema and migrations
