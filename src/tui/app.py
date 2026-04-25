import asyncio
import websockets
import json
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Static
from src.tui.widgets import LiveFeed, PortfolioSnapshot, AgentStrip, OpsHealthBar

class CryptoHedgeTUI(App):
    """A Textual app for CryptoHedgeAI monitoring."""
    
    TITLE = "CryptoHedgeAI Terminal"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("e", "emergency_stop", "EMERGENCY STOP"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Horizontal(
                LiveFeed("FEED_INIT..."),
                Vertical(
                    PortfolioSnapshot(),
                    OpsHealthBar(),
                    Static("ACTIVE_POSITIONS\n[italic]None[/]", id="positions"),
                ),
            )
        )
        yield AgentStrip("AGENTS_INIT...")
        yield Footer()

    def on_mount(self) -> None:
        """Start websocket task."""
        self.run_worker(self.listen_to_ws())

    async def listen_to_ws(self):
        """Listen for events from FastAPI."""
        uri = "ws://localhost:8000/ws/live"
        try:
            async with websockets.connect(uri) as websocket:
                feed = self.query_one(LiveFeed)
                feed.add_event("[blue]INFO:[/] Connected to system engine")
                while True:
                    msg = await websocket.recv()
                    data = json.loads(msg)
                    self.handle_event(data)
        except Exception as e:
            self.query_one(LiveFeed).add_event(f"[red]ERROR:[/] WS Connection failed: {e}")

    def handle_event(self, data: dict):
        event_type = data.get("type")
        payload = data.get("data")
        feed = self.query_one(LiveFeed)
        feed.add_event(f"[yellow]EVENT:[/] {event_type} - {payload}")

    def action_emergency_stop(self):
        # Implementation of emergency stop confirmation
        pass

if __name__ == "__main__":
    app = CryptoHedgeTUI()
    app.run()
