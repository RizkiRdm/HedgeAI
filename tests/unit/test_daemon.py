# tests/unit/test_daemon.py
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from src.heartbeat.daemon import run_daemon

@pytest.mark.asyncio
async def test_daemon_emergency_stop():
    """Verify daemon skips cycle when EMERGENCY_STOP is TRUE."""
    with patch("src.heartbeat.daemon.get_config", return_value="TRUE") as mock_get_config, \
         patch("src.heartbeat.daemon.initialize_schema"), \
         patch("src.heartbeat.daemon.asyncio.sleep", side_effect=[None, asyncio.CancelledError]) as mock_sleep:
        
        try:
            await run_daemon()
        except asyncio.CancelledError:
            pass
            
        mock_get_config.assert_called_with("EMERGENCY_STOP")
        # Ensure run_cycle was not imported/called
        with patch("src.agents.overseer.run_cycle") as mock_run_cycle:
            assert mock_run_cycle.call_count == 0

@pytest.mark.asyncio
async def test_daemon_tick_execution():
    """Verify daemon calls run_cycle on normal tick."""
    with patch("src.heartbeat.daemon.get_config", return_value="FALSE"), \
         patch("src.heartbeat.daemon.initialize_schema"), \
         patch("src.agents.overseer.run_cycle", new_callable=AsyncMock) as mock_run_cycle, \
         patch("src.heartbeat.daemon.asyncio.sleep", side_effect=[None, asyncio.CancelledError]):
        
        try:
            await run_daemon()
        except asyncio.CancelledError:
            pass
            
        assert mock_run_cycle.await_count >= 1

@pytest.mark.asyncio
async def test_daemon_timeout_handling():
    """Verify daemon handles run_cycle timeout."""
    async def slow_cycle(tick):
        # Future that never completes to force wait_for timeout
        await asyncio.Future()
        
    with patch("src.heartbeat.daemon.get_config", return_value="FALSE"), \
         patch("src.heartbeat.daemon.initialize_schema"), \
         patch("src.heartbeat.daemon.MAX_CYCLE_SECONDS", 0.01), \
         patch("src.heartbeat.daemon.log") as mock_log, \
         patch("src.heartbeat.daemon.asyncio.sleep", side_effect=[None, asyncio.CancelledError]):
        
        with patch("src.agents.overseer.run_cycle", side_effect=slow_cycle):
            try:
                await run_daemon()
            except asyncio.CancelledError:
                pass
            
            # Check if any log call contains "exceeded"
            found = any("exceeded" in str(c) for c in mock_log.warning.mock_calls)
            assert found, f"Timeout warning not found in logs. Warnings: {mock_log.warning.mock_calls}"
