import asyncio

from discord.ext import commands

import config


class MessagesManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.unclaimed_channels = []

    async def wait_for_message(self, channel):
        check = lambda c: c == channel
        try:
            await self.bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            await channel.delete()
            self.unclaimed_channels.remove(channel.id)
            return False
        return True

    async def wait_for_claim(self, channel):
        check = lambda c: c == channel
        while channel.id in self.unclaimed_channels:
            try:
                # "Atualizar" a cada 15 segundos
                m = await self.bot.wait_for('message', check=check, timeout=15)
            except asyncio.TimeoutError:
                continue

            for role in m.author.roles:
                if role.id in config.SUPPORT_ROLES:
                    ctx = await self.bot.get_context(m)
                    return await self.bot.get_cog('Commands').claim(ctx)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        """Inicia um timeout."""
        if channel.category_id == config.CATEGORY_ID:
            self.bot.loop.create_task(self.watch_messages(channel))

        self.unclaimed_channels.append(channel.id)

        res = await self.wait_for_message(channel)
        if not res:
            return

        await self.wait_for_claim(channel)


def setup(bot):
    bot.add_cog(MessagesManager(bot))
