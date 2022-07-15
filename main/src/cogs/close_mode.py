import discord
import requests
from discord import Option

from database.systems.server_system import cross_server_system
from extensions.funcs import is_member_in_voice, get_clan_channel_names, total_amount
from utils.close_enum import ClanCloseEnum
from cogs.base import BaseCog
from embeds.clan_embed.clan_close.close import ClanCloseEmbed
from embeds.clan_embed.clan_close.accepted_close import AcceptedClanCloseEmbed
from embeds.base import DefaultEmbed
from main import client
from database.systems.event_system import cross_event_system


class CrossCloseRequest(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        print("Cog 'clan close' connected!")

    # close = discord.SlashCommandGroup('event', 'commands to request event')
    #
    # @close.command(name='request', description='Запрос клоза клан на клан', default_permission=True)
    # async def request(self, interaction: discord.Interaction,
    #                   game_name: Option(int, 'выберите ивент который желаете сыграть', required=True),
    #                   member: Option(discord.Member, 'Укажите пользователя с вражеского клана.', required=True),
    #                   users_count: Option(int, 'Сколько людей у вас собралось?.', required=True),
    #                   comment: Option(str, 'Введите коментарий к ивенту.', required=False)):
    #
    #     author = requests.get(f'https://yukine.ru/api/members/{interaction.guild.id}/{interaction.user.id}')
    #     authpr_info = author.json()
    #     member = requests.get(f'https://yukine.ru/api/members/{interaction.guild.id}/{member.id}')
    #     member_info = member.json()
    #     guild = interaction.guild
    #
    #     event_channel = cross_server_system.get_event_channel(guild.id)
    #
    #     if game_name == 'Dota 2 5x5' or 'CS:GO 5x5' and users_count < 5:
    #         return await interaction.response.send_message(embed=DefaultEmbed(f'***```{interaction.user.name}, количество указаных участников не подходит под данный ивент.```***'))
    #     if comment is None:
    #         comment = 'No comments...'
    #     channel_id, role_id, text_category_id, voice_category_id = cross_event_system.get_all_by_guild_id(guild.id)
    #     member_ids = is_member_in_voice(guild.categories, client.get_channel(voice_category_id).name)
    #
    #     if interaction.user.id not in member_ids:
    #         return await interaction.response.send_message(
    #             embed=DefaultEmbed(f'***```Вы должны быть в голосовом канале клана.```***'),
    #             ephemeral=True
    #         )
    #
    #     await interaction.response.send_message(embed=DefaultEmbed((f'**Отправитель:** {interaction.user.mention}\n***```Запрос на клоз был успешно отправлен.```***'
    #                                                                 f'\n***```Дождитесь ответа ивентёра...```***')), ephemeral=True)

        # try:
        #     await interaction.user.send(embed=DefaultEmbed(f'**Отправитель:** {interaction.user.mention}\n***```Запрос на клоз был успешно отправлен.```***'
        #                                                    f'\n***```Дождитесь ответа...```***\n**Получатель клан:** {member_info["clan"]["name"]}.'))
        #     response_enemy_clan = await interaction.response.send_message(embed=ClanCloseEmbed(event_name=game_name, clan_name=clan_name, comment=comment).embed)
        # except discord.Forbidden:
        #     await interaction.response.send_message(embed=DefaultEmbed(f'**Отправитель:** {interaction.user.mention}\n***```Запрос на клоз был успешно отправлен.```***'
        #                                                                f'\n***```Дождитесь ответа...```***\n**Получатель клан:** {member_info["clan"]["name"]}.'), ephemeral=True)
        #     response_enemy_clan = await interaction.response.send_message(embed=ClanCloseEmbed(event_name=game_name, clan_name=clan_name, comment=comment).embed)

        # async def enemy_accept_callback(ctx: discord.Interaction):
        #     pass
        #
        #     async def acccept_callback(inter: discord.Interaction):
        #         pass
        #
        #     async def decline_callback(inter: discord.Interaction):
        #         pass
        #
        # async def enemy_decline_callback(ctx: discord.Interaction):
        #     pass


def setup(bot):
    bot.add_cog(CrossCloseRequest(bot))
