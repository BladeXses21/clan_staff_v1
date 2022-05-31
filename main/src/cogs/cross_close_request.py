import discord
import requests
from discord import Option

from extensions.funcs import is_member_in_voice, get_clan_channel_names
from utils.close_enum import ClanCloseEnum
from cogs.base import BaseCog
from embeds.clan_events_mode.clan_close.close import ClanCloseEmbed
from embeds.clan_events_mode.clan_close.accepted_close import AcceptedClanCloseEmbed
from embeds.base import DefaultEmbed
from main import client
from systems.cross_events.cross_event_system import cross_event_system


class CrossCloseRequest(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        print("Cog 'clan close' connected!")

        # @commands.command(name='test')
        # async def test(self, ctx, guild_id, member_id):
        #     url = f'https://yukine.ru/api/members/{guild_id}/{member_id}'
        #     r = requests.get(url)
        #     the_user = r.json()
        #     print(the_user['clan']['textId'])

    # close = discord.SlashCommandGroup('event', 'commands to request event')
    #
    # @close.command(name='request', description='Запрос клоза клан на клан', default_permission=True)
    # async def request(self, interaction: discord.Interaction,
    #                   game_name: Option(int, 'выберите ивент который желаете сыграть', required=True),
    #                   member: Option(discord.Member, 'Укажите пользователя с вражеского клана.', required=True),
    #                   users_count: Option(int, 'Сколько людей у вас собралось?.', required=True),
    #                   comment: Option(str, 'Введите коментарий к ивенту.', required=False)):
    #
    #     r = requests.get(f'https://yukine.ru/api/members/{interaction.guild.id}/{member.id}')
    #     enemy = r.json()
    #     guild = interaction.guild
    #
    #     if game_name == 'Dota 2 5x5' or 'CS:GO 5x5' and users_count < 5:
    #         return await interaction.response.send_message(embed=DefaultEmbed(f'***```{interaction.user.name}, количество указаных участников не подходит под данный ивент.```***'))
    #     if comment is None:
    #         comment = 'No comments...'
    #     channel_id, role_id, text_category_id, voice_category_id = cross_event_system.get_all_by_guild_id(guild.id)
    #     member_ids = is_member_in_voice(guild.categories, client.get_channel(voice_category_id).name)
    #
    #     if interaction.user.id in member_ids:
    #         clan_name = interaction.user.voice.channel.name
    #         try:
    #             await interaction.user.send(embed=DefaultEmbed(f'**Отправитель:** {interaction.user.mention}\n***```Запрос на клоз был успешно отправлен.```***'
    #                                                            f'\n***```Дождитесь ответа...```***\n**Получатель клан:** {enemy["clan"]["name"]}.'))
    #             response_enemy_clan = await interaction.response.send_message(embed=ClanCloseEmbed(event_name=game_name, clan_name=clan_name, comment=comment).embed)
    #         except discord.Forbidden:
    #             await interaction.response.send_message(embed=DefaultEmbed(f'**Отправитель:** {interaction.user.mention}\n***```Запрос на клоз был успешно отправлен.```***'
    #                                                                        f'\n***```Дождитесь ответа...```***\n**Получатель клан:** {enemy["clan"]["name"]}.'), ephemeral=True)
    #             response_enemy_clan = await interaction.response.send_message(embed=ClanCloseEmbed(event_name=game_name, clan_name=clan_name, comment=comment).embed)
    #
    #         async def enemy_accept_callback(ctx: discord.Interaction):
    #             response_enemy_clan.edit(embed=AcceptedClanCloseEmbed(clan_name).embed)
    #             pass
    #
    #             async def acccept_callback(inter: discord.Interaction):
    #                 pass
    #
    #             async def decline_callback(inter: discord.Interaction):
    #                 pass
    #
    #         async def enemy_decline_callback(ctx: discord.Interaction):
    #             pass


def setup(bot):
    bot.add_cog(CrossCloseRequest(bot))
