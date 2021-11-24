import discord
from discord.ext import commands
import aiohttp
import ujson
from random import randint
import config as c
import typing
class ReactionsCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession(json_serialize=ujson)
        self.runame = 'Реакции'
    
    async def cog_command_error(self, ctx, error):
        chel = '<Человек>'
        if isinstance(error, commands.MissingRequiredArgument):
            qu = '[{}]' if ctx.command.__defaults__[1] is None else '<{}>'
            emb = discord.Embed(title=f"Параметр {qu.format(chel if error.param.name=='person' else error.param.name)} пропущен",
                                description=f'Правильное использование команды: {ctx.command.usage}',
                                colour=discord.colour.Colour.red())
            await ctx.send(embed=emb)

    async def get_gif(self, param):
        async with self.session.get(f"https://g.tenor.com/v1/search?q={param.replace(' ', '%20')}&key={c.apikey}&limit={str(c.limit)}") as r:
            if r.status == 200:
                while 1:
                    try:
                        return (await r.json())["results"][randint(0, c.limit)]["media"][0]['gif']['url']
                    except IndexError: continue
            else:
                return r.status

    async def build_embed(self, r, author, action, target=None):
        if target is not None:
            if author == target:
                return discord.Embed(title="Вы не можете сделать это с собой  :sob:", colour=discord.colour.Colour.red())
        if not isinstance(r, int):
            return discord.Embed(title=f"{author.name} {action} {target.name if target is not None else '\b'}",
                                colour=discord.colour.Colour.green()).set_image(url=r)
        else:
            return discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {r}",
                                colour=discord.colour.Colour.red())

    @commands.command(usage = 'baka <Человек>', brief = 'Отругать кого-то')
    async def baka(self, ctx, person: typing.Union[discord.Member, str]):
        r = await self.get_gif('anime baka')
        emb = await self.build_embed(r, ctx.autrhor, 'ругает', person)
        await ctx.send(embed=emb)

    @commands.command(usage = 'bangHead', brief = 'Долбиться головой об стену')
    async def bangHead(self, ctx):
        r = await self.get_gif('anime bang head')
        emb = await self.build_embed(r, ctx.autrhor, 'бьётся головой о стену')
        await ctx.send(embed=emb)

    @commands.command(usage = 'bite <Человек>', brief = 'Укусить кого-то')
    async def bite(self, ctx, person: typing.Union[discord.Member, str]):
        r = await self.get_gif('anime bite')
        emb = await self.build_embed(r, ctx.autrhor, 'укусил(а)', person)
        await ctx.send(embed=emb)

    @commands.command(usage = 'blush', brief = 'Покраснеть')
    async def blush(self, ctx):
        r = await self.get_gif('anime blush')
        emb = await self.build_embed(r, ctx.autrhor, 'краснеет')
        await ctx.send(embed=emb)

    @commands.command(usage = 'cry', brief = 'Поплакать. Не надо плакать :(')
    async def cry(self, ctx):
        r = await self.get_gif('anime cry')
        emb = await self.build_embed(r, ctx.autrhor, 'плачет')
        await ctx.send(embed=emb)

    @commands.command(usage = 'cuddle <Человек>', brief = 'Прижаться к кому-то')
    async def cuddle(self, ctx, person: typing.Union[discord.Member, str]):
        r = await self.get_gif('anime cuddlele')
        emb = await self.build_embed(r, ctx.autrhor, 'прижался(ась) к', person)
        await ctx.send(embed=emb)

    @commands.command(usage = 'dance [Человек]', brief = 'Потанцевать с кем-то или в одиночку')
    async def dance(self, ctx, person: typing.Union[discord.Member, str] = None):
        r = await self.get_gif('anime dance')
        emb = await self.build_embed(r, ctx.autrhor, 'танцует' if person is None else 'танцует с', person)
        await ctx.send(embed=emb)

    @commands.command(usage = 'drink [Человек]', brief = 'БУХАЕМ!!! Выпить напиток. С другом или без')
    async def drink(self, ctx, person: typing.Union[discord.Member, str] = None):
        r = await self.get_gif('anime drink tea')
        emb = await self.build_embed(r, ctx.autrhor, 'пьёт' if person is None else 'пьёт с', person)
        await ctx.send(embed=emb)

    @commands.command(usage = 'feed <Человек>', brief = 'Покормить кого-то')
    async def feed(self, ctx, person: typing.Union[discord.Member, str]):
        r = await self.get_gif('anime feed')
        emb = await self.build_embed(r, ctx.autrhor, 'покормил(а)', person)
        await ctx.send(embed=emb)

    @commands.command(usage = 'five <Человек>', brief = 'Пятюню? Дать "пять" кому-то')
    async def five(self, ctx, person: typing.Union[discord.Member, str]):
        r = await self.get_gif('anime high five')
        emb = await self.build_embed(r, ctx.autrhor, 'дал(а) пять', person)
        await ctx.send(embed=emb)

    @commands.command(usage = 'flip', brief = 'Сделать -100000 хп столу. Ой, то есть перевернуть его')
    async def flip(self, ctx):
        r = await self.get_gif('anime table flip')
        emb = await self.build_embed(r, ctx.autrhor, 'опрокинул(а) стол')
        await ctx.send(embed=emb)

    @commands.command(usage = 'hit <Человек>', brief = 'Дать по щам кому-нибудь')
    async def hit(self, ctx, person: typing.Union[discord.Member, str]):
        r = await self.get_gif('anime hit')
        emb = await self.build_embed(r, ctx.autrhor, 'ударил(а)', person)
        await ctx.send(embed=emb)

    @commands.command(usage = 'hug <Человек>', brief = 'Обнимашкиииии!!! Обнимем кого-то?')
    async def hug(self, ctx, person: typing.Union[discord.Member, str]):
        r = await self.get_gif('anime hug')
        emb = await self.build_embed(r, ctx.autrhor, 'обнял(а)', person)
        await ctx.send(embed=emb)

    @commands.command(usage = 'innocent', brief = 'Я точно не импостер, не, ну серьёзно :D')
    async def innocent(self, ctx):
        r = await self.get_gif('anime innocent')
        emb = await self.build_embed(r, ctx.autrhor, 'оправдывается')
        await ctx.send(embed=emb)

    @commands.command(usage = 'kill <Человек>', brief = 'РЕЗНЯ! Убить кого-то')
    async def kill(self, ctx, person: typing.Union[discord.Member, str]):
        r = await self.get_gif('anime kill')
        emb = await self.build_embed(r, ctx.autrhor, 'убил(а)', person)
        await ctx.send(embed=emb)

    @commands.command(usage = 'kiss <Человек>', brief = 'Поцелуемся с кем-то? \*чмок*') # \* чтобы не выделялось курсивом
    async def kiss(self, ctx, person: typing.Union[discord.Member, str]):
        r = await self.get_gif('anime kiss')
        emb = await self.build_embed(r, ctx.autrhor, 'поцеловал(а)', person)
        await ctx.send(embed=emb)

    @commands.command(usage = 'lick <Человек>', brief = 'Лизни кого-то)')
    async def lick(self, ctx, person: typing.Union[discord.Member, str]):
        r = await self.get_gif('anime lick')
        emb = await self.build_embed(r, ctx.autrhor, 'лизнул(а)', person)
        await ctx.send(embed=emb)

    @commands.command(usage = 'pat <Человек>', brief = 'Кто тут у нас хороший? А ну иди сюда, поглажу :)')
    async def pat(self, ctx, person: typing.Union[discord.Member, str]):
        r = await self.get_gif('anime pat')
        emb = await self.build_embed(r, ctx.autrhor, 'погладил(а)', person)
        await ctx.send(embed=emb)

    @commands.command(usage = 'poke <Человек>', brief = 'Тыкнуть в кого-то')
    async def poke(self, ctx, person: typing.Union[discord.Member, str]):
        r = await self.get_gif('anime poke')
        emb = await self.build_embed(r, ctx.autrhor, 'тыкнул(а) в', person)
        await ctx.send(embed=emb)

    @commands.command(usage = 'scare <Человек>', brief = 'Бу! Напугать кого-то')
    async def scare(self, ctx, person: typing.Union[discord.Member, str]):
        r = await self.get_gif('anime scare')
        emb = await self.build_embed(r, ctx.autrhor, 'испугал(а)', person)
        await ctx.send(embed=emb)

    @commands.command(usage = 'slap <Человек>', brief = 'Дать подщёчину кому-то')
    async def slap(self, ctx, person: typing.Union[discord.Member, str]):
        r = await self.get_gif('anime slap')
        emb = await self.build_embed(r, ctx.autrhor, 'дал(а) подщёчину', person)
        await ctx.send(embed=emb)

    @commands.command(usage = 'sleep', brief = 'Поспать. Спокойной ночи 💤')
    async def sleep(self, ctx):
        r = await self.get_gif('anime sleep')
        emb = await self.build_embed(r, ctx.autrhor, 'спит')
        await ctx.send(embed=emb)

    @commands.command(usage = 'spank <Человек>', brief = 'Ударить кого-то... типа hit или slap, но не hit и не slap')
    async def spank(self, ctx, person: typing.Union[discord.Member, str]):
        r = await self.get_gif('anime spank')
        emb = await self.build_embed(r, ctx.autrhor, 'ударил(а)', person)
        await ctx.send(embed=emb)

    @commands.command(usage = 'tickle <Человек>', brief = 'Пощекотать кого-то')
    async def tickle(self, ctx, person: typing.Union[discord.Member, str]):
        r = await self.get_gif('anime tickle')
        emb = await self.build_embed(r, ctx.autrhor, 'пощекотал(а)', person)
        await ctx.send(embed=emb)

    @commands.command(usage = 'walk <Человек>', brief = 'Ходить, гулять, бродить')
    async def walk(self, ctx, person: typing.Union[discord.Member, str] = None):
        r = await self.get_gif('anime walk')
        emb = await self.build_embed(r, ctx.autrhor, 'гуляет' if person is None else 'гуляет с', person)
        await ctx.send(embed=emb)

def setup(client):
    client.add_cog(ReactionsCommand(client))