"""
Cog for executing source code from Discord channel chat message.
"""

import re
import json
import base64
import aiohttp
from http.client import responses
from datetime import datetime

import discord
from discord.ext import commands
from discord import Embed, Color


from typing import Optional
from bot.constants import Lang


class Execution(commands.Cog):
    """
    Represents instance of a Cog for executing source codes.
    """

    def __init__(self, bot):
        self.bot = bot

    def __strip_source_code(self, code: str) -> str:
        """
        Strips the source code from a Discord message.
        
        It strips:
            code wrapped in backticks ` (one line code)
            code wrapped in triple backtick ``` (multiline code)
            code wrapped in triple backticks and
                 language keyword ```python (syntax highlighting)
        """
        code = code.strip("`")
        if re.match(r"\w*\n", code):
            code = "\n".join(code.split("\n")[1:])
        return code

    async def __post_hastebin(self, content):
        """
        Posts output to hastebin/documents if it is too large.
        
        Posts to hastebin if the output(stdout, stderr, compile output)
        is more than 1000 characters long.  
        """
        base_url = "https://hastebin.com/documents"
        async with aiohttp.ClientSession() as session:
            async with session.post(
                base_url, data=content.encode("utf-8")
            ) as resp:
                if resp.status != 200:
                    return f"{resp.status} {responses[resp.status]}"
                return f"{resp}/{(await resp.json())['key']}"

    async def __create_output_embed(
        self,
        stdout: str,
        stderr: str,
        compile_output: str,
        time: float,
        memory: int,
        language: str,
        language_icon: str,
        description: str,
        author_name: str,
        author_icon: str,
    ):
        """
        Creates a Discord embed for the submission execution.
        
        Includes:
            Author of the submission.
            Green or red color of the embed depending on the description.
            Output (stdout, stderr, compile output)
            Link for full output (if any)
            Time and memeroy usage
            Language name, icon and version.
            Datetime of the execution.
        """
        color = Color.green() if description == "Accepted" else Color.red()

        embed = Embed(colour=color, timestamp=datetime.now())
        embed.set_author(name=f"{author_name}'s code execution", icon_url=author_icon)

        output = str()
        if stdout:
            output += base64.b64decode(stdout.encode()).decode()
        if stderr:
            output += base64.b64decode(stderr.encode()).decode()
        if compile_output and not output:
            output += base64.b64decode(compile_output.encode()).decode()
        if not output:
            output = "No output"

        if len(output) > 1000:
            hastebin_post = await self.__post_hastebin(output)

            if hastebin_post.startswith("http"):
                embed.description = f"Output too large - [Full output]({hastebin_post})"
            else:
                embed.description = (
                    f"Output too large - Full output is unavaible due {hastebin_post}"
                )
            output = "(...)\n" + output[-1000:]

        embed.add_field(name="Output", value=f"```yaml\n{output}```", inline=False)

        if time:
            embed.add_field(name="Time", value=f"{time} s")
        if memory:
            embed.add_field(name="Memory", value=f"{round(memory / 1000, 2)} MB")
        embed.set_footer(text=f"{language} | {description}", icon_url=language_icon)

        return embed

    async def __get_submission(self, source_code: str, language_id: int) -> dict:
        """
        Sends submission in judge0 API and waits for output.
        """
        base_url = "https://api.judge0.com/submissions/"
        base64_code = base64.b64encode(source_code.encode()).decode()
        payload = {"source_code": base64_code, "language_id": language_id}

        async with aiohttp.ClientSession() as cs:
            async with cs.post(f"{base_url}?base64_encoded=true", data=payload) as r:
                if r.status not in [200, 201]:
                    return f"{r.status} {responses[r.status]}"
                res = await r.json()
            token = res["token"]

            while True:
                submission = await cs.get(f"{base_url}{token}?base64_encoded=true")
                if submission.status not in [200, 201]:
                    return f"{submission.status} {responses[submission.status]}"

                adict = await submission.json()
                if adict["status"]["id"] not in [1, 2]:
                    break
        return adict

    async def __execute_code(self, ctx, lang: int, code: str):
        """
        The main method for executing source code from a message.

        If version check is passed for arg - it sends language version only.

        The steps for executing code:
            strips the source code
            creates and waits for sumbission output

            if is error it sends the error
            otherwise it creates an embed for the output and sends it in the same chat
        """
        if code.startswith("-v") or code.startswith("-version"):
            await ctx.send(lang.version)
            return

        code = self.__strip_source_code(code)
        submission = await self.__get_submission(code, lang.id)

        if isinstance(submission, str):  # it is error code
            await ctx.send(submission)
            return

        await ctx.send(
            embed=await self.__create_output_embed(
                stdout=submission["stdout"],
                stderr=submission["stderr"],
                compile_output=submission["compile_output"],
                time=submission["time"],
                memory=submission["memory"],
                language=lang.version,
                language_icon=lang.icon,
                description=submission["status"]["description"],
                author_name=str(ctx.message.author),
                author_icon=ctx.message.author.avatar_url,
            )
        )

    @commands.command(name="bash")
    async def execute_bash(self, ctx, *, code: str):
        """Executes Bash code; -v to check version."""
        await self.__execute_code(ctx, Lang.Bash, code)

    @commands.command(name="c")
    async def execute_c(self, ctx, *, code: str):
        """Executes C code; -v to check version."""
        await self.__execute_code(ctx, Lang.C, code)

    @commands.command(name="cpp", aliases=['c++'])
    async def execute_cpp(self, ctx, *, code: str):
        """Executes C++ code; -v to check version."""
        await self.__execute_code(ctx, Lang.Cpp, code)

    @commands.command(name="csharp", aliases=['c#'])
    async def execute_csharp(self, ctx, *, code: str):
        """Executes C# code; -v to check version."""
        await self.__execute_code(ctx, Lang.CSharp, code)

    @commands.command(name="clojure")
    async def execute_clojure(self, ctx, *, code: str):
        """Executes Clojure code; -v to check version."""
        await self.__execute_code(ctx, Lang.Clojure, code)

    @commands.command(name="crystal")
    async def execute_crystal(self, ctx, *, code: str):
        """Executes Crystal code; -v to check version."""
        await self.__execute_code(ctx, Lang.Crystal, code)

    @commands.command(name="elixir")
    async def execute_elixir(self, ctx, *, code: str):
        """Executes Elixir code; -v to check version."""
        await self.__execute_code(ctx, Lang.Elixir, code)

    @commands.command(name="erlang")
    async def execute_erlang(self, ctx, *, code: str):
        """Executes Erlang code; -v to check version."""
        await self.__execute_code(ctx, Lang.Erlang, code)

    @commands.command(name="go", aliases=['golang'])
    async def execute_go(self, ctx, *, code: str):
        """Executes Golang code; -v to check version."""
        await self.__execute_code(ctx, Lang.Go, code)

    @commands.command(name="haskell")
    async def execute_haskell(self, ctx, *, code: str):
        """Executes Haskell code; -v to check version."""
        await self.__execute_code(ctx, Lang.Haskell, code)

    @commands.command(name="java")
    async def execute_java(self, ctx, *, code: str):
        """Executes Java code; -v to check version."""
        await self.__execute_code(ctx, Lang.Java, code)

    @commands.command(name="javascript", aliases=['js'])
    async def execute_js(self, ctx, *, code: str):
        """Executes JavaScript code; -v to check version."""
        await self.__execute_code(ctx, Lang.JavaScript, code)

    @commands.command(name="python", aliases=['py'])
    async def execute_python(self, ctx, *, code: str):
        """Executes Python code; -v to check version."""
        await self.__execute_code(ctx, Lang.Python, code)

    @commands.command(name="ruby")
    async def execute_ruby(self, ctx, *, code: str):
        """Executes Ruby code; -v to check version."""
        await self.__execute_code(ctx, Lang.Ruby, code)

    @commands.command(name="rust")
    async def execute_rust(self, ctx, *, code: str):
        """Executes Rust code; -v to check version."""
        await self.__execute_code(ctx, Lang.Rust, code)


def setup(bot):
    bot.add_cog(Execution(bot))
