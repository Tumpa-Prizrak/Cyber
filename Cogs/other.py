import discord
from discord.ext import commands
import os

class OtherCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.runame = 'Остальное'

    @commands.command()
    async def help(self, ctx, *, cmd_input = None):
        if cmd_input is None:
            emb = discord.Embed(title="Команды:", colour=discord.colour.Colour.green())
            emb.set_footer(text=f"Можешь прописать {ctx.prefix}help <команда>, чтобы узнать больше про нужную команду :)",
                                        icon_url="https://cdn.discordapp.com/attachments/880063679570259969/897478783215476826/0c5aa927105c867558d290d6a1f3f72f.webp")
            for cog in self.bot.cogs:
                if not getattr(cog, 'invisible'):
                    emb.add_field(name=f'**{cog.runame}:**', value=" ".join(f'`{i.name}`' for i in cog.get_commands()))
        else:
            for cmd in self.bot.commands:
                if cmd.name == cmd_input:
                    # в будущем я сделаю так, что если нет cmd.usage, то будет брать по аннотации
                    emb = discord.Embed(title=f"Команда {cmd.name}", description=f'Синтаксис: {ctx.prefix}{cmd.usage if cmd.usage else cmd.name}', colour=discord.colour.Colour.green())
                    emb.add_field(name=cmd.brief if cmd.brief else '<нет краткого описания>', value=cmd.description if cmd.description else '** **')
                    break
        await ctx.send(embed=emb)   

    @commands.command(usage = 'ping', brief = 'Показывает пинг бота')
    async def ping(self, ctx):
        await ctx.send(f"Понг! Задержка {round(self.client.latency * 1000)} мс")

    @commands.command(usage = 'profile', brief = 'Показывает ваш профиль')
    async def profile(self, ctx):
        emb = discord.Embed(title=f"Ваш профиль", color=discord.colour.Colour.dark_orange())
        emb.set_author(name=str(ctx.author))
        emb.set_thumbnail(url=ctx.author.avatar_url)
        emb.add_field(name=f"Статус", value=str(ctx.author.status), inline=False)
        # emb.add_field(name=f"Кастомный статус", value=str(ctx.author.custom_status), inline=False)
        emb.add_field(name=f"Активность", value=str(ctx.author.activity), inline=False)
        emb.add_field(name=f"ID", value=str(ctx.author.id), inline=False)
        emb.add_field(name="Дата регистрации",
                      value=f"<t:{round(ctx.author.created_at.timestamp())}:R>",
                      inline=False)
        emb.add_field(name="Дата вступления",
                      value=f"<t:{round(ctx.author.joined_at.timestamp())}:R>",
                      inline=False)
        emb.add_field(name="Высшая роль", value=ctx.author.top_role, inline=False)
        await ctx.send(embed=emb)

def setup(client):
    client.add_cog(OtherCommand(client))