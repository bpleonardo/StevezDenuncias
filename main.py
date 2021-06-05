import os
from glob import glob
from functools import cached_property

from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands

import config

load_dotenv()

intents = Intents(reactions=True, members=True, guilds=True)


class Bot(commands.Bot):
    @cached_property
    def guild(self):
        return self.get_guild(config.GUILD_ID)

    @cached_property
    def support_roles(self):
        roles = []
        for role_id in config.SUPPORT_ROLES:
            role = self.guild.get_role(role_id)
            if role:
                roles.append(role)

        return roles

    @cached_property
    def tickets_category(self):
        return self.get_channel(config.CATEGORY_ID)

    def load_extensions(self, *extensions):
        for extension in extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'[{extension}] {type(e).__name__}: {e}')
            else:
                print(f'[{extension}] Carregado.')

    async def on_ready(self):
        print(f'Logado como: {bot.user}')


bot = Bot(command_prefix='d!')

extensions = glob('cogs/*.py')
extensions = [ext.replace('/', '.')[:-3] for ext in extensions]
extensions.append('jishaku')

bot.load_extensions(*extensions)

bot.run(os.environ['TOKEN'])
