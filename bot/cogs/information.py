import aiohttp
from datetime import datetime as dt
from http.client import responses

import discord
from discord.ext import commands
from discord import Embed, Color

from bot.paginator import Paginator

from typing import Optional
from bot.constants import (
    BASE_URL,
    LANGUAGES,
    NEWLINES_LIMIT,
    CHARACTERS_LIMIT,
    Emoji,
    JUDGE0_ICON,
    START_TIME,
    PREFIX,
)


class Information(commands.Cog):
    """
    Represents a Cog for retrieving judge0 API information.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        """Sends useful information about the bot and links."""
        uptime = int((dt.utcnow() - START_TIME).total_seconds())
        d, h = divmod(uptime, 86400)
        h, m = divmod(h, 3600)
        m, s = divmod(m, 60)

        embed = Embed(
            title="Judge0Bot",
            url="https://discordbots.org/bot/620609604295852033",
            timestamp=dt.utcnow(),
            description="Discord bot for problem solving and running code in the chat through the Judge0 API.",
        )

        embed.set_author(name=f"{ctx.author} request", icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="Bot",
            value=(
                f"Uptime: {d}d {h}h {m}m {s}s\n"
                f"Servers connected: {len(self.bot.guilds)}\n"
                f"Unique users: {len(self.bot.users)}"
            ),
            inline=False
        )
        embed.add_field(
            name="Links",
            value=(
                f"🔗 [Bot invite](https://discordapp.com/oauth2/authorize?client_id=620609604295852033&scope=bot&permissions=388160)\n"
                f"<:github:707671434427891783>  [GitHub](https://github.com/judge0/discord-bot)\n"
                f"<:discord:707669307454259395>  [Support server](https://discord.gg/6dvxeA8)\n"
                f"<:paypal:707665144276320277>  [Donation on PayPal](https://paypal.me/skilldeliver)\n"
                f"<:patreon:707663083866161232>  [Support me on Patreon](https://www.patreon.com/vmihov)"
            ),
            inline=False
        )
        embed.set_thumbnail(url=JUDGE0_ICON)
        await ctx.send(embed=embed)



    @commands.command(aliases=["sys"])
    async def system(self, ctx):
        """Returns info about system on which Judge0 API is running."""
        base_url = f"{BASE_URL}/system_info"

        async with aiohttp.ClientSession() as cs:
            async with cs.get(base_url) as r:
                if r.status not in [200, 201]:
                    await ctx.send(f"{r.status} {responses[r.status]}")
                    return
                data = await r.json()

        alist = [list(data)[x : x + 5] for x in range(0, len(data), 5)]
        pages = list()

        for item in alist:
            embed = Embed(timestamp=dt.utcnow(), title="System Info")
            embed.set_author(
                name=f"{ctx.author} request", icon_url=ctx.author.avatar_url
            )

            for k in item:
                embed.add_field(name=k, value=data[k], inline=False)
            pages.append(embed)

        paginator = Paginator(self.bot, ctx, pages, 30)
        await paginator.run()

    @commands.command()
    async def languages(self, ctx):
        """Sends a list of all supported languages."""
        pages = list()
        lang_ver = list()

        for _, lang in LANGUAGES['array'].items():
            command = lang['command'] # eval(f"Lang.{lang}.command")
            version = lang['version'] # eval(f"Lang.{lang}.version")
            emoji = lang['emoji'] # eval(f"Lang.{lang}.emoji")

            lang_ver.append((command, version, emoji))

        lang_chunks = [lang_ver[x : x + 5] for x in range(0, len(lang_ver), 5)]

        for chunk in lang_chunks:   
            embed = Embed(timestamp=dt.utcnow(), title="Supported languages")
            embed.set_author(
                name=f"{ctx.author} request", icon_url=ctx.author.avatar_url
            )

            for lang in chunk:
                embed.add_field(
                    name=f"{PREFIX}{lang[0]}",
                    value=f" {lang[2]} {lang[1]}",
                    inline=False,
                )
            pages.append(embed)
        paginator = Paginator(self.bot, ctx, pages, 30)
        await paginator.run()

def setup(bot):
    bot.add_cog(Information(bot))
