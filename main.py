from core.config import settings
from loguru import logger


def main():
    logger.info("HedgeAI System Initializing...")
    logger.info(
        f"Environment Loaded. Capital: ${settings.TOTAL_CAPITAL} | Dry Run: {settings.DRY_RUN}"
    )

    # Placeholder untuk Task 1.4 & 1.5
    print("HedgeAI Foundation Ready.")


if __name__ == "__main__":
    main()
