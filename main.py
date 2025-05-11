from typing import Type 
import discord, os
from discord import Intents, CustomActivity
from discord.app_commands.tree import CommandTree
from discord.ext import commands
from discord.ext.commands.bot import _default
from utilities import logger
from dotenv import load_dotenv

class BOT(commands.Bot):
    def __init__(self, command_prefix: str, *, help_command: commands.HelpCommand | None = None, description: str | None = None, intents: Intents, activity: CustomActivity) -> None:
        super().__init__(command_prefix, help_command=help_command, description=description, intents=intents, activity=activity)
        
    async def on_ready(self):
        files = [filename for filename in os.listdir('cogs') if filename.endswith('.py')]
        for filename in files:
            try:
                await self.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'Loaded extension: {filename[:-3]}')
            except Exception as e:
                logger.error(f'Failed to load extension {filename[:-3]}: {e}')
            logger.info(f'Started bot as {self.user.name}')

    
if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    bot = BOT(intents=Intents.all(), activity=CustomActivity('Enabling your deckbuilding addiction'), command_prefix='#')
    bot.run(token=TOKEN, log_handler=None)