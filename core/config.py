import os
import sys
import json
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError, field_validator

# Load environment variables from .env file
load_dotenv()


class Settings(BaseModel):
    """
    Schema validasi untuk environment variables.
    Menggunakan Pydantic untuk memastikan tipe data benar.
    """

    PRIVATE_KEY: str = Field(..., min_length=1)
    TELEGRAM_BOT_TOKEN: str = Field(..., min_length=1)
    RPC_ENDPOINTS: List[str]
    TOTAL_CAPITAL: float = Field(..., gt=0)
    DRY_RUN: bool = True

    @field_validator("RPC_ENDPOINTS", mode="before")
    @classmethod
    def parse_rpc_endpoints(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [v]  # Fallback jika hanya satu string
        return v


def load_config() -> Settings:
    try:
        # Mengambil data dari os.environ yang sudah di-load dotenv
        config_data = {
            "PRIVATE_KEY": os.getenv("PRIVATE_KEY"),
            "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
            "RPC_ENDPOINTS": os.getenv("RPC_ENDPOINTS"),
            "TOTAL_CAPITAL": os.getenv("TOTAL_CAPITAL"),
            "DRY_RUN": os.getenv("DRY_RUN", "true").lower() in ("true", "1", "t"),
        }

        return Settings(**{k: v for k, v in config_data.items() if v is not None})

    except ValidationError as e:
        # Ambil field yang error
        missing_fields = [str(error["loc"][0]) for error in e.errors()]
        print(
            f"CRITICAL ERROR: Missing or invalid required env: {', '.join(missing_fields)}"
        )
        sys.exit(1)


# Singleton instance untuk digunakan di seluruh aplikasi
settings = load_config()
