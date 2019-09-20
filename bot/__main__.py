import sys

from discord.ext import commands

from bot.constants import PREFIX

bot = commands.Bot(command_prefix=PREFIX)

bot.load_extension('bot.cogs.admin')
bot.load_extension('bot.cogs.execution')
bot.load_extension('bot.cogs.help')
bot.load_extension('bot.cogs.information')

bot.run(sys.argv[1])