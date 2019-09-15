from datetime import datetime as dt
from dataclasses import dataclass

PREFIX = ':'
NEWLINES_LIMIT = 10
CHARACTERS_LIMIT = 300

START_TIME = dt.utcnow()

JUDGE0_TEAM = [365859941292048384, 512551605321596928]
JUDGE0_ICON = 'https://i.imgur.com/Nab2jCa.png'

@dataclass
class Emoji:
    total = '<:total:620744869429641236>'
    available = '<:available:620705066604560405>'
    idle = '<:idle:620702759414661120>'
    working = '<:working:620704067672342528>'
    paused = '<:paused:620704067479666688>'
    failed = '<:failed:620704067525672980>'

@dataclass
class Lang:
    bash = range(1, )
    class Bash:
        command = "bash"
        aliases = ["sh"]
        version = "Bash (4.4)"
        id = 1
        icon = "https://i.imgur.com/6BQ4g4J.png"

    class C:
        command = "c"
        version = "C (gcc 7.2.0)"
        id = 4
        icon = "https://i.imgur.com/Aoo95wm.png"

    class Cpp:
        command = 'cpp'
        version = "C++ (g++ 7.2.0)"
        id = 10
        icon = "https://i.imgur.com/CJYqkG5.png"

    class CSharp:
        command = 'csharp'
        version = "C# (mono 5.4.0.167)"
        id = 16
        icon = "https://i.imgur.com/M1AQVY2.png"

    class Clojure:
        command = 'clojure'
        version = "Clojure (1.8.0)"
        id = 18
        icon = "https://i.imgur.com/N7WspHO.png"

    class Crystal:
        command = 'crystal'
        version = "Crystal (0.23.1)"
        id = 19
        icon = "https://i.imgur.com/wT6nxjq.png"

    class Elixir:
        command = 'elixir'
        version = "Elixir (1.5.1)"
        id = 20
        icon = "https://i.imgur.com/0tigIIL.png"

    class Erlang:
        command = 'erlang'
        version = "Erlang (OTP 20.0)"
        id = 21
        icon = "https://i.imgur.com/5dVX2NF.png"

    class Go:
        command = 'go'
        version = "Go (1.9)"
        id = 22
        icon = "https://i.imgur.com/a3yrHtU.png"

    class Haskell:
        command = 'haskell'
        version = "Haskell (ghc 8.2.1)"
        id = 23
        icon = "https://i.imgur.com/NpyZ3z7.png"

    class Java:
        command = 'java'
        version = "Java (OpenJDK 8)"
        id = 27
        icon = "https://i.imgur.com/5OwBztX.png"

    class JavaScript:
        command = 'javascript'
        version = "JavaScript (nodejs 8.5.0)"
        id = 29
        icon = "https://i.imgur.com/YOsQqBF.png"

    class Python:
        command = 'python'
        version = "Python (3.6.0)"
        id = 34
        icon = "https://i.imgur.com/N4RyEvG.png"

    class Ruby:
        command = 'ruby'
        version = "Ruby (2.4.0)"
        id = 38
        icon = "https://i.imgur.com/u9xb12N.png"

    class Rust:
        command = 'rust'
        version = "Rust (1.20.0)"
        id = 42
        icon = "https://i.imgur.com/l1TnRxU.png"