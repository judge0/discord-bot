"""Run the Judge0 Discord bot with ``python -m bot``."""

import logging

from dotenv import load_dotenv

from bot.app import create_bot
from bot.config import Settings


def main() -> None:
    """Load configuration and connect the bot to Discord."""
    load_dotenv()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("judge0").setLevel(logging.ERROR)
    settings = Settings.from_env()
    bot = create_bot(settings)
    bot.run(settings.bot_token, log_handler=None)


if __name__ == "__main__":
    main()
