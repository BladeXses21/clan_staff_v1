import time
from discord import Interaction, ApplicationContext
from discord.ui import View

from config import STOP_WORD
from database.clan_systems.event_history_system import event_history
from database.clan_systems.event_system import cross_event_system
from database.clan_systems.quest_system import quest_system
from database.clan_systems.saved_stats_system import save_stats_system
from database.clan_systems.server_system import cross_server_system
from embeds.base import DefaultEmbed
from embeds.clan_embed.events.accepted_event_mode import accept_event_embed
from embeds.clan_embed.events.clan_event import full_request_respons
from embeds.clan_embed.events.declined_event_mode import decline_event_embed
from embeds.clan_embed.events.passed_event_mode import pass_event_embed
from embeds.clan_embed.view_builders.event_view_builder import event_view_builder
from extensions.funcs import is_member_in_voice, sum_event_time, quest_info, xp_to_lvl
from extensions.logger import staff_logger
from utils.events import ALL_EVENTS


class EventService:
    def __init__(self, client):
        self.client = client

    async def event_request(self, event_num, users_count, comment, interaction: Interaction,
                            ctx: ApplicationContext = None):

        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        guild = ctx.guild
        event_num = ALL_EVENTS[event_num]
        staff_logger.info(f'{interaction.user} вызвал комаду /event request {event_num} {users_count} {comment}')

        channel_id, role_id, text_category_id, voice_category_id = cross_server_system.get_cross_guild(guild.id)
        event_request_view = event_view_builder.create_event_request_view()

        member_ids = is_member_in_voice(guild.categories, self.client.get_channel(voice_category_id).name)
        get_event_channel = self.client.get_channel(channel_id)

        if ctx.author.id not in member_ids:
            return await ctx.response.send_message(
                embed=DefaultEmbed(f'***```Вы должны быть в голосовом канале клана.```***'),
                ephemeral=True
            )

        clan_name = ctx.user.voice.channel.name

        request_msg = await full_request_respons(
            interaction=ctx, event_channel=get_event_channel,
            role_id=role_id, event_num=event_num, users_count=users_count,
            comment=comment, event_request_view=event_request_view
        )

        cross_event_system.create_request(
            guild_id=ctx.guild.id, message_id=request_msg.id,
            clan_name=clan_name, event_num=event_num,
            member_send_request=ctx.user.id, comment=comment
        )

        async def accept_callback(interact: Interaction):
            user = interact.user
            server = interact.guild
            message = interact.message
            channel = self.client.get_channel(interact.channel.id)
            get_msg = await channel.fetch_message(message.id)
            ev_num, com, clan_n, member_send_id = cross_event_system.get_clan_event(guild_id=server.id,
                                                                                    message_id=message.id)
            get_member_send = server.get_member(member_send_id)

            if cross_event_system.is_clan_staff(server.id, user.id) is False:
                return await interact.response.send_message(
                    embed=DefaultEmbed(f'***```{user.name}, тебя нет в clan staff```***'),
                    ephemeral=True
                )

            if cross_event_system.is_event_completed(server.id, user.id) is False:
                return await interact.response.send_message(
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

            await accept_event_embed(user=get_member_send, request_msg=get_msg, clan_name=clan_n, event_num=ev_num,
                                     clan_staff=user, pass_view=pass_view)

        async def decline_callback(interact: Interaction):
            user = interact.user
            server = interact.guild
            message = interact.message
            channel = self.client.get_channel(interact.channel.id)
            get_msg = await channel.fetch_message(message.id)
            ev_num, com, clan_n, member_send_id = cross_event_system.get_clan_event(guild_id=server.id,
                                                                                    message_id=message.id)
            get_member_send = server.get_member(member_send_id)

            if cross_event_system.is_clan_staff(server.id, user.id) is False:
                return await interact.response.send_message(
                    embed=DefaultEmbed(f'***```{user.name}, тебя нет в clan staff```***'),
                    ephemeral=True
                )

            if cross_event_system.is_event_completed(server.id, user.id) is False:
                return await interact.response.send_message(
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

        async def pass_callback(interact: Interaction):
            user = interact.user
            server = interact.guild
            message = interact.message
            channel = self.client.get_channel(interact.channel.id)
            get_msg = await channel.fetch_message(message.id)
            ev_num, com, clan_n, member_send_id = cross_event_system.get_clan_event(guild_id=server.id,
                                                                                    message_id=message.id)

            time_accept = cross_event_system.get_time_accept_clan_event(guild_id=server.id,
                                                                        message_id=message.id)

            request_member_id = cross_event_system.get_request_msg_id(guild_id=server.id,
                                                                      clan_staff_id=user.id)

            event_request_view.remove_item(event_view_builder.button_pass)

            if cross_event_system.is_clan_staff(server.id, user.id) is False:
                return await interact.response.send_message(
                    embed=DefaultEmbed(f'***```{user.name}, тебя нет в clan staff```***'), ephemeral=True)

            if request_member_id != message.id:
                return await interact.response.send_message(
                    embed=DefaultEmbed(f'***```{user.name}, это не ваш ивент.```***'), ephemeral=True)

            await interact.response.send_message(embed=DefaultEmbed(
                f'***```{user.name}, введите конечный итог ивента по форме\n@link [количество конфет] @link [количество конфет]...\nДля отмены ивента пропишите слово - stop```***'),
                ephemeral=True)

            def check(m):
                if m.channel == channel:
                    if not m.author.bot:
                        return m

            msg = await self.client.wait_for('message', check=check)

            if msg.author.id == ctx.user.id and msg.content == STOP_WORD:
                cross_event_system.delete_clan_event(guild_id=server.id, message_id=get_msg.id)
                cross_event_system.set_member_request(guild_id=server.id, clan_staff_id=ctx.user.id)
                await decline_event_embed(
                    user=server.get_member(ctx.user.id), request_msg=get_msg, clan_name=clan_n, event_num=ev_num,
                    clan_staff=user, decline_view=View()
                )
                await msg.delete()
                print(ev_num, com, clan_n, user.name, 'Ивент отменен!')

            if msg.author.id == interact.user.id:
                sum_time_event = sum_event_time(guild=server.id, message_id=message.id)

                await pass_event_embed(
                    request_msg=get_msg, event_num=ev_num, clan_name=clan_n,
                    clan_staff=user, sum_time_event=sum_time_event,
                    time_accept_request=time_accept, comment=com,
                    pass_view=View(), end_result=msg.content
                )

                cross_event_system.pass_clan_event(guild_id=server.id, clan_staff_id=user.id,
                                                   waisting_time=int(time.time()) - int(time_accept))
                save_stats_system.add_stat(guild_id=server.id, clan_staff_id=user.id,
                                           waisting_time=int(time.time()) - int(time_accept))
                cross_event_system.delete_clan_event(guild_id=server.id, message_id=message.id)
                event_history.note_history(guild_id=server.id, clan_staff_id=user.id, name=ev_num,
                                           time=int(time.time()) - int(time_accept), date_end=int(time.time()),
                                           clan_name=clan_n)

                xp, quest_timer = quest_info(server.id, user.id)
                if ev_num in xp:
                    if int(time.time()) - int(time_accept) // 60 >= quest_timer[ev_num]:
                        # если прошел квест, засчитывает его в профиль
                        cross_event_system.update_xp_counter(guild_id=server.id, clan_staff_id=user.id, xp=xp[ev_num])
                        quest_system.remove_quest(guild_id=server.id, clan_staff_id=user.id, name=ev_num)
                        # просмотр опытна на данный момент
                        current_xp = cross_event_system.get_xp_count(guild_id=server.id, clan_staff_id=user.id)
                        current_level = xp_to_lvl(current_xp)
                        # присваивание уровня в соотношении опыта
                        cross_event_system.set_lvl(guild_id=server.id, clan_staff_id=user.id, lvl=int(current_level))
                await msg.delete()

                member = server.get_member(user.id)
                analitic_msg = await member.send(
                    embed=DefaultEmbed('***```Понравился ли вам ивент?\nДайте свой коментарий.```***'))

                def check(m):
                    if m.channel == analitic_msg.channel:
                        return m

                msg = await self.client.wait_for('message', check=check, timeout=120)
                answer = str(msg.content)
                await get_event_channel.send(content=f"{msg.author.mention} отправил отзыв:",
                                             embed=DefaultEmbed(f'{answer}'))
                await member.send(embed=DefaultEmbed('***```Большое спасибо за отзыв!```***'))

        event_view_builder.button_decline.callback = decline_callback
        event_view_builder.button_accept.callback = accept_callback
        event_view_builder.button_pass.callback = pass_callback
