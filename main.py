import discord
from discord.ext import commands

import logging
import os
import asyncio

import modules.config as config; data = config.load()
import modules.log as log; logger = log.setup('launcher', level=logging.INFO)


async def console():
    while True:
        response = await asyncio.to_thread(input)

        if response.startswith('load '):
            ext = response[5:]
            try:
                await bot.load_extension(ext)
                logger.info(f'{ext} chargé')
            except Exception as e:
                if isinstance(e, discord.ext.commands.errors.ExtensionNotLoaded):
                    logger.error(f"L'extension '{ext}' n'est pas chargé")
                elif isinstance(e, discord.ext.commands.errors.ExtensionAlreadyLoaded):
                    logger.error(f"L'extension '{ext}' est déjà chargé")
                elif isinstance(e, discord.ext.commands.errors.ExtensionNotFound):
                    logger.error(f"L'extension '{ext}' n'existe pas")
                elif isinstance(e, discord.ext.commands.errors.ExtensionNotFound):
                    logger.error(f"L'extension '{ext}' n'existe pas")
                else:
                    logger.error(e)

        elif response.startswith('unload '):
            ext = response[7:]
            try:
                await bot.unload_extension(ext)
                logger.info(f'{ext} déchargé')
            except Exception as e:
                if isinstance(e, discord.ext.commands.errors.ExtensionNotLoaded):
                    logger.error(f"L'extension '{ext}' n'est pas chargé")
                else:
                    logger.error(e)

        elif response.startswith('reload '):
            ext = response[7:]
            try:
                await bot.reload_extension(ext)
                logger.info(f'{ext} rechargé')
            except Exception as e:
                if isinstance(e, discord.ext.commands.errors.ExtensionNotLoaded):
                    logger.error(f"L'extension '{ext}' n'est pas chargé")
                else:
                    logger.error(e)


class client(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix='$',
            intents = discord.Intents.all(),
            application_id = data["app_id"]
        )

        self.synced = 0
        self.initial_extensions = []

        types = ['commands', 'events', 'tasks', 'menus']

        for type in types:
            for root, _, files in os.walk(f"cogs/{type}"):
                for file in files:
                    if file != '__pycache__' and file.endswith('.py'):
                        if root == f"cogs/{type}":
                            self.initial_extensions.append(f"cogs.{type}.{file[:-3]}")
                        else:
                            dir = os.path.basename(root)
                            self.initial_extensions.append(f"cogs.{type}.{dir}.{file[:-3]}")


    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        self.synced = await bot.tree.sync()

    async def on_ready(self):
        logger.info(f'{self.user} est connecté avec {len(self.synced)} commande(s) synchronisée(s) sous la version {data["version"]}')
        await asyncio.create_task(console())


bot = client(); bot.run(data["token"])