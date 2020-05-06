"""
Main program for running the bot:

python -m bot token
"""

import os, sys

from discord.ext import commands

from bot.constants import PREFIX

# create a Client object
bot = commands.Bot(command_prefix=PREFIX)

# load the bot extensions (the bot features)
bot.load_extension("bot.cogs.admin")
bot.load_extension("bot.cogs.execution")
bot.load_extension("bot.cogs.help")
bot.load_extension("bot.cogs.information")
bot.load_extension("bot.cogs.tasks")


# run the bot with the token or enviroment variable
token = sys.argv[1] if len(sys.argv) >= 2 else os.environ["BOT_TOKEN"]
bot.run(token)
