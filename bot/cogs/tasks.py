"""
Cog for submiting and testing tasks
"""

import base64
from datetime import datetime as dt
from dataclasses import dataclass
import json
from typing import Optional

from discord.ext import commands
from discord import Embed, Color as DiscordColor 
from bot.cogs.execution import Execution
from bot.constants import Emoji, LANGUAGES, Color
from bot.paginator import Paginator

class Judge(commands.Cog):
    """
    Represents a Cog for executing tasks.
    """

    def __init__(self, bot):
        self.bot = bot

    async def __check_invalid_language(self):
        if self.language not in LANGUAGES['ids']:
            await self.ctx.send('Invalid language is passed!')
            return True
        return False

    async def __check_invalid_attachment(self):
        if self.ctx.message.attachments:
            try:
                self.content = await self.ctx.message.attachments[0].read() 
                self.code = content.decode('utf-8').strip()
                return False
            except Exception as e:
                await self.ctx.send('Can not read this attachment!')
                return True
        return False 

    async def __check_invalid_task(self):
        if self.task_id not in self.data:
            await self.ctx.send("Invalid task id!")
            return True
        return False

    async def __show_task_description(self):
        if not self.code: # code is not passed only task is shown
            embed = Embed.from_dict(self.__pack_description_embed_dict(self.data,
                                                                       self.task_id)) 
            await self.ctx.send(embed=embed)
            return True
        return False

    async def __send_submitted_message(self):
        language_id = LANGUAGES['ids'][self.language]
        user = self.ctx.message.author.mention
        lang_sub =  LANGUAGES['array'][language_id]['version']
        return await self.ctx.send(f"{user} submited a solution to problem {task_id} in {lang_sub}")

    @commands.command()
    async def judge_list(self, ctx, difficulty: Optional[int]):
        with open("bot/tasks.json", encoding="utf-8") as f:
            data = json.load(f)

            tasks_chunks = self.__create_tasks_chunks(data, difficulty)
            pages = list()

            for chunk in tasks_chunks:
                tasks = self.__concatanate_tasks_to_string(chunk)
                pages.append(Embed.from_dict(
                     self.__pack_tasks_embed_dict(tasks,
                     {"name": f"{ctx.author.name}'s invoke","icon_url": str(ctx.author.avatar_url)})
                    )
                )

        paginator = Paginator(self.bot, ctx, pages, 30)
        await paginator.run()

    @commands.command()
    async def judge(self, ctx, task_id, language="python", *, code: Optional[str]):
        """Runs a judge."""
        print('BRO?')
        # Set arguments as attributes
        self.ctx, self.task_id, self.language, self.code = ctx, task_id, language, code 

        # Perform checks before connecting to the data
        if await self.__check_invalid_language():
            return
        print(1)
        if await self.__check_invalid_attachment():
            return 

        with open("bot/tasks.json", encoding="utf-8") as f:
            self.data = json.load(f)
            
            # invalid task id is inputed and stop
            if self.__check_invalid_task():
                return

            # show only the task and stop
            if self.__show_task_description():
                return
            # get the current task
            task = self.data[task_id]

            # strip the source code that is passed  
            code = Execution.strip_source_code(code)

            # initialize variables
            pages = test_cases = list()
            embed, none_failed, passed_count = None, True, int()

            # delete the message of the user 
            await ctx.message.delete() # we don't want others to see the code
            message = await self.__send_submitted_message()
            # send information message that submission is passed (delete after)
            submissions = self.__create_submissions(tasks)
            result = await Execution.get_batch_submissions(submissions=submissions)

            
            # iterate all test cases of the submission    
            for n, case in enumerate(result['submissions']):
                output = str()
                if case['stdout']:  
                    output = base64.b64decode(case["stdout"].encode()).decode().strip()

                test_case_dict = self.__format_test_case(task, case, output)

                test_case = test_case_dict['test_case']
                info = test_case_dict['info']
                failed = test_case_dict['failed']

                if not failed: 
                    passed_count += 1

                if none_failed and failed:
                    none_failed = False

                if not task['test_cases'][n]['hidden'] and failed: 

                    title = f"**{task['title']}**\n{emoji} Test case #{n + 1}"
                    author =  {"name": f"{ctx.author.name}'s invoke",
                               "icon_url": str(ctx.author.avatar_url)}
                    embed = Embed.from_dict(self.__pack_failed_case_embed_dict())

                    pages.append(embed)
                test_cases.append(test_case)

            color = DiscordColor.green() if none_failed else DiscordColor.red()

            main_page = Embed(timestamp=dt.utcnow(),
                              title=(f"**{task['title']}**\n"
                                     f"Test results {passed_count}/"
                                     f"{len(task['test_cases'])}\n\n"),
                             color=color) 
            main_page.set_author(name=f"{ctx.message.author}'s solution", icon_url=ctx.message.author.avatar_url)
            main_page.description = "\n".join(test_cases)

            
            pages.insert(0, main_page)
            await message.delete()
            paginator = Paginator(self.bot, ctx, pages, 30)
            await paginator.run()

    @staticmethod
    def __create_submissions(tasks: dict) -> list:
        submissions = list()
        for n, case in enumerate(task['test_cases']):
            submissions.append(Execution.prepare_paylad(source_code=code,
                                                        language_id=LANGUAGES['ids'][language],
                                                        stdin='\n'.join(case['inputs']),
                                                        expected_output=case['output']))
        return submissions

    @staticmethod
    def __create_tasks_chunks(data: dict, difficulty: int) -> list:
        lst = [(k, v) for k, v in data.items() if k != 'authors']  

        if difficulty:
            lst = list(filter(lambda x: x[1]["difficulty"] == difficulty, lst))     

        return [lst[i:i + 10] for i in range(0, len(lst), 10)]

    @staticmethod
    def __concatanate_tasks_to_string(chunk: list) -> str:
        tasks = str()
        d = "difficulty"
        
        for e in chunk:
            tasks += f"`{e[0]}` **{e[1]['title']}**: {d} {e[1][d]}\n"
        return tasks

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

    @staticmethod
    def __pack_tasks_embed_dict(tasks_str: str, author: dict) -> dict:
        embed_dict = {
            "title": "Problem solving tasks in Judge",
            "description": tasks_str,
            "author": {
                **author
            }
        }
        return embed_dict

    @staticmethod
    def __pack_failed_case_embed_dict(title: str, author: dict,  info: str) -> dict:
        embed_dict = {
            'timestamp': dt.utcnow(),
            'title': title,
            'description': info,
            'author': {
                **author
            }   
        } 
        return embed_dict

    @staticmethod
    def __trim_output(output: str) -> str:
        if output.count("\n") > 10:
            output = "(...)\n" + "\n".join(output.split("\n")[:10])
        if len(output) > 300:
            output = "(...)\n" + output[:300]
        return output

    @staticmethod
    def __format_test_case(task: dict, case: dict, output: str) -> dict:
        trimed_output = self.__trim_output(output)

        emoji = Emoji.Execution.error
        failed = True
        test_case = f"{emoji} **Test case #{n + 1}**"
        if task['test_cases'][n]['hidden']:
            test_case += " (Hidden)"

        if case['compile_output']:
            info = base64.b64decode(case["compile_output"].encode()).decode().strip()    
        elif case['stderr']:
            info = base64.b64decode(case["stderr"].encode()).decode().strip()
        elif output != task['test_cases'][n]['output']:
            test_input = '\n'.join(task['test_cases'][n]['inputs'])
            info = (
                    f"**On input:**\n"
                    f"{test_input}\n"
                    f"**Expected:**\n"
                    f"{task['test_cases'][n]['output']}\n"
                    f"**Got:**\n{trimed_output}"
                    )
        else:
            emoji = Emoji.Execution.successful
            test_case = f"{emoji} **Test case #{n + 1}**"
            failed = False

        return {'test_case': test_case,
                'info': info,
                'failed': failed}
                

def setup(bot):
    bot.add_cog(Judge(bot))