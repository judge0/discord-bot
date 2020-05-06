import discord
from discord import Embed
from discord.ext import commands

from bot.constants import PREFIX, JUDGE0_TEAM, JUDGE0_GUILD, JUDGE0_JOIN_CHANNEL


def is_team_member():
    """Check for asserting that the commands invoker is in the team."""
    async def predicate(ctx):
        return ctx.author.id in JUDGE0_TEAM

    return commands.check(predicate)


class Admin(commands.Cog):
    """
    Represents a Cog for Admin only commands.
    """
    def __init__(self, bot):
        self.bot = bot
        self.activity_str = f"with {PREFIX}help"
        self.status_str = "online"

    @commands.Cog.listener()
    async def on_ready(self):
        """Prints on the console that the bot is ready and changes the presence."""
        print(f"Logged on as {self.bot.user}")
        await self.bot.change_presence(
            activity=discord.Game(self.activity_str),
            status=eval(f"discord.Status.{self.status_str}"),
        )

    @commands.Cog.listener()
    async def on_command_error(self, context, exception):
        """Reminds that the bot is missing permissions."""
        if str(exception).endswith("Missing Permissions"):
            await context.send(
                "The bot should have **Add reactions** permission to work properly!"
            )
        else:
            print(exception)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Sends a entry message if new user joined the Judge0 support server."""
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
    async def terminate(self, ctx):
        """Shuts down the bot."""
        await ctx.send("Terminates.")
        await self.bot.logout()

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
    @commands.command(aliases=["g"])
    async def get_emoji(self, ctx, arg):
        """Changing the bot status."""
        await ctx.send(f'```{str(arg)}```')

    @is_team_member()
    @commands.command()
    async def emoji_list(self, ctx):
        for guild in self.bot.guilds:
            if guild.id == 620615182116323328:
                for emoji in guild.emojis:
                    print(str(emoji))
        
    @is_team_member()
    @commands.command()
    async def guild_list(self, ctx):
        guildlist = str()
        for guild in self.bot.guilds:
            guildlist += f"{guild.name} - {len(guild.members)}\n"
        await ctx.send(guildlist)


def setup(bot):
    bot.add_cog(Admin(bot))
