# src/utils/logger.py
import logging
import re
from typing import Any

SENSITIVE_PATTERNS = [
    r"PRIVATE_KEY\s*[:=]\s*\S+",
    r"API_SECRET\s*[:=]\s*\S+",
    r"API_KEY\s*[:=]\s*\S+",
    r"SEED\s*[:=]\s*\S+",
    r"password\s*[:=]\s*\S+",
    r"passphrase\s*[:=]\s*\S+",
]

class SecretFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        msg = str(record.getMessage())
        for pattern in SENSITIVE_PATTERNS:
            if re.search(pattern, msg, re.IGNORECASE):
                record.msg = "[REDACTED — sensitive data blocked by SecretFilter]"
                record.args = ()
                return True
        return True

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    logger.addFilter(SecretFilter())
    logger.setLevel(logging.INFO)
    return logger
