import discord
from discord.ext import commands
import sqlite3
doc = """Кто тут у нас плохой?)"""
syntax = "warn [Человек]"
conn = sqlite3.connect("Cogs/mysqldb.db")
curor = conn.cursor()


class ModerationCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def warns(self, ctx, man: discord.Member = None):
        Pers_warns = list(curor.execute("SELECT * FROM warns WHERE person=? AND server=?", (ctx.author.id if man == None else man.id, ctx.guild.id)))
        if Pers_warns == []:
            all_warns = "\n*`Ничего`*"
        else:
            all_warns = ""
            for i in Pers_warns:
                all_warns += "\n\n"
                all_warns += "`" + i[2] + "`"
                all_warns += ";"
        embed = discord.Embed(title=f'Предупреждения \"{man.display_name if man != None else ctx.author.display_name}\": {all_warns}', colour=discord.colour.Color.green())
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(ModerationCommand(client))
