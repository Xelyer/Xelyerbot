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



bot.run(os.getenv('token'))
