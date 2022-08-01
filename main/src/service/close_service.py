import requests
from discord import Interaction, ApplicationContext, Member, Forbidden

from database.systems.event_system import cross_event_system
from database.systems.server_system import cross_server_system
from embeds.base import DefaultEmbed
from embeds.clan_embed.clan_close.enemy_response import ClanCloseEmbed
from embeds.clan_embed.view_builders.event_view_builder import event_view_builder
from extensions.funcs import is_member_in_voice


class CloseService:
    def __init__(self, client):
        self.client = client

    async def close_request(self, member: Member, game_name, comment, users_count, interaction: Interaction, ctx: ApplicationContext = None):

        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        author = requests.get(f'https://yukine.ru/api/members/{interaction.guild.id}/{interaction.user.id}')
        author_info = author.json()
        member = requests.get(f'https://yukine.ru/api/members/{interaction.guild.id}/{member.id}')
        member_info = member.json()
        guild = interaction.guild

        accept_view = event_view_builder.create_event_request_view()

        event_channel = cross_server_system.get_event_channel(guild.id)

        if game_name == 'Dota 2 5x5' or 'CS:GO 5x5' and users_count < 5:
            return await interaction.response.send_message(embed=DefaultEmbed(f'***```{interaction.user.name}, количество указаных участников не подходит под данный ивент.```***'))
        if comment is None:
            comment = 'No comments...'
        channel_id, role_id, text_category_id, voice_category_id = cross_event_system.get_all_by_guild_id(guild.id)
        member_ids = is_member_in_voice(guild.categories, self.client.get_channel(voice_category_id).name)

        if interaction.user.id not in member_ids:
            return await interaction.response.send_message(
                embed=DefaultEmbed(f'***```Вы должны быть в голосовом канале клана.```***'),
                ephemeral=True
            )

        await interaction.response.send_message(embed=DefaultEmbed((f'**Отправитель:** {interaction.user.mention}\n***```Запрос на клоз был успешно отправлен.```***'
                                                                    f'\n***```Дождитесь ответа ивентёра...```***')), ephemeral=True)

        try:
            await interaction.user.send(embed=DefaultEmbed(f'**Отправитель:** {interaction.user.mention}\n***```Запрос на клоз был успешно отправлен.```***'
                                                           f'\n***```Дождитесь ответа...```***\n**Получатель клан:** {member_info["clan"]["name"]}.'))
            response_enemy_clan = await interaction.response.send_message(embed=ClanCloseEmbed(event_name=game_name, clan_name=member_info["clan"]["name"], comment=comment).embed,
                                                                          view=accept_view)
        except Forbidden:
            await interaction.response.send_message(embed=DefaultEmbed(f'**Отправитель:** {interaction.user.mention}\n***```Запрос на клоз был успешно отправлен.```***'
                                                                       f'\n***```Дождитесь ответа...```***\n**Получатель клан:** {member_info["clan"]["name"]}.'), ephemeral=True)
            response_enemy_clan = await interaction.response.send_message(embed=ClanCloseEmbed(event_name=game_name, clan_name=member_info["clan"]["name"], comment=comment).embed,
                                                                          view=accept_view)

        async def enemy_accept_callback(interact: Interaction):
            if interact.user.id not in member['members']:
                await response_enemy_clan.edit()

            async def acccept_callback(inter: Interaction):
                pass

            async def decline_callback(inter: Interaction):
                pass

        async def enemy_decline_callback(interact: Interaction):
            if interact.user.id not in member['members']:
                pass

        event_view_builder.button_accept.callback = enemy_accept_callback
        event_view_builder.button_decline.callback = enemy_decline_callback
