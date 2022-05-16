import discord
from discord.ext import commands

from cogs.base import BaseCog
from config import CLAN_STAFF, AUCTION_STOP_WORD, AUCTION_BET_LIMIT, OWNER_IDS, BLADEXSES_ID
from embeds.clan_events_mode.staff_embed.auction import AuctionStartEmbed, AuctionLot
from embeds.clan_events_mode.staff_embed.clan_command import ClanCommandsEmbed
from embeds.def_embed import DefaultEmbed
from embeds.def_view_builder import default_view_builder
from main import client
from base.funcs import *
from systems.clan_staff.cross_event_system import cross_event_system
from embeds.clan_events_mode.staff_embed.sending_message_to_clan import SendingMessagesClans


class Clan(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        self.client = client
        self.stats_chat = None

    @commands.group(aliases=['клан'])
    @commands.has_any_role(*CLAN_STAFF)
    async def clan(self, ctx):
        if not ctx.invoked_subcommand:
            if len(ctx.message.role_mentions) != 1:
                return await ctx.send(embed=ClanCommandsEmbed().embed, delete_after=60)

    @clan.command(description='Добавить новый сервер в бд')
    async def guild(self, ctx, guild: discord.Guild, event_channel: discord.TextChannel,
                    text_category: discord.CategoryChannel, voice_category: discord.CategoryChannel,
                    clan_staff_role: discord.Role, auction_channel: discord.TextChannel):
        # only for owner - BladeXses
        author = ctx.author.id

        # TODO: make a decorator like @is_owner that will
        #  allow only the owner to execute the command
        if author != BLADEXSES_ID:
            return

        if cross_event_system.add_guild(
                guild_id=guild.id,
                event_channel_id=event_channel.id,
                text_category_id=text_category.id,
                voice_category_id=voice_category.id,
                clan_staff_role_id=clan_staff_role.id,
                auction_channel_id=auction_channel.id
        ):
            return await ctx.send(embed=DefaultEmbed('Сервер был успешно добавлен'))
        else:
            return await ctx.send(embed=DefaultEmbed('Сервер уже существует в БД'))

    @clan.command(description='Выставить клан на аукцион')
    async def auction(self, ctx, role: discord.Role, amount: int):
        author = ctx.author.id

        if author not in OWNER_IDS:
            return False

        get_auction_channel = client.get_channel(cross_event_system.get_auction_channel(ctx.guild.id))
        auction_msg = await get_auction_channel.send(embed=AuctionStartEmbed(
            clan=role.mention,
            amount=amount,
            guild=ctx.guild
        ).embed)

        await auction_msg.pin()

        def check(m):
            if m.channel == get_auction_channel:
                if not m.author.bot:
                    return m

        while True:
            msg = await client.wait_for('message', check=check)
            if msg.author.id == ctx.author.id and msg.content == AUCTION_STOP_WORD:
                break
            try:
                if amount < int(msg.content) <= amount + AUCTION_BET_LIMIT:
                    amount = int(msg.content)
                    await get_auction_channel.send(embed=AuctionLot(msg.author, msg.content).embed)
                else:
                    raise ValueError
            except ValueError:
                await msg.delete()
        return await get_auction_channel.send(f'Аукцион окончен.')

    @clan.command(description='Отправка сообщения по всем кланам')
    async def send(self, ctx, *args):
        def_view = default_view_builder.create_choice_view()
        author = ctx.author.id
        send_message = ' '.join(args)

        if author not in OWNER_IDS:
            return False

        msg = await ctx.send(
            embed=DefaultEmbed(f'{ctx.author.name}, подтвердите отправку оповещений.'),
            view=def_view,
            delete_after=60
        )

        async def accept_callback(interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                return False

            get_text_category = client.get_channel(cross_event_system.get_text_category_by_guild_id(ctx.guild.id))

            for category in interaction.guild.categories:
                if category.name == get_text_category.name:
                    for channel in category.text_channels:
                        await channel.send(embed=SendingMessagesClans(args=send_message).embed)

            return await msg.edit(
                embed=DefaultEmbed('Отправка сообщение по кланам прошла успешно'),
                view=default_view_builder.create_view(),
                delete_after=60
            )

        async def decline_callback(interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                return False

            return await msg.edit(
                embed=DefaultEmbed(f'Команда была отклонена'),
                view=default_view_builder.create_view(),
                delete_after=60
            )

        default_view_builder.button_accept.callback = accept_callback
        default_view_builder.button_decline.callback = decline_callback


def setup(bot):
    bot.add_cog(Clan(bot))
    print("Cog 'clan command' connected!")
