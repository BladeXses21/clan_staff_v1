from cogs.base import BaseCog
from service.close_service import CloseService


class CloseMode(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        self.close_service = CloseService(client)
        print("Cog 'clan close' connected!")

    # close = discord.SlashCommandGroup('close', 'commands to request close')
    #
    # @close.command(name='request', description='Запрос клоза клан на клан', default_permission=True)
    # async def request(self, interaction: Interaction,
    #                   game_name: Option(int, 'выберите ивент который желаете сыграть', required=True),
    #                   member: Option(discord.Member, 'Укажите пользователя с вражеского клана.', required=True),
    #                   users_count: Option(int, 'Сколько людей у вас собралось?.', required=True),
    #                   comment: Option(str, 'Введите коментарий к ивенту.', required=False)):

    # todo - вызвать функцию self.close_service

    # @close.command(name='profile', description='Просмотреть профиль клозов', default_permission=True)
    # async def profile(self, interaction: Interaction, member: discord.Member = None):
    #     if member is not None:
    #         return await interaction.response.send_message(embed=ProfileClose(user_avatar=member.avatar.url, user_name=interaction.user.name,
    #                                                                           game_counter=10, rating=str(333), winrate=str(46), first_game=int(time.time()),
    #                                                                           last_game=int(time.time()), clan='Clown').embed)


def setup(bot):
    bot.add_cog(CloseMode(bot))
