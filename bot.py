import discord
import requests
import json
import dotenv
import os
import aiohttp
import shutil
import random
import praw
import asyncio
import io

# From Cmd !
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

prefix = "!"  # Choose your preferred prefix
bot = commands.Bot(command_prefix=prefix,intents=intents)


# Bot Status !
async def status_task():
    while True:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Github.com/Xelyer"))
        await asyncio.sleep(600000)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="xelyerbot.netlify.app"))
        await asyncio.sleep(600000)
        await bot.change_presence(activity=discord.Game(name="!getstarted"))
        await asyncio.sleep(600000)


@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user.name}")
    bot.loop.create_task(status_task())

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


# Memes
@bot.command()
async def meme(ctx):
    try:
        response = requests.get("https://meme-api.com/gimme")
        response.raise_for_status()  # Raise an exception for non-2xx HTTP status codes
        json_data = response.json()
        meme_url = json_data['url']
    
        # Fetch the image from the URL
        meme_response = requests.get(meme_url)
        meme_image = io.BytesIO(meme_response.content)

        await ctx.send(ctx.message.author.mention)
        await ctx.send('This is your Meme!')
        # Send the image to the Discord channel 
        await ctx.send(file=discord.File(meme_image, 'meme.png'))
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"Error fetching meme: {e}")
        await ctx.send(ctx.message.author.mention)
        await ctx.send("Failed to fetch a meme at the moment. Please try again later.")

# Help Cmd
@bot.command()
async def getstarted(ctx):
    # Create an embed message to display the help information
    embed = discord.Embed(title="Bot Commands", description="List of available commands", color=discord.Color.blue())
    
    # Add fields for each command
    embed.add_field(name="!joke", value="Gets Jokes", inline=False)
    embed.add_field(name="!search_repo [repo_name]", value="Search a Repo on Github And Send it ", inline=False)
    embed.add_field(name="!meme", value="Gets Meme From Memeapi", inline=False)
    
    # Send the embed message to the channel
    await ctx.send(embed=embed)


bot.run(os.getenv('token'))