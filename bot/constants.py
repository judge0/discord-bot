from datetime import datetime as dt
from dataclasses import dataclass

PREFIX = ";"
NEWLINES_LIMIT = 10
CHARACTERS_LIMIT = 300

START_TIME = dt.utcnow()

JUDGE0_GUILD = 620615182116323328
JUDGE0_JOIN_CHANNEL = 623949481167290410
JUDGE0_TEAM = [365859941292048384, 512551605321596928]
JUDGE0_ICON = "https://i.imgur.com/Nab2jCa.png"


@dataclass
class Emoji:
    class Workers:
        total = "<:total:620744869429641236>"
        available = "<:available:620705066604560405>"
        idle = "<:idle:620702759414661120>"
        working = "<:working:620704067672342528>"
        paused = "<:paused:620704067479666688>"
        failed = "<:failed:620704067525672980>"

    class Execution:
        loading = ""


@dataclass
class Lang:
    count = 19

    class Bash:
        command = "bash"
        aliases = ["sh"]
        version = "Bash (4.4)"
        id = 1
        icon = "https://i.imgur.com/6BQ4g4J.png"
        emoji = "<:bash:623909088572735498>"

    class C:
        command = "c"
        version = "C (gcc 7.2.0)"
        id = 4
        icon = "https://i.imgur.com/Aoo95wm.png"
        emoji = "<:c_:623909093136138240>"

    class Cpp:
        command = "cpp"
        version = "C++ (g++ 7.2.0)"
        id = 10
        icon = "https://i.imgur.com/CJYqkG5.png"
        emoji = "<:cpp:623909088459227149>"

    class CSharp:
        command = "csharp"
        version = "C# (mono 5.4.0.167)"
        id = 16
        icon = "https://i.imgur.com/M1AQVY2.png"
        emoji = "<:csharp:623909092402003999>"

    class Clojure:
        command = "clojure"
        version = "Clojure (1.8.0)"
        id = 18
        icon = "https://i.imgur.com/N7WspHO.png"
        emoji = "<:clojure:623909092712251396>"

    class Crystal:
        command = "crystal"
        version = "Crystal (0.23.1)"
        id = 19
        icon = "https://i.imgur.com/wT6nxjq.png"
        emoji = "<:crystal:623909088551763988>"

    class Elixir:
        command = "elixir"
        version = "Elixir (1.5.1)"
        id = 20
        icon = "https://i.imgur.com/0tigIIL.png"
        emoji = "<:elixir:623909093148590094>"

    class Erlang:
        command = "erlang"
        version = "Erlang (OTP 20.0)"
        id = 21
        icon = "https://i.imgur.com/5dVX2NF.png"
        emoji = "<:erlang:623909088782450707>"

    class Go:
        command = "go"
        version = "Go (1.9)"
        id = 22
        icon = "https://i.imgur.com/a3yrHtU.png"
        emoji = "<:golang:623909092913840128>"

    class Haskell:
        command = "haskell"
        version = "Haskell (ghc 8.2.1)"
        id = 23
        icon = "https://i.imgur.com/NpyZ3z7.png"
        emoji = "<:haskell:623909088622936065>"

    class Insect:
        command = "insect"
        version = "Insect (5.0.0)"
        id = 25
        icon = "https://i.imgur.com/VKbx9uC.png"
        emoji = "<:insect:623909088706691092>"

    class Java:
        command = "java"
        version = "Java (OpenJDK 8)"
        id = 27
        icon = "https://i.imgur.com/5OwBztX.png"
        emoji = "<:java:623909088614678544>"

    class JavaScript:
        command = "javascript"
        version = "JavaScript (nodejs 8.5.0)"
        id = 29
        icon = "https://i.imgur.com/YOsQqBF.png"
        emoji = "<:javascript:623909088727924747>"

    class OCaml:
        command = "ocaml"
        version = "OCaml (4.05.0)"
        id = 31
        icon = "https://i.imgur.com/pKLADe6.png"
        emoji = "<:ocaml:623909088597901342>"

    class Octave:
        command = "octave"
        version = "Octave (4.2.0)"
        id = 32
        icon = "https://i.imgur.com/dPwBc2g.png"
        emoji = "<:octave:623909089033846834>"

    class Pascal:
        command = "pascal"
        version = "Pascal (fpc 3.0.0)"
        id = 33
        icon = "https://i.imgur.com/U1CA0bT.png"
        emoji = "<:pascal:623909088421478402>"

    class Python:
        command = "python"
        version = "Python (3.6.0)"
        id = 34
        icon = "https://i.imgur.com/N4RyEvG.png"
        emoji = "<:python:623909092989075468>"

    class Ruby:
        command = "ruby"
        version = "Ruby (2.4.0)"
        id = 38
        icon = "https://i.imgur.com/u9xb12N.png"
        emoji = "<:ruby:623909093471420446>"

    class Rust:
        command = "rust"
        version = "Rust (1.20.0)"
        id = 42
        icon = "https://i.imgur.com/l1TnRxU.png"
        emoji = "<:rust:623909092628496384>"
