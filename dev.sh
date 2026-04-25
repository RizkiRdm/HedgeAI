#!/bin/bash

# Konfigurasi Environment
export PAPER_TRADING=true
export PYTHONPATH=$PYTHONPATH:.
export DB_PATH="data/cryptohedge.duckdb"
mkdir -p logs

# Fungsi Cleanup: Matikan semua proses background saat TUI atau script distop
cleanup() {
    echo ""
    echo "🛑 Stopping all engines and dashboard..."
    kill $(jobs -p) 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

echo "🚀 Starting CryptoHedgeAI Full Suite..."

# 1. Start Go Execution Engine
echo "📦 [1/5] Launching Go Execution Engine..."
(cd go_engine && go run main.go) > logs/go.log 2>&1 &
sleep 2

# 2. Start FastAPI Backend
echo "🌐 [2/5] Launching FastAPI Backend..."
uv run uvicorn src.api.main:app --port 8000 --log-level info > logs/api.log 2>&1 &
sleep 2

# 3. Start Heartbeat Daemon (AI Brain)
echo "🧠 [3/5] Launching Heartbeat Daemon..."
uv run python -m src.heartbeat.daemon > logs/heartbeat.log 2>&1 &

# 4. Start Web Dashboard (Next.js)
echo "🖥️  [4/5] Launching Web Dashboard (http://localhost:3000)..."
if [ -d "dashboard/node_modules" ]; then
    (cd dashboard && npm run dev) > ../logs/web.log 2>&1 &
else
    echo "⚠️  node_modules not found in /dashboard. Web skipped. Run 'npm install' manually."
fi

echo "📺 [5/5] Launching Terminal UI..."
echo "------------------------------------------------"
echo "💡 All logs are being saved to the /logs directory."
echo "💡 Close the TUI (press 'q') to stop all services."
echo "------------------------------------------------"
sleep 2

# 5. Start TUI in Foreground
uv run python src/tui/app.py

# Jika TUI ditutup, jalankan cleanup
cleanup
