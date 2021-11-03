import discord
from discord.ext import commands
doc = """Выгнать человека с сервера"""
syntax = "kick <Человек> [Причина]"


class ModerationCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.someShit = {
            "man": "<Человек>"
        }

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, man: discord.Member, *, reason: str = ""):
        await man.kick(reason=reason)
        emb = discord.Embed(title=f"\"{man.display_name}\" Был кикнут", colour=discord.colour.Color.green())
        await ctx.send(embed=emb)

    @kick.error
    async def Some_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(title="Бро, у тебя нет прав", colour=discord.colour.Colour.red())
        elif isinstance(error, commands.MissingRequiredArgument):
            try:
                emb = discord.Embed(title=f"Параметр \"{self.someShit[error.param.name]}\" пропущен", colour=discord.colour.Colour.red())
            except KeyError:
                emb = discord.Embed(title=f"Параметр \"{error.param.name}\" пропущен", colour=discord.colour.Colour.red())

        await ctx.send(embed=emb)


def setup(client):
    client.add_cog(ModerationCommand(client))
