import discord
from discord.ext import commands
doc = """Дать Фениксу в лапы Банхаммер и указать на человека"""
syntax = "ban <Человек> [Причина]"


class ModerationCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.someShit = {
            "man": "<Человек>"
        }
        self.runame = 'Модерация'
        self.invisible = False

    async def cog_command_error(self, ctx, error):
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
        elif isinstance(error, discord.Forbidden):
            emb = discord.Embed(title="Я не могу это сделать, прав не хватает :sob:")
            await ctx.send(embed=emb)
        else:
            raise error

    @commands.command(usage = 'ban <Участник> [причина]', brief='Дать Фениксу в лапы Банхаммер и стукнуть им человека', description = 'Банит человека по указанной причине. Он не сможет вернуться на сервер с основного аккаунта вплоть до его разбана. Требуется право ban_members (банить участников) как у бота, так и у вызвавшего команду')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, man: discord.Member, *, reason = "Bad guy"):
        if man == ctx.author:
            emb = discord.Embed(title="Вы не можете сделать это с собой  :sob:", colour=discord.colour.Colour.red())
            return await ctx.send(embed=emb)
        if ctx.author.top_role.position <= man.top_role.position or ctx.guild.owner != ctx.author:
            emb = discord.Embed(title="Бро, у тебя нет прав", colour=discord.colour.Colour.red())
            await ctx.send(embed=emb)
            return
        await man.ban(reason=reason)
        emb = discord.Embed(title=f"**{man.display_name}** был забанен", colour=discord.colour.Color.green())
        await ctx.send(embed=emb)

    @commands.command(usage = 'kick <Участник> [причина]', brief = 'Выгнать участника с сервера', description='При помощи данной команды можно выгнать человека с сервера. Он сможет вернуться по ссылке-приглашению, если найдёт её. Требуется право kick_members (выгонять участников) как у бота, так и у вызвавшего команду')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, man: discord.Member, *, reason: str = "Bad guy"):
        if man == ctx.author:
            emb = discord.Embed(title="Вы не можете сделать это с собой  :sob:", colour=discord.colour.Colour.red())
            return await ctx.send(embed=emb)
        if ctx.author.top_role.position <= man.top_role.position or ctx.guild.owner != ctx.author:
            emb = discord.Embed(title="Бро, у тебя нет прав", colour=discord.colour.Colour.red())
            await ctx.send(embed=emb)
            return
        await man.kick(reason=reason)
        emb = discord.Embed(title=f"**{man.display_name}** был кикнут", colour=discord.colour.Color.green())
        await ctx.send(embed=emb)

    # mute временно на доработке, сорян
    # @commands.command()
    # @commands.has_permissions(manage_roles=True)
    # async def mute(self, ctx, man: discord.Member):
    #     if ctx.author.top_role.position <= man.top_role.position and ctx.guild.owner != ctx.author:
    #         raise commands.MissingPermissions
    #     curor.execute(f"INSERT INTO warns VALUES (?, ?)", (man.id, ctx.guild.id))
    #     conn.commit()
    #     embed = discord.Embed(title=f"\"{man.mention}\" был замьючен",
    #                           colour=discord.colour.Color.green())
    #     await ctx.send(embed=embed)

    # @commands.command(usage = 'warn <Участник> <причина>', brief = 'Ай-ай, не делай так больше!', description = 'Выносит предупреждение участнику по определённой причине. Требуется право manage_roles (управлять ролями) у вызвавшего команду')
    # @commands.has_permissions(manage_roles=True)
    # async def warn(self, ctx, man: discord.Member, *, reason: str):
    #    if ctx.author.top_role.position <= man.top_role.position and ctx.guild.owner != ctx.author:
    #        raise commands.MissingPermissions
    #    await self.db.insert_one({'guild': ctx.guild.id, 'member': man.id}, {'$push': {'warns': reason}}) # we need id's
    #    embed = discord.Embed(title=f"**{man.mention}** ({man})  получил предупреждение", colour=discord.colour.Color.green())
    #    await ctx.send(embed=embed)

    # мне лень фиксить это, но ладно
    # @commands.command(usage = 'warns [Участник]', brief = 'Посмотреть варны участника', description = 'Выводит все предупреждения участника/выполнившего команду')
    # async def warns(self, ctx, man: discord.Member = None):
    #     Pers_warns = (await self.db.find_one({'guild': ctx.guild.id, 'member': man.id if man else ctx.author.id}))['warns'] # да, биполярка, тут не будет is None
    #     if Pers_warns == []:
    #         all_warns = "\n*`Ничего`*"
    #     else:
    #         all_warns = ""
    #         for i in Pers_warns:
    #             all_warns += "\n\n"
    #             all_warns += "`" + i[2] + "`"
    #             all_warns += ";"
    #     embed = discord.Embed(title=f'Предупреждения {man.display_name if man else ctx.author.display_name}: {all_warns}', colour=discord.colour.Color.green())
    #     await ctx.send(embed=embed)


def setup(client):
    client.add_cog(ModerationCommand(client))
