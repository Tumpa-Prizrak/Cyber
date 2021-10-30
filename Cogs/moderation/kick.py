import discord
from discord.ext import commands
doc = """Выгнать человека с сервера"""
syntax = "kick <Человек> [Причина]"


class ModerationCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, man: discord.Member, *, reason: str = ""):
        await man.kick(reason=reason)
        emb = discord.Embed(title=f"\"{man.display_name}\" Был кикнут", colour=discord.colour.Color.green())
        await ctx.send(embed=emb)


def setup(client):
    client.add_cog(ModerationCommand(client))
