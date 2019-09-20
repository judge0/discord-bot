"""Embed paginator for paginating too large embes"""

import asyncio


# emojis for input
FAST_PREVIOUS = "\u23EA"  # [:track_previous:]
PREVIOUS = "\u25C0"  # [:arrow_left:]
NEXT = "\u25B6"  # [:arrow_right:]
FAST_NEXT = "\u23E9"  # [:track_next:]
DELETE_EMOJI = "\U0001F1FD"  # [:x:]

# unite the emojis in one list
EMOJIS = [FAST_PREVIOUS, PREVIOUS, NEXT, FAST_NEXT, DELETE_EMOJI]


class Paginator:
    """
    Represents the interactive paginator.
    """
    def __init__(self, bot, ctx, pages, timeout):
        self.bot = bot
        self.ctx = ctx
        self.pages = pages
        self.timeout = timeout

        self.index = int()
        self.paginating = True

        self.func = None
        self.emoji_func = {
            FAST_PREVIOUS: self.fast_previous,
            PREVIOUS: self.prev,
            NEXT: self.next,
            FAST_NEXT: self.fast_next,
            DELETE_EMOJI: self.delete,
        }

    async def fast_previous(self):
        """Skip to the first page."""
        self.index = 0

    async def fast_next(self):
        """Skip to the last page."""
        self.index = len(self.pages) - 1

    async def next(self):
        """Move to the next page."""
        if self.index != len(self.pages) - 1:
            self.index += 1

    async def prev(self):
        """Move to the previous page."""
        if self.index != 0:
            self.index -= 1

    async def delete(self):
        """Delete the emojis. Session is terminated."""
        self.paginating = False
        for emoji in EMOJIS:
            await self.message.remove_reaction(emoji, self.bot.user)

    def check(self, reaction, user):
        """Checks:
			If the emoji which is added is one of the emojis
			which are used as an input utility
			
			If the user who is adding emojis is the user
			who invoked the command
			
			If the messages are the same one."""
        if reaction.emoji in EMOJIS:
            self.func = self.emoji_func[reaction.emoji]
        return (
            user == self.ctx.message.author
            and self.message.id == reaction.message.id
            and reaction.emoji in EMOJIS
        )

    async def run(self):
        """Main interactive loop for the paginator."""
        self.pages[self.index].set_footer(
            text=f"Page {self.index + 1}/{len(self.pages)}"
        )
        self.message = await self.ctx.send(embed=self.pages[self.index])

        for emoji in EMOJIS:
            await self.message.add_reaction(emoji)

        while self.paginating:
            try:
                await self.wait_first(
                    self.wait_for_reaction_add(), self.wait_for_reaction_remove()
                )
            except asyncio.TimeoutError:
                self.paginating = False
                for emoji in EMOJIS:
                    await self.message.remove_reaction(emoji, self.bot.user)
                self.pages[self.index].set_footer(text=f"Session timed out")
                await self.message.edit(embed=self.pages[self.index])
            else:
                await self.func()
                if self.paginating:
                    self.pages[self.index].set_footer(
                        text=f"Page {self.index + 1}/{len(self.pages)}"
                    )
                    await self.message.edit(embed=self.pages[self.index])
                else:
                    self.pages[self.index].set_footer(text=f"Session closed")
                    await self.message.edit(embed=self.pages[self.index])

    async def wait_first(self, *futures):
        """Wait for reaction add or reaction remove."""
        done, pending = await asyncio.wait(futures, return_when=asyncio.FIRST_COMPLETED)
        gather = asyncio.gather(*pending)
        gather.cancel()
        try:
            await gather
        except asyncio.CancelledError:
            pass
        return done.pop().result()

    async def wait_for_reaction_add(self):
        """Wait for reaction add."""
        return await self.bot.wait_for(
            "reaction_add", check=self.check, timeout=self.timeout
        )

    async def wait_for_reaction_remove(self):
        """Wait for reaction remove."""
        return await self.bot.wait_for(
            "reaction_remove", check=self.check, timeout=self.timeout
        )
