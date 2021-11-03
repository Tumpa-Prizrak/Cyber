import discord
from discord.ext import commands
import os
doc = """Помощь по боту"""
syntax = "help [команда]"


class OtherCommand(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.rus_categories = {
                "other": "Другое:",
                "moderation": "Модерация:",
                "economy": "Экономика:",
                "reactions": "Реакции:"
                }

    @commands.command()
    async def help(self, ctx, *, command: str = None):
        if command == None:
            categories = []
            for i in os.listdir("Cogs"):
                if len(str.split(i, ".")) != 1 or i == '__pycache__':
                    continue
                else:
                    categories.append(i)

            emb = discord.Embed(title="Команды:", colour=discord.colour.Colour.green())
            emb.set_footer(text="Можешь прописать =help <команда>, чтобы узнать больше про нужную команду :)",
            icon_url="https://cdn.discordapp.com/attachments/880063679570259969/897478783215476826/0c5aa927105c867558d290d6a1f3f72f.webp")

            for category in categories:
                desc = ""
                for i in os.listdir("Cogs/" + category):
                    if i.startswith("config.") or not i.endswith(".py"):
                        continue
                    else:
                        desc += f"`{i[:-3]}` "
                emb.add_field(name=self.rus_categories[category], value=desc, inline=False)
                # print(f"emb.add_field(name={category}, value={desc}, inline=False)")

            await ctx.send(embed=emb)
        else:
            try:
                for i in os.listdir("Cogs"):
                    if command + ".py" in os.listdir("Cogs\\" + i):
                        comm = __import__(f"Cogs.{i}.{command}", fromlist=["doc", "syntax"])

                        emb = discord.Embed(title=f"Команда {command}", colour=discord.colour.Colour.green())
                        emb.add_field(name=str(comm.doc), value="Синтаксис: " + str(comm.syntax), inline=False)

                        await ctx.send(embed=emb)

                        raise TypeError
                raise SyntaxError
            except TypeError:
                pass
            except SyntaxError:
                await ctx.send("Такой команды не существует")


def setup(client):
    client.add_cog(OtherCommand(client))
