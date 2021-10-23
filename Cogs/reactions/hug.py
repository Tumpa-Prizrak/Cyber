import discord
from discord.ext import commands
import requests
import json
from random import randint
import config as c


class ReactionsCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

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


def setup(client):
    client.add_cog(ReactionsCommand(client))
