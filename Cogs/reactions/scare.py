import discord
from discord.ext import commands
import requests
import json
from random import randint
import config as c
doc = """Бу! Страшно?"""
syntax = "scare <Человек>"


class ReactionsCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.someShit = {
            "person": "<Человек>"
        }

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

        @baka.error
        async def Some_error(self, ctx, error):
            if isinstance(error, commands.MissingRequiredArgument):
                try:
                    emb = discord.Embed(title=f"Параметр \"{self.someShit[error.param.name]}\" пропущен",
                                        colour=discord.colour.Colour.red())
                except KeyError:
                    emb = discord.Embed(title=f"Параметр \"{error.param.name}\" пропущен",
                                        colour=discord.colour.Colour.red())

            await ctx.send(embed=emb)

    @scare.error
    async def Some_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            try:
                emb = discord.Embed(title=f"Параметр \"{self.someShit[error.param.name]}\" пропущен",
                                    colour=discord.colour.Colour.red())
            except KeyError:
                emb = discord.Embed(title=f"Параметр \"{error.param.name}\" пропущен",
                                    colour=discord.colour.Colour.red())

        await ctx.send(embed=emb)


def setup(client):
    client.add_cog(ReactionsCommand(client))
