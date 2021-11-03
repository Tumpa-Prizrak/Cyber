import discord
from discord.ext import commands
import sqlite3
doc = """Выдать придупреждение"""
syntax = "warn <Человек> <Причина>"
conn = sqlite3.connect("Cogs/mysqldb.db")
curor = conn.cursor()


class ModerationCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.someShit = {
            "man": "<Человек>",
            "reason": "<Причина>"
        }

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def warn(self, ctx, man: discord.Member, *, reason: str):
        curor.execute(f"INSERT INTO warns VALUES (?, ?, ?)", (man.id, ctx.guild.id, reason))
        conn.commit()
        embed = discord.Embed(title=f"\"{man.display_name}\" получил предупреждение", colour=discord.colour.Color.green())
        await ctx.send(embed=embed)

    @warn.error
    async def Some_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(title="Бро, у тебя нет прав", colour=discord.colour.Colour.red())
        elif isinstance(error, commands.MissingRequiredArgument):
            try:
                emb = discord.Embed(title=f"Параметр \"{self.someShit[error.param.name]}\" пропущен", colour=discord.colour.Colour.red())
            except KeyError:
                emb = discord.Embed(title=f"Параметр \"{error.param.name}\" пропущен", colour=discord.colour.Colour.red())
        else:
            emb = discord.Embed(title=str(error), colour=discord.Colour.red())

        await ctx.send(embed=emb)


def setup(client):
    client.add_cog(ModerationCommand(client))
