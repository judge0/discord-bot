"""Environment-based bot configuration."""

import os
from dataclasses import dataclass, field


def _optional_positive_int(name: str) -> int | None:
    value = os.getenv(name, "").strip()
    if not value:
        return None

    try:
        parsed = int(value)
    except ValueError as error:
        raise ValueError(f"{name} must be an integer") from error

    if parsed <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return parsed


def _positive_int(name: str, default: int) -> int:
    value = os.getenv(name, str(default)).strip()
    try:
        parsed = int(value)
    except ValueError as error:
        raise ValueError(f"{name} must be an integer") from error

    if parsed <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return parsed


def _positive_float(name: str, default: float) -> float:
    value = os.getenv(name, str(default)).strip()
    try:
        parsed = float(value)
    except ValueError as error:
        raise ValueError(f"{name} must be a number") from error

    if parsed <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return parsed


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    bot_token: str = field(repr=False)
    guild_id: int | None = None
    channel_name: str | None = None
    max_concurrent_submissions: int = 4
    submission_timeout_seconds: float = 30.0

    @classmethod
    def from_env(cls) -> "Settings":
        """Build settings from the process environment."""
        bot_token = os.getenv("BOT_TOKEN", "").strip()
        if not bot_token:
            raise ValueError("BOT_TOKEN is required")

        channel_name = os.getenv("DISCORD_CHANNEL_NAME", "").strip() or None
        return cls(
            bot_token=bot_token,
            guild_id=_optional_positive_int("DISCORD_GUILD_ID"),
            channel_name=channel_name,
            max_concurrent_submissions=_positive_int("MAX_CONCURRENT_SUBMISSIONS", 4),
            submission_timeout_seconds=_positive_float(
                "SUBMISSION_TIMEOUT_SECONDS", 30.0
            ),
        )
