"""
Includes a lot of useful constants that are used in the bot.
"""

from os import environ as env
import json

from datetime import datetime as dt
from dataclasses import dataclass

from discord import Colour

PREFIX = ":"

BASE_URL = env['BASE_URL'] if 'BASE_URL' in env else 'https://judge0.p.rapidapi.com'
IDE_LINK = "https://ide.judge0.com/"

AUTH_HEADER = env['AUTH_HEADER'] if 'AUTH_HEADER' in env else 'X-RapidAPI-Key'
AUTH_KEY = env['AUTH_KEY'] if 'AUTH_KEY' in env else ''


# output embed limits
NEWLINES_LIMIT = 10 
CHARACTERS_LIMIT = 300

# time used for calculating uptime
START_TIME = dt.utcnow()


# some information for the Judge0 support server
JUDGE0_GUILD = 620615182116323328
JUDGE0_JOIN_CHANNEL = 623949481167290410
JUDGE0_TEAM = [365859941292048384, 512551605321596928]
JUDGE0_ICON = "https://i.imgur.com/Nab2jCa.png"

with open('bot/languages.json') as f:
    LANGUAGES = json.load(f)

@dataclass
class Emoji:
    """
    Represents storage for custom and external emojis.
    """
    class Workers:
        """
        Represents emojis for workers health check.
        (command in bot.cogs.information)
        """
        total= "<:total:620744869429641236>"
        available = "<:available:620705066604560405>"
        idle = "<:idle:620702759414661120>"
        working = "<:working:620704067672342528>"
        paused = "<:paused:620704067479666688>"
        failed = "<:failed:620704067525672980>"

    class Execution:
        loading = "<a:typing:705421984141672470>"
        error = "<:dnd:705421983952666674>"
        successful = "<:online:705421983927763055>"
        offline = "<:offline:705421983873105920>"
        idle = "<:idle:705421983906660454>"

@dataclass
class Color:
    difficulties = [
5025872, 9225035, 13491257, 16772154, 16761352, 16750593, 16668450, 16073527
]
