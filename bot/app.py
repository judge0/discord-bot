"""Discord application client and slash commands."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

import discord
import judge0
from discord import app_commands
from judge0 import Status, Submission
from judge0.errors import PreviewClientLimitError

from bot.config import Settings
from bot.judge import (
    LANGUAGES,
    Judge0Service,
    SubmissionTimeoutError,
    display_language,
    language_choices,
    resolve_language,
    strip_code_fence,
)

LOGGER = logging.getLogger(__name__)
BOT_NAME = "Judge0 Discord Bot"
IDE_URL = "https://ide.judge0.com/"
MAX_EMBED_OUTPUT = 3_800


def _channel_names(channel: object | None) -> set[str]:
    names = set()
    channel_name = getattr(channel, "name", None)
    if isinstance(channel_name, str):
        names.add(channel_name.casefold())

    parent_name = getattr(getattr(channel, "parent", None), "name", None)
    if isinstance(parent_name, str):
        names.add(parent_name.casefold())
    return names


def interaction_is_allowed(
    settings: Settings,
    *,
    guild_id: int | None,
    channel: object | None,
) -> bool:
    """Check optional test-guild and test-channel restrictions."""
    if settings.guild_id is not None and guild_id != settings.guild_id:
        return False
    if settings.channel_name is not None:
        return settings.channel_name.casefold() in _channel_names(channel)
    return True


def _escape_code_block(value: str) -> str:
    return value.replace("\x00", "\\0").replace("```", "``\u200b`")


def _truncate(value: str, limit: int = MAX_EMBED_OUTPUT) -> str:
    if len(value) <= limit:
        return value
    suffix = "\n\n[Output truncated by the Discord bot.]"
    return value[: limit - len(suffix)] + suffix


def submission_output(submission: Submission) -> str:
    """Combine Judge0 output streams into one bounded Discord-safe string."""
    sections = [
        ("stdout", submission.stdout),
        ("stderr", submission.stderr),
        ("compiler output", submission.compile_output),
        ("message", submission.message),
    ]
    populated = [(name, str(value)) for name, value in sections if value]

    if not populated:
        output = "No output."
    elif len(populated) == 1 and populated[0][0] == "stdout":
        output = populated[0][1]
    else:
        output = "\n\n".join(f"{name}:\n{value}" for name, value in populated)
    return _truncate(_escape_code_block(output))


def submission_embed(
    submission: Submission,
    *,
    language: str,
    author: discord.User | discord.Member,
) -> discord.Embed:
    """Build a result embed from an SDK Submission."""
    status = str(submission.status) if submission.status is not None else "Unknown"
    color = (
        discord.Color.green()
        if submission.status == Status.ACCEPTED
        else discord.Color.red()
    )
    embed = discord.Embed(
        title=f"{display_language(language)}: {status}",
        description=f"```\n{submission_output(submission)}\n```",
        color=color,
        timestamp=discord.utils.utcnow(),
    )
    if submission.token is not None:
        embed.url = f"{IDE_URL}?{submission.token}"

    embed.set_author(
        name=f"{author.display_name}'s execution",
        icon_url=author.display_avatar.url,
    )
    if submission.time is not None:
        embed.add_field(name="Time", value=f"{submission.time:g} s")
    if submission.memory is not None:
        embed.add_field(
            name="Memory",
            value=f"{submission.memory / 1024:.2f} MiB",
        )
    if submission.exit_code is not None:
        embed.add_field(name="Exit code", value=str(submission.exit_code))
    embed.set_footer(text="Executed securely by Judge0")
    return embed


def _format_uptime(started_at: datetime) -> str:
    seconds = int((datetime.now(timezone.utc) - started_at).total_seconds())
    days, seconds = divmod(seconds, 86_400)
    hours, seconds = divmod(seconds, 3_600)
    minutes, seconds = divmod(seconds, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"


class RestrictedCommandTree(app_commands.CommandTree):
    """Command tree that can be limited to one test guild and channel."""

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        settings = self.client.settings
        if interaction_is_allowed(
            settings,
            guild_id=interaction.guild_id,
            channel=interaction.channel,
        ):
            return True

        if interaction.type is discord.InteractionType.autocomplete:
            await interaction.response.autocomplete([])
            return False

        if settings.channel_name:
            message = f"This bot instance is limited to #{settings.channel_name}."
        else:
            message = "This bot instance is limited to its configured test server."
        await interaction.response.send_message(message, ephemeral=True)
        return False


class Judge0DiscordBot(discord.Client):
    """Discord client that owns Judge0 slash commands."""

    settings: Settings
    tree: RestrictedCommandTree

    def __init__(
        self,
        settings: Settings,
        service: Judge0Service | None = None,
    ) -> None:
        intents = discord.Intents.none()
        intents.guilds = True
        super().__init__(
            intents=intents,
            allowed_mentions=discord.AllowedMentions.none(),
            activity=discord.Game(name=f"{BOT_NAME}: /run"),
        )
        self.settings = settings
        self.service = service or Judge0Service(
            timeout_seconds=settings.submission_timeout_seconds,
            max_concurrent=settings.max_concurrent_submissions,
        )
        self.started_at = datetime.now(timezone.utc)
        self.tree = RestrictedCommandTree(self)
        _register_commands(self)

    async def setup_hook(self) -> None:
        if self.settings.guild_id is None:
            synced = await self.tree.sync()
            scope = "globally"
        else:
            guild = discord.Object(id=self.settings.guild_id)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            scope = f"to guild {self.settings.guild_id}"
        LOGGER.info("Synced %d application commands %s", len(synced), scope)

    async def on_ready(self) -> None:
        if self.user is None:
            return
        LOGGER.info("Logged in as %s (%d)", self.user, self.user.id)

        if self.settings.guild_id and self.settings.channel_name:
            guild = self.get_guild(self.settings.guild_id)
            channel_found = guild is not None and any(
                channel.name.casefold() == self.settings.channel_name.casefold()
                for channel in guild.channels
            )
            if channel_found:
                LOGGER.info(
                    "Test scope is guild %d, channel #%s",
                    self.settings.guild_id,
                    self.settings.channel_name,
                )
            else:
                LOGGER.warning(
                    "Configured channel #%s was not found in guild %d",
                    self.settings.channel_name,
                    self.settings.guild_id,
                )


async def _send_ephemeral(interaction: discord.Interaction, message: str) -> None:
    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)


def _register_commands(bot: Judge0DiscordBot) -> None:
    @bot.tree.command(name="run", description="Run source code securely with Judge0")
    @app_commands.describe(
        language="Programming language, such as python, javascript, or cpp",
        code="Source code, optionally wrapped in a Markdown code block",
        stdin="Optional standard input passed to the program",
    )
    @app_commands.checks.cooldown(
        1,
        5.0,
        key=lambda interaction: (interaction.guild_id, interaction.user.id),
    )
    async def run_code(
        interaction: discord.Interaction,
        language: str,
        code: str,
        stdin: str | None = None,
    ) -> None:
        try:
            canonical_language, language_alias = resolve_language(language)
        except ValueError:
            await interaction.response.send_message(
                "Unsupported language. Use `/languages` or select an "
                "autocomplete option.",
                ephemeral=True,
            )
            return

        source_code = strip_code_fence(code)
        if not source_code.strip():
            await interaction.response.send_message(
                "Source code cannot be empty.",
                ephemeral=True,
            )
            return
        if len(source_code) > 6_000 or (stdin is not None and len(stdin) > 2_000):
            await interaction.response.send_message(
                "Code is limited to 6,000 characters and stdin to 2,000 characters.",
                ephemeral=True,
            )
            return

        await interaction.response.defer(thinking=True)
        try:
            submission = await bot.service.execute(
                source_code=source_code,
                language=language_alias,
                stdin=stdin or None,
            )
        except PreviewClientLimitError:
            await interaction.followup.send(
                "The credential-free Judge0 preview request limit was reached. "
                "Please try again later.",
                ephemeral=True,
            )
            return
        except SubmissionTimeoutError:
            await interaction.followup.send(
                "Judge0 did not finish this submission before the bot timeout.",
                ephemeral=True,
            )
            return
        except Exception:
            LOGGER.exception(
                "Judge0 execution failed for language %s", canonical_language
            )
            await interaction.followup.send(
                "Judge0 could not execute this submission. "
                "Check the bot logs for details.",
                ephemeral=True,
            )
            return

        await interaction.followup.send(
            embed=submission_embed(
                submission,
                language=canonical_language,
                author=interaction.user,
            )
        )

    @run_code.autocomplete("language")
    async def language_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        del interaction
        return [
            app_commands.Choice(name=display_name, value=value)
            for display_name, value in language_choices(current)
        ]

    @bot.tree.command(
        name="languages",
        description="List language aliases supported by the Judge0 Python SDK",
    )
    async def languages(interaction: discord.Interaction) -> None:
        names = sorted(LANGUAGES, key=lambda name: display_language(name).casefold())
        embed = discord.Embed(
            title="Supported languages",
            description=", ".join(f"`{name}`" for name in names),
            color=discord.Color.blurple(),
        )
        embed.set_footer(
            text=(
                "Aliases resolve to the latest version available from your "
                "Judge0 provider"
            )
        )
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(
        name="help",
        description=f"Show how to use {BOT_NAME}",
    )
    async def help_command(interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title=BOT_NAME,
            description="Run code directly from Discord with the Judge0 Python SDK.",
            color=discord.Color.blurple(),
        )
        embed.add_field(
            name="Run code",
            value=(
                "Use `/run`, choose a language, and paste code. "
                "Markdown code blocks are accepted. You can also provide stdin."
            ),
            inline=False,
        )
        embed.add_field(
            name="Discover languages",
            value="Use `/languages`, or start typing in `/run language:`.",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="`/run language:python code:print(6 * 7)`",
            inline=False,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(
        name="info",
        description=f"Show {BOT_NAME} and SDK status",
    )
    async def info(interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title=f"{BOT_NAME} status",
            url="https://github.com/judge0/discord-bot",
            color=discord.Color.blurple(),
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(name="Uptime", value=_format_uptime(bot.started_at))
        embed.add_field(name="Discord", value=f"discord.py {discord.__version__}")
        embed.add_field(name="Judge0", value=f"Python SDK {judge0.__version__}")
        embed.add_field(name="Latency", value=f"{bot.latency * 1_000:.0f} ms")
        embed.add_field(name="Servers", value=str(len(bot.guilds)))
        await interaction.response.send_message(embed=embed)

    @bot.tree.error
    async def on_app_command_error(
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            await _send_ephemeral(
                interaction,
                f"Please wait {error.retry_after:.1f} seconds before "
                "running more code.",
            )
            return

        LOGGER.error("Unhandled application command error", exc_info=error)
        await _send_ephemeral(
            interaction,
            "The command failed unexpectedly. Check the bot logs for details.",
        )


def create_bot(
    settings: Settings,
    service: Judge0Service | None = None,
) -> Judge0DiscordBot:
    """Create a configured Discord client."""
    return Judge0DiscordBot(settings, service)
