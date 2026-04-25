import click
import json
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from src.state import db
from src.execution_bridge import grpc_client

console = Console()

@click.group()
def cli():
    """CryptoHedgeAI Control CLI."""
    pass

@cli.command()
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def status(as_json):
    """View bot status and capital."""
    stop = db.get_config("EMERGENCY_STOP") or "FALSE"
    balance = db.get_ops_fund_balance()
    
    data = {
        "emergency_stop": stop,
        "ops_balance": balance
    }
    
    if as_json:
        console.print_json(data=data)
        return

    table = Table(title="Bot Status")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("EMERGENCY_STOP", stop)
    table.add_row("Ops Fund Balance", f"${balance:,.2f}")
    console.print(table)

@cli.command()
@click.option("--limit", default=10, help="Number of trades to show")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def trades(limit, as_json):
    """View recent trade history."""
    with db.get_connection() as conn:
        res = conn.execute(
            "SELECT ticker, entry_p, exit_p, fas_score, pnl, created_at FROM trade_history ORDER BY created_at DESC LIMIT ?",
            [limit]
        ).fetchall()
        cols = [d[0] for d in conn.description]
        data = [dict(zip(cols, row)) for row in res]

    if as_json:
        console.print_json(data=data)
        return

    table = Table(title=f"Last {limit} Trades")
    for col in cols:
        table.add_column(col)
    
    for row in res:
        table.add_row(*[str(val) for val in row])
    console.print(table)

@cli.command()
def stop():
    """Trigger emergency stop."""
    if click.confirm("Are you sure you want to stop the bot?"):
        db.set_config("EMERGENCY_STOP", "TRUE")
        console.print("[bold red]EMERGENCY_STOP set to TRUE[/]")

@cli.command()
def resume():
    """Resume bot operations."""
    db.set_config("EMERGENCY_STOP", "FALSE")
    console.print("[bold green]EMERGENCY_STOP set to FALSE[/]")

if __name__ == "__main__":
    cli()
