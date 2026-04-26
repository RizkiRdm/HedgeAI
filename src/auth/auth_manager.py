# src/auth/auth_manager.py
"""
Single-user authentication for the dashboard.
Flow:
  1. User enters API key in dashboard modal
  2. SHA-256(key) is compared against AUTH_KEY_HASH in .env
  3. On match: JWT (HS256) is issued with 24h expiry
  4. All subsequent API/WS calls include JWT in Authorization header
  5. FastAPI dependency verifies JWT on every protected endpoint

Why NOT seed phrase auth:
  - Seed phrases in a web form = catastrophic security hole (XSS, extensions, MITM)
  - If seed phrase leaks, entire wallet is gone — no recovery
  - This SHA-256 key approach: if key leaks, you just regenerate it

Setup (run once):
  python -m src.auth.auth_manager generate
  → prints AUTH_KEY_HASH=<hash> and ENCRYPTION_SALT=<salt> for .env
"""
import os
import sys
import hashlib
import secrets
import time
from typing import Optional
import jwt  # PyJWT
from src.utils.logger import get_logger

log = get_logger(__name__)

_ALGORITHM = "HS256"
_TOKEN_EXPIRY_SECONDS = 86400  # 24h


def _get_jwt_secret() -> str:
    s = os.getenv("JWT_SECRET", "")
    if not s:
        raise EnvironmentError("JWT_SECRET not set")
    return s


def _get_key_hash() -> str:
    h = os.getenv("AUTH_KEY_HASH", "")
    if not h:
        raise EnvironmentError("AUTH_KEY_HASH not set — run: python -m src.auth.auth_manager generate")
    return h


def hash_key(plaintext_key: str) -> str:
    """SHA-256 hash of the plaintext API key. Deterministic."""
    return hashlib.sha256(plaintext_key.encode()).hexdigest()


def verify_key(plaintext_key: str) -> bool:
    """Compare submitted key hash against stored hash in .env."""
    expected = _get_key_hash()
    actual = hash_key(plaintext_key)
    # Constant-time comparison to prevent timing attacks
    return secrets.compare_digest(actual, expected)


def issue_token(subject: str = "dashboard") -> str:
    """Issue a signed JWT valid for 24 hours."""
    payload = {
        "sub": subject,
        "iat": int(time.time()),
        "exp": int(time.time()) + _TOKEN_EXPIRY_SECONDS,
    }
    return jwt.encode(payload, _get_jwt_secret(), algorithm=_ALGORITHM)


def verify_token(token: str) -> Optional[dict]:
    """
    Verify JWT. Returns decoded payload or None if invalid/expired.
    Never raises — caller checks None.
    """
    try:
        return jwt.decode(token, _get_jwt_secret(), algorithms=[_ALGORITHM])
    except jwt.ExpiredSignatureError:
        log.warning("auth: JWT expired")
        return None
    except jwt.InvalidTokenError as e:
        log.warning(f"auth: invalid JWT — {e}")
        return None


def generate_setup() -> None:
    """
    Generate AUTH_KEY_HASH and ENCRYPTION_SALT.
    Prints lines to add to .env.
    Called via: python -m src.auth.auth_manager generate
    """
    from src.utils.encryptor import generate_salt

    raw_key = secrets.token_urlsafe(32)
    key_hash = hash_key(raw_key)
    salt = generate_salt()
    jwt_secret = secrets.token_urlsafe(32)

    print("\n" + "="*60)
    print("CryptoHedgeAI — First-Time Setup")
    print("="*60)
    print("\nAdd these to your .env file:\n")
    print(f"JWT_SECRET={jwt_secret}")
    print(f"AUTH_KEY_HASH={key_hash}")
    print(f"ENCRYPTION_SALT={salt}")
    print(f"\nYour dashboard API key (keep this safe, never commit):")
    print(f"\n  {raw_key}\n")
    print("="*60)
    print("This key is shown ONCE. Store it in a password manager.")
    print("="*60 + "\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "generate":
        generate_setup()
    else:
        print("Usage: python -m src.auth.auth_manager generate")
