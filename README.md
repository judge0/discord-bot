
<p align="center">
  <img src="https://i.imgur.com/vKqLL6V.png" width="1024">
</p>

<h1 align="center">
Judge0Bot
</h1>
<h4 align="center">Code execution in Discord chat</h4>



<div align="center">
<a href="https://github.com/Rapptz/discord.py/">
      <img src="https://img.shields.io/badge/discord-py-blue.svg" alt="discord.py">
</a>
<a>
    <img src="https://img.shields.io/github/v/tag/judge0/discord-bot" alt="Version">
</a>
<a href="https://github.com/ambv/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style: Black">
</a>
<a href="https://discord.gg/6dvxeA8">
      <img src="https://discordapp.com/api/guilds/620615182116323328/embed.png" alt="Judge0 server">
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
It executes code from nearly 20 programming languages directly in your Discord server.

# Get to the bot
The bot is hosted and this means that you can use its commands in  a Discord server.
There are three ways of interacting with our bot on Discord:

1. **Add the bot to your own server**.
    You can add the bot to servers where you have the Manage Server permmision with [this link.](https://discordapp.com/oauth2/authorize?client_id=620609604295852033&scope=bot&permissions=388160)
1. **Use the bot in our support server**.
    You can use the bot in the Judge0 support server. Join the server [here.](https://discord.gg/6dvxeA8)
1. **Use the bot in major programming servers.**
    The bot is included in large IT related communties like [discord.py](https://discord.gg/r3sSKJJ) and [ITBG](http://discord.gg/dRrdYQf)!
    
# Usage
The bot is quite easy to use. Send `;help` in the chat and the bot will give you helpful information for usage.

#### Executing code
Code execution is done through sending a language command with the code you want to execute.
You can view all supported languages by sending `;languages` in the chat.
Every language command has three use cases (Python is used here as an example):

<br>

`;python print("Executing source code")`
<p align="left">
  <img src="https://i.imgur.com/Enafvtn.png" width="256">
</p>

This command executes the code provided andreturns an embed which includes information like the time it took to execute, memory usage and the code's output including standart output, standart error, compiler messages and sandbox messages (if any).

<br>

`;python`
<p align="left">
  <img src="https://i.imgur.com/4zW9yd1.png" width="256">
</p>


If a language command is sebt without any code it will return an useful guide on how to pass the code. There are three methods: passing the code in plain text, passing the code in a code block or passing the code in a highlighted code block.

<br>

`;python -v`
<p align="left">
  <img src="https://i.imgur.com/881hbFc.png" width="256">
</p>


If `-v` is passed instead of source code it will return the version of the language Judge0 is using.

# Development
*It is highly prefered if you don't run an instance of this bot unless you want to contribute.*

The installation and running steps are as follows:

1. **Make sure to get git and Python 3.6 or higher**

This is required to clone the repository and run the bot.

2. **Clone the repository**

`git clone https://github.com/judge0/discord-bot.git`

3. **Go to the directory**

`cd discord-bot`

4. **Install Pipenv**

`python -m pip install pipenv`

5. **Install the required dependencies**

`pipenv install --dev`

6. **Run the bot**

Set the bot token as enviorment variable (**BOT_TOKEN**):
Set the Rapid API auth key as enviorment variable (**AUTH_KEY**):
Get your auth key from here: [Judge0 Rapid API](https://rapidapi.com/hermanzdosilovic/api/judge0)

`pipenv run start`
