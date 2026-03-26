# UX Design Document: CryptoHedgeAI Crew (v2.0)
**Project:** Autonomous Altcoin Hunting Quant Agent
**Author:** AI Specialist & Rizki
**Date:** 21 Maret 2026

---

## 1. Fondasi dan Riset (Strategi & Lingkup)

### Tujuan Bisnis & Kebutuhan Pengguna
* **Tujuan**: Menciptakan sistem trading *autonomous* yang mampu mendeteksi peluang "10x potential" di market altcoin secara real-time tanpa intervensi manual yang konstan.
* **Kebutuhan**: Pengguna membutuhkan sistem yang disiplin secara algoritma, memiliki manajemen risiko yang ketat (Max 2% risk), dan mampu menangani operasional finansialnya sendiri (Self-funding).

### User Persona: "The Silent Alpha Hunter"
* **Profil**: Trader/Developer yang sibuk, tidak punya waktu scanning 500+ koin manual, tapi ingin tetap ekspos ke market high-growth.
* **Pain Points**: *Analysis paralysis*, emosi saat *cut loss*, dan ribet mengurus biaya langganan API/Server secara manual.

### User Journey Map
1.  **Deployment**: User menjalankan bot di VPS.
2.  **Passive Monitoring**: User melihat log teks di Terminal PC untuk memastikan "jantung" sistem berdetak (Oracle scan, Strategist calculate).
3.  **Critical Alert**: User menerima notifikasi Telegram saat trade eksekusi terjadi.
4.  **Quarterly Review**: User menerima PDF laporan otomatis, mengevaluasi performa, dan membiarkan bot melakukan optimasi mandiri jika hasil minus.

---

## 2. Arsitektur Informasi & Alur (Struktur)

### Informasi Arsitektur (IA)
* **Terminal (Real-time Engine)**:
    * `Engine Status`: Uptime, Agent Consensus state.
    * `Live Logs`: Raw text logs dari 7 agents.
    * `Cashflow`: Real-time balance (Equity & Ops Wallet).
* **Telegram (Command & Alert)**:
    * `Trade Alerts`: Info Buy/Sell + Swap details.
    * `Reports`: Quarterly PDF files.
    * `Manual Override`: Emergency stop/status commands.

### User Flow: Automated Trade & Optimization
1.  **Sinyal Muncul** (FAS ≥ 75) → **Risk Check** (Max 2%) → **Swap & Buy**.
2.  **Notifikasi Telegram** dikirim ke User (Silent: Off for trade).
3.  **Akhir Kuartal** → **Generate PDF** → **Kirim Telegram**.
4.  **Performa < Target** → **Auto-Backtest** → **Update Config** secara mandiri.

---

## 3. Desain Interaksi (Rangka/Skeleton)

### Wireframe Visual (ASCII Style)

#### A. Terminal PC (Log-Centric Dashboard)
Fokus pada estetika teks fungsional dan keterbacaan log.
```text
┌───────────────── CryptoHedgeAI Engine ──────────────────┐
│  PORTFOLIO VALUE: $1,240.50 [▲ 4.5%]  DRAWDOWN: 2.1%    │
├─────────────────────────────────────────────────────────┤
│ [LOGS]                                                  │
│ 14:02:01 [ORACLE] Scanned 500 pairs. 12 filtered.       │
│ 14:02:05 [STRAT]  $PAPA FAS Score: 88. Triggering Buy.  │
│ 14:02:06 [RISK]   Limit 2% OK. Position: $24.8.         │
│ 14:02:08 [TRADER] Swapping USDT -> SOL -> PAPA...      │
│ 14:02:10 [ACC]    Trade Logged to DuckDB.               │
└─────────────────────────────────────────────────────────┘
│ [CASHFLOW]                                              │
│ (+) $0.50 (Profit Tax to Ops)                           │
│ (-) $12.00 (Server Bill Paid via Ops_Wallet)            │
└─────────────────────────────────────────────────────────┘
```

#### B. Telegram HP (Silent/Active Notifications)
```text
[ 🤖 HedgeAI Alert ] - (NOTIF: SOUND ON)
──────────────────────
TRADE EXECUTED: BUY $PAPA
Network: SOLANA
Risk Applied: 2.0% ($24.8)
FAS Score: 88%
Status: Confirmed 🟢
──────────────────────

[ 📈 HedgeAI Report ] - (NOTIF: SOUND ON)
──────────────────────
Q1_Performance_Report.pdf (2.4 MB)
Status: UNDERPERFORM (Sharpe: 0.9)
Action: Auto-Optimization Started.
──────────────────────

[ ℹ️ System Log ] - (NOTIF: SILENT)
Next scan in 15 minutes...
Ops_Wallet balance updated.
```

### Anotasi Fungsi
* **Terminal Log**: Log harus menggunakan *timestamp* dan label agent (ORACLE, STRAT, RISK, dll).
* **Equity Dashboard**: Menampilkan angka real-time yang di-update setiap kali ada perubahan saldo di DuckDB.
* **Telegram Notification**: Menggunakan mode `Silent: True` untuk log rutin dan `Silent: False` untuk pesan kritis (Trade & Report).

---

## 4. Desain Visual & Prototipe (Permukaan/Surface)

* **High-Fidelity (Terminal)**: Menggunakan skema warna *Monokrom/Matrix* (Hijau/Putih di atas Hitam) untuk mengurangi kelelahan mata.
* **Desain Sistem**: 
    * `Hijau`: Transaksi sukses / Profit.
    * `Merah`: Drawdown / Emergency Shutdown.
    * `Kuning`: Sinyal masuk / Tahap kalkulasi.
* **PDF Report**: Laporan kuartalan menggunakan desain minimalis dengan grafik garis P&L dan tabel ringkasan transaksi.

---

## 5. Validasi dan Iterasi

### Laporan Riset Pengguna (Rizki's Feedback)
* **Update v2.0**: Penambahan logika *auto-swap* karena kebutuhan trading di chain non-USDT.
* **Update v2.1**: Implementasi *Silent Notification* untuk mengurangi *noise* di HP user.

### Dokumentasi Iteratif
* **Iterasi 1**: Fokus pada trading big caps (Manual).
* **Iterasi 2 (Current)**: Full autonomous altcoin hunting, self-funding operasional, dan optimasi mandiri berbasis backtest.