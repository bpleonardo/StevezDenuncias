import asyncio

from discord.ext import commands

import config


class MessagesManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def wait_for_message(self, channel):
        check = lambda m: m.channel == channel and not m.author.bot
        try:
            await self.bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            await channel.delete()
            return False
        return True

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        """Inicia um timeout."""
        if channel.category_id != config.CATEGORY_ID:
            return

        res = await self.wait_for_message(channel)
        if not res:
            return


def setup(bot):
    bot.add_cog(MessagesManager(bot))
