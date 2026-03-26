# SPRINT PLAN – CryptoHedgeAI Crew

## Sprint 1: Foundation & Glue (Semua yang bikin sistem bisa jalan)

**Goal**: Bikin fondasi runtime yang stabil, environment siap, dan orchestrator dasar yang bisa manggil agent-agent nanti.

| ID  | Task                         | Deskripsi                                                                                                                                                                                                           | Dependency | Acceptance Criteria                                                                                                   |
|-----|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|-----------------------------------------------------------------------------------------------------------------------|
| 1.1 | Project setup & dependencies | Python 3.11+ virtual env, `requirements.txt` (crewai, duckdb, httpx, asyncio, python-dotenv, etc.)                                                                                                                  | -          | `pip install -r requirements.txt` berhasil; struktur folder `/agents`, `/core`, `/state`, `/tools`, `/heartbeat` ada. |
| 1.2 | Environment config loader    | Load `.env` file; validasi ada `PRIVATE_KEY`, `TELEGRAM_BOT_TOKEN`, `RPC_ENDPOINTS`, `TOTAL_CAPITAL`; exit dengan pesan jelas jika ada yang kurang.                                                                 | 1.1        | Sistem gagal start dengan pesan "Missing required env: ..." jika ada yang kosong.                                     |
| 1.3 | DuckDB schema & migration    | Buat file `state/schema.sql` dengan semua tabel (`market_cache`, `trade_history`, `system_config`, `pending_expenses` dll) sesuai BLUEPRINT. Buat script `init_db.py` yang jalan pertama kali dan nge‑create tabel. | 1.1        | `init_db.py` create semua tabel; index pada `ticker` dan `status` sesuai spesifikasi.                                 |
| 1.4 | Heartbeat daemon dasar       | Script `heartbeat.py` yang loop setiap interval (misal 30 detik) dan trigger `Overseer.run_cycle()`. Pakai asyncio.                                                                                                 | 1.1        | Loop jalan, log "Heartbeat tick" setiap interval.                                                                     |
| 1.5 | Overseer agent skeleton      | Buat class `Overseer` dengan method `run_cycle()`. Untuk sprint ini, cuma logging "Overseer starting cycle".                                                                                                        | 1.4        | Saat heartbeat trigger, log muncul.                                                                                   |
| 1.6 | Structured logging           | Setup `logging` dengan JSON formatter, output ke file `logs/cryptohedge.log` dan console. Level INFO/DEBUG via env.                                                                                                 | 1.1        | Log muncul dalam format JSON, rotasi harian.                                                                          |
| 1.7 | Error handler decorator      | Buat decorator `@handle_errors` yang catch exception, log error, dan bisa return fallback.                                                                                                                          | 1.6        | Decorator bisa dipasang di agent methods.                                                                             |

**Sprint 1 Done Criteria**: `python heartbeat.py` jalan tanpa error, log muncul, database terinisialisasi, dan environment validation sukses.

---

## Sprint 2: Data Oracle & Alpha Engine (Dengan Error Tolerance)

**Goal**: Oracle bisa fetch data async, handle kegagalan, terapkan TTL, dan Quant Strategist bisa hitung FAS.

| ID  | Task                               | Deskripsi                                                                                                                                          | Dependency | Acceptance Criteria                                                           |
|-----|------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|------------|-------------------------------------------------------------------------------|
| 2.1 | Data Oracle – async fetcher        | Class `DataOracle` dengan method `fetch_metrics(tickers)`. Gunakan `httpx.AsyncClient`. Query DexScreener, CCXT, dll.                              | 1.1        | Bisa fetch 100 koin dalam <8 detik (paralel).                                 |
| 2.2 | DuckDB cache dengan TTL            | Oracle pertama cek cache. Jika data masih dalam TTL (15s untuk price/volume, 1h social, 24h security), return dari cache. Jika stale, fetch ulang. | 2.1, 1.3   | Data yang sama dalam TTL tidak memanggil API; setelah TTL habis, fetch ulang. |
| 2.3 | Network failure & retry logic      | Implement retry dengan exponential backoff (max 3x) saat API call gagal. Jika gagal total, fallback ke cache (meskipun stale) dan log warning.     | 2.2        | Simulasi matikan internet: Oracle tetap return data dari cache, tidak crash.  |
| 2.4 | Rate limit handler                 | Deteksi response 429; sleep sesuai `Retry-After` atau default 60s; ulang request.                                                                  | 2.3        | Rate limit di-handle tanpa crash.                                             |
| 2.5 | Partial failure tolerance          | Oracle fetch 100 tickers, jika 5 gagal, tetap return 95 yang sukses. Log error untuk yang gagal.                                                   | 2.3        | Sistem tetap jalan, hanya koin yang gagal di-skip.                            |
| 2.6 | Quant Strategist – FAS formula     | Implementasi fungsi `calculate_fas(metrics)` di `/core/fas.py`. Gunakan formula dari BLUEPRINT (28 metrik, bobot tertentu).                        | 2.2        | FAS score antara 0-100; unit test membuktikan perhitungan sesuai contoh.      |
| 2.7 | Unit test untuk FAS                | Tulis test di `tests/test_fas.py` dengan mock data. Pastikan FAS >=75 menghasilkan signal.                                                         | 2.6        | `pytest tests/` berhasil dengan coverage >80% untuk core math.                |
| 2.8 | Strategist integration ke Overseer | Overseer panggil Oracle, terus panggil Strategist untuk setiap koin. Simpan FAS score di memori (belum eksekusi).                                  | 2.6, 1.5   | Overseer loop log "Coin X FAS: Y".                                            |

**Sprint 2 Done Criteria**: Oracle bisa fetch data dengan retry dan fallback, FAS dihitung dengan benar, unit test lulus, dan Overseer bisa print FAS untuk koin.

---

## Sprint 3: Risk Guardian & Execution Trader (Dengan Dry‑Run)

**Goal**: Risk Guardian enforce sizing & sector cap, Trader execute swap (atau simulasi), Accountant catat.

| ID  | Task                                                                  | Deskripsi                                                                                                                                                     | Dependency                                | Acceptance Criteria                                                 |
|-----|-----------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------|---------------------------------------------------------------------|
| 3.1 | Risk Guardian – position sizing                                       | Implement `calculate_allocation(fas, total_capital)` berdasarkan Inverse Kelly matrix (High/Medium/Low).                                                      | 1.1                                       | FAS=90 → alokasi 4.5% dari modal; FAS=70 → alokasi 0.8%.            |
| 3.2 | Risk Guardian – sector cap                                            | Maintain in‑memory set of active positions per sector. Tolak jika dalam sektor yang sama sudah mencapai 3 token.                                              | 3.1, 1.3 (baca posisi dari trade_history) | Koin AI ke‑4 di‑veto dengan log "Sector cap AI reached".            |
| 3.3 | Risk Guardian – global cap                                            | Hitung total alokasi semua posisi aktif. Jika >100%, veto semua sinyal baru.                                                                                  | 3.2                                       | Tidak ada eksekusi baru jika modal sudah fully allocated.           |
| 3.4 | Execution Trader – swap simulation                                    | Method `simulate_swap(token_in, token_out, amount, chain)` hitung slippage, gas fee, return estimated output.                                                 | 1.1, CCXT integration                     | Simulasi mengembalikan estimated slippage; jika >2.0%, veto.        |
| 3.5 | Execution Trader – real swap                                          | Implement `execute_swap()` dengan private key dari env. Gunakan CCXT atau custom RPC. Pastikan tidak ada private key di log.                                  | 3.4, 1.2                                  | Swap sukses, hash tercatat, tidak ada key muncul di log.            |
| 3.6 | Dry‑run mode                                                          | Tambahkan flag `DRY_RUN=true` di env. Jika aktif, `execute_swap()` hanya log "would execute" tanpa on‑chain.                                                  | 3.5                                       | Swap tidak terjadi di on‑chain saat dry‑run.                        |
| 3.7 | Accountant – logging trade                                            | Setelah swap, Accountant catat ke `trade_history`: timestamp, token, chain, amount, price, slippage, gas, pnl (jika close).                                   | 3.5, 1.3                                  | Data trade masuk ke DuckDB.                                         |
| 3.8 | Accountant – profit tax & expenses                                    | Hitung 0.5% profit tax untuk setiap realized profit. Kurangi dari modal dan catat di `pending_expenses`.                                                      | 3.7                                       | Profit bersih sudah dipotong tax.                                   |
| 3.9 | Integration flow (Overseer → Strategist → Risk → Trader → Accountant) | Overseer sekarang panggil Strategist, lalu untuk koin dengan FAS>=75, panggil Risk Guardian, jika lolos, panggil Trader (dry‑run atau real), lalu Accountant. | 2.8, 3.1, 3.5, 3.7                        | Satu cycle penuh berjalan tanpa error; trade terjadi sesuai aturan. |

**Sprint 3 Done Criteria**: Dari start hingga trade tercatat di database, semua constraint (sector cap, sizing, slippage) di-enforce. Bisa jalan di dry‑run mode tanpa duit real.

---

## Sprint 4: Self‑Correction, Observability & Deployment

**Goal**: Evaluator bisa feedback ke sistem, health check, dan deployment siap.

| ID  | Task                                | Deskripsi                                                                                                                  | Dependency | Acceptance Criteria                                                      |
|-----|-------------------------------------|----------------------------------------------------------------------------------------------------------------------------|------------|--------------------------------------------------------------------------|
| 4.1 | Evaluator – performa kuartalan      | Analisis P&L dari `trade_history`, hitung Sharpe ratio, win rate, drawdown. Buat ringkasan.                                | 3.7        | Bisa generate laporan PDF dengan metrik dasar.                           |
| 4.2 | Evaluator – auto‑optimization       | Jika 3 kuartal berturut‑turut rugi, update `system_config` untuk turunkan FAS threshold atau ubah parameter Kelly.         | 4.1        | Sistem otomatis menurunkan ambang FAS setelah rugi terus.                |
| 4.3 | Evaluator – stop loss & take profit | Pantau posisi aktif, jika profit > target (misal 30%), Accountant jual sebagian; jika loss >15%, liquidasi.                | 4.1, 3.7   | Stop loss trigger dan close posisi.                                      |
| 4.4 | Emergency stop handler              | Overseer bisa menerima command `/panic` via Telegram. Saat panic, semua posisi close, sistem mati.                         | 4.3        | Command /panic dalam 30 detik semua posisi terjual, notifikasi Telegram. |
| 4.5 | Health check endpoint               | Buat file `/tmp/health` yang diupdate setiap cycle dengan timestamp dan status terakhir. Atau HTTP endpoint sederhana.     | 1.5        | File health menunjukkan "OK" dan timestamp.                              |
| 4.6 | Alerting enhancement                | Jika drawdown >15% atau emergency stop, kirim Telegram notif dengan prioritas tinggi.                                      | 4.4        | Notif darurat diterima di Telegram.                                      |
| 4.7 | Dockerfile & deployment script      | Buat Dockerfile, `docker-compose.yml` dengan volume untuk data dan logs. Tambah script `deploy.sh` untuk pull dan restart. | 1.1        | `docker-compose up` berhasil, sistem jalan.                              |
| 4.8 | Integration test (full simulation)  | Test dengan mock API, jalankan 10 cycle simulasi, verifikasi trade history dan constraint terpenuhi.                       | 3.9, 4.1   | Test lulus tanpa error, coverage >70%.                                   |


**Sprint 4 Done Criteria**: Evaluator bisa auto‑adjust parameter, emergency stop berfungsi, sistem bisa di‑deploy dengan Docker, dan ada integration test yang passing.

---

## 3. Catatan Tambahan

- **Urutan sprint** sudah disusun agar setiap sprint menghasilkan sesuatu yang *runnable* sendiri. Sprint 1 menghasilkan skeleton, Sprint 2 bisa menghitung FAS, Sprint 3 bisa execute trade, Sprint 4 bikin self‑correcting dan siap deploy.
- **Task dependency** gua cantumkan ID task yang harus selesai sebelumnya. Lu bisa tracking progress dengan mudah.
- **Acceptance criteria** dibuat spesifik supaya lu tahu kapan satu task benar‑benar selesai.