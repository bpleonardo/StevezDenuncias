import discord
from discord.ext import commands

import config


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role(*config.SUPPORT_ROLES)
    async def add(self, ctx: commands.Context, member: discord.Member):
        if ctx.channel.category_id != config.CATEGORY_ID:
            return

        await ctx.channel.set_permissions(
            member, send_messages=True, view_channel=True
        )
        await ctx.message.delete()

    @commands.command(aliases=['remove'])
    @commands.has_any_role(*config.SUPPORT_ROLES)
    async def rm(self, ctx: commands.Context, member: discord.Member):
        if ctx.channel.category_id != config.CATEGORY_ID:
            return

        await ctx.channel.set_permissions(member, overwrite=None)

        await ctx.message.delete()

    @commands.command()
    @commands.has_any_role(*config.SUPPORT_ROLES)
    async def close(self, ctx: commands.Context):
        if ctx.channel.category_id != config.CATEGORY_ID:
            return

        await ctx.channel.delete()


def setup(bot):
    bot.add_cog(Commands(bot))
