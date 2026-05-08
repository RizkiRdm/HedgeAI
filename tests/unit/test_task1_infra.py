# tests/unit/test_task1_infra.py
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from src.tools.market_fetcher import MarketFetcher
from src.utils.telegram_notifier import _send_message, send_trade_executed

@pytest.mark.asyncio
async def test_market_fetcher_retry_logic():
    fetcher = MarketFetcher()
    mock_func = AsyncMock()
    # Fail twice, succeed on third
    mock_func.side_effect = [Exception("Fail 1"), Exception("Fail 2"), "Success"]
    
    with patch("asyncio.sleep", return_value=None):  # Don't actually wait
        result = await fetcher._retry_request(mock_func)
    
    assert result == "Success"
    assert mock_func.call_count == 3
    await fetcher.close()

@pytest.mark.asyncio
async def test_market_fetcher_failure():
    fetcher = MarketFetcher()
    mock_func = AsyncMock()
    mock_func.side_effect = Exception("Permanent Fail")
    
    with patch("asyncio.sleep", return_value=None):
        result = await fetcher._retry_request(mock_func)
    
    assert result is None
    assert mock_func.call_count == 3
    await fetcher.close()

@pytest.mark.asyncio
async def test_dex_screener_fetch_format():
    fetcher = MarketFetcher()
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "pairs": [{
            "liquidity": {"usd": 1000},
            "volume": {"h24": 500},
            "priceChange": {"h24": 5.0},
            "fdv": 50000,
            "pairCreatedAt": 123456789
        }]
    }
    mock_response.raise_for_status = MagicMock()
    
    with patch.object(fetcher.client, "get", AsyncMock(return_value=mock_response)):
        metrics = await fetcher.fetch_onchain_metrics("solana", "some_pair")
        
    assert metrics["liquidity"] == 1000
    assert metrics["market_cap"] == 50000
    await fetcher.close()

@pytest.mark.asyncio
async def test_telegram_notifier_async():
    # Test that it doesn't crash and uses the provided token/chat_id
    with patch("src.utils.telegram_notifier.TOKEN", "test_token"), \
         patch("src.utils.telegram_notifier.CHAT_ID", "test_chat"), \
         patch("src.utils.telegram_notifier.Bot") as MockBot:
        
        mock_bot_inst = MockBot.return_value
        mock_bot_inst.send_message = AsyncMock(return_value=True)
        
        success = await send_trade_executed("SOL", 100.0, 0.85, "0x123")
        
        # Note: send_trade_executed doesn't return anything now, 
        # but we check if send_message was called
        assert mock_bot_inst.send_message.called
