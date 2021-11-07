import discord
from discord.ext import commands
doc = """Дать Фениксу в лапы Банхаммер и указать на человека"""
syntax = "ban <Человек> [Причина]"


class ModerationCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.someShit = {
            "man": "<Человек>"
        }

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, man: discord.Member, *, reason: str = ""):
        if ctx.author.top_role.position <= man.top_role.position and ctx.guild.owner != ctx.author:
            raise commands.MissingPermissions
        if man == ctx.author:
            emb = discord.Embed(title="Вы не можете сделать это с собой  :sob:", colour=discord.colour.Colour.red())
            await ctx.send(embed=emb)
        await man.ban(reason=reason)
        emb = discord.Embed(title=f"\"{man.display_name}\" был забанен", colour=discord.colour.Color.green())
        await ctx.send(embed=emb)

    @ban.error
    async def Some_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(title="Бро, у тебя нет прав", colour=discord.colour.Colour.red())
            await ctx.send(embed=emb)
        elif isinstance(error, commands.MissingRequiredArgument):
            try:
                emb = discord.Embed(title=f"Параметр \"{self.someShit[error.param.name]}\" пропущен", colour=discord.colour.Colour.red())
                await ctx.send(embed=emb)
            except KeyError:
                emb = discord.Embed(title=f"Параметр \"{error.param.name}\" пропущен", colour=discord.colour.Colour.red())
                await ctx.send(embed=emb)
        elif isinstance(error, discord.Forbidden):
            emb = discord.Embed(title="Я не могу это сделать :sob:")
            await ctx.send(embed=emb)


def setup(client):
    client.add_cog(ModerationCommand(client))
