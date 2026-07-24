from types import SimpleNamespace

import pytest
from judge0 import Status, Submission

from bot.app import (
    MAX_EMBED_OUTPUT,
    create_bot,
    interaction_is_allowed,
    submission_embed,
    submission_output,
)
from bot.config import Settings


def test_interaction_scope_allows_configured_channel_and_its_threads() -> None:
    settings = Settings(
        bot_token="token",
        guild_id=123,
        channel_name="test-discord-bot",
    )
    channel = SimpleNamespace(name="test-discord-bot", parent=None)
    thread = SimpleNamespace(name="a-thread", parent=channel)

    assert interaction_is_allowed(settings, guild_id=123, channel=channel)
    assert interaction_is_allowed(settings, guild_id=123, channel=thread)
    assert not interaction_is_allowed(settings, guild_id=456, channel=channel)
    assert not interaction_is_allowed(
        settings,
        guild_id=123,
        channel=SimpleNamespace(name="general", parent=None),
    )


def test_submission_output_combines_and_escapes_streams() -> None:
    submission = Submission()
    submission.stdout = "hello ``` world"
    submission.stderr = "warning"

    output = submission_output(submission)

    assert output.startswith("stdout:\nhello")
    assert "stderr:\nwarning" in output
    assert "```" not in output


def test_submission_output_is_bounded() -> None:
    submission = Submission()
    submission.stdout = "x" * (MAX_EMBED_OUTPUT + 100)

    output = submission_output(submission)

    assert len(output) == MAX_EMBED_OUTPUT
    assert output.endswith("[Output truncated by the Discord bot.]")


def test_submission_embed_contains_execution_metadata() -> None:
    submission = Submission()
    submission.status = Status.ACCEPTED
    submission.stdout = "42\n"
    submission.time = 0.01
    submission.memory = 2_048
    submission.exit_code = 0
    author = SimpleNamespace(
        display_name="Ada",
        display_avatar=SimpleNamespace(url="https://example.com/avatar.png"),
    )

    embed = submission_embed(submission, language="python", author=author)

    assert embed.title == "Python: Accepted"
    assert embed.description == "```\n42\n\n```"
    assert embed.author.name == "Ada's execution"
    assert [field.name for field in embed.fields] == [
        "Time",
        "Memory",
        "Exit code",
    ]


@pytest.mark.asyncio
async def test_bot_registers_native_application_commands() -> None:
    bot = create_bot(Settings(bot_token="token"))
    try:
        assert {command.name for command in bot.tree.get_commands()} == {
            "help",
            "info",
            "languages",
            "run",
        }
        assert bot.intents.guilds
        assert not bot.intents.message_content
        assert not bot.intents.members
    finally:
        await bot.close()
