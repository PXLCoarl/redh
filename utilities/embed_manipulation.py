from discord import Embed, Interaction, Color
from discord.ui import View
from datetime import datetime
import uuid as gen_uuid



async def create_queue_embed(players: int, uuid:str):
    uuid = str(gen_uuid.uuid4())
    embed = Embed(color=Color.blurple(), title='RDPH | Queue', description='Ready to join a RDPH Battle?\nPress \'Join\' to challenge yourself to build a pauper commander deck in 1:30h.', timestamp=datetime.now())
    embed.set_footer(text=uuid)
    embed.add_field(name=f'Brewers: (0/{players})', value='')
    return embed

async def create_loading_embed(current:int, players:int, uuid:str):
    embed = Embed(color=Color.yellow(), title='RDPH | Waiting', description='Card cache is missing or corrupted.\nFetching fresh data...')
    embed.set_footer(text=uuid)
    embed.add_field(name=f'Brewers: ({current}/{players})', value='')
    return embed

async def create_error_embed(uuid:str, error:str):
    embed = Embed(color=Color.red(), title='RDPH | Error', description = 'Something went wrong, and the match had to be canceled.')
    embed.set_footer(text=uuid)
    embed.add_field(name='Reason:', value=error)
    return embed

        