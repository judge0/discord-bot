import discord
from discord import Embed
from discord.ext import commands

from bot.constants import PREFIX, JUDGE0_TEAM, JUDGE0_GUILD, JUDGE0_JOIN_CHANNEL


def is_team_member():
    async def predicate(ctx):
        return ctx.author.id in JUDGE0_TEAM

    return commands.check(predicate)


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

    @commands.Cog.listener()
    async def on_command_error(self, context, exception):
        if str(exception).endswith("Missing Permissions"):
            await context.send(
                "The bot should have **Add reactions** permission to work properly!"
            )
        else:
            print(exception)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == JUDGE0_GUILD:
            join_channel = self.bot.get_channel(JUDGE0_JOIN_CHANNEL)
            await join_channel.send(
                (
                    "```python\n"
                    "import server\n"
                    f"user = {member.mention} # {member.display_name}\n"
                    "user.join(server)```\n"
                    f"Welcome to **Judge0 support server** {member.mention}!"
                )
            )

    @is_team_member()
    @commands.command(aliases=["q"])
    async def quit(self, ctx):
        """Shuts down the bot."""
        await ctx.send("Terminates.")
        await self.bot.logout()

    @is_team_member()
    @commands.command()
    async def servers(self, ctx):

        #     # guild = self.bot.get_guild(622750805451341844)
        #     channel = self.bot.get_channel(623850862112014377)
        #     messages = await channel.history(limit=10).flatten()

        #     print(len(messages))
        #     for m in messages:
        #         print(m.content)
        #     # await ctx.send('\n'.join(f"{g.name} {g.id}" for g in guild.channels))
        await ctx.send(
            "\n".join(f"{g.name} -> {len(g.members)}" for g in self.bot.guilds)
        )

    @is_team_member()
    @commands.command(aliases=["r"])
    async def reload(self, ctx, arg):
        """Reloads extension."""
        self.bot.reload_extension(f"bot.cogs.{arg}")
        await ctx.send(f"bot.cogs.{arg} reloaded.")

    @is_team_member()
    @commands.command(aliases=["a"])
    async def activity(self, ctx, *, arg):
        """Changes the bot activity"""
        self.activity_str = arg
        await self.bot.change_presence(
            activity=discord.Game(self.activity_str),
            status=eval(f"discord.Status.{self.status_str}"),
        )

    @is_team_member()
    @commands.command(aliases=["s"])
    async def status(self, ctx, arg):
        """Changing the bot status."""
        self.status_str = arg
        await self.bot.change_presence(
            activity=discord.Game(self.activity_str),
            status=eval(f"discord.Status.{self.status_str}"),
        )

    @is_team_member()
    @commands.command()
    async def emoji(self, ctx, arg: discord.Emoji):
        """Returns the emoji ID."""
        await ctx.send(arg.id)

    @is_team_member()
    @commands.command()
    async def emoji_list(self, ctx):
        for guild in self.bot.guilds:
            if guild.id == 620615182116323328:
                for emoji in guild.emojis:
                    print(str(emoji))


def setup(bot):
    bot.add_cog(Admin(bot))
