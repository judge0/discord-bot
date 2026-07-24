import pytest

from bot.config import Settings

CONFIG_VARIABLES = (
    "BOT_TOKEN",
    "DISCORD_GUILD_ID",
    "DISCORD_CHANNEL_NAME",
    "MAX_CONCURRENT_SUBMISSIONS",
    "SUBMISSION_TIMEOUT_SECONDS",
)


def clear_config(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in CONFIG_VARIABLES:
        monkeypatch.delenv(name, raising=False)


def test_settings_load_defaults_without_exposing_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clear_config(monkeypatch)
    monkeypatch.setenv("BOT_TOKEN", "secret-token")

    settings = Settings.from_env()

    assert settings.guild_id is None
    assert settings.channel_name is None
    assert settings.max_concurrent_submissions == 4
    assert settings.submission_timeout_seconds == 30
    assert "secret-token" not in repr(settings)


def test_settings_load_test_scope(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_config(monkeypatch)
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("DISCORD_GUILD_ID", "620615182116323328")
    monkeypatch.setenv("DISCORD_CHANNEL_NAME", " test-discord-bot ")
    monkeypatch.setenv("MAX_CONCURRENT_SUBMISSIONS", "2")
    monkeypatch.setenv("SUBMISSION_TIMEOUT_SECONDS", "12.5")

    settings = Settings.from_env()

    assert settings.guild_id == 620615182116323328
    assert settings.channel_name == "test-discord-bot"
    assert settings.max_concurrent_submissions == 2
    assert settings.submission_timeout_seconds == 12.5


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("DISCORD_GUILD_ID", "nope"),
        ("MAX_CONCURRENT_SUBMISSIONS", "0"),
        ("SUBMISSION_TIMEOUT_SECONDS", "-1"),
    ],
)
def test_settings_reject_invalid_numbers(
    monkeypatch: pytest.MonkeyPatch,
    name: str,
    value: str,
) -> None:
    clear_config(monkeypatch)
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv(name, value)

    with pytest.raises(ValueError, match=name):
        Settings.from_env()


def test_settings_require_token(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_config(monkeypatch)

    with pytest.raises(ValueError, match="BOT_TOKEN"):
        Settings.from_env()
