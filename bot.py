import discord
import requests
import json
import dotenv
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

prefix = "!"  # Choose your preferred prefix
bot = commands.Bot(command_prefix=prefix,intents=intents)



@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user.name} ({bot.user.id})")
    await bot.change_presence(activity=discord.Game('!joke'))


@bot.command()
async def joke(ctx):
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    joke = json.loads(response.text)
    await ctx.send(f"{joke['setup']}\n{joke['punchline']}")



bot.run(os.getenv('token'))
