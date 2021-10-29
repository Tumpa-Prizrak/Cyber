import discord
import asyncio
from discord.ext import commands, tasks
class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        self.bot.logger.error(f'Command \'{ctx.command.name}\' execution failed:\n\t\tPython error: {err}')
        raise err


def setup(bot):
    bot.add_cog(Errors(bot))
