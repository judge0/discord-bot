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

# run the bot with the token
token = sys.argv[1] if sys.argv[1] else os.environ["BOT_TOKEN"]
bot.run(token)
