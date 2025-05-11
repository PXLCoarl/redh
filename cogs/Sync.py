from discord.ext import commands
from discord.app_commands import AppCommand
from main import BOT
from utilities import logger


async def setup(bot: BOT) -> None:
    await bot.add_cog(Sync(bot))


class Sync(commands.Cog):
    def __init__(self, bot: BOT) -> None:
        self.bot = bot
        
    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.message.delete()
        commands = [command.name for command in fmt]
        logger.info(f"Synced command(s) {', '.join(commands)} to '{ctx.guild.name}'")
        answer = await ctx.send(f"Synced {', '.join(commands)}.")
        await answer.delete(delay=5)
        return
        