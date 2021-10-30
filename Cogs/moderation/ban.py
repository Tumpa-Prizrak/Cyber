import discord
from discord.ext import commands
doc = """Дать Фениксу в лапы Банхаммер и указать на человека"""
syntax = "ban <Человек> [Причина]"


class ModerationCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, man: discord.Member, *, reason: str = ""):
        await man.ban(reason=reason)
        emb = discord.Embed(title=f"\"{man.display_name}\" был забанен", colour=discord.colour.Color.green())
        await ctx.send(embed=emb)


def setup(client):
    client.add_cog(ModerationCommand(client))
