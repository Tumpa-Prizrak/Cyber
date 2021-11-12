import discord
from discord.ext import commands
doc = """Проверка состояния бота"""
syntax = "ping"


class OtherCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"pong! Задержка {round(self.client.latency * 1000)} мс")


def setup(client):
    client.add_cog(OtherCommand(client))
