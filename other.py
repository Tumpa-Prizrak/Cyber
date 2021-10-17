import discord
import sqlite3
from discord.ext import commands
conn = sqlite3.connect("mydb.db")
curor = conn.cursor()


class OtherCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        await ctx.send("Команда в переработке, ожидайте")

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

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command()
    async def profile(ctx):
        bal = list(curor.execute("SELECT * FROM balance WHERE name=?", [(str(ctx.author.id))]))
        cookies = list(curor.execute("SELECT * FROM cookies WHERE name=?", [(str(ctx.author.id))]))
        emb = discord.Embed(title=f"Ваш профиль", color=discord.colour.Colour.dark_orange())
        joined_at = ctx.author.joined_at
        created_at = ctx.author.created_at
        roles = ""
        for i in ctx.author.roles:
            if str(i.name) != "@everyone":
                roles += f'"{i.name}"; '
        if len(bal) == 0:
            curor.execute(f"INSERT INTO balance VALUES ('{str(ctx.author.id)}', 0, null, null, null, null)")
            conn.commit()
            bal = list(curor.execute("SELECT * FROM balance WHERE name=?", [(str(ctx.author.id))]))
        try:
            emb.set_author(name=str(ctx.author.id) + f" | 🍪: {cookies[0][1]}")
        except IndexError:
            emb.set_author(name=str(ctx.author))
        emb.set_thumbnail(url=ctx.author.avatar_url)
        emb.add_field(name=f"Статус", value=str(ctx.author.status), inline=False)
        emb.add_field(name=f"Кастомный статус", value=str(ctx.author.activity), inline=False)
        emb.add_field(name=f"Валюта", value=str(bal[0][1]), inline=False)
        emb.add_field(name=f"ID", value=str(ctx.author.id), inline=False)
        emb.add_field(name="Дата регистрации",
                      value=f"{created_at.day}.{created_at.month}.{created_at.year} {created_at.hour}:{created_at.minute}",
                      inline=False)
        emb.add_field(name="Дата вступления",
                      value=f"{joined_at.day}.{joined_at.month}.{joined_at.year} {joined_at.hour}:{joined_at.minute}",
                      inline=False)
        emb.add_field(name="О себе", value=bal[0][2] if bal[0][2] != None else "*Ничто не сказано*", inline=False)
        emb.add_field(name="Роли", value=roles, inline=False)
        await ctx.send(embed=emb)


def setup(client):
    client.add_cog(OtherCommand(client))
