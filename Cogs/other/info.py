import discord
import sqlite3
from discord.ext import commands
conn = sqlite3.connect("../mydb.db")
curor = conn.cursor()


class OtherCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx, type_of_info, *, value):
        try:
            if type_of_info in ['name', 'balance']:
                raise TypeError(f"no such column: {type_of_info}")
            curor.execute(f"UPDATE profile SET {type_of_info}='{value}' WHERE name = '{str(ctx.author.id)}'")
            conn.commit()
            emb = discord.Embed(title="Успешно выполнено", colour=discord.colour.Colour.green())
            await ctx.send(embed=emb)
        except Exception as e:
            emb = discord.Embed(title="Проиошла ошибка", colour=discord.colour.Colour.red())
            emb.add_field(name="Ошибка", value=str(e))
            await ctx.send(embed=emb)


def setup(client):
    client.add_cog(OtherCommand(client))
