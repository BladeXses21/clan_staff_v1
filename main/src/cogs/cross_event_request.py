import datetime
import time

import discord
from discord.commands import Option
from discord.ext import commands, tasks

from discord.ui import View

from extensions.decorator import is_owner_rights
from staff_event.staff_service import ClanService
from embeds.clan_events_mode.staff.staff import StaffEmbed
from embeds.clan_events_mode.view_builders.staff_view_builder import staff_view_builder
from embeds.clan_events_mode.view_builders.event_view_builder import event_view_builder
from embeds.clan_events_mode.events.accepted_event_mode import accept_event_embed
from embeds.clan_events_mode.events.declined_event_mode import decline_event_embed
from embeds.clan_events_mode.events.clan_event import full_request_respons
from embeds.clan_events_mode.events.passed_event_mode import pass_event_embed
from embeds.clan_events_mode.staff.staff_command import StaffCommandsEmbed
from embeds.view_builder import default_view_builder
from embeds.base import DefaultEmbed
from extensions.funcs import sum_event_time, is_member_in_voice, get_guilds_list_async, get_staff_list_async, get_staff_event_list, remove_clan_staff_response, add_clan_staff_response
from extensions.logger import staff_logger
from systems.cross_events.cross_event_system import cross_event_system
from systems.cross_events.saved_stats_system import save_stats_system
from systems.cross_events.server_system import cross_server_system
from utils.events import ALL_EVENTS
from config import TENDERLY_ID, META_ID, DARKNESS_ID, HATORY_ID, CLAN_STAFF, OWNER_IDS, STOP_WORD
from cogs.base import BaseCog
from main import client


class CrossEventsMode(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        self.clan_service = ClanService(client)
        print("Cog 'clan event' connected!")

    event = discord.SlashCommandGroup('event', 'commands to request event')
    staffs = discord.SlashCommandGroup('staff', 'commands to request event')

    @commands.group(aliases=['стафф'])
    @commands.has_any_role(*CLAN_STAFF)
    async def staff(self, ctx):
        if not ctx.invoked_subcommand:
            if len(ctx.message.role_mentions) != 1:
                return await ctx.send(embed=StaffCommandsEmbed().embed, delete_after=60)

    @staff.command(description='Добавить человека в clan staff')
    @is_owner_rights()
    async def add(self, ctx, member: discord.Member):
        author_name = ctx.author.name
        guild = ctx.guild.id
        get_channel_id = cross_server_system.get_event_channel_by_guild_id(guild_id=ctx.guild.id)
        event_channel = client.get_channel(get_channel_id)
        overwrite = discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)
        if member is None:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, вы не указали пользователя```***'),
                delete_after=60
            )

        if cross_server_system.find_guild_id(guild_id=guild) is False:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, клан стафф не существует на этом сервере```***'),
                delete_after=60
            )

        if cross_event_system.is_clan_staff(guild_id=guild, clan_staff_id=member.id) is True:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, пользователь {member.name}, уже есть в списке clan staff```***'),
                delete_after=60
            )
        # <end>
        await event_channel.set_permissions(member, overwrite=overwrite)
        staff_logger.info(f'{ctx.author}, use !staff add to {member}')
        cross_event_system.add_clan_staff(guild_id=guild, clan_staff_id=member.id)
        save_stats_system.create_stat(guild_id=guild, clan_staff_id=member.id)
        return await ctx.send(embed=DefaultEmbed(add_clan_staff_response(member)))

    @staff.command(description='Убрать человека из clan staff')
    @is_owner_rights()
    async def kick(self, ctx, member: discord.Member):
        author_name = ctx.author.name
        guild = ctx.guild.id
        get_channel_id = cross_server_system.get_event_channel_by_guild_id(guild_id=ctx.guild.id)
        event_channel = client.get_channel(get_channel_id)
        if member is None:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, вы не указали пользователя```***'),
                delete_after=60
            )

        if cross_server_system.find_guild_id(guild_id=guild) is False:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, клан стафф не существует на этом сервере```***'),
                delete_after=60
            )

        if cross_event_system.is_clan_staff(guild_id=guild, clan_staff_id=member.id) is False:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, пользователя {member.name}, нет в списке clan staff```***'),
                delete_after=60
            )

        await event_channel.set_permissions(member, overwrite=None)
        staff_logger.info(f'{ctx.author}, use !staff kick to {member}')
        cross_event_system.delete_clan_staff(guild_id=guild, clan_staff_id=member.id)
        return await ctx.send(embed=DefaultEmbed(remove_clan_staff_response(member)))

    @staff.command(description='Очистка статы clan staff')
    @is_owner_rights()
    async def clear(self, ctx):
        author_name = ctx.author.name
        guild = ctx.guild.id
        def_view = default_view_builder.create_choice_view()

        if cross_server_system.find_guild_id(guild_id=guild) is False:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, клан стафф не существует на этом сервере```***'),
                delete_after=60
            )

        msg = await ctx.send(
            embed=DefaultEmbed(f'{ctx.author.name}, подтвердите очистку статистики.'),
            view=def_view,
            delete_after=60
        )

        async def accept_callback(interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                return False

            cross_event_system.reset_staff_stats(guild)
            return await msg.edit(
                embed=DefaultEmbed(f'***```{author_name}, вы успешно очистили статистику clan staff на {ctx.guild.name}```***'),
                delete_after=60,
                view=default_view_builder.create_view()
            )

        async def decline_callback(interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                return False

            return await msg.edit(
                embed=DefaultEmbed(f'Команда была отклонена'),
                delete_after=60,
                view=default_view_builder.create_view()
            )

        default_view_builder.button_accept.callback = accept_callback
        default_view_builder.button_decline.callback = decline_callback

    @staff.command(description='Просмотреть список всех челиксов из clan staff')
    @commands.has_any_role(*CLAN_STAFF)
    async def list(self, ctx):
        staff_button = staff_view_builder.create_staff_list_view()
        members = cross_event_system.get_event_organizers(guild_id=ctx.guild.id)
        description = get_staff_event_list(members)
        list_response = await ctx.send(
            embed=StaffEmbed(
                description=description,
                guild=ctx.guild.name,
                user=ctx.author.name,
                icon=ctx.guild.icon
            ).embed,
            view=staff_button,
            delete_after=160
        )

        async def tenderly_callback(interact: discord.Interaction):
            await get_staff_list_async(
                interaction=interact,
                ctx=ctx,
                clan_id=TENDERLY_ID,
                list_response=list_response,
                button=staff_button
            )

        async def meta_callback(interact: discord.Interaction):
            await get_staff_list_async(
                interaction=interact,
                ctx=ctx,
                clan_id=META_ID,
                list_response=list_response,
                button=staff_button
            )

        async def darkness_callback(interact: discord.Interaction):
            await get_staff_list_async(
                interaction=interact,
                ctx=ctx,
                clan_id=DARKNESS_ID,
                list_response=list_response,
                button=staff_button
            )

        async def hatory_callback(interact: discord.Interaction):
            await get_staff_list_async(
                interaction=interact,
                ctx=ctx,
                clan_id=HATORY_ID,
                list_response=list_response,
                button=staff_button
            )

        async def guild_callback(interact: discord.Interaction):
            guild_button = staff_view_builder.create_guild_list_view()
            await get_guilds_list_async(
                interaction=interact,
                ctx=ctx,
                clan_id=TENDERLY_ID,
                list_response=list_response,
                button=guild_button
            )

            async def guild_tenderly_callback(inter: discord.Interaction):
                await get_guilds_list_async(
                    interaction=inter,
                    ctx=ctx,
                    clan_id=TENDERLY_ID,
                    list_response=list_response,
                    button=guild_button
                )

            async def guild_meta_callback(inter: discord.Interaction):
                await get_guilds_list_async(
                    interaction=inter,
                    ctx=ctx,
                    clan_id=META_ID,
                    list_response=list_response,
                    button=guild_button
                )

            async def guild_darkness_callback(inter: discord.Interaction):
                await get_guilds_list_async(
                    interaction=inter,
                    ctx=ctx,
                    clan_id=DARKNESS_ID,
                    list_response=list_response,
                    button=guild_button
                )

            async def guild_hatory_callback(inter: discord.Interaction):
                await get_guilds_list_async(
                    interaction=inter,
                    ctx=ctx,
                    clan_id=HATORY_ID,
                    list_response=list_response,
                    button=guild_button
                )

            staff_view_builder.button_guild_tenderly.callback = guild_tenderly_callback
            staff_view_builder.button_guild_meta.callback = guild_meta_callback
            staff_view_builder.button_guild_darkness.callback = guild_darkness_callback
            staff_view_builder.button_guild_hatory.callback = guild_hatory_callback
            staff_view_builder.button_guild_back.callback = tenderly_callback

        staff_view_builder.button_tenderly.callback = tenderly_callback
        staff_view_builder.button_meta.callback = meta_callback
        staff_view_builder.button_darkness.callback = darkness_callback
        staff_view_builder.button_hatory.callback = hatory_callback
        staff_view_builder.button_guild.callback = guild_callback

    @event.command(name='request', description='Запрос ивента в клане', default_permission=True)
    async def request(self, interaction: discord.Interaction,
                      event_num: Option(int, 'укажите номер ивента из чата #клан-ивенты',
                                        min_value=1, max_value=61, required=True),
                      users_count: Option(int, 'Введите количество человек на ивенте.', required=True),
                      comment: Option(str, 'Введите коментарий к ивенту.', required=True)):
        guild = interaction.guild
        event_num = ALL_EVENTS[event_num]

        staff_logger.info(f'{interaction.user} вызвал комаду /event request {event_num} {users_count} {comment}')

        channel_id, role_id, text_category_id, voice_category_id = cross_server_system.get_cross_guild(guild.id)
        event_request_view = event_view_builder.create_event_request_view()

        member_ids = is_member_in_voice(guild.categories, client.get_channel(voice_category_id).name)
        get_event_channel = client.get_channel(channel_id)

        if interaction.user.id not in member_ids:
            return await interaction.response.send_message(
                embed=DefaultEmbed(f'***```Вы должны быть в голосовом канале клана.```***'),
                ephemeral=True
            )

        clan_name = interaction.user.voice.channel.name

        request_msg = await full_request_respons(
            interaction=interaction, event_channel=get_event_channel,
            role_id=role_id, event_num=event_num, users_count=users_count,
            comment=comment, event_request_view=event_request_view
        )

        cross_event_system.create_request(
            guild_id=interaction.guild.id, message_id=request_msg.id,
            clan_name=clan_name, event_num=event_num,
            member_send_request=interaction.user.id, comment=comment
        )

        async def accept_callback(ctx):
            user = ctx.user
            server = ctx.guild
            message = ctx.message
            channel = client.get_channel(ctx.channel.id)
            get_msg = await channel.fetch_message(message.id)
            ev_num, com, clan_n, member_send_id = cross_event_system.get_clan_event(guild_id=server.id,
                                                                                    message_id=ctx.message.id)
            get_member_send = ctx.guild.get_member(member_send_id)

            if cross_event_system.is_clan_staff(server.id, user.id) is False:
                return await ctx.response.send_message(
                    embed=DefaultEmbed(f'***```{user.name}, тебя нет в clan staff```***'),
                    ephemeral=True
                )

            if cross_event_system.is_event_completed(server.id, user.id) is False:
                return await ctx.response.send_message(
                    embed=DefaultEmbed(f'***```{user.name}, ты не закончил прошлый ивент.```***'),
                    ephemeral=True
                )

            cross_event_system.accept_clan_event(
                guild_id=server.id,
                message_id=request_msg.id,
                clan_staff_id=user.id
            )

            event_request_view.remove_item(event_view_builder.button_accept)
            event_request_view.remove_item(event_view_builder.button_decline)

            pass_view = event_view_builder.pass_event_request_view()

            await accept_event_embed(user=get_member_send, request_msg=get_msg, clan_name=clan_n, event_num=ev_num, clan_staff=user, pass_view=pass_view)

        async def decline_callback(ctx):
            user = ctx.user
            server = ctx.guild
            message = ctx.message
            channel = client.get_channel(ctx.channel.id)
            get_msg = await channel.fetch_message(message.id)
            ev_num, com, clan_n, member_send_id = cross_event_system.get_clan_event(guild_id=server.id,
                                                                                    message_id=ctx.message.id)
            get_member_send = ctx.guild.get_member(member_send_id)

            if cross_event_system.is_clan_staff(server.id, user.id) is False:
                return await ctx.response.send_message(
                    embed=DefaultEmbed(f'***```{user.name}, тебя нет в clan staff```***'),
                    ephemeral=True
                )

            if cross_event_system.is_event_completed(server.id, user.id) is False:
                return await ctx.response.send_message(
                    embed=DefaultEmbed(f'***```{user.name}, ты не закончил прошлый ивент.```***'),
                    ephemeral=True
                )

            cross_event_system.delete_clan_event(guild_id=server.id, message_id=get_msg.id)

            event_request_view.remove_item(event_view_builder.button_accept)
            event_request_view.remove_item(event_view_builder.button_decline)

            await decline_event_embed(
                user=get_member_send,
                request_msg=get_msg,
                clan_name=clan_n,
                event_num=ev_num,
                clan_staff=user,
                decline_view=event_request_view
            )

        async def pass_callback(ctx):
            user = ctx.user
            server = ctx.guild
            message = ctx.message
            channel = client.get_channel(ctx.channel.id)
            get_msg = await channel.fetch_message(message.id)
            ev_num, com, clan_n, member_send_id = cross_event_system.get_clan_event(guild_id=server.id,
                                                                                    message_id=ctx.message.id)

            time_accept = cross_event_system.get_time_accept_clan_event(guild_id=server.id,
                                                                        message_id=message.id)

            request_member_id = cross_event_system.get_request_msg_id(guild_id=server.id,
                                                                      clan_staff_id=user.id)

            event_request_view.remove_item(event_view_builder.button_pass)

            if cross_event_system.is_clan_staff(server.id, user.id) is False:
                return await ctx.response.send_message(embed=DefaultEmbed(f'***```{user.name}, тебя нет в clan staff```***'), ephemeral=True)

            if request_member_id != message.id:
                return await ctx.response.send_message(embed=DefaultEmbed(f'***```{user.name}, это не ваш ивент.```***'), ephemeral=True)

            await ctx.response.send_message(embed=DefaultEmbed(
                f'***```{user.name}, введите конечный итог ивента по форме\n@link [количество конфет] @link [количество конфет]...\nДля отмены ивента пропишите слово - stop```***'),
                ephemeral=True)

            def check(m):
                if m.channel == channel:
                    if not m.author.bot:
                        return m

            msg = await client.wait_for('message', check=check)

            if msg.author.id == ctx.user.id and msg.content == STOP_WORD:
                cross_event_system.delete_clan_event(guild_id=server.id, message_id=get_msg.id)
                cross_event_system.set_member_request(guild_id=server.id, clan_staff_id=ctx.user.id)
                await decline_event_embed(
                    user=ctx.guild.get_member(ctx.user.id), request_msg=get_msg, clan_name=clan_n, event_num=ev_num, clan_staff=user, decline_view=View()
                )
                await msg.delete()
                print(ev_num, com, clan_n, user.name, 'Ивент отменен!')

            if msg.author.id == ctx.user.id:
                sum_time_event = sum_event_time(guild=server.id, message_id=ctx.message.id)

                await pass_event_embed(
                    request_msg=get_msg, event_num=ev_num, clan_name=clan_n,
                    clan_staff=user, sum_time_event=sum_time_event,
                    time_accept_request=time_accept, comment=com,
                    pass_view=View(), end_result=msg.content
                )

                cross_event_system.pass_clan_event(guild_id=server.id, clan_staff_id=user.id, waisting_time=int(time.time()) - int(time_accept))
                save_stats_system.add_stat(guild_id=server.id, clan_staff_id=user.id, waisting_time=int(time.time()) - int(time_accept))
                cross_event_system.delete_clan_event(guild_id=server.id, message_id=message.id)
                await msg.delete()
                print(ev_num, com, clan_n, user.name, 'Ивент завершен!')

        event_view_builder.button_decline.callback = decline_callback
        event_view_builder.button_accept.callback = accept_callback
        event_view_builder.button_pass.callback = pass_callback

    @staffs.command(name='profile', description='Профиль clan staff', default_permission=False)
    @commands.has_any_role(*CLAN_STAFF)
    async def profile(self, interaction: discord.Interaction):
        staff_logger.info(f'{interaction.user.name} use command /staff profile')
        await self.clan_service.drop_menu(interaction)


# todo - Дневные задания ||| Балы и магазин - clan staff ||| Команда /close request |||
#  автоматически отклонять ивент если его не приняли на протяжении 15 минут |||
#  !staff add - возможность удаления сервера, указывая только его id |||
# todo - профиль для челиксов из clan staff - выбор рабочих дней(онли куратор) -
#  выбор выходных(онли куратор) - стата проведенных ивентов для каждого для и сумарно - поинты по времени - выговоры.

# @tasks.loop(time=datetime.time(0, 0, 1, 0))
# def clear(self):
#     pass


def setup(bot):
    bot.add_cog(CrossEventsMode(bot))
