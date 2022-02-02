import discord
from discord.ext import commands

import config


class ReactionManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def open_ticket(self, payload):
        """Abrir ticket."""
        if payload.message_id != config.MESSAGE_ID or payload.member.bot:
            return

        if payload.emoji.name != config.OPEN_REACTION:
            return

        await self.bot.http.remove_reaction(
            payload.channel_id,
            payload.message_id,
            payload.emoji,
            payload.user_id,
        )

        category = self.bot.tickets_category

        channel_name = f'denuncia-{str(payload.user_id >> 22)}'

        if discord.utils.get(category.text_channels, name=channel_name):
            return

        perms_allowed = discord.PermissionOverwrite(
            send_messages=True, view_channel=True
        )

        overwrites = {role: perms_allowed for role in self.bot.support_roles}
        overwrites[payload.member] = perms_allowed
        # overwrites[self.bot.guild.me] = perms_allowed
        overwrites[self.bot.guild.default_role] = discord.PermissionOverwrite(
            view_channel=False
        )

        channel = await category.create_text_channel(
            channel_name, overwrites=overwrites
        )

        embed = discord.Embed(title='Faça sua denúncia aqui', color=0xFF2E17)
        embed.description = '**• Para abrir uma denúncia você precisa:**\n > Do ID do infrator (Como copiar ID em <#936691125526351922>);\n> De um motivo plausível;\n> De provas e/ou testemunhas'
        embed.set_footer(text='Ao clicar em "🔒" e fechar o ticket, a staff NÃO poderá mais o ver.')

        msg = await channel.send(content=payload.member.mention, embed=embed)
        await msg.add_reaction(config.CLOSE_REACTION)

    def is_first_message(self, message_id, channel_id):
        # 1s é o tempo limite entre a criação do canal e a mensagem
        return (message_id >> 22) - (channel_id >> 22) < 1000

    @commands.Cog.listener('on_raw_reaction_add')
    async def close_ticket(self, payload):
        """Fechar ticket."""
        if payload.member.bot or payload.emoji.name != config.CLOSE_REACTION:
            return

        if self.is_first_message(payload.message_id, payload.channel_id):
            await self.bot.http.delete_channel(payload.channel_id)


def setup(bot):
    bot.add_cog(ReactionManager(bot))
