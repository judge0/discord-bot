"""
Cog for submiting and testing tasks
"""

import base64
from datetime import datetime as dt
import json
from typing import Optional

from discord.ext import commands
from discord import Embed 
from bot.cogs.execution import Execution
from bot.constants import Emoji, Lang, Color
from bot.paginator import Paginator


class Judge(commands.Cog):
    """
    Represents a Cog for executing tasks.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def judge(self, ctx, task_id, language="python"   , *, code: Optional[str]):
        """Runs a judge."""

        # Invalid language passed
        if language not in Lang.ids:
            await ctx.send('Invalid language is passed!')
            return 

        with open("bot/tasks.json") as f:
            data = json.load(f)

            # invalid task id is inputed
            if task_id not in data:
                await ctx.send("Invalid task id!")
                return

            task = data[task_id]
            if not code: # code is not passed only task is shown
                embed = Embed.from_dict(self.__pack_embed_dict(task))
                await ctx.send(embed=embed)
                return

            await ctx.message.add_reaction(Emoji.Execution.loading)
            code = Execution.strip_source_code(code)

            result = str()
            none_failed = True
            pages = list()
            embed = None

            for n, case in enumerate(task['test_cases']):
                submission = await Execution.get_submission(code,
                                                            Lang.ids[language],
                                                            stdin='\n'.join(case['inputs']))

                if isinstance(submission, str):  # it is error code
                    await ctx.message.add_reaction(Emoji.Execution.offline)
                    await ctx.send(submission)
                    await ctx.message.remove_reaction(
                        Emoji.Execution.loading, self.bot.user
                    )
                    return

                output = base64.b64decode(submission["stdout"].encode()).decode().strip()


                if n % 5 == 0 or n == 0 or n == len(task['test_cases']) - 1:
                    if n != 0:
                        pages.append(embed)
                    embed = Embed(timestamp=dt.utcnow(), title="Judge0 Result")
                    embed.set_author(
                        name=f"{ctx.author} submission", icon_url=ctx.author.avatar_url
                    )

                if  output != case["output"]:
                    none_failed = False
                    info = "Hidden."
                    if not case["hidden"]:
                        info = f'Expected {case["output"]} Got {output}'

                    embed.add_field(
                        name=f"{Emoji.Execution.error} Test Case {n+1}.",
                        value=info,
                        inline=False
                    )
                else:
                    embed.add_field(
                        name=f"{Emoji.Execution.successful} Test Case {n+1}.",
                        value=f"Got the expected input.",
                        inline=False
                    )
                
            if none_failed:
                await ctx.message.add_reaction(Emoji.Execution.successful)
            else:
                await ctx.message.add_reaction(Emoji.Execution.error)
            await ctx.message.remove_reaction(
                Emoji.Execution.loading, self.bot.user
            )

            paginator = Paginator(self.bot, ctx, pages, 30)
            await paginator.run()

    @staticmethod
    def __get_language_id(language: str) -> int:
        pass


 
    @staticmethod        
    def __pack_embed_dict(data: dict) -> dict:
        embed_dict = {
            "color": Color.difficulties[data['difficulty'] - 1],
            "title": data["title"],
            "description": data["description"],
            "fields": [
                {
                    "name": "Example",
                    "value": data["example"]
                }
            ],
        }
        return embed_dict
            
            # code = Execution.strip_source_code(code)
            # submission = await self.get_submission(code, lang.id, stdin="\n".join())

        # await self.__execute_code(ctx, Lang.TypeScript, code)

    
def setup(bot):
    bot.add_cog(Judge(bot))