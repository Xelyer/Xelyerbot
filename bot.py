import discord
import requests
import json
import dotenv
import os
import aiohttp
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

prefix = "!"  # Choose your preferred prefix
bot = commands.Bot(command_prefix=prefix,intents=intents)



@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user.name}")
    print(f"Bot Status Is Spiced Up ! {bot.user.name}")
    await bot.change_presence(activity=discord.Game('!joke and !search_repo <query>'))

# Joke api 

@bot.command()
async def joke(ctx: commands.Context):
    embed = discord.Embed(
        title="Joke!",
        description="Please wait! I'm generating your joke ...",
        color=discord.Color.random()
    )
    joke_msg = await ctx.send(embed=embed, content=f"{ctx.author.mention}")
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    joke = json.loads(response.text)
    new_embed = discord.Embed(
        title=f"{joke['setup']}",
        description=f"{joke['punchline']}",
        color=discord.Color.blurple()
    )
    await joke_msg.edit(embed=new_embed)
    await joke_msg.add_reaction('😂')
    await joke_msg.add_reaction('👎')

# Github Search 

@bot.command()
async def search_repo(ctx, query):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.github.com/search/repositories?q={query}') as response:
            data = await response.json()
            if 'items' in data:
                for item in data['items']:
                    name = item['name']
                    url = item['html_url']
                    description = item['description']
                    await ctx.send(f'Name: {name}\nURL: {url}\nDescription: {description}')
                    break
            else:
                await ctx.send('No repositories found.')



bot.run(os.getenv('token'))