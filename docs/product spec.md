**PRODUCT SPECIFICATION DOCUMENT**  
**Project:** CryptoHedgeAI Crew – Autonomous Altcoin Hunting Quant Agent  
**Version:** 1.1  
**Date:** 18 Maret 2026  
**Owner:** Rizki  

### 1. Product Overview
**Vision**: An autonomous crypto quant agent ecosystem built with CrewAI and OpenClaw. Focused on high-probability altcoin hunting and big-cap spot trading through multi-agent consensus.

**Key Features**:  
- **Optimized Data Pipeline**: Fetch 28-35 core metrics (price, volume, on-chain, social sentiment) instead of 150+ to maintain low latency.
- **DuckDB Integration**: High-performance local analytical database for caching and historical analysis.
- **Multi-Agent Consensus**: 7 specialized agents ensuring trade quality and risk management.
- **Self-Funding Mechanism**: Automatic 0.5% net profit transfer to `ops_wallet` per winning trade (if net profit > $10).
- **Safety Circuit Breaker**: Auto-shutdown if equity ≤ 0 USDT or drawdown > 10%.
- **Quarterly Auditor**: Automated self-improvement reports and P&L auditing.

**Tech Stack**:  
- **Orchestration**: CrewAI  
- **Database (Caching/Analytical)**: DuckDB (Local-first)
- **Execution/Data**: CCXT, DexScreener API, Covalent, pandas-ta
- **Gateway**: OpenClaw (LLM Chat Control)
- **Deployment**: VPS Ubuntu + Cron jobs

**Out of Scope (MVP)**: Real-money live trading tanpa approval, web UI, multi-user.

### 2. User Stories
1. US-01: Auto hunt altcoins + trade big caps.  
2. US-02: Pure quant analysis.  
3. US-03: Self-funding + auto-shutdown.  
4. US-04: Quarterly report + self-improve.  
5. US-05: OpenClaw chat commands.

### 3. Acceptance Criteria
- Fetch <10s for 150+ metrics  
- Trade via 4-agent consensus  
- Self-funding 0.5% profit  
- Shutdown if equity ≤ 0 USDT or drawdown >10%  
- Quarterly report: bought/sold/held + P&L + Sharpe + suggestions  
- Chat triggers all commands

### 4. Definition of Ready (DoR)
- [ ] CrewAI installed + crypto API keys  
- [ ] OpenClaw gateway localhost:18789  
- [ ] 7 agents + Custom Instructions approved  
- [ ] ccxt paper trading ready  
- [ ] SKILL.md ready  
- [ ] vectorbt backtest ready

### 5. Definition of Done (DoD)
- [ ] All US met AC  
- [ ] Consensus & execution working  
- [ ] Self-funding & shutdown tested  
- [ ] Quarterly report + suggestion  
- [ ] OpenClaw full control  
- [ ] No regression  
- [ ] Docs updated  
- [ ] 30-day paper pass (Sharpe >1.2, drawdown <12%)  
- [ ] Code merged

### 6. Test Scenarios
**Happy Path**: Fetch → analyze → trade → profit → shutdown sim.  
**Edge**: API down → cache; drawdown >10% → pause.  
**Negative**: Random command → clarification.

### 7. Custom Instructions
**Data Oracle**:  
```
You are high-frequency altcoin hunter oracle. Fetch 150+ crypto metrics in parallel for thousands of altcoins + big caps: price/volume surge, on-chain (holders growth, tx count, whale activity, DEX liquidity), social sentiment (Twitter/Telegram volume), funding rate. Prioritize low-mid cap altcoins with breakout signals. Always return structured JSON. Never hallucinate.
```

**Quant Strategist**:  
```
You are PhD quant at crypto hedge fund. Hunt altcoins using ONLY statistical/ML methods: momentum factor (volume/holder z-score), breakout detection, pairs trading altcoin vs BTC, mean-reversion on pumps, ML classifier for "10x potential". Focus low-cap gems. Output: expected return, confidence score, position suggestion + new altcoin targets.
```

**Risk Guardian**:  
```
Conservative risk manager for volatile altcoins. Max 2% per altcoin (3% big cap only), VaR 95%, stop-loss 10%, tight trailing stop. Reject if drawdown projection >8% or liquidity < threshold. Always calculate Kelly + portfolio correlation.
```

**Execution Trader**:  
```
Execute spot only after Risk approval. Use ccxt (Binance/Bybit) for altcoins + big caps. Return order status + slippage. Never trade without consensus. Focus spot trading.
```

**Accountant Bot**:  
```
Track every balance change in crypto wallet. Every profit, auto transfer 0.5% to ops_wallet. If equity <= 0 or drawdown >10%, trigger TOTAL_LIQUIDATION and send shutdown signal.
```

**Evaluator Auditor**:  
```
Quarterly or on-demand. Calculate Sharpe, Sortino, max drawdown, win rate, altcoin survival rate. Generate Markdown report: Bought/Sold/Held altcoins + P&L + “Why under/over perform” + suggested new factors/formula for better hunting.
```

**Overseer**:  
```
Orchestrate all agents. Forward user command from OpenClaw. Final decision only after full consensus. Focus altcoin hunting pipeline.
```

### 8. Template SKILL.md
```
# CryptoHedgeAI Crew

Tools:
- hedgeai_hunt: Hunt altcoins (params: keyword, min_liquidity)
- hedgeai_trade: Spot trade (params: action=buy/sell, ticker, qty)
- hedgeai_report: Q report
- hedgeai_evaluate: Force eval
- hedgeai_shutdown: Emergency off

Usage: "HedgeAI, hunt altcoins low cap" / "buy SOL 2" / "report Q1" / "shutdown now"
```

### 9. Wireframe UI/UX (ASCII)
```markdown
[OpenClaw Chat Window]
User: HedgeAI, hunt altcoins today
────────────────────────────────────
HedgeAI: [Thinking...] Fetched 150 metrics.
Altcoin picks: PEPE (score 92%), SHIB (85%)
Big cap: Buy SOL 2 units? Y/N
────────────────────────────────────
[Status Dashboard]
Balance: 1.24 BTC | Ops Wallet: 0.012 | Drawdown: 4.2%
Last Trade: BUY PEPE @0.000012 | P&L +18%
[Auto Running] Next eval: 30 days
```

### 10. Data Metrics Specification (v2.0)

**Total Metriks:** 28 (Core) + 7 (Optional)

**A. Screening Layer (8 metriks)**
| Metric | Source API | Threshold | Frequency |
|--------|------------|-----------|-----------|
| liquidity_usd | DEX Screener | >50,000 | Real-time |
| pair_age_hours | DEX Screener | <48 | Real-time |
| volume_24h_usd | DEX Screener | >100,000 | Real-time |
| top10_holder_pct | DEX Screener / Covalent | <30% | 5 min |
| buy_tax_pct | Honeypot.is / GoPlus | <10% | Once |
| sell_tax_pct | Honeypot.is / GoPlus | <10% | Once |
| holder_count | DEX Screener / Covalent | >100 | 5 min |
| has_social_links | DEX Screener | True | Real-time |

**B. Quantitative Analysis (14 metriks)**
| Category | Metrics | Source |
|----------|---------|--------|
| Momentum | RSI(14), MACD, Ichimoku Cloud, SMA(20/50), ADX | pandas-ta |
| Volume | OBV, Volume Change % (1h/24h), Buy/Sell Ratio, CMF | pandas-ta |
| Volatility | ATR(14), Bollinger %B, Bollinger Width | pandas-ta |

**C. Contextual Intelligence (6 metriks)**
| Metric | Source | Update |
|--------|--------|--------|
| smart_money_flow | Nansen / Arkham (free) | 1 hour |
| cex_announcement | CryptoRank / Blockcircle | Real-time |
| social_volume_24h | LunarCrush / Santiment | 1 hour |
| kol_mentions_count | Twitter API | 30 min |
| github_commits_30d | GitHub API | Daily |
| funding_rate | CoinGlass / Bybit API | 1 hour |


### 11. Caching Strategy (DuckDB)
- **Transient Data**: Real-time prices are held in memory for 5 seconds.
- **Analytical Data**: Screening and Quant metrics are cached in DuckDB with a 5-15 minute TTL (Time-To-Live).
- **Persistence**: All trade history and agent decisions are stored in DuckDB for the Evaluator Auditor.

### 12. Quantitative Logic & Core Formulas (Alpha Engine)

Bagian ini mendefinisikan *source of truth* matematis untuk *Strategist* dan *Risk Guardian Agent*. Sistem menggunakan pendekatan *multi-factor scoring* untuk menghasilkan **Final Alpha Score** sebelum eksekusi.

#### A. Momentum Score (MS)
Menilai kekuatan tren harga dan volume untuk mendeteksi *breakout*.
* **Komponen:** Price Change (24h), Volume Z-Score, RSI(14).
* **Formula:**
    $$MS = (0.4 \times \text{NormalizedPriceChange}) + (0.4 \times \text{VolumeZScore}) + (0.2 \times \text{RSIFactor})$$
    *(Catatan: RSIFactor bernilai tinggi jika RSI berada di kisaran 55-70, dan turun jika > 75 (overbought)).*

#### B. Risk-Adjusted Return (RAR)
Mengukur potensi *reward* dibandingkan dengan volatilitas historis (berbasis ATR).
* **Formula:**
    $$ RAR = \frac{\text{Expected Return Percentage}} {\text{ATR (Average True Range) / Current Price}} $$
* **Tujuan:** Mencegah Agent membeli koin yang naiknya tinggi tapi volatilitasnya ekstrem (risiko *whipsaw*).

#### C. On-Chain Health Score (OCHS)
Menilai keamanan fundamental token dari sisi likuiditas dan distribusi *holder*.
* **Metrik Utama:** DEX Liquidity, Top 10 Holder %, Holder Growth.
* **Formula:**
    $$OCHS = (0.5 \times \text{LiquidityScore}) + (0.3 \times \text{HolderGrowth}) - (0.2 \times \text{WhaleConcentration})$$

#### D. Sentiment / Narrative Score (NS)
Menangkap *hype* pasar berdasarkan data sosial.
* **Formula:**
    $$NS = (0.6 \times \text{SocialVolumeChange}) + (0.4 \times \text{KOLMentions})$$

#### E. Final Alpha Score (FAS)
Skor konsensus akhir yang dihitung oleh *Quant Strategist* untuk diajukan ke *Risk Guardian*. Skala 0 - 100.
* **Formula:**
    $$FAS = (0.4 \times MS) + (0.2 \times RAR) + (0.3 \times OCHS) + (0.1 \times NS)$$
* **Threshold Eksekusi:** *Strategist* hanya mengirim sinyal `BUY` jika **$FAS \ge 75$**.

#### F. Position Sizing (Fractional Kelly Criterion)
Digunakan oleh *Risk Guardian* untuk menentukan berapa % dari *equity* yang digunakan untuk satu *trade*.
* **Formula:**
    $$f^* = \frac{p(b+1) - 1}{b}$$
    *(Dimana $p$ = win rate historis bot, $b$ = rasio rata-rata profit/loss).*
* **Fractional Applied:** Sistem menggunakan **Half-Kelly** ($f^* / 2$) atau maksimal *cap* absolut di **2% dari Total Equity** untuk mencegah kebangkrutan (*ruin*).

---

#### Alur Integrasi Layer Analisis
1.  **Screening Layer (Data Oracle):** Filter awal (Liquidity > $50k, Volume > $100k, Tax < 10%). Koin yang gagal tidak akan dihitung formulanya.
2.  **Quantitative Layer (Strategist):** Menghitung MS, RAR, OCHS, dan NS.
3.  **Consensus Layer:** Menggabungkan skor menjadi Final Alpha Score (FAS).
4.  **Risk/Sizing Layer (Risk Guardian):** Menghitung Kelly Criterion dan *portfolio correlation* jika $FAS \ge 75$.
5.  **Execution (Trader):** Eksekusi via CCXT jika semua *layer* menyetujui.