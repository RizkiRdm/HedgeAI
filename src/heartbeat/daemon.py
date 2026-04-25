# src/heartbeat/daemon.py
import asyncio
import signal
import logging
from datetime import datetime, UTC
from src.state.db import initialize_schema, get_config
from src.utils.logger import get_logger

log = get_logger(__name__)

TICK_INTERVAL_SECONDS = 15
MAX_CYCLE_SECONDS = 14

async def run_daemon() -> None:
    """
    Main daemon loop. Fires every 15 seconds.
    Checks EMERGENCY_STOP before each cycle.
    Calls overseer.run_cycle() for each tick.
    """
    initialize_schema()
    log.info("Heartbeat daemon started")
    tick_count = 0

    while True:
        tick_start = datetime.now(UTC)
        tick_count += 1

        emergency = get_config("EMERGENCY_STOP")
        if emergency == "TRUE":
            log.warning(f"Tick #{tick_count}: EMERGENCY_STOP active — skipping cycle")
            await asyncio.sleep(TICK_INTERVAL_SECONDS)
            continue

        log.info(f"Tick #{tick_count}: cycle start")

        try:
            # Import inside loop to avoid circular imports
            from src.agents.overseer import run_cycle
            await asyncio.wait_for(run_cycle(tick_count), timeout=MAX_CYCLE_SECONDS)
        except asyncio.TimeoutError:
            log.warning(f"Tick #{tick_count}: cycle exceeded {MAX_CYCLE_SECONDS}s — WARNING")
        except Exception as e:
            log.error(f"Tick #{tick_count}: unhandled error in cycle: {e}")

        elapsed = (datetime.now(UTC) - tick_start).total_seconds()
        sleep_time = max(0, TICK_INTERVAL_SECONDS - elapsed)
        await asyncio.sleep(sleep_time)

def handle_shutdown(sig, frame):
    log.info("Shutdown signal received — stopping daemon")
    raise SystemExit(0)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)
    try:
        asyncio.run(run_daemon())
    except (KeyboardInterrupt, SystemExit):
        pass
