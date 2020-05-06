"""
Includes a lot of useful constants that are used in the bot.
"""

from datetime import datetime as dt
from dataclasses import dataclass

from discord import Colour

PREFIX = ";"

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


LANGUAGES = {
    "ids_map": {
        "assembly": 45,
        "bash": 46,
        "sh": 46,
        "c": 50,
        "cpp": 54,
        "c++": 54,
        "csharp": 51,
        "c#": 51,
        "lisp": 55,
        "d": 56,
        "elixir": 57,
        "erlang": 58,
        "go": 60,
        "golang": 60,
        "haskell": 61,
        "java": 62,
        "javascript": 63,
        "js": 63,
        "lua": 64,
        "ocaml": 65,
        "octave": 66,
        "pascal": 67,
        "php": 68,
        "prolog": 69,
        "python": 71,
        "py": 71,
        "ruby": 72,
        "rust": 73,
        "typescript": 74,
        "ts": 74,
    }
}


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

        total = "<:total:620744869429641236>"
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
        5025872,
        9225035,
        13491257,
        16772154,
        16761352,
        16750593,
        16668450,
        16073527,
    ]


@dataclass
class Lang:
    """
    Represents storage for supported languages.
    """

    count = 23  # supported languages

    class Assembly:
        command = "assembly"
        version = "Assembly (NASM 2.14.02)"
        id = 45
        icon = "https://i.imgur.com/ObWopeS.png"
        emoji = "<:assembly:662723858859556865>"

    class Bash:
        command = "bash"
        aliases = ["sh"]
        version = "Bash (4.4)"
        id = 46
        icon = "https://i.imgur.com/6BQ4g4J.png"
        emoji = "<:bash:623909088572735498>"

    class C:
        command = "c"
        version = "C (GCC 9.2.0)"
        id = 50
        icon = "https://i.imgur.com/Aoo95wm.png"
        emoji = "<:c_:623909093136138240>"

    class Cpp:
        command = "cpp"
        version = "C++ (GCC 9.2.0)"
        aliases = ["c++"]
        id = 54
        icon = "https://i.imgur.com/CJYqkG5.png"
        emoji = "<:cpp:623909088459227149>"

    class CSharp:
        command = "csharp"
        version = "C# (Mono 6.6.0.161)"
        aliases = ["c#"]
        id = 51
        icon = "https://i.imgur.com/M1AQVY2.png"
        emoji = "<:csharp:623909092402003999>"

    class CommonLisp:
        command = "lisp"
        version = "Common Lisp (SBCL 2.0.0)"
        id = 55
        icon = "https://i.imgur.com/ms9qW6e.png"
        emoji = "<:common_lisp:662723858066964490>"

    class D:
        command = "d"
        version = "D (DMD 2.089.1)"
        id = 56
        icon = "https://i.imgur.com/uoeBAsf.png"
        emoji = "<:d_language:662725748552892437>"

    class Elixir:
        command = "elixir"
        version = "Elixir (1.9.4)"
        id = 57
        icon = "https://i.imgur.com/0tigIIL.png"
        emoji = "<:elixir:623909093148590094>"

    class Erlang:
        command = "erlang"
        version = "Erlang (OTP 22.2)"
        id = 58
        icon = "https://i.imgur.com/5dVX2NF.png"
        emoji = "<:erlang:623909088782450707>"

    class Go:
        command = "go"
        version = "Go (1.13.5)"
        aliases = ["golang"]
        id = 60
        icon = "https://i.imgur.com/a3yrHtU.png"
        emoji = "<:golang:623909092913840128>"

    class Haskell:
        command = "haskell"
        version = "Haskell (GHC 8.8.1)"
        id = 61
        icon = "https://i.imgur.com/NpyZ3z7.png"
        emoji = "<:haskell:623909088622936065>"

    class Java:
        command = "java"
        version = "Java (OpenJDK 13.0.1)"
        id = 62
        icon = "https://i.imgur.com/5OwBztX.png"
        emoji = "<:java:623909088614678544>"

    class JavaScript:
        command = "javascript"
        aliases = ["js"]
        version = "JavaScript (Node.js 12.14.0)"
        id = 63
        icon = "https://i.imgur.com/YOsQqBF.png"
        emoji = "<:javascript:623909088727924747>"

    class Lua:
        command = "lua"
        version = "Lua (5.3.5)"
        id = 64
        icon = "https://i.imgur.com/WVKZnEo.png"
        emoji = "<:lua:662723859593691156>"

    class OCaml:
        command = "ocaml"
        version = "OCaml (4.09.0)"
        id = 65
        icon = "https://i.imgur.com/pKLADe6.png"
        emoji = "<:ocaml:623909088597901342>"

    class Octave:
        command = "octave"
        version = "Octave (5.1.0)"
        id = 66
        icon = "https://i.imgur.com/dPwBc2g.png"
        emoji = "<:octave:623909089033846834>"

    class Pascal:
        command = "pascal"
        version = "Pascal (FPC 3.0.4)"
        id = 67
        icon = "https://i.imgur.com/KjSF3JE.png"
        emoji = "<:pascal:624678099518357504>"

    class Php:
        command = "php"
        version = "PHP (7.4.1)"
        id = 68
        icon = "https://i.imgur.com/cnnYSIE.png"
        emoji = "<:php:662723859572588564>"

    class Prolog:
        command = "prolog"
        version = "Prolog (GNU Prolog 1.4.5)"
        id = 69
        icon = "https://i.imgur.com/yQAknfK.png"
        emoji = "<:prolog:662723857878089809>"

    class Python:
        command = "python"
        version = "Python (3.8.1)"
        aliases = ["py"]
        id = 71
        icon = "https://i.imgur.com/N4RyEvG.png"
        emoji = "<:python:623909092989075468>"

    class Ruby:
        command = "ruby"
        version = "Ruby (2.7.0)"
        id = 72
        icon = "https://i.imgur.com/u9xb12N.png"
        emoji = "<:ruby:623909093471420446>"

    class Rust:
        command = "rust"
        version = "Rust (1.40.0)"
        id = 73
        icon = "https://i.imgur.com/l1TnRxU.png"
        emoji = "<:rust:623909092628496384>"

    class TypeScript:
        command = "typescript"
        aliases = ["ts"]
        version = "TypeScript (3.7.4)"
        id = 74
        icon = "https://i.imgur.com/IBjXVQv.png"
        emoji = "<:typescript:662723857643208716>"

    ids = {
        "assembly": 45,
        "bash": 46,
        "sh": 46,
        "c": 50,
        "cpp": 54,
        "c++": 54,
        "csharp": 51,
        "c#": 51,
        "lisp": 55,
        "d": 56,
        "elixir": 57,
        "erlang": 58,
        "go": 60,
        "golang": 60,
        "haskell": 61,
        "java": 62,
        "javascript": 63,
        "js": 63,
        "lua": 64,
        "ocaml": 65,
        "octave": 66,
        "pascal": 67,
        "php": 68,
        "prolog": 69,
        "python": 71,
        "py": 71,
        "ruby": 72,
        "rust": 73,
        "typescript": 74,
        "ts": 74,
    }
