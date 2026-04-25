from textual.widgets import Static, DataTable
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal

class LiveFeed(Static):
    """Real-time event feed."""
    DEFAULT_CSS = """
    LiveFeed {
        background: $boost;
        border: solid $accent;
        padding: 1;
        height: 100%;
        overflow-y: scroll;
    }
    """
    def add_event(self, msg: str):
        self.update(self.renderable + "\n" + msg)

class PortfolioSnapshot(Static):
    """Current portfolio metrics."""
    DEFAULT_CSS = """
    PortfolioSnapshot {
        background: $surface;
        border: double $primary;
        height: auto;
        padding: 1;
    }
    """
    def update_values(self, total: float, available: float):
        self.update(f"PORTFOLIO_VALUE: [bold green]${total:,.2f}[/]\nAVAILABLE_CAPITAL: ${available:,.2f}")

class AgentStrip(Static):
    """Bottom strip showing agent status."""
    DEFAULT_CSS = """
    AgentStrip {
        dock: bottom;
        height: 1;
        background: $primary;
        color: $on-primary;
        content-align: center middle;
    }
    """
    def set_status(self, agents: dict):
        status_line = " | ".join([f"{name.upper()}: [bold]OK[/]" for name in agents.keys()])
        self.update(status_line)

class OpsHealthBar(Static):
    """Visual representation of fund health."""
    DEFAULT_CSS = """
    OpsHealthBar {
        height: 3;
        border: sunken $warning;
        padding: 0 1;
    }
    """
    def set_health(self, pct: float):
        bar = "█" * int(pct * 20) + "░" * (20 - int(pct * 20))
        self.update(f"OPS_HEALTH: [{bar}] {pct:.0%}")
