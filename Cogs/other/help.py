import discord
from discord.ext import commands


class OtherCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        await ctx.send("Команда в переработке, ожидайте")


def setup(client):
    client.add_cog(OtherCommand(client))
