import discord
from discord.ext import commands
from discord import Embed, Color

from bot.paginator import Paginator
from typing import Optional
from datetime import datetime as dt

from discord.ext import commands

from bot.paginator import Paginator
from bot.constants import PREFIX


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, arg: Optional[str]):
        if arg:
            pass
        else:
            pages = list()
            first_page = Embed(
                timestamp=dt.utcnow(),
                description=f"Note that **{PREFIX}lang** is a placeholder for a command from **{PREFIX}languages**",
            )
            first_page.set_author(
                name=f"{ctx.author} request", icon_url=ctx.author.avatar_url
            )

            first_page.add_field(
                name=f"{PREFIX}languages",
                value=("Sends a list of all language commands"),
                inline=False,
            )
            first_page.add_field(
                name=f"{PREFIX}lang\ncode",
                value=("Executes the **code** and sends the output"),
                inline=False,
            )
            first_page.add_field(
                name=f"{PREFIX}lang",
                value=("Sends a guide how to pass the code\n"),
                inline=False,
            )
            first_page.add_field(
                name=f"{PREFIX}lang -v",
                value=("Sends the version of the language\n"),
                inline=False,
            )
            first_page.set_author(
                name=f"{ctx.author} request", icon_url=ctx.author.avatar_url
            )

            first_page.add_field(
                name=f"{PREFIX}info",
                value=(
                    "Sends useful information and links for the bot, Judge0 and the developers"
                ),
                inline=False,
            )
            first_page.add_field(
                name=f"{PREFIX}workers",
                value=(
                    "Sends workers health check information\n"
                    "Workers do the job of running untrusted programs in sandboxed environment."
                ),
                inline=False,
            )
            first_page.add_field(
                name=f"{PREFIX}sytem",
                value=(
                    "Sends detailed information about system on which Judge0 API is running.\n"
                ),
                inline=False,
            )
            await ctx.send(embed=first_page)

    @commands.command()
    async def lang(self, ctx, arg: Optional[str]):
        await ctx.send(
            f" **{PREFIX}lang** should be a command from **{PREFIX}languages**."
        )


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Help(bot))
