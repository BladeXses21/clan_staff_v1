import requests
from discord import Interaction, ApplicationContext, Member
from discord.ui import View

from config import RIGHT_AMOUNT_PEOPLE, STOP_WORD
from database.systems.close_system import close_system
from database.systems.event_system import cross_event_system
from database.systems.server_system import cross_server_system
from embeds.base import DefaultEmbed
from embeds.clan_embed.clan_close.accepted_close_embed import accept_enemy_embed
from embeds.clan_embed.clan_close.decline_close_embed import decline_enemy_embed
from embeds.clan_embed.clan_close.enemy_response import request_to_the_enemy
from embeds.clan_embed.clan_close.running_close_embed import take_close_embed
from embeds.clan_embed.clan_close.winning_close_embed import pass_close_embed
from embeds.clan_embed.view_builders.close_view_builder import close_view_builder
from embeds.clan_embed.view_builders.event_view_builder import event_view_builder
from extensions.funcs import is_member_in_voice, sum_event_time
from extensions.logger import staff_logger


class CloseService:
    def __init__(self, client):
        self.client = client

    async def close_request(self, member: Member, game_name, comment, users_count, interaction: Interaction, ctx: ApplicationContext = None):
        staff_logger.info(f'{interaction.user} вызвал комаду /event request {member.name} {game_name} {comment} {users_count}')

        if ctx is None:
            ctx = await self.client.get_application_context(interaction)
        server = ctx.guild
        author = ctx.user

        if RIGHT_AMOUNT_PEOPLE[game_name] != users_count:
            return await interaction.response.send_message(
                embed=DefaultEmbed(f'***```{author.name}, количество указаных участников не подходит под данный ивент.\n Нужное количество: {RIGHT_AMOUNT_PEOPLE[game_name]}```***'),
                ephemeral=True)
        if comment is None:
            comment = 'No comments...'
        channel_id, role_id, text_category_id, voice_category_id = cross_event_system.get_cross_guild(server.id)
        member_ids = is_member_in_voice(server.categories, self.client.get_channel(voice_category_id).name)

        if author.id not in member_ids:
            return await interaction.response.send_message(
                embed=DefaultEmbed(f'***```Вы должны быть в голосовом канале клана.```***'),
                ephemeral=True
            )

        author_response = requests.get(f'https://yukine.ru/api/members/{server.id}/{author.id}')
        member_response = requests.get(f'https://yukine.ru/api/members/{server.id}/{member.id}')
        author_info = author_response.json()
        member_info = member_response.json()

        if author_info['clan']['name'] == member_info['clan']['name']:
            return await interaction.response.send_message(
                embed=DefaultEmbed(f'***```Вы из одного клана.```***'),
                ephemeral=True
            )

        choice_view = event_view_builder.create_event_request_view()
        event_channel = cross_server_system.get_event_channel(server.id)

        enemy_txt_channel = self.client.get_channel(member_info['clan']['textId'])
        enemy_msg = await request_to_the_enemy(interaction, member_send=author, enemy_channel=enemy_txt_channel, event_name=game_name, clan_name=enemy_txt_channel.name, comment=comment,
                                               view=choice_view)
        close_system.create_close(guild_id=server.id, event_name=game_name, member_send_request=author.id, clan_send_request=author_info['clan']['name'], comment=comment,
                                  enemy_msg_id=enemy_msg.id)

        async def enemy_accept_callback(interact: Interaction):
            if interact.user.id not in member_info['members']:
                return await interact.response.send_message(
                    embed=DefaultEmbed(f'***```{interact.user.name}, ты не являешься участником клана.```***'),
                    ephemeral=True)

            event_channel_msg = await accept_enemy_embed(member_send=author, request_msg=enemy_msg, clan_name=member_info['clan']['name'], member_enemy=interact.user, view=View(),
                                                         event_channel=event_channel, event_name=game_name, clan_enemy=enemy_txt_channel.name, staff_view=choice_view)
            close_system.enemy_accept_close(guild_id=interact.guild.id, enemy_msg_id=interact.message.id, close_message_id=event_channel_msg.id)

            async def closemod_acccept_callback(inter: Interaction):
                user = inter.user
                view = close_view_builder.wining_close()
                if cross_event_system.is_clan_staff(server.id, user.id) is False:
                    return await interact.response.send_message(
                        embed=DefaultEmbed(f'***```{user.name}, тебя нет в clan staff```***'),
                        ephemeral=True)

                if cross_event_system.is_event_completed(server.id, user.id) is False:
                    return await interact.response.send_message(
                        embed=DefaultEmbed(f'***```{user.name}, ты не закончил прошлый ивент.```***'),
                        ephemeral=True)

                close_system.staff_accept_close(guild_id=inter.guild.id, message_id=inter.message.id, clan_staff_id=inter.user.id)
                event_channel_message = await take_close_embed(event_channel_msg=inter.message.id, )

                async def team_one_win(inte: Interaction):
                    await inte.response.send_message(embed=DefaultEmbed(
                        f'***```{inte.user.name}, введите конечный итог ивента по форме\n@link [количество конфет] @link [количество конфет]...\nДля отмены ивента пропишите слово - stop```***'),
                        ephemeral=True)

                    def check(m):
                        if m.channel == inte.channel:
                            if not m.author.bot:
                                return m

                    msg = await self.client.wait_for('message', check=check)

                    if msg.author.id == ctx.user.id and msg.content == STOP_WORD:
                        # todo - закрытие ивента
                        await msg.delete()

                    if msg.author.id == interact.user.id:
                        sum_time_event = sum_event_time(guild=server.id, message_id=inte.message.id)

                        await pass_close_embed(reques_msg=event_channel_message, event_name=game_name, team_win=author_info['clan']['name'], team_lose=member_info['clan']['name'],
                                               clan_staff=inte.user, time_start=123, sum_time=sum_time_event, end_result=msg.content)

                async def team_two_win(inte: Interaction):
                    await inte.response.send_message(embed=DefaultEmbed(
                        f'***```{inte.user.name}, введите конечный итог ивента по форме\n@link [количество конфет] @link [количество конфет]...\nДля отмены ивента пропишите слово - stop```***'),
                        ephemeral=True)

                    def check(m):
                        if m.channel == inte.channel:
                            if not m.author.bot:
                                return m

                    msg = await self.client.wait_for('message', check=check)

                    if msg.author.id == ctx.user.id and msg.content == STOP_WORD:
                        # todo - закрытие ивента
                        await msg.delete()

                    if msg.author.id == interact.user.id:
                        sum_time_event = sum_event_time(guild=server.id, message_id=inte.message.id)

                        await pass_close_embed(reques_msg=event_channel_message, event_name=game_name, team_win=author_info['clan']['name'], team_lose=member_info['clan']['name'],
                                               clan_staff=inte.user, time_start=123, sum_time=sum_time_event, end_result=msg.content)

                async def draw_close(inte: Interaction):
                    pass

                async def reject_close(inte: Interaction):
                    pass

            async def closemod_decline_callback(inter: Interaction):
                user = inter.user
                if cross_event_system.is_clan_staff(server.id, user.id) is False:
                    return await interact.response.send_message(
                        embed=DefaultEmbed(f'***```{user.name}, тебя нет в clan staff```***'),
                        ephemeral=True)

                if cross_event_system.is_event_completed(server.id, user.id) is False:
                    return await interact.response.send_message(
                        embed=DefaultEmbed(f'***```{user.name}, ты не закончил прошлый ивент.```***'),
                        ephemeral=True)

            event_view_builder.button_accept.callback = closemod_acccept_callback
            event_view_builder.button_decline.callback = closemod_decline_callback

        async def enemy_decline_callback(interact: Interaction):
            if interact.user.id not in member_info['members']:
                return await interact.response.send_message(
                    embed=DefaultEmbed(f'***```{interact.user.name}, ты не являешься участником клана.```***'),
                    ephemeral=True)
            return await decline_enemy_embed(member_send=author, request_msg=enemy_msg, event_name=game_name, member_enemy=interact.user)

        event_view_builder.button_accept.callback = enemy_accept_callback
        event_view_builder.button_decline.callback = enemy_decline_callback
