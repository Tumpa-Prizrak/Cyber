import discord
from discord import colour
from discord.ext import commands
import sqlite3
import config as c
import json
import requests
from random import randint, randrange
import datetime

bot = commands.Bot(command_prefix=c.BotToken, intents=discord.Intents.all(), case_insensitive=True)
bot.remove_command("help")
# slash = InteractionClient(bot)
conn = sqlite3.connect("mydb.db")
curor = conn.cursor()
helpCommands = {}
namesHelpCommands = []


class UserCommand:
    def __init__(self, name, desc) -> None:
        self.name = name
        self.desc = desc
    
    def __str__(self) -> str:
        return self.name


def CommandToHelp(func, desc, categ):
    try:
        helpCommands[categ]
    except KeyError:
        helpCommands.update({categ: []})
    finally:
        userFunc = UserCommand(func.name.lower(), desc)
        namesHelpCommands.append(userFunc.name + "-" + categ)
        helpCommands[categ].append(userFunc)
        swapped = True
        while swapped:
            swapped = False
            for i in range(len(helpCommands[categ]) - 1):
                if helpCommands[categ][i].name > helpCommands[categ][i + 1].name:
                    helpCommands[categ][i], helpCommands[categ][i + 1] = helpCommands[categ][i + 1], helpCommands[categ][i]
                    swapped = True


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Streaming(name="!help",
        platform="Twitch", details=f"{c.BotToken}help", game="Create bot", url="https://www.twitch.tv/andrew_k9"))
    print("Ready")


@bot.command()
async def ping(ctx):
    await ctx.send("pong")
CommandToHelp(ping, "Возвращает pong", "Другое:")


@bot.command()
async def zooy(ctx):
    emb = discord.Embed(title="Магазин\n:cat2: - магазин петиков", colour=discord.colour.Colour.green())
    msg = await ctx.send(embed=emb)
    await msg.add_reaction("🐈")

    def check(reaction, user):
        if user == ctx.author:
            return True
        else:
            return False

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction) == "🐈":
        await msg.clear_reactions()
        emb = discord.Embed(title="Выберите пета, которого хотите купить:\n:cat2: - Кот",
                            colour=discord.colour.Colour.orange())
        await msg.edit(embed=emb)
        await msg.add_reaction("🐈")

        def pet(reaction, user):
            if user == ctx.author:
                return True
            else:
                return False

        reaction, user = await bot.wait_for('reaction_add', check=pet)

        await ctx.send("Введите имя пета")

        def waitname(m):
            return m.author == ctx.author

        msg = await bot.wait_for('message', check=waitname)

        name = msg.content

        curor.execute(f"INSERT INTO pets VALUES ('кот', '{name}', '{str(ctx.author.id)}')")
        conn.commit()

        await ctx.send(f"Вы купили {reaction} с именем \"{name}\"")
CommandToHelp(zooy, "Зоомагазин", "Петы:")


@bot.command()
async def pets(ctx):
    out = []
    sql = f"SELECT * FROM pets WHERE Discor=? ORDER BY name"
    for i in curor.execute(sql, [(str(ctx.author.id))]):
        out.append(i)
    if len(out) > 0:
        emb = discord.Embed(title="Твои петы", colour=discord.colour.Colour.dark_orange())
        for i in out:
            emb.add_field(name=f"Твой {i[0]}", value=f"Имя: {i[1]}")
    else:
        emb = discord.Embed(title="У тебя нет петов", colour=discord.colour.Colour.dark_red())
    await ctx.send(embed=emb)
CommandToHelp(pets, "Список петов", "Петы:")


@bot.command()
async def profile(ctx):
    bal = list(curor.execute("SELECT * FROM balance WHERE name=?", [(str(ctx.author.id))]))
    cookies = list(curor.execute("SELECT * FROM cookies WHERE name=?", [(str(ctx.author.id))]))
    emb = discord.Embed(title=f"Ваш профиль", color=discord.colour.Colour.dark_orange())
    joined_at = ctx.author.joined_at
    created_at = ctx.author.created_at
    roles = ""
    for i in ctx.author.roles:
        if str(i.name) != "@everyone":
            roles += f'"{i.name}"; '
    if len(bal) == 0:
        curor.execute(f"INSERT INTO balance VALUES ('{str(ctx.author.id)}', 0, null, null, null, null)")
        conn.commit()
        bal = list(curor.execute("SELECT * FROM balance WHERE name=?", [(str(ctx.author.id))]))
    try:
        emb.set_author(name=str(ctx.author.id) + f" | 🍪: {cookies[0][1]}")
    except IndexError:
        emb.set_author(name=str(ctx.author))
    emb.set_thumbnail(url=ctx.author.avatar_url)
    emb.add_field(name=f"Статус", value=str(ctx.author.status), inline=False)
    emb.add_field(name=f"Кастомный статус", value=str(ctx.author.activity), inline=False)
    emb.add_field(name=f"Валюта", value=str(bal[0][1]), inline=False)
    emb.add_field(name=f"ID", value=str(ctx.author.id), inline=False)
    emb.add_field(name="Дата регистрации",
                  value=f"{created_at.day}.{created_at.month}.{created_at.year} {created_at.hour}:{created_at.minute}",
                  inline=False)
    emb.add_field(name="Дата вступления",
                  value=f"{joined_at.day}.{joined_at.month}.{joined_at.year} {joined_at.hour}:{joined_at.minute}",
                  inline=False)
    emb.add_field(name="О себе", value=bal[0][2] if bal[0][2] != None else "*Ничто не сказано*", inline=False)
    emb.add_field(name="Роли", value=roles, inline=False)
    await ctx.send(embed=emb)
CommandToHelp(profile, "Профиль", "Другое:")


@bot.command()
async def info(ctx, type_of_info, *, value):
    try:
        if type_of_info in ['name', 'balance']:
            raise TypeError(f"no such column: {type_of_info}")
        curor.execute(f"UPDATE profile SET {type_of_info}='{value}' WHERE name = '{str(ctx.author.id)}'")
        conn.commit()
        emb = discord.Embed(title="Успешно выполнено", colour=discord.colour.Colour.green())
        await ctx.send(embed=emb)
    except Exception as e:
        emb = discord.Embed(title="Проиошла ошибка", colour=discord.colour.Colour.red())
        emb.add_field(name="Ошибка", value=str(e))
        await ctx.send(embed=emb)
CommandToHelp(info, "Установить информацию о вас", "Другое:")


@bot.command()
async def poke(ctx, person: discord.Member):
    if ctx.author == person:
        return

    r = requests.get(f"https://g.tenor.com/v1/search?q=anime poke&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} тыкнул в {person.name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(poke, "Тыкнуть в <user>", "Реакции:")


@bot.command()
async def baka(ctx, person: discord.Member):
    if ctx.author == person:
        return

    r = requests.get(f"https://g.tenor.com/v1/search?q=anime baka&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} ругает {person.name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(baka, "Ругать <user>", "Реакции:")


@bot.command()
async def tickle(ctx, person: discord.Member):
    if ctx.author == person:
        return

    r = requests.get(f"https://g.tenor.com/v1/search?q=anime tickle&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} щекочет {person.name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(tickle, "Щекотать <user>", "Реакции:")


@bot.command()
async def cuddle(ctx, person: discord.Member):
    if ctx.author == person:
        return

    r = requests.get(f"https://g.tenor.com/v1/search?q=anime cuddlele&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} прижался к {person.name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(cuddle, "Прижаться к <user>", "Реакции:")


@bot.command()
async def kiss(ctx, person: discord.Member):
    if ctx.author == person:
        return

    r = requests.get(f"https://g.tenor.com/v1/search?q=anime kiss&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} поцеловал {person.name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(kiss, "Поцеловать <user>", "Реакции:")


@bot.command()
async def spank(ctx, person: discord.Member):
    if ctx.author == person:
        return

    r = requests.get(f"https://g.tenor.com/v1/search?q=anime spank&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} ударил {person.name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)


@bot.command()
async def hug(ctx, person: discord.Member):
    if ctx.author == person:
        return

    r = requests.get(f"https://g.tenor.com/v1/search?q=anime hug&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} обнял {person.name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(hug, "Обнять <user>", "Реакции:")


@bot.command()
async def slap(ctx, person: discord.Member):
    if ctx.author == person:
        return

    r = requests.get(f"https://g.tenor.com/v1/search?q=anime slap&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} дал пощёчину {person.name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(slap, "дать пощёчину <user>", "Реакции:")


@bot.command()
async def pat(ctx, person: discord.Member):
    if ctx.author == person:
        return

    r = requests.get(f"https://g.tenor.com/v1/search?q=anime pat&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} погладил {person.name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(pat, "Погладить <user>", "Реакции:")


@bot.command()
async def lick(ctx, person: discord.Member):
    if ctx.author == person:
        return

    r = requests.get(f"https://g.tenor.com/v1/search?q=anime lick&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} лизнул {person.name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(lick, "Лизнуть <user>", "Реакции:")


@bot.command()
async def five(ctx, person: discord.Member):
    if ctx.author == person:
        return

    r = requests.get(f"https://g.tenor.com/v1/search?q=anime high five&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} дал пять {person.name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(five, "Дать пять <user>", "Реакции:")


@bot.command()
async def bite(ctx, person: discord.Member):
    if ctx.author == person:
        return

    r = requests.get(f"https://g.tenor.com/v1/search?q=anime bite&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} укусил {person.name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(bite, "Укусить <user>", "Реакции:")


@bot.command()
async def kill(ctx, person: discord.Member):
    if ctx.author == person:
        return

    r = requests.get(f"https://g.tenor.com/v1/search?q=anime kill&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} убил {person.name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(kill, "Убить <user>", "Реакции:")


@bot.command()
async def feed(ctx, person: discord.Member):
    if ctx.author == person:
        return

    r = requests.get(f"https://g.tenor.com/v1/search?q=anime feed&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} покормил {person.name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    now = list(curor.execute("SELECT * FROM cookies WHERE name=?", [(str(person))]))
    if len(now) == 0:
        curor.execute(f"INSERT INTO cookies VALUES ('{str(person.id)}', 0)")
        conn.commit()
    curor.execute(f"UPDATE cookies SET col={now[0][1] + 1} WHERE name = '{str(person)}'")
    conn.commit()

    await ctx.send(embed=emb)
CommandToHelp(feed, "Покормить <user>", "Реакции:")


@bot.command()
async def scare(ctx, person: discord.Member):
    if ctx.author == person:
        return

    r = requests.get(f"https://g.tenor.com/v1/search?q=anime scare&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} напугал {person.name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(scare, "Напугать <user>", "Реакции:")


@bot.command()
async def hit(ctx, person: discord.Member):
    if ctx.author == person:
        return

    r = requests.get(f"https://g.tenor.com/v1/search?q=anime hit&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} ударил {person.name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(hit, "Ударить <user>", "Реакции:")


@bot.command()
async def bangHead(ctx):
    r = requests.get(f"https://g.tenor.com/v1/search?q=anime bang head&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} бьётся головой о стену",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(bangHead, "Биться головой об стену", "Реакции:")


@bot.command()
async def innocent(ctx):
    r = requests.get(f"https://g.tenor.com/v1/search?q=anime innocent&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} оправдываться",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(innocent, "Оправдываться", "Реакции:")


@bot.command()
async def cry(ctx):
    r = requests.get(f"https://g.tenor.com/v1/search?q=anime cry&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} плачет",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(cry, "Плакать", "Реакции:")


@bot.command()
async def blush(ctx):
    r = requests.get(f"https://g.tenor.com/v1/search?q=anime blush&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} краснеет",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(blush, "Краснеть", "Реакции:")


@bot.command()
async def sleep(ctx):
    r = requests.get(f"https://g.tenor.com/v1/search?q=anime sleep&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} спит",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(sleep, "Спать", "Реакции:")


@bot.command()
async def dance(ctx):
    r = requests.get(f"https://g.tenor.com/v1/search?q=anime dance&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} танцует",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(dance, "Танцевать", "Реакции:")


@bot.command()
async def flip(ctx):
    r = requests.get(f"https://g.tenor.com/v1/search?q=anime table flip&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} опрокидывает стол",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(flip, "Опрокинуть стол", "Реакции:")


@bot.command()
async def suicide(ctx):
    r = requests.get(f"https://g.tenor.com/v1/search?q=anime suicide&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} откинулся",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(suicide, "Убить себя(осуждаю)", "Реакции:")


@bot.command()
async def coffee(ctx, person: discord.Member = None):
    r = requests.get(f"https://g.tenor.com/v1/search?q=anime drink coffee&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} пьёт кофе" if person == None else f"{ctx.author.name} пьёт кофе с {person.display_name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(coffee, "Пить кофе [user]", "Реакции:")


@bot.command()
async def tea(ctx, person: discord.Member = None):
    r = requests.get(f"https://g.tenor.com/v1/search?q=anime drink tea&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} пьёт чай" if person == None else f"{ctx.author.name} пьёт чай с {person.display_name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(tea, "Пить чай [user]", "Реакции:")


@bot.command()
async def alcohol(ctx, person: discord.Member = None):
    r = requests.get(f"https://g.tenor.com/v1/search?q=anime drink alcohol&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} бухает" if person == None else f"{ctx.author.name} бухает с {person.display_name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(alcohol, "Бухать [user]", "Реакции:")


@bot.command()
async def walk(ctx, person: discord.Member = None):
    r = requests.get(f"https://g.tenor.com/v1/search?q=anime walk&key={c.apikey}&limit={str(c.limit)}")

    if r:
        emb = discord.Embed(title=f"{ctx.author.name} гуляет" if person == None else f"{ctx.author.name} гуляет с {person.display_name}",
                            colour=discord.colour.Colour.green())
        while True:
            try:
                emb.set_image(url=json.loads(r.content)["results"][randint(0, c.limit)]["media"][0]['gif']['url'])
                break
            except IndexError:
                continue
    else:
        emb = discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r.status_code}",
                            colour=discord.colour.Colour.red())

    await ctx.send(embed=emb)
CommandToHelp(walk, "Гулять [user]", "Реакции:")


@bot.command()
async def work(ctx):
    try:
        lastWork = datetime.datetime.strptime(list(curor.execute("SELECT lastWork FROM balance WHERE name=?", [529302484901036043]))[0][0], '%Y-%m-%d %H:%M:%S.%f')
    except TypeError:
        lastWork = None
    if lastWork == None or lastWork + datetime.timedelta(minutes=30) < datetime.datetime.now():
        try:
            nowBal = list(curor.execute("SELECT * FROM balance WHERE name=?", [(str(ctx.author.id))]))[0][1]
        except IndexError:
            nowBal = 0
            curor.execute(f"INSERT INTO balance VALUES ('{str(ctx.author.id)}', 0, null, null, null, null)")
        addBal = randrange(10, 1001, 10)
        curor.execute(f"UPDATE balance SET bal={nowBal + addBal} WHERE name = '{str(ctx.author.id)}'")
        curor.execute(f"UPDATE balance SET lastWork=? WHERE name=?", [datetime.datetime.now(), str(ctx.author.id)])
        conn.commit()
        emb = discord.Embed(title="Работа", colour=discord.colour.Colour.green())
        emb.add_field(name="Ты получил(а)", value=str(addBal) + "$", inline=False)
        emb.add_field(name="У тебя", value=str(nowBal + addBal) + "$", inline=False)
        await ctx.send(embed=emb)
    else:
        normal_datetime = lastWork.strftime("%A %H:%M")
        normal_next_datetime = lastWork + datetime.timedelta(minutes=30)
        emb = discord.Embed(title="Ошибка", colour=colour.Color.red())
        emb.add_field(name=f"Ещё не прошло 30 минут с {normal_datetime}", value=f'В следующий раз вы можете использовать эту команду в {normal_next_datetime.strftime("%A %H:%M")}')
        await ctx.send(embed=emb)
CommandToHelp(work, "Работать", "Экономика:")


@bot.command()
async def daily(ctx):
    try:
        lastDaily = datetime.datetime.strptime(list(curor.execute("SELECT lastDaily FROM balance WHERE name=?", [529302484901036043]))[0][0], '%Y-%m-%d %H:%M:%S.%f')
    except TypeError:
        lastDaily = None
    if lastDaily == None or lastDaily + datetime.timedelta(days=1) < datetime.datetime.now():
        try:
            nowBal = list(curor.execute("SELECT * FROM balance WHERE name=?", [(str(ctx.author.id))]))[0][1]
        except IndexError:
            nowBal = 0
            curor.execute(f"INSERT INTO balance VALUES ('{str(ctx.author.id)}', 0, null, null, null, null)")
        addBal = 500
        curor.execute(f"UPDATE balance SET bal={nowBal + addBal} WHERE name = '{str(ctx.author.id)}'")
        curor.execute(f"UPDATE balance SET lastDaily=? WHERE name=?", [datetime.datetime.now(), str(ctx.author.id)])
        conn.commit()
        emb = discord.Embed(title="Дневной доход", colour=discord.colour.Colour.green())
        emb.add_field(name="Ты получил(а)", value=str(addBal) + "$", inline=False)
        emb.add_field(name="У тебя", value=str(nowBal + addBal) + "$", inline=False)
        await ctx.send(embed=emb)
    else:
        normal_datetime = lastDaily.strftime("%A %H:%M")
        normal_next_datetime = lastDaily + datetime.timedelta(days=1)
        emb = discord.Embed(title="Ошибка", colour=colour.Color.red())
        emb.add_field(name=f"Ещё не прошло 1 день с {normal_datetime}", value=f'В следующий раз вы можете использовать эту команду в {normal_next_datetime.strftime("%A %H:%M")}')
        await ctx.send(embed=emb)
CommandToHelp(daily, "Ежедневный доход", "Экономика:")


@bot.command()
async def weekly(ctx):
    try:
        lastDaily = datetime.datetime.strptime(list(curor.execute("SELECT lastWeekly FROM balance WHERE name=?", [529302484901036043]))[0][0], '%Y-%m-%d %H:%M:%S.%f')
    except TypeError:
        lastDaily = None
    if lastDaily == None or lastDaily + datetime.timedelta(days=7) < datetime.datetime.now():
        try:
            nowBal = list(curor.execute("SELECT * FROM balance WHERE name=?", [(str(ctx.author.id))]))[0][1]
        except IndexError:
            nowBal = 0
            curor.execute(f"INSERT INTO balance VALUES ('{str(ctx.author.id)}', 0, null, null, null, null)")
        addBal = 3000
        curor.execute(f"UPDATE balance SET bal={nowBal + addBal} WHERE name = '{str(ctx.author.id)}'")
        curor.execute(f"UPDATE balance SET lastWeekly=? WHERE name=?", [datetime.datetime.now(), str(ctx.author.id)])
        conn.commit()
        emb = discord.Embed(title="Недельный доход", colour=discord.colour.Colour.green())
        emb.add_field(name="Ты получил(а)", value=str(addBal) + "$", inline=False)
        emb.add_field(name="У тебя", value=str(nowBal + addBal) + "$", inline=False)
        await ctx.send(embed=emb)
    else:
        normal_datetime = lastDaily.strftime("%A %H:%M")
        normal_next_datetime = lastDaily + datetime.timedelta(days=7)
        emb = discord.Embed(title="Ошибка", colour=colour.Color.red())
        emb.add_field(name=f"Ещё не прошло 1 неделя с {normal_datetime}", value=f'В следующий раз вы можете использовать эту команду в {normal_next_datetime.strftime("%A %H:%M")}')
        await ctx.send(embed=emb)
CommandToHelp(weekly, "Недельный доход", "Экономика:")


@bot.command()
async def crime(ctx):
    try:
        lastDaily = datetime.datetime.strptime(list(curor.execute("SELECT lastCrime FROM balance WHERE name=?", [529302484901036043]))[0][0], '%Y-%m-%d %H:%M:%S.%f')
    except TypeError:
        lastDaily = None
    if lastDaily == None or lastDaily + datetime.timedelta(hours=1) < datetime.datetime.now():
        try:
            nowBal = list(curor.execute("SELECT * FROM balance WHERE name=?", [(str(ctx.author.id))]))[0][1]
        except IndexError:
            nowBal = 0
            curor.execute(f"INSERT INTO balance VALUES ('{str(ctx.author.id)}', 0, null, null, null, null)")
        addBal = randrange(1000, 10001, 100)
        if randint(0, 1) != 0:
            curor.execute(f"UPDATE balance SET bal={nowBal + addBal} WHERE name = '{str(ctx.author.id)}'")
            emb = discord.Embed(title="Преступление", colour=discord.colour.Colour.green())
            emb.add_field(name="Ты получил(а)", value=str(addBal) + "$", inline=False)
            emb.add_field(name="У тебя", value=str(nowBal + addBal) + "$", inline=False)
            await ctx.send(embed=emb)
        else:
            curor.execute(f"UPDATE balance SET bal={nowBal - nowBal // randint(2, 10)} WHERE name = '{str(ctx.author.id)}'")
            emb = discord.Embed(title="Преступление", colour=discord.colour.Colour.red())
            emb.add_field(name="У тебя забрали", value=str(addBal) + "$", inline=False)
            emb.add_field(name="У тебя", value=str(nowBal + addBal) + "$", inline=False)
            await ctx.send(embed=emb)
        curor.execute(f"UPDATE balance SET lastCrime=? WHERE name=?", [datetime.datetime.now(), str(ctx.author.id)])
        conn.commit()
    else:
        normal_datetime = lastDaily.strftime("%A %H:%M")
        normal_next_datetime = lastDaily + datetime.timedelta(hours=1)
        emb = discord.Embed(title="Ошибка", colour=colour.Color.red())
        emb.add_field(name=f"Ещё не прошло 1 час с {normal_datetime}", value=f'В следующий раз вы можете использовать эту команду в {normal_next_datetime.strftime("%A %H:%M")}')
        await ctx.send(embed=emb)
CommandToHelp(crime, "Совершить преступление", "Экономика:")


@bot.command()
async def help(ctx, comm: str = None):
    if comm == None:
        emb = discord.Embed(title="Команды: ", colour=discord.colour.Colour.green())
        categories = helpCommands.keys()
        for category in categories:
            try:
                category_commands = ""
                for i in [i.name for i in helpCommands[category]][:-1]:
                    category_commands += i + ", "
                category_commands += [i.name for i in helpCommands[category]][0]
                emb.add_field(name=f"{category}", value=f"{category_commands}", inline=False)
            except Exception as e:
                emb.add_field(name=f"{category}", value=f"Error: {e}", inline=False)
    else:
        if comm in [str.split(i, "-")[0] for i in namesHelpCommands]:
            Thiscommand = namesHelpCommands[[str.split(i, "-")[0] for i in namesHelpCommands].index(comm)]
            Thiscommand = helpCommands[str.split(Thiscommand, "-")[1]]
            for i in Thiscommand:
                if i.name == comm:
                    Thiscommand = i
            emb = discord.Embed(title=f"Команда {comm}", colour=discord.colour.Colour.green())
            emb.add_field(name=Thiscommand.name, value=Thiscommand.desc)
        else:
            emb = discord.Embed(title="Такой команды не существует", colour=discord.colour.Colour.red())
    await ctx.send(embed=emb)
CommandToHelp(help, "Помощь по командам", "Другое:")


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


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, man: discord.Member, *, reason: str = ""):
    await man.kick(reason=reason)
    emb = discord.Embed(title=f"\"{man.display_name}\" Был кикнут", colour=discord.colour.Color.green())
    await ctx.send(embed=emb)
CommandToHelp(kick, "Кикнуть [user]", "Модерирование:")


@bot.command()
@commands.has_permissions(kick_members=True)
async def ban(ctx, man: discord.Member, *, reason: str = ""):
    await man.ban(reason=reason)
    emb = discord.Embed(title=f"\"{man.display_name}\" был забанен", colour=discord.colour.Color.green())
    await ctx.send(embed=emb)
CommandToHelp(ban, "Забанить [user]", "Модерирование:")


bot.run(c.tocen)
