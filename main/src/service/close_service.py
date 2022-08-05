import requests
from discord import Interaction, ApplicationContext, Member
from discord.ui import View

from config import RIGHT_AMOUNT_PEOPLE
from database.systems.event_system import cross_event_system
from database.systems.server_system import cross_server_system
from embeds.base import DefaultEmbed
from embeds.clan_embed.clan_close.accepted_close import accept_enemy_embed
from embeds.clan_embed.clan_close.enemy_response import request_to_the_enemy
from embeds.clan_embed.view_builders.event_view_builder import event_view_builder
from extensions.funcs import is_member_in_voice


class CloseService:
    def __init__(self, client):
        self.client = client

    async def close_request(self, member: Member, game_name, comment, users_count, interaction: Interaction, ctx: ApplicationContext = None):

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
        channel_id, role_id, text_category_id, voice_category_id = cross_event_system.get_all_by_guild_id(server.id)
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

        choice_view = event_view_builder.create_event_request_view()
        event_channel = cross_server_system.get_event_channel(server.id)

        enemy_txt_channel = self.client.get_channel(member_info['clan']['textId'])
        response_msg = await request_to_the_enemy(interaction, member_send=author, enemy_channel=enemy_txt_channel, event_name=game_name, clan_name=enemy_txt_channel.name, comment=comment,
                                                  view=choice_view)

        async def enemy_accept_callback(interact: Interaction):
            if interact.user.id not in member_info['members']:
                pass
            # todo - добавить view для ивентеров в этой функции
            await accept_enemy_embed(member_send=author, request_msg=response_msg, clan_name=enemy_txt_channel.name, enemy_member=interact.user, view=View(), event_channel=event_channel,
                                     event_name=game_name, clan_enemy=enemy_txt_channel.name)

            async def closemod_acccept_callback(inter: Interaction):
                pass

            async def closemod_decline_callback(inter: Interaction):
                pass

        async def enemy_decline_callback(interact: Interaction):
            if interact.user.id not in member_info['members']:
                pass

        event_view_builder.button_accept.callback = enemy_accept_callback
        event_view_builder.button_decline.callback = enemy_decline_callback
