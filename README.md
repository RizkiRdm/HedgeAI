# 🦅 CryptoHedgeAI Crew
**Autonomous Agent Runtime for High-Probability Altcoin Discovery & Risk-Shielded Execution.**

HedgeAI adalah sistem kuantitatif berbasis agen (CrewAI) yang dirancang untuk mendeteksi peluang di pasar crypto menggunakan formula **Final Alpha Score (FAS)** dan eksekusi yang dijaga ketat oleh **Risk Guardian**.

---

## 🚀 Quick Start

### 1. Prerequisites
* **Runtime**: Python 3.11+
* **Package Manager**: [uv](https://github.com/astral-sh/uv) (Recommended) or `pip`

### 2. Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd CryptoHedgeAI

# Install dependencies
uv pip install -r requirements.txt
```

### 3. Environment Setup
Salin template env dan isi kredensial lu. **Penting**: Sistem tidak akan jalan jika ada key yang kosong.
```bash
cp .env.example .env
# Edit .env dengan PRIVATE_KEY, TELEGRAM_BOT_TOKEN, dll.
```

### 4. Initialize Database
Buat schema DuckDB untuk pertama kali.
```bash
python state/init_db.py
```

### 5. Run the Engine
```bash
python heartbeat.py
```

---

## 🧠 The Crew (Agents)
Sistem ini digerakkan oleh 7 agen spesialis dengan tugas spesifik:
* **Overseer**: Konduktor orkestrasi siklus.
* **Data Oracle**: Fetcher data 28 metrik secara async.
* **Quant Strategist**: Otak di balik kalkulasi FAS Score.
* **Risk Guardian**: Pertahanan terakhir (Veto & Sizing).
* **Execution Trader**: Sniper eksekusi on-chain (SOL, BSC, BASE).
* **Accountant**: Pencatat P&L dan pengelola fee operasional.
* **Evaluator**: Auditor performa dan self-optimization.

---

## 🛡️ Safety & Constraints
* **Inverse Kelly Sizing**: Alokasi modal dinamis berdasarkan convition score.
* **Sector Cap**: Maksimal 3 koin per sektor untuk diversifikasi.
* **Emergency Stop**: Gunakan `/panic` via Telegram untuk likuidasi instan.
* **Dry Run**: Aktifkan `DRY_RUN=true` untuk testing tanpa dana riil.

---

## 📁 Directory Structure
* `/agents`: Definisi agen & prompt.
* `/core`: Formula matematika (FAS, Kelly).
* `/state`: Schema DuckDB & maintenance.
* `/tools`: Wrapper API (DexScreener, CCXT).
* `/heartbeat`: Daemon script untuk loop sistem.

---

## 📜 Documentation
Untuk detail arsitektur mendalam, silakan baca [ARCHITECTURE.md](./docs/ARCHITECTURE.md).
