import discord
from discord import app_commands
from discord.ext import commands

import logging
import requests
import asyncio
import traceback
import sys

import modules.config as config; data = config.load()
import modules.message as messageConfig
import modules.log as log; logger = log.setup(__name__, level=logging.ERROR)


class nitro(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    class stockButtons(discord.ui.View):
        def __init__(self):
            timeout = data["nitro"]["stock"]["timeout"]
            if str(timeout).lower() == "none":
                timeout = None
            super().__init__(timeout=timeout)
        
        @discord.ui.button(label=f"{len([line for line in open(data['nitro']['stock']['file']['classic'], 'r').readlines() if line.startswith('discord.gift/')])} {messageConfig.get('nitro.classic')}", style=discord.ButtonStyle.blurple, disabled=False)
        async def classicButton(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
        
        @discord.ui.button(label=f"{len([line for line in open(data['nitro']['stock']['file']['boost'], 'r').readlines() if line.startswith('discord.gift/')])} {messageConfig.get('nitro.boost')}", style=discord.ButtonStyle.blurple, disabled=False)
        async def nitroButton(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
        
        async def on_timeout(self):
            pass
    
    
    group = app_commands.Group(name='nitro', description='...')
    
    
    @group.command(name = "stock", description = "Consulter le stock de nitro")
    async def stock(
        self,
        interaction: discord.Interaction
    ) -> None:
        embed = discord.Embed(description=f"## {messageConfig.get('nitro.stock')}", colour=int(data['colour']['embed'], 16))

        await interaction.response.send_message(embed=embed, view=self.stockButtons())
    
    @stock.error
    async def stock_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.errors.AppCommandError
    ):
        TYPE, VALUE, TRACEBACK = sys.exc_info()
        trace = traceback.format_exception(TYPE, VALUE, TRACEBACK)
        logger.error(f'{trace[-1]}')
    
    
    def deleteLine(self, TYPE, line):
        with open(data['nitro']['stock']['file'][TYPE], 'r') as file:
            lines = file.readlines()

        with open(data['nitro']['stock']['file'][TYPE], 'w') as file:
            for i, content in enumerate(lines, 1):
                if i != line:
                    file.write(content)
    
    @app_commands.choices(type=[
        app_commands.Choice(name=data['nitro']['drop']['type']['classic'], value='classic'),
        app_commands.Choice(name=data['nitro']['drop']['type']['boost'], value='boost')
    ])
    
    @app_commands.describe(type="Type de nitro", salon="Salon ou est envoyé le nitro")
    
    @app_commands.checks.has_any_role(*data['help']['roles']['admins'])
    
    @group.command(name = "drop", description = "Drop un nitro dans un salon")
    async def drop(
        self,
        interaction: discord.Interaction,
        type: str,
        salon: discord.TextChannel = None
    ) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        
        if salon == None:
            salon = interaction.channel
        
        gifts = [[value, line+1] for line, value in enumerate(open(data['nitro']['stock']['file'][type], 'r').readlines()) if value.startswith('discord.gift/')]
        for gift in gifts:
            gift[0] = gift[0].split('/')[1]
            
            if requests.get(f'https://discordapp.com/api/v9/entitlements/gift-codes/{gift[0]}?with_application=false&with_subscription_plan=true').status_code == 404:
                logger.error(f'Nitro invalide : discord.gift/{gift[0]}')
            elif requests.get(f'https://discordapp.com/api/v9/entitlements/gift-codes/{gift[0]}?with_application=false&with_subscription_plan=true').status_code == 200:
                self.deleteLine(type, gift[1])
                break
            
            await asyncio.sleep(3)
            gift = None
        
        if not gift:
            embed = discord.Embed(description=f"## {messageConfig.get('nitro.noNitro')}", colour=int(data['colour']['error'], 16))
            await interaction.followup.send(embed=embed)
            return
        
        embed = discord.Embed(description=f"{messageConfig.get('nitro.drop.message').replace('[nitro]', f'https://discord.gift/{gift[0]}').replace('[type]', type)}", colour=int(data['colour']['embed'], 16))
        await salon.send(embed=embed)
        
        embed = discord.Embed(description=f"## {messageConfig.get('nitro.drop.response').replace('[channel]', f'<#{salon.id}>')}", colour=int(data['colour']['message'], 16))
        await interaction.followup.send(embed=embed)
    
    @drop.error
    async def drop_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.errors.AppCommandError
    ):
        if isinstance(error, discord.errors, app_commands.MissingAnyRole):
            embed = discord.Embed(description=f"## {messageConfig.get('noPermission')}", colour=int(data['colour']['error'], 16))
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            TYPE, VALUE, TRACEBACK = sys.exc_info()
            trace = traceback.format_exception(TYPE, VALUE, TRACEBACK)
            logger.error(f'{trace[-1]}')

    
    @app_commands.choices(type=[
        app_commands.Choice(name=data['nitro']['drop']['type']['classic'], value='classic'),
        app_commands.Choice(name=data['nitro']['drop']['type']['boost'], value='boost')
    ])
    
    @app_commands.describe(type="Type de nitro", utilisateur="Utilisateur à qui est envoyé le nitro")
    
    @app_commands.checks.has_any_role(*data['help']['roles']['admins'])
    
    @group.command(name = "give", description = "Donner un nitro à un utilisateur")
    async def give(
        self,
        interaction: discord.Interaction,
        type: str,
        utilisateur: discord.User
    ) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        
        gifts = [[value, line+1] for line, value in enumerate(open(data['nitro']['stock']['file'][type], 'r').readlines()) if value.startswith('discord.gift/')]
        for gift in gifts:
            gift[0] = gift[0].split('/')[1]
            
            if requests.get(f'https://discordapp.com/api/v9/entitlements/gift-codes/{gift[0]}?with_application=false&with_subscription_plan=true').status_code == 404:
                logger.error(f'Nitro invalide : discord.gift/{gift[0]}')
            elif requests.get(f'https://discordapp.com/api/v9/entitlements/gift-codes/{gift[0]}?with_application=false&with_subscription_plan=true').status_code == 200:
                self.deleteLine(type, gift[1])
                break
            
            await asyncio.sleep(3)
            gift = None
        
        if not gift:
            embed = discord.Embed(description=f"## {messageConfig.get('nitro.noNitro')}", colour=int(data['colour']['error'], 16))
            await interaction.followup.send(embed=embed)
            return
        
        embed = discord.Embed(description=f"{messageConfig.get('nitro.give.message').replace('[nitro]', f'https://discord.gift/{gift[0]}').replace('[type]', type)}", colour=int(data['colour']['embed'], 16))
        await utilisateur.send(embed=embed)
        
        embed = discord.Embed(description=f"## {messageConfig.get('nitro.give.response').replace('[user]', f'<#{utilisateur.id}>')}", colour=int(data['colour']['message'], 16))
        await interaction.followup.send(embed=embed)
    
    @give.error
    async def give_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.errors.AppCommandError
    ):
        if isinstance(error, discord.errors, app_commands.MissingAnyRole):
            embed = discord.Embed(description=f"## {messageConfig.get('noPermission')}", colour=int(data['colour']['error'], 16))
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            TYPE, VALUE, TRACEBACK = sys.exc_info()
            trace = traceback.format_exception(TYPE, VALUE, TRACEBACK)
            logger.error(f'{trace[-1]}')


    @app_commands.choices(type=[
        app_commands.Choice(name=data['nitro']['drop']['type']['classic'], value='classic'),
        app_commands.Choice(name=data['nitro']['drop']['type']['boost'], value='boost')
    ])
    
    @app_commands.describe(type="Type de nitro", gift="Lien du nitro")
    
    @app_commands.checks.has_any_role(*data['help']['roles']['admins'])
    
    @group.command(name = "add", description = "Ajouter un nitro à la liste")
    async def add(
        self,
        interaction: discord.Interaction,
        gift: str,
        type: str
    ) -> None:
        gift = gift.replace('https://', '').replace('http://', '').replace('discord.gift', '').replace('/', '')
        
        if not requests.get(f'https://discordapp.com/api/v9/entitlements/gift-codes/{gift}?with_application=false&with_subscription_plan=true').status_code == 200:
            embed = discord.Embed(description=f"## {messageConfig.get('nitro.add.invalid')}", colour=int(data['colour']['message'], 16))
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        with open(data['nitro']['stock']['file'][type], 'a+') as f:
            f.write(f'\ndiscord.gift/{gift}')
        
        embed = discord.Embed(description=f"## {messageConfig.get('nitro.add.response')}", colour=int(data['colour']['embed'], 16))
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @add.error
    async def add_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.errors.AppCommandError
    ):
        if isinstance(error, discord.errors, app_commands.MissingAnyRole):
            embed = discord.Embed(description=f"## {messageConfig.get('noPermission')}", colour=int(data['colour']['error'], 16))
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            TYPE, VALUE, TRACEBACK = sys.exc_info()
            trace = traceback.format_exception(TYPE, VALUE, TRACEBACK)
            logger.error(f'{trace[-1]}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        nitro(bot)
    )