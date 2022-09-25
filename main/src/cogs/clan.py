import json
import time
from json import JSONDecodeError

import discord
import requests
from discord import ApplicationContext, Embed, Option
from discord.ext import commands

from cogs.base import BaseCog
from config import CLAN_STAFF, STOP_WORD, AUCTION_BET_LIMIT, PERMISSION_ROLE, OWNER_IDS, CLAN_MEMBER_ACCESS_ROLE
from database.clan_systems.clan_warn import clan_warn_system
from database.clan_systems.server_system import cross_server_system
from embeds.base import DefaultEmbed
from embeds.clan_embed.clan_embed.auction.auction import AuctionEmbed
from embeds.clan_embed.clan_embed.auction.lot import AuctionLot
from embeds.clan_embed.clan_embed.help.help_embed import HelpEmbed
from embeds.clan_embed.clan_embed.permittedMember import PermittedEmbed
from embeds.clan_embed.clan_embed.warn import ClanWarnEmbed
from embeds.clan_embed.staff.clan_command import ClanCommandsEmbed
from embeds.clan_embed.view_builders.help_view_builder import help_view_builder
from embeds.view_builder import default_view_builder
from extensions.decorator import is_owner, is_owner_rights
from extensions.logger import staff_logger
from main import client
from models.modal import StaffModal, ClanModal
from utils.access_enum_for_clan import AccessEnum


def get_embed(json_):
    embed_json = json.loads(json_)

    embed = Embed().from_dict(embed_json)
    return embed


class Clan(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        self.client = client
        self.stats_chat = None

    clans = discord.SlashCommandGroup('clan', 'commands to clan')

    @commands.group(aliases=['клан'])
    @commands.has_any_role(*CLAN_STAFF)
    async def clan(self, ctx):
        if not ctx.invoked_subcommand:
            if len(ctx.message.role_mentions) != 1:
                staff_logger.info(self.clan)
                if ctx.author.id in OWNER_IDS:
                    return await ctx.send(embed=ClanCommandsEmbed().embed, delete_after=60)
                else:
                    pass

    @clan.command(aliases=['афк'])
    async def afk(self, ctx: ApplicationContext, member: discord.Member):
        staff_logger.info(f'!clan afk command use: {ctx.author.id} for {member.id}')
        if member is not None:
            return False
        response_json = requests.get(f'https://yukine.ru/api/members/{ctx.guild.id}/{member.id}').json()
        await member.move_to(channel=None)
        await client.get_channel(982672022003924992).send(
            embed=DefaultEmbed(
                f'1. {ctx.author.mention}\n2. <t:{int(time.time())}>\n3. {member.mention}\n4. {response_json["clan"]["name"]}\n5. <@{709820533176270911}>'))
        clan_leader = client.get_user(response_json["userId"])
        return await clan_leader.send(embed=DefaultEmbed(f"***```Предупреждение за афк!\n{member.name}\n{member.id}```***"))

    @clans.command(name='v_lock', description='Выдать или забрать доступ в клан наборы', default_permission=True)
    @commands.has_any_role(*CLAN_MEMBER_ACCESS_ROLE)
    async def v_lock(self, interaction: discord.Interaction, member: discord.Member,
                     access: Option(str, 'Открыть или Закрыть доступ в войс', choices=AccessEnum.list(), required=True)):
        staff_logger.info(f'/clan v_lock command use: {interaction.user.id}')
        response_json = requests.get(f'https://yukine.ru/api/members/{interaction.guild.id}/{interaction.user.id}').json()
        recruit_voice = self.client.get_channel(int(response_json['clan']['recruitId']))
        if interaction.user.id == member.id:
            return False
        if access == 'Close':
            await recruit_voice.set_permissions(member, connect=False)
            await member.move_to(channel=None)
            return await interaction.response.send_message(embed=DefaultEmbed(f'***```Набор был закрыт для {member}```***'), ephemeral=True)
        if access == 'Open':
            await recruit_voice.set_permissions(member, connect=True)
            return await interaction.response.send_message(embed=DefaultEmbed(f'***```Набор был открыт для {member}```***'), ephemeral=True)

    @clans.command(name='v_list', description='Просмотреть список доступов в клан', default_permission=True)
    @commands.has_any_role(*CLAN_MEMBER_ACCESS_ROLE)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def v_list(self, interaction: discord.Interaction):
        staff_logger.info(f'/clan v_list command use: {interaction.user.id}')
        response_json = requests.get(f'https://yukine.ru/api/members/{interaction.guild.id}/{interaction.user.id}').json()
        permitted_description = ''
        counter = 1
        for permittedMember in response_json['clan']['permittedMembers']:
            permitted_description += f"**#{counter}** <@{permittedMember}>\n"
            counter += 1
        await interaction.response.send_message(
            embed=PermittedEmbed(clan_name=response_json['clan']['altName'], description=permitted_description).embed,
            delete_after=120, ephemeral=True)

    @clan.command(description='Добавить новый сервер в бд')
    @is_owner()
    async def guild(self, ctx, guild: discord.Guild, event_channel: discord.TextChannel,
                    text_category: discord.CategoryChannel, voice_category: discord.CategoryChannel,
                    clan_staff_role: discord.Role, auction_channel: discord.TextChannel,
                    trash_channel: discord.TextChannel, leader_role_id, consliger_role_id, find_clan_channel_id,
                    clan_info_channel_id, create_clan_url, verify_url, clan_staff_url, team_lead_id, senior_lead_id):
        # only for owner - BladeXses
        if cross_server_system.add_guild(
                guild_id=guild.id,
                event_channel_id=event_channel.id,
                text_category_id=text_category.id,
                voice_category_id=voice_category.id,
                clan_staff_role_id=clan_staff_role.id,
                auction_channel_id=auction_channel.id,
                trash_channel_id=trash_channel.id,
                leader_role_id=leader_role_id,
                consigliere_role_id=consliger_role_id,
                find_clan_channel_id=find_clan_channel_id,
                clan_info_channel_id=clan_info_channel_id,
                create_clan_url=create_clan_url,
                verify_url=verify_url,
                clan_staff_url=clan_staff_url,
                team_lead_id=team_lead_id,
                senior_lead_id=senior_lead_id,

        ):
            return await ctx.send(embed=DefaultEmbed('Сервер был успешно добавлен'))
        else:
            return await ctx.send(embed=DefaultEmbed('Сервер уже существует в БД'))

    @clans.command(name='help', description='Помощник по кланам', default_permission=True)
    async def help(self, interaction: discord.Interaction):
        leader_role_id, consliger_role_id, find_clan_id, clan_info_id, create_url, verify_url, clan_staff_url, team_lead_id, senior_lead_id = cross_server_system.get_help_fields(
            interaction.guild.id)
        leader_role, consliger_role = interaction.guild.get_role(leader_role_id), interaction.guild.get_role(
            consliger_role_id)
        find_clan, clan_info = interaction.guild.get_channel(find_clan_id), interaction.guild.get_channel(clan_info_id)
        staff_logger.info(f'help command use :: {interaction.user}')

        help_view = help_view_builder.create_staff_view()
        await interaction.response.send_message(
            embed=HelpEmbed(guild_name=interaction.guild.name, leader_role=leader_role.mention,
                            consliger_role=consliger_role.mention,
                            find_clan_channel=find_clan.mention, create_clan_url=create_url, verify_url=verify_url,
                            clan_info=clan_info.mention,
                            clan_staff_url=clan_staff_url, lead=f'<@{team_lead_id}>',
                            senior=f'<@{senior_lead_id}>').embed, view=help_view, ephemeral=True)

        async def request_staff_callback(interact: interaction):
            staff_modal = StaffModal(interact)
            await interact.response.send_modal(modal=staff_modal)

        async def request_clan_callback(interact: interaction):
            clan_modal = ClanModal(interact, title="Форма для создания клана")
            await interact.response.send_modal(modal=clan_modal)

        help_view_builder.button_staff.callback = request_staff_callback
        help_view_builder.button_clan.callback = request_clan_callback

    @clan.command(description='Выставить клан на аукцион')
    @is_owner_rights()
    async def auction(self, ctx, role: discord.Role, amount: int, *args):
        from extensions.funcs import send_trash_auction

        get_auction_channel = client.get_channel(cross_server_system.get_auction_channel(ctx.guild.id))
        send_message = ' '.join(args)
        auction_msg = await get_auction_channel.send(embed=AuctionEmbed(
            clan=role.mention,
            amount=amount,
            guild=ctx.guild,
            end_date=send_message
        ).embed)

        await auction_msg.pin()
        send_trash_auction.start(ctx, role.mention)

        def check(m):
            if m.channel == get_auction_channel:
                if not m.author.bot:
                    return m

        while True:
            msg = await client.wait_for('message', check=check)

            staff_logger.info(f'auction msg: {msg.author} :: {msg.content}')

            if msg.author.id == ctx.author.id and msg.content == STOP_WORD:
                break
            try:
                if amount + 99 < int(msg.content) <= amount + AUCTION_BET_LIMIT:
                    amount = int(msg.content)
                    await get_auction_channel.send(embed=AuctionLot(msg.author, msg.content).embed)
                else:
                    raise ValueError
            except ValueError:
                await msg.delete()
        send_trash_auction.cancel()
        return await get_auction_channel.send(f'Аукцион окончен.')

    @clan.command(description='Отправка сообщения по всем кланам')
    @is_owner_rights()
    async def send(self, ctx, *, args):
        def_view = default_view_builder.create_choice_view()
        try:
            embed = get_embed(args)
            test_message = await ctx.send(content=f'{ctx.author.name}, подтвердите отправку оповещений.', embed=embed, view=def_view, delete_after=60)
            await ctx.message.delete()

        except JSONDecodeError as e:
            await ctx.send(embed=DefaultEmbed(f'Error: {str(e)}'))
            return await ctx.message.delete()

        async def accept_callback(interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                return False

            get_text_category = client.get_channel(cross_server_system.get_text_category(interaction.guild.id))
            for category in interaction.guild.categories:
                if category.name == get_text_category.name:
                    for channel in category.text_channels:
                        await channel.send(embed=embed)

            staff_logger.info(f'{ctx.author.name} вызвал команду !clan send {args}')

            return await test_message.edit(
                embed=DefaultEmbed('Отправка сообщения по кланам прошла успешно\nОтправлять еще раз не нужно!!!\nРуки оторву.'),
                view=default_view_builder.create_view(),
                delete_after=60
            )

        async def decline_callback(interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                return False

            return await test_message.edit(
                embed=DefaultEmbed(f'Команда была отклонена'),
                view=default_view_builder.create_view(),
                delete_after=60
            )

        default_view_builder.button_accept.callback = accept_callback
        default_view_builder.button_decline.callback = decline_callback

    @commands.command(description='Отправка эмбеда')
    @commands.has_any_role(*PERMISSION_ROLE)
    async def emb(self, ctx: ApplicationContext, *, args):
        try:
            embed = get_embed(args)
            await ctx.send(embed=embed)
            return await ctx.message.delete()

        except JSONDecodeError as e:
            await ctx.send(embed=DefaultEmbed(f'Error: {str(e)}'))
            return await ctx.message.delete()

    @clan.command(description='Просмотр выговоров кланов')
    @is_owner_rights()
    async def warn(self, ctx: ApplicationContext):
        from extensions.funcs import get_clan_warn
        clan_role, reason, remove_date = get_clan_warn(guild_id=ctx.guild.id)
        await ctx.send(
            embed=ClanWarnEmbed(guild=ctx.guild, clan_role=clan_role, reason=reason, remove_date=remove_date, command_use=ctx.author).embed,
            delete_after=120)
        return await ctx.message.delete()

    @clan.command(description='Выдать выговор клану')
    @is_owner_rights()
    async def add_warn(self, ctx: ApplicationContext, clan_role_id: int, warn_day: int, *args):
        guild_id = ctx.guild.id
        reason = ' '.join(args)
        clan_warn_system.addGuildToWarnSystem(guild_id=guild_id)
        clan_warn_system.addWarn(guild_id=guild_id, clan_staff_id=ctx.author.id, clan_role_id=clan_role_id,
                                 warn_days=warn_day, reason=reason)
        await ctx.send(embed=DefaultEmbed(f'Выдан выговор клану <@&{clan_role_id}> с причиной {reason}.'), delete_after=30)
        return await ctx.message.delete()


def setup(bot):
    bot.add_cog(Clan(bot))
    print("Cog 'clan command' connected!")
