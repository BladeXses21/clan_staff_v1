import discord
from discord import Option

from base.funcs import is_member_in_voice, get_clan_channel_names
from clan_staff_service.close_list import CloseListEnum
from cogs.base import BaseCog
from embeds.clan_events_mode.request_close_embed.embed_to_enemy_clan import RequestToEnemy
from embeds.clan_events_mode.request_close_embed.enemy_accept_close import EnemyAcceptClose
from embeds.def_embed import DefaultEmbed
from main import client
from systems.clan_staff.cross_event_system import cross_event_system


class CrossCloseRequest(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        print("Cog 'clan close' connected!")

    # close = discord.SlashCommandGroup('event', 'commands to request event')
    #
    # @close.command(name='request', description='Запрос клоза клан на клан', default_permission=True)
    # async def request(self, interaction: discord.Interaction,
    #                   game_name: Option(int, 'выберите ивент который желаете сыграть', required=True),
    #                   clan_name: Option(discord.TextChannel, 'укажите текстовый канал клана, для отправки запроса.', required=True),
    #                   users_count: Option(int, 'Сколько людей у вас собралось?.', required=True),
    #                   comment: Option(str, 'Введите коментарий к ивенту.', required=False)):
    #     guild = interaction.guild
    #     if game_name == 'Dota 2 5x5' or 'CS:GO 5x5' and users_count < 5:
    #         return await interaction.response.send_message(embed=DefaultEmbed(f'***```{interaction.user.name}, количество указаных участников не подходит под данный ивент.```***'))
    #     if comment is None:
    #         comment = 'No comments...'
    #     channel_id, role_id, text_category_id, voice_category_id = cross_event_system.get_all_by_guild_id(guild.id)
    #     member_ids = check_member_on_voice(guild.categories, client.get_channel(voice_category_id).name)
    #     text_channel_list = clan_text_channel_list(interaction, client.get_channel(text_category_id).name)
    #
    #     if interaction.user.id in member_ids:
    #         if clan_name in text_channel_list:
    #             clan_name = interaction.user.voice.channel.name
    #             try:
    #                 await interaction.user.send(embed=DefaultEmbed(f'**Отправитель:** {interaction.user.mention}\n***```Запрос на клоз был успешно отправлен.```***'
    #                                                                f'\n***```Дождитесь ответа...```***\n**Получатель клан:** {clan_name}.'))
    #                 response_enemy_clan = await interaction.response.send_message(embed=RequestToEnemy(event_name=game_name, clan_name=clan_name, comment=comment).embed)
    #             except discord.Forbidden:
    #                 await interaction.response.send_message(embed=DefaultEmbed(f'**Отправитель:** {interaction.user.mention}\n***```Запрос на клоз был успешно отправлен.```***'
    #                                                                            f'\n***```Дождитесь ответа...```***\n**Получатель клан:** {clan_name}.'), ephemeral=True)
    #                 response_enemy_clan = await interaction.response.send_message(embed=RequestToEnemy(event_name=game_name, clan_name=clan_name, comment=comment).embed)
    #
    #             async def enemy_accept_callback(ctx: discord.Interaction):
    #                 response_enemy_clan.edit(embed=EnemyAcceptClose())
    #                 pass
    #
    #                 async def acccept_callback(inter: discord.Interaction):
    #                     pass
    #
    #                 async def decline_callback(inter: discord.Interaction):
    #                     pass
    #
    #             async def enemy_decline_callback(ctx: discord.Interaction):
    #                 pass


def setup(bot):
    bot.add_cog(CrossCloseRequest(bot))
