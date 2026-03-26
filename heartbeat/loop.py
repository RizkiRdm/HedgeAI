import asyncio
import logging
from typing import Callable, Awaitable

class HeartbeatDaemon:
    """
    The async loop that triggers the Overseer agent based on the tick interval.
    """
    def __init__(self, interval: int = 60):
        self.interval = interval
        self.is_running = False
        self._stop_event = asyncio.Event()

    async def start(self, task_callback: Callable[[], Awaitable[None]]):
        logging.info(f"Heartbeat Daemon started with {self.interval}s interval.")
        self.is_running = True
        
        while not self._stop_event.is_set():
            try:
                logging.info("--- New Heartbeat Tick ---")
                await task_callback()
            except Exception as e:
                logging.error(f"Error in heartbeat cycle: {e}")
            
            await asyncio.sleep(self.interval)

    def stop(self):
        logging.info("Stopping Heartbeat Daemon...")
        self._stop_event.set()
        self.is_running = False
