import discord
import sqlite3
import datetime
from discord import colour
from discord.ext import commands
from random import randrange, randint
conn = sqlite3.connect("../mydb.db")
curor = conn.cursor()


class EconomyCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def crime(self, ctx):
        try:
            lastDaily = datetime.datetime.strptime(
                list(curor.execute("SELECT lastCrime FROM balance WHERE name=?", [529302484901036043]))[0][0],
                '%Y-%m-%d %H:%M:%S.%f')
        except TypeError:
            lastDaily = None
        if lastDaily == None or lastDaily + datetime.timedelta(hours=1) < datetime.datetime.now():
            try:
                nowBal = list(curor.execute("SELECT * FROM balance WHERE name=?", [(str(ctx.author.id))]))[0][1]
            except IndexError:
                nowBal = 0
                curor.execute(f"INSERT INTO balance VALUES ('{str(ctx.author.id)}', 0, null, null, null, null)")
            addBal = randrange(1000, 10001, 100)
            if randint(0, 1) != 0:
                curor.execute(f"UPDATE balance SET bal={nowBal + addBal} WHERE name = '{str(ctx.author.id)}'")
                emb = discord.Embed(title="Преступление", colour=discord.colour.Colour.green())
                emb.add_field(name="Ты получил(а)", value=str(addBal) + "$", inline=False)
                emb.add_field(name="У тебя", value=str(nowBal + addBal) + "$", inline=False)
                await ctx.send(embed=emb)
            else:
                curor.execute(
                    f"UPDATE balance SET bal={nowBal - nowBal // randint(2, 10)} WHERE name = '{str(ctx.author.id)}'")
                emb = discord.Embed(title="Преступление", colour=discord.colour.Colour.red())
                emb.add_field(name="У тебя забрали", value=str(addBal) + "$", inline=False)
                emb.add_field(name="У тебя", value=str(nowBal + addBal) + "$", inline=False)
                await ctx.send(embed=emb)
            curor.execute(f"UPDATE balance SET lastCrime=? WHERE name=?", [datetime.datetime.now(), str(ctx.author.id)])
            conn.commit()
        else:
            normal_datetime = lastDaily.strftime("%A %H:%M")
            normal_next_datetime = lastDaily + datetime.timedelta(hours=1)
            emb = discord.Embed(title="Ошибка", colour=colour.Color.red())
            emb.add_field(name=f"Ещё не прошло 1 час с {normal_datetime}",
                          value=f'В следующий раз вы можете использовать эту команду в {normal_next_datetime.strftime("%A %H:%M")}')
            await ctx.send(embed=emb)


def setup(client):
    client.add_cog(EconomyCommand(client))
