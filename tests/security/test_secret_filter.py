import logging
from src.utils.logger import SecretFilter

def test_filter_blocks_all_sensitive_keys():
    """Exhaustive check of secret filter."""
    f = SecretFilter()
    
    keys = ["PRIVATE_KEY", "API_SECRET", "API_KEY", "SEED", "password", "passphrase"]
    
    for key in keys:
        msg = f"Logging my {key}=super-secret-123"
        record = logging.LogRecord("name", logging.INFO, "path", 1, msg, (), None)
        f.filter(record)
        assert "[REDACTED" in record.msg
        assert "super-secret-123" not in record.msg

def test_filter_blocks_case_insensitive():
    """Verify filter ignores case."""
    f = SecretFilter()
    msg = "api_key: secret"
    record = logging.LogRecord("name", logging.INFO, "path", 1, msg, (), None)
    f.filter(record)
    assert "[REDACTED" in record.msg
