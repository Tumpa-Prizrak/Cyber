import discord
import sqlite3
from discord.ext import commands
conn = sqlite3.connect("Cogs/mysqldb.db")
curor = conn.cursor()
doc = """Получить информацию о профиле"""
syntax = "profile"


class OtherCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def profile(self, ctx):
        emb = discord.Embed(title=f"Ваш профиль", color=discord.colour.Colour.dark_orange())
        joined_at = ctx.author.joined_at
        created_at = ctx.author.created_at
        roles = ""
        for i in ctx.author.roles:
            if str(i.name) != "@everyone":
                roles += f'"{i.name}"; '
        emb.set_author(name=str(ctx.author))
        emb.set_thumbnail(url=ctx.author.avatar_url)
        emb.add_field(name=f"Статус", value=str(ctx.author.status), inline=False)
        emb.add_field(name=f"Кастомный статус", value=str(ctx.author.activity), inline=False)
        emb.add_field(name=f"ID", value=str(ctx.author.id), inline=False)
        emb.add_field(name="Дата регистрации",
                      value=f"{created_at.day}.{created_at.month}.{created_at.year} {created_at.hour}:{created_at.minute}",
                      inline=False)
        emb.add_field(name="Дата вступления",
                      value=f"{joined_at.day}.{joined_at.month}.{joined_at.year} {joined_at.hour}:{joined_at.minute}",
                      inline=False)
        emb.add_field(name="Роли", value=roles, inline=False)
        await ctx.send(embed=emb)


def setup(client):
    client.add_cog(OtherCommand(client))
