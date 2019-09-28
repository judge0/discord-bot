
<p align="center">
  <img src="https://i.imgur.com/vKqLL6V.png" width="1024">
</p>

<h1 align="center">
Judge0Bot
</h1>
<h4 align="center">Code execution in the chat</h4>



<div align="center">
<a href="https://discord.gg/6dvxeA8">
      <img src="https://discordapp.com/api/guilds/620615182116323328/embed.png" alt="Judge0 server">
</a>
<a href="https://github.com/Rapptz/discord.py/">
      <img src="https://img.shields.io/badge/discord-py-blue.svg" alt="discord.py">
</a>
<a href="https://github.com/ambv/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style: Black">
</a>
</div>

<p align="center">
  <a href="#overview">Overview</a>
  •
  <a href="#get-to-the-bot">Get to the bot</a>
  •
  <a href="#usage">Usage</a>
  •
  <a href="#development">Development</a>
</p>

# Overview
**Judge0Bot** is a Discord bot for interacting with the [Judge0 API](https://api.judge0.com/).
It executes source code of near 20 programming languages directly in the Discord channel chat.

# Get to the bot
The bot is hosted and this means that you can use its commands from a Discord server.
Three of the ways of interacting with our bot in the Discord platform:

1. **Invite the bot in your server**.
    You can invite the bot in servers which you manage with this [invite link.](https://discordapp.com/oauth2/authorize?client_id=620609604295852033&scope=bot&permissions=388160)
1. **Use the bot from our support server**.
    You can use the bot from our Judge0 support server. Join the server [here.]()
1. **Use the bot from programming servers.**
    The bot is included in large IT related communties.
    [discord.py](https://discord.gg/r3sSKJJ), [ITBG](http://discord.gg/dRrdYQf)
    
# Usage
The bot is quite easy and straightforward for use. There is integrated
help command in the bot. Send `;help` in the chat and the bot will send helpful
information for usage.

#### Executing code
The code execution is done through sending a language command and passing the source code.
You can view all language commands after sending `;languages` in the chat.
Every language command have three use cases (Python example):

<br>

`;python print("Executing source code")`
This command will execute the passed source code and it will return an output embed which includes information like time and memory usage and output which includes standart output, standart error, compiler message and sandbox message if any.

<br>


`;python`
If a language command is send without source code it will return an useful guide how to pass the source code. There are three methods: passing source code in plain format, passing soure code in code block or passing source code in highlighted code block.

<br>

`;python -v`
If argument `-v` is passed instead of source code it will return the version of the language.

# Development
It is highly preferable if you don't run an instance of my this bot unless you want to contribute.
