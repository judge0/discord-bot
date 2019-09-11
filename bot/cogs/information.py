import aiohttp
from datetime import datetime as dt
from http.client import responses

import discord
from discord.ext import commands
from discord import Embed, Color

from bot.paginator import Page, Paginator

from typing import Optional
from bot.constants import Lang, NEWLINES_LIMIT, CHARACTERS_LIMIT, Emoji


class Information(commands.Cog):
    """
    Represents instance of a Cog for retrieving judge0 API information.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def workers(self, ctx):
        """Returns health check information about the workers."""
        base_url = "https://api.judge0.com/workers"

        async with aiohttp.ClientSession() as cs:
            async with cs.get(base_url) as r:
                if r.status not in [200, 201, 500]:
                    await ctx.send(f"{r.status} {responses[r.status]}")
                    return

                data = (await r.json())[0]
        embed = Embed(colour=Color.green(), timestamp=dt.utcnow(), title='Workers Health Check')

        embed.set_author(name=f'{ctx.author} request',
                         icon_url=ctx.author.avatar_url)
        
        embed.add_field(name=f"{Emoji.available} Available", value=data['available'])
        embed.add_field(name=f"{Emoji.idle} IDLE", value=data['idle'])
        embed.add_field(name=f"{Emoji.total} Total", value=data['total'])
        embed.add_field(name=f"{Emoji.working} Working", value=data['working'])
        embed.add_field(name=f"{Emoji.paused} Paused", value=data['paused'])
        embed.add_field(name=f"{Emoji.failed} Failed", value=data['failed'])

        await ctx.send(embed=embed)

    @commands.command(aliases=['sys'])
    async def system(self, ctx):
        """Returns info about system on which Judge0 API is running."""
        base_url = "https://api.judge0.com/system_info"

        async with aiohttp.ClientSession() as cs:
            async with cs.get(base_url) as r:
                if r.status not in [200, 201]:
                    await ctx.send(f"{r.status} {responses[r.status]}")
                    return
                data = (await r.json())

        embed = Embed(colour=Color.green(), timestamp=dt.utcnow(), title='System Info')
        embed.set_author(name=f'{ctx.author} request',
                         icon_url=ctx.author.avatar_url)
        
        for k, v in data.items():
            embed.add_field(name=k, value=v)
        await ctx.send(embed=embed)

    @commands.command()
    async def languages(self, ctx):
        """Returns a list of all languages supported by the Judge0 API."""
        base_url = "https://api.judge0.com/languages"
    
        async with aiohttp.ClientSession() as cs:
            async with cs.get(base_url) as r:
                if r.status not in [200, 201]:
                    await ctx.send(f"{r.status} {responses[r.status]}")
                    return
                data = (await r.json())

        alist = [data[x:x+10] for x in range(0, len(data),10)]
        description = '\n'.join(f'**{i["id"]}.** {i["name"]}' for i in data)
        embed = Embed(colour=Color.green(),
                      timestamp=dt.utcnow(),
                      title='Languages List',
                      description=description)
        embed.set_author(name=f'{ctx.author} request',
                         icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def test(self, ctx):
        page = [Page(author=ctx.author, title='Test1'),
                Page(author=ctx.author, title='Test2'),
                Page(author=ctx.author, title='Test3'),
                Page(author=ctx.author, title='Test4'),
                Page(author=ctx.author, title='Test5'),
                Page(author=ctx.author, title='Test6')]
        paginator = Paginator(self.bot, message=ctx.message, page_list=page)
        await paginator.paginate()

def setup(bot):
    bot.add_cog(Information(bot))
