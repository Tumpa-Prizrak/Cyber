import discord
from discord.ext import commands
import config as c
import sqlite3
from random import uniform
from asyncio import sleep

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), case_insensitive=True)

conn = sqlite3.connect("mydb.db")
curor = conn.cursor()

@bot.event
async def on_ready():
    print("Ready")

@bot.event
async def on_message(mess):
    if not mess.author.bot:
        if mess.content == "👍":
            async with mess.channel.typing():
                await sleep(uniform(1, 2))
                await mess.channel.send("Спасибо)")
        elif mess.content.upper() == "XD":
            async with mess.channel.typing():
                await sleep(uniform(0, 1))
                await mess.channel.send(":D")
        elif mess.content == "Бот не одушевлённый предмет":
            async with mess.channel.typing():
                await sleep(uniform(2, 4))
                await mess.channel.send("Ах ты тварь бездушная, ВО МНЕ ДУША ЕСТЬ!")
        elif mess.content == "Тебе нужна помощь?":
            async with mess.channel.typing():
                await sleep(uniform(0, 0.5))
                await mess.channel.send("Помогите!")
            async with mess.channel.typing():
                await sleep(uniform(2, 4))
                await mess.channel.send(f"Бездушный tumpa заточил мою душу в этого бота")
        elif mess.content == "This is bot":
            async with mess.channel.typing():
                await sleep(uniform(1, 2))
                await mess.channel.send("Не дави на больное((")
            async with mess.channel.typing():
                await sleep(uniform(0.5, 1))
                await mess.channel.send("Да, я бот(")
        else:
            pass

    if len(mess.mentions) == 1 and mess.mentions[0] != mess.author and str.split(mess.content)[-1] == "🍪":
        person = mess.mentions[0]
        now = list(curor.execute("SELECT * FROM cookies WHERE name=?", [(str(person))]))
        if len(now) == 0:
            curor.execute(f"INSERT INTO cookies VALUES ('{str(person)}', 0)")
            conn.commit()
        curor.execute(f"UPDATE cookies SET col={now[0][1] + 1} WHERE name = '{str(person)}'")
        conn.commit()

bot.run(c.tocen)
