import discord
from discord.ext import commands

import config


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role(*config.SUPPORT_ROLES)
    async def claim(self, ctx: commands.Context):
        cog = self.bot.get_cog('MessagesManager')

        if ctx.channel.id in cog.unclaimed_channels:
            cog.unclaimed_channels.remove(ctx.channel.id)

        overwrites = ctx.channel.overwrites
        overwrites[ctx.author] = discord.PermissionOverwrite(
            send_messages=True
        )
        for role in self.bot.support_roles:
            overwrites[role] = discord.PermissionOverwrite(
                send_messages=False, view_channel=True
            )

        await ctx.channel.edit(overwrites=overwrites)

    @commands.command()
    @commands.has_any_role(*config.SUPPORT_ROLES)
    async def add(self, ctx: commands.Context, member: discord.Member):
        await ctx.channel.set_permissions(member, view_channel=True)
        await ctx.message.delete()

    @commands.command()
    @commands.has_any_role(*config.SUPPORT_ROLES)
    async def close(self, ctx: commands.Context):
        await ctx.channel.delete()


def setup(bot):
    bot.add_cog(Commands(bot))
