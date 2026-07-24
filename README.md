# Judge0 Discord Bot

Judge0 Discord Bot runs source code from Discord using the official
[Judge0 Python SDK](https://github.com/judge0/judge0-python) and native Discord
slash commands.

## Commands

- `/run language code [stdin]` executes source code. The language option has
  autocomplete, and code can be plain text or a Markdown code block.
- `/languages` lists Judge0 Python SDK language aliases.
- `/help` shows a short usage guide.
- `/info` shows the running Discord and Judge0 Python SDK versions.

Example:

```text
/run language:python code:print(6 * 7)
```

The bot uses slash commands only. It does not need Discord's privileged
Message Content or Server Members intents.

## Requirements

- Python 3.10 or newer, or Docker
- A Discord application and bot token

Judge0 Discord Bot intentionally uses the SDK's credential-free preview
client. No Judge0 API key, custom endpoint, or Judge0 authentication setting
is needed. The public preview service is rate-limited.

## Judge0 Server Test

The existing `.env` in this workspace already contains `BOT_TOKEN`. Add these
settings to register commands instantly in the Judge0 server and reject
commands anywhere except `#test-discord-bot`:

```dotenv
DISCORD_GUILD_ID=620615182116323328
DISCORD_CHANNEL_NAME=test-discord-bot
```

Then start the bot:

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/python -m bot
```

In `#test-discord-bot`, run `/info`, followed by:

```text
/run language:python code:print("Judge0 Discord Bot is working")
```

The Discord application represented by `BOT_TOKEN` must already be installed
in the Judge0 server. Stop any old process using the same token before starting
this implementation, otherwise both processes can respond to Discord events.

For a private test channel, open **Edit Channel > Permissions**, add the bot
member, and allow View Channel, Send Messages, and Embed Links. Users who test
the bot also need Use Application Commands.

## Your Discord Server

1. Open the [Discord Developer Portal](https://discord.com/developers/applications)
   and create or select an application.
2. On its **Bot** page, create a bot and put its token in `.env` as
   `BOT_TOKEN=...`. Do not commit this file.
3. Install the app using this URL, replacing `YOUR_APPLICATION_ID` with the
   application ID:

   ```text
   https://discord.com/oauth2/authorize?client_id=YOUR_APPLICATION_ID&scope=bot%20applications.commands&permissions=19456
   ```

   The permission value grants View Channels, Send Messages, and Embed Links.
4. For instant command registration during setup, set your server ID as
   `DISCORD_GUILD_ID`. You can optionally restrict the bot to one channel with
   `DISCORD_CHANNEL_NAME`.
5. Start the bot with `.venv/bin/python -m bot` or Docker Compose.

Remove `DISCORD_GUILD_ID` and `DISCORD_CHANNEL_NAME` for a public deployment.
On the next start, commands are registered globally. Discord guild command
updates are immediate; global command updates can take longer to appear.

Optional bot settings:

```dotenv
MAX_CONCURRENT_SUBMISSIONS=4
SUBMISSION_TIMEOUT_SECONDS=30
```

## Docker

The Compose service reads `.env` automatically:

```bash
docker compose up --build -d
docker compose logs -f bot
```

Stop it with `docker compose down`.

## Development

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/ruff check .
.venv/bin/pytest
```

The Judge0 Python SDK is synchronous internally. Judge0 Discord Bot executes it on
bounded worker threads so Discord's event loop remains responsive, and applies
a submission timeout before responding to the interaction.

## License

[MIT](LICENSE)
