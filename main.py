import discord
from discord.ext import commands
import sqlite3
import config as c
import os

bot = commands.Bot(command_prefix=c.prefix, intents=discord.Intents.all(), case_insensitive=True)
bot.remove_command("help")
# slash = InteractionClient(bot)
conn = sqlite3.connect("Cogs/mysqldb.db")
curor = conn.cursor()

categories = []
for i in os.listdir("Cogs"):
    if i.endswith(".db") or i.endswith(".py"):
        continue
    else:
        categories.append(i)

for directory in categories:
    for file in os.listdir("Cogs/" + directory):
        try:
            if f"{directory}/{file}".endswith(".py"):
                bot.load_extension(f"Cogs.{directory}.{file[:-3]}")
                print("Load cog: " + f"Cogs.{directory}.{file[:-3]}")
        except discord.ext.commands.errors.NoEntryPointError:
            continue


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Streaming(name="!help",
            platform="Twitch",
            details=f"{c.prefix}help",
            game="Create bot",
            url="https://www.twitch.tv/andrew_k9"))
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


bot.run(c.token)
