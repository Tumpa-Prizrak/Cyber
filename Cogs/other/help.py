import discord
from discord.ext import commands
import os



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
    async def help(self, ctx):
        categories = []
        for i in os.listdir("Cogs"):
            if i.endswith(".db") or i.endswith(".py") or i == '__pycache__':
                continue
            else:
                categories.append(i)

        emb = discord.Embed(title="Команды:", colour=discord.colour.Colour.green())

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


def setup(client):
    client.add_cog(OtherCommand(client))
