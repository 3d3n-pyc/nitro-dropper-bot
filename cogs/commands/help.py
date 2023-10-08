import discord
from discord import app_commands
from discord.ext import commands

import logging
import traceback
import sys

import modules.config as config; data = config.load()
import modules.message as messageConfig
import modules.log as log; logger = log.setup(__name__, level=logging.ERROR)


class help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    
    group = app_commands.Group(name='help', description='...')
    
    @group.command(name = "membre", description = "Liste des commandes de membre")
    async def membre(
        self,
        interaction: discord.Interaction
    ) -> None:
        embed = discord.Embed(description=f'''\
# Voici les commandes
***[obligatoire]***
***(optionel)***
\u200b
## Membre
### /nitro stock
Consulter le stock de nitro.
\u200b
## Autres
### /about
Récupérer des informations par rapport au bot.
''', colour=int(data['colour']['embed'], 16))
            
        await interaction.response.send_message(embed=embed, ephemeral=True if data['help']['ephemeral']['membre'] == "True" else False)
    
    @membre.error
    async def membre_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.errors.AppCommandError
    ):
        TYPE, VALUE, TRACEBACK = sys.exc_info()
        trace = traceback.format_exception(TYPE, VALUE, TRACEBACK)
        logger.error(f'{trace[-1]}')

     
    @app_commands.checks.has_any_role(*data['help']['roles']['admins'])
    
    @group.command(name = "administration", description = "Liste des commandes d'administration")
    async def admin(
        self,
        interaction: discord.Interaction
    ) -> None:
        embed = discord.Embed(description=f'''\
# Voici les commandes
***[obligatoire]***
***(optionel)***
\u200b
## Administration
### /nitro add [nitro:str]
Ajouter un nitro à la liste.
### /nitro drop [type:str] (salon:Channel)
Donner un nitro à un utilisateur.
### /nitro give [type:str] [user:User]
Donner un nitro à un utilisateur.
\u200b
## Autres
### /about
Récupérer des informations par rapport au bot.
''', colour=int(data['colour']['embed'], 16))
        
        await interaction.response.send_message(embed=embed, ephemeral=True if data['help']['ephemeral']['admin'] == "True" else False)
    
    @admin.error
    async def admin_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.errors.AppCommandError
    ):
        if isinstance(error, app_commands.MissingAnyRole):
            await interaction.response.send_message(
                embed=discord.Embed(description=f"### {messageConfig.get('noPermission')}", colour=int(data['colour']['error'], 16)),
                ephemeral = True
            )
        else:
            TYPE, VALUE, TRACEBACK = sys.exc_info()
            trace = traceback.format_exception(TYPE, VALUE, TRACEBACK)
            logger.error(f'{trace[-1]}'[:-1])
    


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        help(bot)
    )