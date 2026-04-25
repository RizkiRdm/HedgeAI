# DESIGN.md — CryptoHedgeAI Interface Specification
> Design reference for Web Dashboard and Terminal interfaces (TUI + CLI).
> This file is the single source of truth for all interface decisions.

---

## TABLE OF CONTENTS

1. [Design Philosophy](#1-design-philosophy)
2. [Shared Design System](#2-shared-design-system)
3. [Web Dashboard](#3-web-dashboard)
4. [TUI — Terminal User Interface](#4-tui--terminal-user-interface)
5. [CLI — Command Line Interface](#5-cli--command-line-interface)
6. [Interaction Patterns](#6-interaction-patterns)

---

## 1. DESIGN PHILOSOPHY

### Core Principle: Data First, Decoration Never

Both interfaces serve one purpose: **give the operator instant situational awareness**. Every design decision is justified by: "does this help the user understand what the bot is doing right now?"

### Aesthetic Direction

```
Web    → Swiss Minimalism  — grid-based, high contrast, monospace accents, zero decoration
TUI    → Bloomberg Terminal — dense but organized, status-driven color, keyboard-first
CLI    → Unix Precision     — structured output, predictable format, machine-readable option
```

### Shared Principles

- **Information density over empty space** — every pixel/character earns its place
- **Status colors are semantic** — colors carry meaning, not branding
- **Monospace for data, proportional for labels** — distinguish data from UI chrome
- **No success theater** — don't over-celebrate. Quiet confidence when things work.
- **Loud failure** — errors are impossible to miss, with exact reason and next action

---

## 2. SHARED DESIGN SYSTEM

### 2.1 Color Tokens

```
SEMANTIC COLORS (apply across both web and TUI)
─────────────────────────────────────────────────
Status: PROFIT    → Green   web:#16a34a  tui:bright_green
Status: LOSS      → Red     web:#dc2626  tui:bright_red
Status: NEUTRAL   → Muted   web:#808080  tui:dim
Status: WARNING   → Amber   web:#d97706  tui:yellow
Status: CRITICAL  → Red     web:#dc2626  tui:bright_red  (bold)
Status: ACTIVE    → White   web:#000000  tui:bright_white (bold)
Status: VETO      → Red     web:#dc2626  tui:red

SURFACE COLORS
─────────────────────────────────────────────────
bg-primary    → #FFFFFF / #000000  (light/dark)
bg-secondary  → #F5F1E8 / #0a0a0a
border        → #000000 / #FFFFFF
text-primary  → #000000 / #FFFFFF
text-muted    → #808080
text-accent   → #B38B6D  (taupe — ops/finance contexts)
```

### 2.2 Typography Scale

```
Web:
  display  → font-size: clamp(2rem, 5vw, 4rem), weight: 700, tracking: -0.03em
  heading  → font-size: 1.25rem, weight: 700, tracking: -0.01em
  label    → font-family: monospace, size: 0.7rem, tracking: 0.15em, UPPERCASE
  body     → font-size: 0.875rem, line-height: 1.7
  data     → font-family: monospace, size: 0.875rem

TUI / CLI:
  All text is monospace by default (terminal constraint)
  Use BOLD for headings and active values
  Use DIM for muted/secondary text
  Use ITALIC sparingly — only for status labels
```

### 2.3 Status Badge Format

```
Web:   [ LIVE ]  [ VETOED ]  [ EXECUTING ]  [ PAUSED ]
TUI:   ● LIVE    ✗ VETOED    → EXECUTING    ⏸ PAUSED
CLI:   [LIVE]    [VETO]      [EXEC]         [PAUSED]
```

### 2.4 Number Formatting Rules

```
PnL positive   → prefix +, green color    → +$14.23
PnL negative   → prefix -, red color      → -$3.10
PnL zero       → neutral, no prefix       → $0.00
FAS score      → always 3 decimal places  → 0.847
Percentage     → always 1 decimal place   → 12.4%
USD amounts    → 2 decimal places         → $1,204.50
Large numbers  → K suffix at 1000+        → 1.2K coins
Timestamps     → ISO-ish, local TZ        → 2026-04-24 14:32:01
Duration       → Xh Ym Zs                 → 2h 14m 03s
```

---

## 3. WEB DASHBOARD

### 3.1 Tech Stack

```
Framework  : Next.js 14 (App Router)
Styling    : Tailwind CSS (utility-first, no component library)
Charts     : Recharts
Real-time  : WebSocket (native browser API → FastAPI backend)
Auth       : JWT stored in httpOnly cookie
Font       : IBM Plex Mono (data) + IBM Plex Sans (labels)
Icons      : Lucide React (stroke icons only, no fill)
```

### 3.2 Layout System

```
Grid: 12-column, gap: 2rem, max-width: 1440px
Sidebar: 240px fixed left, full height
Main: fluid right of sidebar
Topbar: 56px fixed top (zero on mobile)

Breakpoints:
  mobile   → < 640px   : sidebar collapses to bottom tab bar
  tablet   → 640–1024px: sidebar becomes 64px icon-only
  desktop  → > 1024px  : full sidebar visible
```

```
┌─────────────────────────────────────────────────────────────────┐
│  TOPBAR [56px] — status strip + cycle counter + emergency btn   │
├──────────────┬──────────────────────────────────────────────────┤
│              │                                                  │
│   SIDEBAR    │              MAIN CONTENT AREA                   │
│   [240px]    │              (fluid, scrollable)                 │
│              │                                                  │
│  Navigation  │                                                  │
│  items       │                                                  │
│              │                                                  │
│  ──────────  │                                                  │
│              │                                                  │
│  Ops fund    │                                                  │
│  health bar  │                                                  │
│              │                                                  │
└──────────────┴──────────────────────────────────────────────────┘
```

### 3.3 Topbar

```
LEFT:  ◆ CryptoHedgeAI  |  Tick #4821  |  ● LIVE (pulsing dot)
RIGHT: [Capital: $312.40]  [Ops: $8.14]  [■ EMERGENCY STOP]
```

- Pulsing green dot = system active, ticks every 15s
- Red dot = EMERGENCY_STOP active
- Emergency Stop button: red border, requires double-click confirmation
- Capital and Ops fund update via WebSocket push

### 3.4 Sidebar Navigation

```
◆ CryptoHedgeAI
─────────────────
⬡  Live Feed
▤  Portfolio
◎  Analytics
⬚  Agents
⊡  Ops & Finance
—
⊘  Eval History
⚙  Config
─────────────────
Ops Fund
████████░░  81%
$8.14 / $10.00
~1.8 mo runway
```

- Active nav item: black background, white text (inverted)
- Ops fund health bar: green >50%, amber 20–50%, red <20%
- All navigation items are keyboard-navigable (1-7 hotkeys)

### 3.5 Page: Live Feed

```
LAYOUT: 2-column  →  [Feed: 8col] [Snapshot: 4col]

FEED COLUMN:
─────────────────────────────────────────────────────
14:32:01  OVERSEER     Cycle #4821 started
14:32:01  ORACLE       Fetching 300 coins...
14:32:04  ORACLE       ✓ Cache updated [3.2s]  [300 coins]
14:32:04  QUANT        Scoring batch...
14:32:07  QUANT        ✓ 3 signals above FAS 0.75
14:32:07  RISK         Evaluating SOL/USDC  FAS: 0.847
14:32:07  RISK         ✓ Approved  size: $6.25  sector: DeFi [1/3]
14:32:07  TRADER       Dry-run: slippage 0.31% → Safe
14:32:08  TRADER       Executing on Jupiter...
14:32:09  TRADER       ✓ TX confirmed [tx:7xKp...3mR9]
14:32:09  ACCOUNTANT   Tax: +$0.03 → ops_fund  Net PnL: +$0.14
─────────────────────────────────────────────────────
Agent label colors: OVERSEER=muted, ORACLE=blue, QUANT=yellow,
RISK=red/green depending on veto/approve, TRADER=white, ACCOUNTANT=taupe

SNAPSHOT COLUMN:
┌─────────────────────────┐
│ ACTIVE POSITIONS        │
│                         │
│ SOL/USDC  +2.1%  $6.30 │
│ BNB/USDC  -0.4%  $6.22 │
│                         │
│ LAST SIGNAL             │
│ FAS  0.847   ████████▒░ │
│ MS   0.91    ████████▒░ │
│ RAR  0.74    ███████░░░ │
│ OCHS 0.88    ████████▒░ │
│ NS   0.79    ███████▒░░ │
│                         │
│ CYCLE TIMING            │
│ Last: 7.8s   Max: 8.0s  │
└─────────────────────────┘
```

### 3.6 Page: Portfolio

```
LAYOUT: Top KPI strip → 2-column content

KPI STRIP (4 cards, horizontal):
┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
│ CAPITAL   │ │ ACTIVE    │ │ UNREALIZED│ │ TODAY PnL │
│ $312.40   │ │ 2 POS     │ │ +$0.51    │ │ +$1.24    │
│ ─────     │ │ ─────     │ │ ─────     │ │ ─────     │
│ Available │ │ of 6 max  │ │ +0.16%    │ │ +0.40%    │
└───────────┘ └───────────┘ └───────────┘ └───────────┘

LEFT: Active Positions Table
┌──────────────────────────────────────────────────────────┐
│ TICKER    ENTRY      CURRENT    PnL        FAS    CHAIN  │
├──────────────────────────────────────────────────────────┤
│ SOL/USDC  $142.10    $145.10    +$0.37     0.847  SOL    │
│ BNB/USDC  $312.00    $310.80    +$0.14     0.812  BSC    │
└──────────────────────────────────────────────────────────┘

RIGHT: Sector Exposure
┌─────────────────────────┐
│ SECTOR CAPS             │
│                         │
│ DeFi   ██░░  1 / 3      │
│ AI     ██░░  1 / 3      │
│ Meme   ░░░░  0 / 3      │
│ L1     ░░░░  0 / 3      │
│                         │
│ CHAIN ALLOCATION        │
│ SOL  ████░░  $6.25  50% │
│ BSC  ████░░  $6.22  50% │
└─────────────────────────┘
```

### 3.7 Page: Analytics

```
CONTROLS: [Weekly ▾] [Monthly] [Quarterly] [Annual]
           date range picker on the right

ROW 1 — HEADLINE METRICS (5 cards):
  Sharpe Ratio | Win Rate | Avg RR | Max Drawdown | FAS Accuracy

ROW 2 — EQUITY CURVE (full width, Recharts LineChart):
  X-axis: date, Y-axis: portfolio value in USD
  Show: equity line (black), drawdown shading (red fill below baseline)
  Hover tooltip: date, value, drawdown %, active trades count

ROW 3 — 2-column:
  LEFT:  Win/Loss distribution (Recharts BarChart, green/red bars)
  RIGHT: Sector performance table
         SECTOR | TRADES | WIN% | TOTAL PnL | AVG FAS
         DeFi   | 12     | 75%  | +$3.21    | 0.831
         AI     | 8      | 62%  | +$1.87    | 0.802
         Meme   | 4      | 25%  | -$0.44    | 0.761

ROW 4 — FAS ACCURACY ANALYSIS:
  Table: FAS Range | Signals | Profitable | Win% | Avg PnL
         0.75–0.80 | 8       | 4          | 50%  | +$0.12
         0.80–0.85 | 12      | 9          | 75%  | +$0.31
         0.85–1.00 | 4       | 4          | 100% | +$0.58
```

### 3.8 Page: Agents

```
7 agent cards in a responsive grid (4-col desktop, 2-col tablet, 1-col mobile)

CARD STRUCTURE:
┌─────────────────────────────┐
│ 01  OVERSEER                │
│     System Orchestrator     │
│ ─────────────────────────── │
│ Status    ● ACTIVE          │
│ Uptime    99.8%  14d 3h     │
│ Cycles    4,821             │
│ Failures  2  (last: 2d ago) │
│ ─────────────────────────── │
│ Avg cycle   7.8s / 14s max  │
│ Delegations 14,463          │
└─────────────────────────────┘

RISK GUARDIAN card extras:
│ Vetos total   47            │
│ Capital saved $187.30       │
│ Veto reasons (pie chart)    │
│  Slippage 40% | Sector 35%  │
│  Drawdown 15% | Chain 10%   │

EVAL AGENT card extras:
│ Next micro eval  3d 14h     │
│ Next quarterly   41d        │
│ Last action  weight adj.    │
│ Config changes  3           │
```

### 3.9 Page: Ops & Finance

```
TOP: Ops Fund status
┌──────────────────────────────────────────┐
│ OPS FUND                                 │
│ $8.14          ████████████░░░░  81%     │
│                                          │
│ Monthly burn est.    $4.50               │
│ Runway               ~1.8 months         │
│ Auto-pay status      ● ENABLED           │
└──────────────────────────────────────────┘

MIDDLE: Upcoming Bills table
┌─────────────────────────────────────────────────────┐
│ SERVICE     AMOUNT  DUE DATE    STATUS               │
├─────────────────────────────────────────────────────┤
│ Hetzner VPS $4.50   2026-05-01  ⏳ Pending (7d)     │
│ LunarCrush  $29.00  2026-05-15  ● Scheduled          │
└─────────────────────────────────────────────────────┘

BOTTOM: Ledger history (paginated, 20 rows/page)
TYPE          AMOUNT    CATEGORY       DATE        NOTE
profit_tax    +$0.03    Trade #4821    2026-04-24  SOL/USDC
bill_payment  -$4.50    Server         2026-04-01  Auto: Hetzner
profit_tax    +$0.08    Trade #4819    2026-04-24  BNB/USDC
```

### 3.10 CSS Design Tokens

```css
/* Copy these into your global CSS / tailwind.config.js */
:root {
  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;

  /* Typography */
  --font-sans: 'IBM Plex Sans', sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;

  /* Colors — light mode */
  --color-bg: #FFFFFF;
  --color-bg-secondary: #F5F1E8;
  --color-border: #000000;
  --color-text: #000000;
  --color-muted: #808080;
  --color-accent: #B38B6D;
  --color-profit: #16a34a;
  --color-loss: #dc2626;
  --color-warn: #d97706;

  /* Layout */
  --sidebar-width: 240px;
  --topbar-height: 56px;
  --border-radius: 0px;       /* Swiss: no radius */
  --border-width: 1.5px;
}

[data-theme="dark"] {
  --color-bg: #000000;
  --color-bg-secondary: #0a0a0a;
  --color-border: #FFFFFF;
  --color-text: #FFFFFF;
}

/* Component patterns */
.card {
  border: var(--border-width) solid var(--color-border);
  padding: var(--space-6);
  background: var(--color-bg);
}

.data-value {
  font-family: var(--font-mono);
  font-weight: 700;
}

.status-live::before   { content: "●"; color: var(--color-profit); margin-right: 0.5ch; }
.status-paused::before { content: "⏸"; color: var(--color-warn); margin-right: 0.5ch; }
.status-error::before  { content: "✗"; color: var(--color-loss); margin-right: 0.5ch; }
```

### 3.11 Component Library (Build these in order)

```
Priority 1 — Used everywhere:
  StatusBadge       → <StatusBadge status="live|veto|active|paused|error" />
  DataCard          → KPI card with label, value, delta
  AgentTag          → Colored label per agent name
  ScoreBar          → Horizontal bar for FAS/MS/RAR/OCHS/NS 0–1
  PnlValue          → Colored +/- formatted dollar value

Priority 2 — Page-specific:
  FeedRow           → Single activity log row (timestamp + agent + message)
  PositionRow       → Table row for active positions
  AgentCard         → Full agent status card
  OpsHealthBar      → Ops fund percentage bar with runway estimate
  BillRow           → Ops ledger table row

Priority 3 — Charts (Recharts wrappers):
  EquityCurveChart  → LineChart with drawdown shading
  WinLossBar        → BarChart green/red
  SectorPieChart    → Simple pie for veto reasons
```

---

## 4. TUI — TERMINAL USER INTERFACE

### 4.1 Framework

```
Library:   Python Textual  (pip install textual)
Why:       Native Python, CSS-like styling, async-ready, rich widgets
File:      src/tui/app.py
Run:       python -m src.tui.app
           OR: cryptohedge tui
```

### 4.2 TUI Layout

```
┌─ CryptoHedgeAI ─────────────────── Tick #4821 ─ ● LIVE ─────────────────┐
│                                                                           │
│ ┌─ LIVE FEED ──────────────────────────────┐ ┌─ PORTFOLIO ─────────────┐ │
│ │ 14:32:09  TRADER   ✓ TX confirmed         │ │ Capital   $312.40       │ │
│ │ 14:32:08  TRADER   → Executing Jupiter    │ │ Positions 2 / 6 max     │ │
│ │ 14:32:07  TRADER   Dry-run OK  slip:0.31% │ │ Unreal.   +$0.51 +0.16% │ │
│ │ 14:32:07  RISK     ✓ Approved $6.25 DeFi  │ │ Today     +$1.24 +0.40% │ │
│ │ 14:32:07  RISK     Eval: SOL/USDC 0.847   │ ├─────────────────────────┤ │
│ │ 14:32:04  ORACLE   ✓ Cache 300 coins 3.2s │ │ OPS FUND                │ │
│ │ 14:32:01  OVERSEER Cycle #4821 started    │ │ $8.14  ████████░░  81%  │ │
│ │                                           │ │ ~1.8 mo runway          │ │
│ │                                           │ ├─────────────────────────┤ │
│ │                                           │ │ ACTIVE POSITIONS         │ │
│ │                                           │ │ SOL  +$0.37  +2.1% SOL  │ │
│ │                                           │ │ BNB  +$0.14  +0.5% BSC  │ │
│ └───────────────────────────────────────────┘ └─────────────────────────┘ │
│                                                                           │
│ ┌─ AGENTS ─────────────────────────────────────────────────────────────┐  │
│ │ OVERSEER ●  ORACLE ●  QUANT ●  RISK ●  TRADER ●  ACCOUNT ●  EVAL ●  │  │
│ │ Cycle:7.8s  300c/3.2s 3 sigs  0 vetos  OK         Tax+$0.03  idle   │  │
│ └───────────────────────────────────────────────────────────────────────┘  │
│                                                                           │
│ [q]uit  [e]mergency  [t]rades  [o]ps  [a]nalytics  [c]onfig  [?]help   │
└───────────────────────────────────────────────────────────────────────────┘
```

### 4.3 TUI Views (Tab Navigation)

```
TAB 1: Dashboard  (default, shown above)
TAB 2: Trades     (trade history table, filterable)
TAB 3: Agents     (per-agent detailed stats)
TAB 4: Analytics  (ASCII equity curve + metrics table)
TAB 5: Ops        (ops ledger + bill schedule)
TAB 6: Config     (read-only view of system_config table)
```

### 4.4 TUI Color Scheme (Textual CSS)

```css
/* src/tui/styles/app.tcss */

Screen {
    background: $background;
    color: $foreground;
}

.panel {
    border: solid $primary;
    padding: 0 1;
}

.panel--title {
    color: $primary;
    text-style: bold;
}

/* Agent status dots */
.agent-live   { color: ansi_bright_green; }
.agent-warn   { color: ansi_yellow; }
.agent-error  { color: ansi_bright_red; }
.agent-idle   { color: $text-muted; }

/* Feed rows */
.feed-time     { color: $text-muted; width: 10; }
.feed-overseer { color: $text-muted; }
.feed-oracle   { color: ansi_cyan; }
.feed-quant    { color: ansi_yellow; }
.feed-risk-ok  { color: ansi_bright_green; }
.feed-risk-veto{ color: ansi_bright_red; text-style: bold; }
.feed-trader   { color: $foreground; text-style: bold; }
.feed-account  { color: ansi_bright_yellow; }
.feed-eval     { color: ansi_magenta; }

/* PnL coloring */
.pnl-positive { color: ansi_bright_green; }
.pnl-negative { color: ansi_bright_red; }
.pnl-zero     { color: $text-muted; }

/* Score bars */
.score-bar-fill  { color: ansi_white; }
.score-bar-empty { color: $text-muted; }
```

### 4.5 TUI Widgets to Build

```python
# src/tui/widgets.py

class LiveFeed(ScrollableContainer):
    """
    Scrollable log of agent activity.
    Auto-scrolls to bottom on new event.
    Max rows: 200 (trim older rows)
    Update via: app.post_message(FeedEvent(agent, message))
    """

class PortfolioSnapshot(Static):
    """
    Right panel: capital, positions, ops fund health bar.
    Reactive: updates every WebSocket push.
    """

class AgentStrip(Horizontal):
    """
    Bottom strip: one StatusIndicator per agent.
    Shows: name, status dot, last action summary.
    Click to open AgentDetailModal.
    """

class ScoreBar(Static):
    """
    Renders: [label]  ████████░░  0.847
    Width: configurable, fill char: █, empty: ░
    """

class OpsHealthBar(Static):
    """
    Renders: $8.14  ████████░░  81%  ~1.8mo runway
    Color: green >50%, yellow 20–50%, red <20%
    """

class TradeTable(DataTable):
    """
    Columns: #, Ticker, Entry, Exit, PnL, FAS, Chain, Time
    Sortable by any column (keyboard: s + column letter)
    Filterable (press / to search)
    """
```

### 4.6 TUI Keyboard Shortcuts

```
Global:
  q       → Quit (confirm dialog)
  e       → Emergency Stop (confirm: type "STOP" to confirm)
  1–6     → Switch tab
  ?       → Show help overlay
  Ctrl+R  → Force refresh (manual tick trigger in dry-run mode)

Feed view:
  f       → Toggle follow mode (auto-scroll)
  c       → Clear feed
  /       → Filter feed by agent name

Trades view:
  s       → Sort cycle (ticker → pnl → fas → time)
  /       → Search/filter
  Enter   → Expand trade detail

Config view:
  r       → Refresh from DB
  (read-only — no editing from TUI)
```

### 4.7 TUI Real-Time Update Flow

```python
# TUI connects to same WebSocket as dashboard
# src/tui/ws_client.py

async def connect_and_stream(app: TuiApp):
    async with websockets.connect("ws://localhost:8000/ws/live") as ws:
        async for message in ws:
            event = json.loads(message)
            match event["type"]:
                case "agent_activity":
                    app.post_message(FeedEvent(**event["data"]))
                case "portfolio_update":
                    app.post_message(PortfolioEvent(**event["data"]))
                case "trade_executed":
                    app.post_message(TradeEvent(**event["data"]))
                case "alert":
                    app.post_message(AlertEvent(**event["data"]))
```

### 4.8 ASCII Analytics (Tab 4)

```
ANALYTICS ─── Period: [Monthly ▾] ──────────────────────────────────

EQUITY CURVE (last 30 days)
$350 ┤                                              ╭──
$340 ┤                                         ╭───╯
$330 ┤                              ╭──────────╯
$320 ┤                   ╭──────────╯
$312 ┤────────────────────╯
$300 ┤╭─────────────────╮
$295 ┤│                 ╰──────
     └┴────────────────────────────────────────────────
      Apr 01                  Apr 15              Apr 24

KEY METRICS
──────────────────────────────────────────
  Win Rate        ████████░░  71.4%  (15/21 trades)
  Avg RR          ████████░░  1:2.3
  Sharpe Ratio    ██████░░░░  1.42
  Max Drawdown    ███░░░░░░░  8.2%   (target: ≤15%)
  FAS Accuracy    █████████░  82.4%  (signals profitable)
  Quarterly ROI   ██████░░░░  +6.1%  (target: +10%)
──────────────────────────────────────────
```

---

## 5. CLI — COMMAND LINE INTERFACE

### 5.1 Framework

```
Library:  Rich + Click  (pip install rich click)
Why:      Lightweight, no TUI overhead, scriptable, pipe-friendly
File:     src/cli/main.py
Entrypoint: cryptohedge (registered in pyproject.toml)
```

### 5.2 Command Structure

```
cryptohedge
├── status          → Current bot status (one-screen summary)
├── trades          → Trade history
│   ├── --limit N      → Last N trades (default: 10)
│   ├── --ticker SYM   → Filter by ticker
│   └── --json         → Machine-readable JSON output
├── portfolio       → Current positions + capital
├── ops             → Ops fund + bill schedule
├── eval            → Evaluation history
├── config
│   ├── get KEY        → Read config value
│   └── list           → All config params
├── agents          → Agent status summary
├── stop            → Emergency stop (requires confirmation)
├── resume          → Clear EMERGENCY_STOP
└── tui             → Launch TUI interface
```

### 5.3 Output Style

**`cryptohedge status`**
```
╭─ CryptoHedgeAI ────────────────────────────────────────────────╮
│  Status    ● LIVE            Tick #4,821                       │
│  Uptime    14d 3h 12m        Started 2026-04-10 09:41:00       │
│  Capital   $312.40           Positions 2 / 6 max               │
│  Today     +$1.24 (+0.40%)   This month +$18.40 (+6.27%)       │
│  Ops Fund  $8.14  ████████░░  81%   ~1.8 months runway         │
│  Last Tick 14:32:09 (3s ago) Duration 7.8s                     │
╰────────────────────────────────────────────────────────────────╯
```

**`cryptohedge trades --limit 5`**
```
  RECENT TRADES (last 5)
  ────────────────────────────────────────────────────────────────
  #    TICKER      ENTRY      EXIT       PnL        FAS    TIME
  ────────────────────────────────────────────────────────────────
  4821 SOL/USDC    $142.10    OPEN       +$0.37 ↑   0.847  14:32
  4819 BNB/USDC    $312.00    OPEN       +$0.14 ↑   0.812  13:18
  4815 DOGE/USDC   $0.1420    $0.1398    -$0.18 ↓   0.763  11:02
  4810 JUP/USDC    $0.5210    $0.5480    +$0.31 ↑   0.891  09:44
  4804 SOL/USDC    $139.40    $142.10    +$0.41 ↑   0.824  2d ago
  ────────────────────────────────────────────────────────────────
  Win: 3/5 (60%)   Net PnL: +$1.05
```

**`cryptohedge ops`**
```
  OPS FUND
  ──────────────────────────────────
  Balance   $8.14
  Health    ████████░░  81%
  Reserve   $9.00  (2× $4.50/mo burn)
  Runway    ~1.8 months
  Auto-pay  ● ENABLED

  UPCOMING BILLS
  ──────────────────────────────────────────────────────
  SERVICE       AMOUNT   DUE         STATUS
  ──────────────────────────────────────────────────────
  Hetzner VPS   $4.50    2026-05-01  ⏳ Pending (7d)
  LunarCrush    $29.00   2026-05-15  ● Scheduled
  ──────────────────────────────────────────────────────
  ⚠  LunarCrush: ops_fund insufficient at current rate.
     Need $37.50 — current $8.14. 30 profitable trades req.
```

**`cryptohedge stop`**
```
  ⚠  EMERGENCY STOP

  This will:
  → Set EMERGENCY_STOP = TRUE in system_config
  → Halt all new trade executions
  → Send Telegram alert
  → Active positions will NOT be liquidated (use --liquidate to force)

  Type "STOP" to confirm: STOP

  ✓ Emergency stop activated.
  ✓ Telegram alert sent.
  Resume with: cryptohedge resume
```

**`cryptohedge agents`**
```
  AGENT STATUS
  ────────────────────────────────────────────────────────
  AGENT         STATUS    LAST ACTION         CYCLES  FAILS
  ────────────────────────────────────────────────────────
  Overseer      ● LIVE    Delegated #4821     4,821   2
  Data Oracle   ● LIVE    300c cached 3.2s    4,821   0
  Quant Strat   ● LIVE    3 signals FAS≥0.75  4,821   0
  Risk Guardian ● LIVE    Approved SOL $6.25  4,821   47 vetos
  Exec Trader   ● LIVE    TX confirmed        4,819   0
  Accountant    ● LIVE    Tax +$0.03 ops      4,819   0
  Eval Agent    ● IDLE    Next micro: 3d 14h  12      0
  ────────────────────────────────────────────────────────
```

### 5.4 Error Output Format

```
All errors follow this format — no raw Python tracebacks shown to user:

  ✗ ERROR: [ERROR_CODE]
  ─────────────────────────────────────────
  What happened : DuckDB connection failed
  Reason        : File locked by another process
  Location      : src/state/db.py:get_config()
  ─────────────────────────────────────────
  Fix           : Stop any other running instance of cryptohedge
  Command       : ps aux | grep cryptohedge
                  kill <PID>
```

### 5.5 JSON Mode (for scripts/automation)

Every command supports `--json` flag:
```bash
cryptohedge status --json
cryptohedge trades --json --limit 50
cryptohedge portfolio --json
```

Output:
```json
{
  "timestamp": "2026-04-24T14:32:09",
  "status": "live",
  "tick": 4821,
  "capital": 312.40,
  "positions": 2,
  "today_pnl": 1.24,
  "ops_fund": 8.14
}
```

---

## 6. INTERACTION PATTERNS

### 6.1 Confirmation Pattern (destructive actions)

```
Web:    Modal dialog → "Type STOP to confirm" input → red button
TUI:    Full-screen overlay → text input → Enter to confirm
CLI:    Inline prompt → "Type STOP to confirm: " → waits for input
```

### 6.2 Notification Hierarchy

```
LEVEL 1 — INFO (non-blocking):
  Web: bottom-right toast (auto-dismiss 3s)
  TUI: feed row (green prefix ✓)
  CLI: normal stdout
  Telegram: silent message

LEVEL 2 — WARNING (attention needed):
  Web: amber banner below topbar (dismissible)
  TUI: amber alert widget top of screen (press Enter to dismiss)
  CLI: stderr, yellow color
  Telegram: notification with sound

LEVEL 3 — CRITICAL (action required):
  Web: full-width red banner, never auto-dismiss
  TUI: fullscreen blocking overlay, requires keypress
  CLI: stderr, red bold text, exit code 1
  Telegram: notification with sound + vibrate

LEVEL 4 — EMERGENCY (system halt):
  Web: entire UI turns red overlay "EMERGENCY STOP ACTIVE"
  TUI: fullscreen red, all panels disabled
  CLI: cryptohedge status shows EMERGENCY at top, all commands blocked
  Telegram: alarm notification, repeated every 30min until /resume
```

### 6.3 Empty States

```
No trades yet:
  Web: "No trades recorded. Bot is scanning and waiting for FAS ≥ 0.75 signals."
  TUI: "Scanning... No signals above threshold yet."
  CLI: "No trades in this period."  (exit 0, not error)

No positions:
  "0 active positions. Capital: $312.40 fully available."

Ops fund empty:
  Web: full-width amber alert with exact shortfall amount
  TUI: OpsHealthBar turns red, flash animation
  CLI: warning line in ops output
```

---

*Version: 4.0 | Last Updated: 2026-04-24*
*Interfaces: Web Dashboard (Next.js) + TUI (Python Textual) + CLI (Rich + Click)*
