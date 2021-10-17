import discord
from discord.ext import commands
import sqlite3
import config as c
import json
import requests
from random import randint, randrange
import datetime

bot = commands.Bot(command_prefix=c.BotToken, intents=discord.Intents.all(), case_insensitive=True)
bot.remove_command("help")
bot.load_extension("other")
bot.load_extension("reactions")
# slash = InteractionClient(bot)
conn = sqlite3.connect("mydb.db")
curor = conn.cursor()


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Streaming(name="!help",
        platform="Twitch", details=f"{c.BotToken}help", game="Create bot", url="https://www.twitch.tv/andrew_k9"))
    print("Ready")


@bot.command()
async def code(ctx, *, code: str):
    if ctx.author.id not in c.owners:
        return

    in_code = ""

    for i in str.split(code, "\n"):
        if i.startswith("```"):
            continue
        else:
            in_code += i
            in_code += "\n"
    
    try:
        exec(in_code)
    except Exception as e:
        await ctx.send(e)


bot.run(c.tocen)
