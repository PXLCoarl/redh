from main import BOT
from typing import Literal
from discord import app_commands, Interaction, ButtonStyle, SelectOption, Embed, Color, Object, Button
from discord.ui import View, Select, select, button
from discord.ext import commands
from utilities import logger, generate_cards
from datetime import datetime
import uuid as gen_uuid, discord, re

async def setup(bot: BOT) -> None:
    await bot.add_cog(RDPHGenerator(bot), guild=Object(841127630564622366))
    
    
    
class RDPHGenerator(commands.Cog):
    def __init__(self, bot: BOT) -> None:
        super().__init__()
        self.bot = bot
        
    
    @app_commands.command(name='rdph', description='rdph queue')
    async def queue(self, interaction: Interaction, players: Literal[1, 2, 3, 4]):
        uuid = str(gen_uuid.uuid4())
        embed = Embed(color= Color.dark_magenta(), title=f'RDPH | Queue', description='Ready to join a RDPH Battle?\nPress \'Join\' to challenge yourself to build a pauper commander deck in 1:30h.', timestamp=datetime.now())
        embed.set_footer(text=uuid)
        embed.add_field(name=f'Brewers: (0/{players})', value='')
        
        view = QueueView()
        await interaction.response.send_message(embed=embed, view=view)
        
        
class OnGoingButton(discord.ui.Button):
    def __init__(self, label, style, id):
        super().__init__(label=label, style=style)
        self.id = id
    
    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        await reroll(interaction)

class OnGoingView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(OnGoingButton(label='Reroll', style=ButtonStyle.grey, id='Reroll'))



class QueueButton(discord.ui.Button):
    def __init__(self, label, style, id):
        super().__init__(label=label, style=style)
        self.id = id
        
    async def callback(self, interaction: Interaction) -> None:
        if self.id == 'Join':
            await interaction.response.defer()
            await join(interaction)
        if self.id == 'Leave':
            await interaction.response.defer()
            await leave(interaction)
        if self.id == 'Debug':
            await interaction.response.defer()
            pass
        
class QueueView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(QueueButton(label='Join', style=ButtonStyle.green, id='Join'))
        self.add_item(QueueButton(label='Leave', style=ButtonStyle.red, id='Leave'))
        self.add_item(QueueButton(label='Debug', style=ButtonStyle.grey, id='Debug'))
        
        
async def join(interaction: Interaction) -> None:
    players = int(re.search(r'\((\d+)/(\d+)\)', interaction.message.embeds[0].fields[0].name).group(2))
    username = interaction.user.name
    embed = interaction.message.embeds[0]
    match_uuid = interaction.message.embeds[0].footer.text
    names = interaction.message.embeds[0].fields[0].value
    
    player_list = names.split('\n') if names else []
    if username in player_list:
        return
    player_list.append(username)
    current = len(player_list)
    
    if current == players:
        cards = generate_cards(players, match_uuid)
        if not cards:
            logger.error(f'No cards could be generated for {match_uuid}')
            embed.title = 'RDPH | Error'
            embed.description = (
                "Something went wrong while generating the cards for the match.\n"
                "Please check if [Scryfall](https://scryfall.com/) is accesible,\n"
                "or try again later. If the issue persists, contact <@261118995464192000>."
            )
            embed.clear_fields()
            await interaction.edit_original_response(embed=embed, view=None)
            return
        embed.clear_fields()
        i = 0
        for player in player_list:
            player_list[i] = f'**{player}**\n  - Commander: [{cards[i]["name"]}]({cards[i]["scryfall_uri"]})'
            embed.add_field(name=f'**{player}**', value=f'Commander: [{cards[i]["name"]}]({cards[i]["scryfall_uri"]})', inline=False)
            i += 1
        
        logger.info(f'Match {match_uuid} has started')
        embed.title = 'RDPH | Ongoing'
        embed.description = f'Brewers: ({current}/{players})'
        await interaction.edit_original_response(embed=embed, view=OnGoingView())
        return
    
    names = '\n'.join(player_list)
    embed = interaction.message.embeds[0]
    embed.set_field_at(0, name=f'Brewers: ({current}/{players})', value=names)
    
    logger.info(f'{username} joined Queue {match_uuid}')
    await interaction.edit_original_response(embed=embed)

async def leave(interaction: Interaction) -> None:
    players = int(re.search(r'\((\d+)/(\d+)\)', interaction.message.embeds[0].fields[0].name).group(2))
    username = interaction.user.name
    match_uuid = interaction.message.embeds[0].footer.text
    names = interaction.message.embeds[0].fields[0].value
    
    player_list = names.split('\n') if names else []
    if not username in player_list:
        return
    player_list.remove(username)
    current = len(player_list)
    names = '\n'.join(player_list)
    
    embed = interaction.message.embeds[0]
    embed.set_field_at(0, name=f'Brewers: ({current}/{players})', value=names)
    logger.info(f'{username} left Queue {match_uuid}')
    await interaction.edit_original_response(embed=embed)
    
async def reroll(interaction: Interaction) -> None:
    username = interaction.user.name
    embed = interaction.message.embeds[0]
    fields = embed.fields
    match_id = embed.footer.text
    card = generate_cards(1, match_id)[0]
    field, index = next(((f, idx) for idx, f in enumerate(fields) if f.name == f'**{username}**'), (None, None))

    if not field:
        logger.error('this shouldnt happen rn')
        return
    value = f'Commander: [{card["name"]}]({card["scryfall_uri"]})'
    embed.set_field_at(index, name=f'**{username}**', value=value)
    await interaction.edit_original_response(embed=embed)