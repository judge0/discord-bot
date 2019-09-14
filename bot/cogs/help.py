import discord
from discord.ext import commands
from discord import Embed, Color

from bot.paginator import Paginator
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        pass

    async def help(self, ctx):
        await ctx.send("^:- LOL- :^")
    
