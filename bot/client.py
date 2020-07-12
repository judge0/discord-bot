from discord.ext import commands
from bot.db import BotDataBase

extensions = (
    "bot.cogs.admin",
    "bot.cogs.execution",
    "bot.cogs.help",
    "bot.cogs.information",
    "bot.cogs.tasks"
)

class Judge0Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for ext in extensions:
            try:
                self.load_extension(ext)
            except Exception as e:
                print(f'Failed to load extension {ext}. {e}')
 
    async def load_db(self):
        self.db = await BotDataBase()

    async def init_db(self):
        await BotDataBase.initialize()