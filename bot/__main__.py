"""
Main program for running the bot:

python -m bot token
"""

import asyncio
import os, sys, time

from bot.client import Judge0Bot
from bot.constants import PREFIX

# main run
async def main():
    bot = Judge0Bot(command_prefix=PREFIX)
    await bot.load_db()
    # run the bot with the token or enviroment variable
    token = sys.argv[1] if len(sys.argv) >= 2 else os.environ["BOT_TOKEN"]
    await bot.start(token)

time.sleep(3)  # wait for postgres to start

loop = asyncio.get_event_loop()
loop.run_until_complete(main())