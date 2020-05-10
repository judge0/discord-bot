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
from bot.constants import Emoji, LANGUAGES, Color
from bot.paginator import Paginator


class Judge(commands.Cog):
    """
    Represents a Cog for executing tasks.
    """

    def __init__(self, bot):
        self.bot = bot

    
    async def __create_output_embed():
        pass

    @commands.command()
    async def judge(self, ctx, task_id, language="python", *, code: Optional[str]):
        """Runs a judge."""

        # Invalid language passed
        if language not in LANGUAGES['ids']:
            await ctx.send('Invalid language is passed!')
            return 

        with open("bot/tasks.json", encoding="utf-8") as f:
            data = json.load(f)

            if task_id == 'list':
                await ctx.send('\n'.join(f'`{i}` **{data[i]["title"]}**: difficulty ({data[i]["difficulty"]})'for i in data if i != 'authors'))
                return
            
            # invalid task id is inputed
            if task_id not in data:
                await ctx.send("Invalid task id!")
                return

            task = data[task_id]
            if not code: # code is not passed only task is shown
                embed = Embed.from_dict(self.__pack_description_embed_dict(data, task_id)) 
                await ctx.send(embed=embed)
                return

            # await ctx.message.add_reaction(Emoji.Execution.loading)
            code = Execution.strip_source_code(code)
            none_failed = True
            pages = list()
            embed = None
            submissions = list()

            await ctx.message.delete()

            language_id = LANGUAGES['ids'][language]
            message = await ctx.send(f"{ctx.message.author.mention} submited a solution to problem {task_id} in {LANGUAGES['array'][language_id]['version']}")

            for n, case in enumerate(task['test_cases']):
                submissions.append(Execution.prepare_paylad(source_code=code,
                                                            language_id=LANGUAGES['ids'][language],
                                                            stdin='\n'.join(case['inputs']),
                                                            expected_output=case['output']))

            result = await Execution.get_batch_submissions(submissions=submissions)

            for n, case in enumerate(result['submissions']):
                embed = Embed(timestamp=dt.utcnow(), title="Judge0 Result")
                embed.set_author(
                    name=f"{ctx.author} submission", icon_url=ctx.author.avatar_url
                )

                emoji = Emoji.Execution.error
                
                failed = True

                output = str()
                if case['stdout']:  
                    output = base64.b64decode(case["stdout"].encode()).decode().strip()

                trimed_output = output
                if trimed_output.count("\n") > 10:
                    trimed_output = "(...)\n" + "\n".join(trimed_output.split("\n")[:10])
                if len(output) > 300:
                    trimed_output = "(...)\n" * trimed_output[:300]
                
                if case['compile_output']:
                    info = "Compilation error."
                elif case['stderr']:
                    error = base64.b64decode(case["stderr"].encode()).decode().strip()
                    info = f"Runtime error. {error}"
                elif output != task['test_cases'][n]['output']:
                    if task['test_cases'][n]['hidden']:
                        info = "Hidden."
                    else:
                        test_input = '\n'.join(task['test_cases'][n]['inputs'])
                        info = (
                                f"**On input:**\n"
                                f"{test_input}\n"
                                f"**Expected:**\n"
                                f"{task['test_cases'][n]['output']}\n"
                                f"**Got:**\n{trimed_output}"
                                )
                        
                else:
                    info = "Got the expected output."
                    emoji = Emoji.Execution.successful
                    failed = False
                
                if none_failed and failed:
                    none_failed = False

                embed.add_field(
                    name=f"{emoji} Test Case {n+1}.",
                    value=info,
                    inline=False
                )
                pages.append(embed)
                
            # if none_failed:
            #     await ctx.message.add_reaction(Emoji.Execution.successful)
            # else:
            #     await ctx.message.add_reaction(Emoji.Execution.error)
            await message.delete()
            paginator = Paginator(self.bot, ctx, pages, 30)
            await paginator.run()

    @staticmethod
    def __get_language_id(language: str) -> int:
        pass    
 
    @staticmethod        
    def __pack_description_embed_dict(data: dict, task_id: str) -> dict:

        task = data[task_id]
        embed_dict = {
            "title": task["title"],
            "description": task["description"],
            "color": Color.difficulties[task['difficulty']],
            "author": {
                **data["authors"][task["author"]]
            },
            "fields": [
                {
                    "name": "Example",
                    "value": task["example"]
                }
            ],

        }
        return embed_dict
            
            # code = Execution.strip_source_code(code)
            # submission = await self.get_submission(code, lang.id, stdin="\n".join())

        # await self.__execute_code(ctx, Lang.TypeScript, code)

    
def setup(bot):
    bot.add_cog(Judge(bot))