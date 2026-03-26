# Scenario Registry: CryptoHedgeAI Crew (v2.0)
**Status:** Ready for Implementation  
**Version:** 2.0 (Integrated Math Logic & Multi-Chain Support)  
**Date:** 21 Maret 2026

---

## A. Trading & Discovery (Alpha Engine)

### S1 – Multi-Chain Alpha Hunting & Auto-Swap
**Precondition:**
- Wallet memiliki saldo USDT yang cukup.
- Data Oracle telah melakukan screening awal (Liquidity > $50k, Tax < 10%, Volume > $100k).

**Flow:**
1. **Strategist** menghitung *Final Alpha Score* (FAS) berdasarkan MS, RAR, OCHS, dan NS.
2. Jika **FAS ≥ 75**, Strategist mengirimkan sinyal `BUY` ke Risk Guardian.
3. **Risk Guardian** menghitung *Position Sizing* menggunakan **Half-Kelly Criterion** dengan *hard-cap* **maksimal 2%** dari total equity per koin.
4. **Execution Trader** melakukan pengecekan pair (misal: PAPA/SOL).
5. **Execution Trader** menjalankan swap otomatis: `USDT → Native Token (SOL/BASE/dll)` → `Native Token → Target Coin`.
6. **Terminal PC** menampilkan log eksekusi, rincian swap, dan perubahan saldo secara real-time.

**Expected Result:**
- Transaksi tereksekusi pada koin target meskipun berbeda jaringan.
- Risiko per transaksi tidak pernah melebihi 2%.
- Seluruh langkah tercatat di DuckDB dan Terminal.

---

## B. Financial & OpEx Management

### S2 – Automated Self-Funding & Expense Payment
**Precondition:**
- Terdapat transaksi profit dengan nilai Net Profit > $10.
- Tabel `pending_expenses` di DuckDB berisi tagihan operasional aktif.

**Flow:**
1. **Accountant Bot** memotong 0.5% profit dan mengirimkannya ke `ops_wallet`.
2. **Accountant Bot** melakukan scan tagihan rutin (API, Server, dll) dengan tenggat waktu 1 bulan.
3. Jika saldo `ops_wallet` mencukupi, bot melakukan pembayaran otomatis ke provider.
4. **Accountant Bot** mencatat detail log pembayaran (apa yang dibayar & sisa saldo) ke DuckDB.

**Expected Result:**
- Biaya operasional terbayar secara mandiri tanpa intervensi user.
- Log pembayaran dapat diaudit melalui Terminal atau query SQL.

---

## C. Reporting & Optimization

### S3 – Proactive Reporting & Auto-Optimization (Quarterly)
**Precondition:**
- Siklus kuartal (3 bulan) berakhir secara otomatis berdasarkan sistem clock.

**Flow:**
1. **Evaluator Auditor** menarik data performa (Sharpe, Win Rate, Drawdown) dari DuckDB.
2. **Evaluator Auditor** men-generate laporan dalam format **PDF**.
3. Bot mengirimkan PDF tersebut ke **Telegram HP** user tanpa diminta.
4. **Logic Check:**
    - Jika laporan menunjukkan **Profit/Sesuai Target**: Bot meminta validasi di Telegram untuk evaluasi ulang.
    - Jika laporan menunjukkan **Minus / Underperform**: Bot langsung menjalankan backtesting (optimization) secara otomatis.
5. Hasil optimasi yang memiliki backtest positif langsung di-apply ke sistem trading real-money.

**Expected Result:**
- User menerima laporan PDF tepat waktu.
- Sistem memperbaiki parameter strateginya sendiri jika performa buruk.

### S4 – Annual Strategic Optimization
**Precondition:**
- Penutupan tahun kalender (Q4 selesai).

**Flow:**
1. **Evaluator Auditor** menggabungkan data dari seluruh kuartal (Q1-Q4).
2. Agent menjalankan optimasi menyeluruh (Annual Backtest) untuk meningkatkan performa di Q1 tahun baru.
3. Hasil optimasi diterapkan otomatis ke konfigurasi agent tanpa perubahan manual oleh user.

**Expected Result:**
- Strategi trading berevolusi mengikuti tren market tahunan.

---

## D. Interface & Safety

### S5 – Remote Monitoring & Emergency Shutdown
**Precondition:**
- OpenClaw dan Telegram Bot aktif.

**Flow:**
1. User memonitor status melalui **Telegram** (High Level) dan **Terminal PC** (Technical Logs).
2. Jika sistem mendeteksi **Equity ≤ 0 USDT** atau **Total Drawdown > 10%**:
3. **Accountant Bot** memicu signal `TOTAL_LIQUIDATION`.
4. **Execution Trader** menutup semua posisi aktif ke USDT.
5. Sistem mengirimkan notifikasi shutdown ke Telegram dan Terminal.

**Expected Result:**
- Modal terlindungi dari kerugian lebih lanjut secara otomatis.
- User mendapatkan notifikasi instan di HP.