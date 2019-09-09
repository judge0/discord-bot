import discord
from discord import Embed
from discord.ext import commands

from bot.constants import PREFIX

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.activity_str = f"with {PREFIX}help"
        self.status_str = "online"

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged on as {self.bot.user}")
        await self.bot.change_presence(
            activity=discord.Game(self.activity_str),
            status=eval(f"discord.Status.{self.status_str}"),
        )

    @commands.is_owner()
    @commands.command(aliases=["q"])
    async def quit(self, ctx):
        """Shuts down the bot."""
        await ctx.send("Terminates.")
        await self.bot.logout()

    @commands.is_owner()
    @commands.command(aliases=["r"])
    async def reload(self, ctx, arg):
        """Reloads extension."""
        self.bot.reload_extension(f"app.cogs.{arg}")
        await ctx.send(f"app.cogs.{arg} reloaded.")

    @commands.is_owner()
    @commands.command(aliases=["a"])
    async def activity(self, ctx, *, arg):
        """Changes the bot activity"""
        self.activity_str = arg
        await self.bot.change_presence(
            activity=discord.Game(self.activity_str),
            status=eval(f"discord.Status.{self.status_str}"),
        )

    @commands.is_owner()
    @commands.command(aliases=["s"])
    async def status(self, ctx, arg):
        """Changing the bot status."""
        self.status_str = arg
        await self.bot.change_presence(
            activity=discord.Game(self.activity_str), status=eval(f"discord.Status.{self.status_str}")
        )

def setup(bot):
    bot.add_cog(Admin(bot))
