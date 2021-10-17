import discord
import sqlite3
from random import randint
import json
import requests
import config as c
from discord.ext import commands
conn = sqlite3.connect("mydb.db")
curor = conn.cursor()


class ReactionsCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def poke(self, ctx, person: discord.Member):
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

    @commands.command()
    async def baka(self, ctx, person: discord.Member):
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

    @commands.command()
    async def tickle(self, ctx, person: discord.Member):
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

    @commands.command()
    async def cuddle(self, ctx, person: discord.Member):
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

    @commands.command()
    async def kiss(self, ctx, person: discord.Member):
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

    @commands.command()
    async def spank(self, ctx, person: discord.Member):
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

    @commands.command()
    async def hug(self, ctx, person: discord.Member):
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

    @commands.command()
    async def slap(self, ctx, person: discord.Member):
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

    @commands.command()
    async def pat(self, ctx, person: discord.Member):
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

    @commands.command()
    async def lick(self, ctx, person: discord.Member):
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

    @commands.command()
    async def five(self, ctx, person: discord.Member):
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

    @commands.command()
    async def bite(self, ctx, person: discord.Member):
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

    @commands.command()
    async def kill(self, ctx, person: discord.Member):
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

    @commands.command()
    async def feed(self, ctx, person: discord.Member):
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

    @commands.command()
    async def scare(self, ctx, person: discord.Member):
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

    @commands.command()
    async def hit(self, ctx, person: discord.Member):
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

    @commands.command()
    async def bangHead(self, ctx):
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

    @commands.command()
    async def innocent(self, ctx):
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

    @commands.command()
    async def cry(self, ctx):
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

    @commands.command()
    async def blush(self, ctx):
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

    @commands.command()
    async def sleep(self, ctx):
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

    @commands.command()
    async def dance(self, ctx):
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

    @commands.command()
    async def flip(self, ctx):
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

    @commands.command()
    async def suicide(self, ctx):
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

    @commands.command()
    async def coffee(self, ctx, person: discord.Member = None):
        r = requests.get(f"https://g.tenor.com/v1/search?q=anime drink coffee&key={c.apikey}&limit={str(c.limit)}")

        if r:
            emb = discord.Embed(
                title=f"{ctx.author.name} пьёт кофе" if person == None else f"{ctx.author.name} пьёт кофе с {person.display_name}",
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

    @commands.command()
    async def tea(self, ctx, person: discord.Member = None):
        r = requests.get(f"https://g.tenor.com/v1/search?q=anime drink tea&key={c.apikey}&limit={str(c.limit)}")

        if r:
            emb = discord.Embed(
                title=f"{ctx.author.name} пьёт чай" if person == None else f"{ctx.author.name} пьёт чай с {person.display_name}",
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

    @commands.command()
    async def alcohol(self, ctx, person: discord.Member = None):
        r = requests.get(f"https://g.tenor.com/v1/search?q=anime drink alcohol&key={c.apikey}&limit={str(c.limit)}")

        if r:
            emb = discord.Embed(
                title=f"{ctx.author.name} бухает" if person == None else f"{ctx.author.name} бухает с {person.display_name}",
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

    @commands.command()
    async def walk(self, ctx, person: discord.Member = None):
        r = requests.get(f"https://g.tenor.com/v1/search?q=anime walk&key={c.apikey}&limit={str(c.limit)}")

        if r:
            emb = discord.Embed(
                title=f"{ctx.author.name} гуляет" if person == None else f"{ctx.author.name} гуляет с {person.display_name}",
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


def setup(client):
    client.add_cog(ReactionsCommand(client))
