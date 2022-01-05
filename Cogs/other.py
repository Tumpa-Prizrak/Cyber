import nextcord
from nextcord.ext import commands
from nextcord.utils import _IS_ASCII
from Cogs.helper import *

class OtherCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.runame = 'Остальное'
        self.invisible = False

    @commands.command()
    async def help(self, ctx, *, cmd_input = None):
        if cmd_input is None:
            emb = nextcord.Embed(title="Команды:", colour=nextcord.colour.Colour.green())
            emb.set_footer(text=f"Можешь прописать {ctx.prefix}help <команда>, чтобы узнать больше про нужную команду :)",
                                        icon_url="https://cdn.discordapp.com/attachments/880063679570259969/897478783215476826/0c5aa927105c867558d290d6a1f3f72f.webp")
            for cog in self.client.cogs.values():
                if not getattr(cog, 'invisible'):
                    emb.add_field(name=f'**{cog.runame}:**', value=" ".join(f'`{i.name}`' for i in cog.get_commands()),
                                  inline=False)
        else:
            for cmd in self.client.commands:
                if cmd.name == cmd_input:
                    # в будущем я сделаю так, что если нет cmd.usage, то будет брать по аннотации
                    emb = nextcord.Embed(title=f"Команда {cmd.name}", description=f'Синтаксис: {ctx.prefix}{cmd.usage if cmd.usage else cmd.name}', colour=nextcord.colour.Colour.green())
                    emb.add_field(name=cmd.brief if cmd.brief else '<нет краткого описания>', value=cmd.description if cmd.description else '** **')
                    break
        await ctx.send(embed=emb)   

    @commands.command(usage = 'ping', brief = 'Показывает пинг бота')
    async def ping(self, ctx):
        await ctx.send(f"Понг! Задержка {round(self.client.latency * 1000)} мс")

    @commands.command(usage = 'profile', brief = 'Показывает ваш профиль')
    async def profile(self, ctx: commands.Context, person: nextcord.Member = None):
        if person == None:
            person = ctx.author
        emb = nextcord.Embed(title="Ваш профиль" if person == None else f"Профиль {person.display_name}", color=person.top_role.colour)
        emb.set_author(name=str(person))
        emb.set_thumbnail(url=person.avatar)
        emb.add_field(name=f"Статус", value=str(person.status), inline=False)
        # emb.add_field(name=f"Кастомный статус", value=str(person.custom_status), inline=False)
        emb.add_field(name=f"Активность", value=str(person.activity), inline=False)
        emb.add_field(name=f"ID", value=str(person.id), inline=False)
        emb.add_field(name="Дата регистрации",
                      value=f"<t:{round(person.created_at.timestamp())}:R>",
                      inline=False)
        emb.add_field(name="Дата вступления",
                      value=f"<t:{round(person.joined_at.timestamp())}:R>",
                      inline=False)
        emb.add_field(name="Высшая роль", value=person.top_role, inline=False)
        await ctx.send(embed=emb)
    
    """@commands.command(usage = 'vote <Текст> <Вариант1> [Вариант2] ... [Вариант20]', brief = 'Начинает голосование')
    async def vote(self, ctx: commands.Context, text, *, variants):
        if len(variants) > 20:
            return embed_builder("Слишком много аргументов!", desc="Макимальное кол-во аргументов: 20", color=nextcord.Colour.red())
        emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '🔴', '🟠', '🟡', '🟢', '🔵', '🟣', '🟤', '🔶', "🔷"]
        conter = dict()
        voited = [ctx.author.id]
        for i in emojis[:len(variants) + 1]:
            conter.update({str(i): 0})
        
        desc = ""
        desc += "*Тема*" + "\n" + text + "\n"
        desc += "*Варианты*\n"
        
        a = 0
        for i in conter.keys():
            desc += f"{i}|{variants[a]}" + "\n"
            a += 1
        del a

        def if_already(_, user):
            return not user in voited
        
        updated_text = f"Текущий статус ({len(voited)} проголосовавших)\n"
        for i in conter.keys():
            updated_text += f"{i}|[{conter[i]}]\n"
        
        updated_text += f"{ctx.author.mention}: чтобы закончить голосование нажмите на красную кнопку"
        emb = embed_builder("🗳️ Опросник", desc=desc + updated_text)
        mess = await ctx.send(embed=emb)

        while True:
            del emb, updated_text
            emoj, pers = self.client.wait_for('reaction_add', check=if_already)
            voited.append(pers.id)
            conter[str(emoj.emoji)] += 1
            updated_text = f"Текущий статус ({len(voited)} проголосовавших)\n"
            for i in conter.keys():
                updated_text += f"{i}|[{conter[i]}]\n"
        
            updated_text += f"{ctx.author.mention}: чтобы закончить голосование нажмите на красную кнопку"
            emb = embed_builder("🗳️ Опросник", desc=desc + updated_text)
            await mess.edit(embed=emb)"""

def setup(client):
    client.add_cog(OtherCommand(client))
