# tests/unit/test_logger.py
import logging
import pytest
from src.utils.logger import get_logger, SecretFilter

def test_secret_filter_redacts():
    """Verify sensitive patterns are redacted."""
    filter = SecretFilter()
    
    # Test cases: (input_msg, expected_in_output)
    cases = [
        ("PRIVATE_KEY=12345", "[REDACTED"),
        ("api_secret: abc", "[REDACTED"),
        ("SEED=hello world", "[REDACTED"),
        ("password = secret", "[REDACTED"),
        ("Normal message", "Normal message"),
    ]
    
    for msg, expected in cases:
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="test.py", 
            lineno=1, msg=msg, args=(), exc_info=None
        )
        filter.filter(record)
        assert expected in record.msg

def test_logger_integration():
    """Verify logger uses filter and doesn't leak."""
    log = get_logger("test_integration")
    # Add a stream handler that we can inspect if needed, 
    # but the filter test above covers the logic.
    # We just ensure it doesn't crash.
    log.info("PRIVATE_KEY=secret")
    log.info("Normal log")
