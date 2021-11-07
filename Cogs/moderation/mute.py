import discord
from discord.ext import commands
import sqlite3
doc = """Замолчи!!!"""
syntax = "mute <Человек> <Причина>"
conn = sqlite3.connect("Cogs/mysqldb.db")
curor = conn.cursor()


class ModerationCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.someShit = {
            "man": "<Человек>"
        }

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, man: discord.Member):
        if ctx.author.top_role.position <= man.top_role.position and ctx.guild.owner != ctx.author:
            raise commands.MissingPermissions
        curor.execute(f"INSERT INTO warns VALUES (?, ?)", (man.id, ctx.guild.id))
        conn.commit()
        embed = discord.Embed(title=f"\"{man.mention}\" был замьючен",
                              colour=discord.colour.Color.green())
        await ctx.send(embed=embed)

    @mute.error
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
        else:
            emb = discord.Embed(title=str(error), colour=discord.Colour.red())
            await ctx.send(embed=emb)


def setup(client):
    client.add_cog(ModerationCommand(client))
