import asyncio

from discord.ext import commands

import config


class MessagesManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.unclaimed_channels = []

    async def watch_messages(self, channel):
        check = lambda c: c.channel == channel
        while True:
            try:
                m = await self.bot.wait_for('message', check=check, timeout=60)

                if channel.id in self.unclaimed_channels:
                    for role in m.author.roles:
                        if role.id in config.SUPPORT_ROLES:
                            ctx = await self.bot.get_context(m)
                            await self.bot.get_cog('Commands').claim(ctx)
                            break

            except asyncio.TimeoutError:
                try:
                    await channel.delete()
                    if channel.id in self.unclaimed_channels:
                        self.unclaimed_channels.remove(channel.id)
                except Exception:
                    pass
                break

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        """Inicia um timeout."""
        if channel.category_id == config.CATEGORY_ID:
            self.bot.loop.create_task(self.watch_messages(channel))

        self.unclaimed_channels.append(channel.id)


def setup(bot):
    bot.add_cog(MessagesManager(bot))
