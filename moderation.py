import discord
from discord.ext import commands


class ModerationCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, man: discord.Member, *, reason: str = ""):
        await man.kick(reason=reason)
        emb = discord.Embed(title=f"\"{man.display_name}\" Был кикнут", colour=discord.colour.Color.green())
        await ctx.send(embed=emb)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, man: discord.Member, *, reason: str = ""):
        await man.ban(reason=reason)
        emb = discord.Embed(title=f"\"{man.display_name}\" был забанен", colour=discord.colour.Color.green())
        await ctx.send(embed=emb)


def setup(client):
    client.add_cog(ModerationCommand(client))
