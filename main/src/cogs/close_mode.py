import discord
from discord import Option, Interaction

from cogs.base import BaseCog
from service.close_service import CloseService
from utils.close_enum import CloseEnumList


class CloseMode(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        self.close_service = CloseService(client)
        print("Cog 'clan close' connected!")

    close = discord.SlashCommandGroup('close', 'commands to request close', guild_ids=[798264256231243816])

    # @close.command(name='request', description='Запрос клоза клан на клан', default_permission=True)
    # async def request(self, interaction: Interaction,
    #                   game_name: Option(str, 'Выберите ивент', choices=CloseEnumList.list(), required=True),
    #                   member: Option(discord.Member, 'Укажите пользователя с вражеского клана.', required=True),
    #                   users_count: Option(int, 'Сколько людей у вас собралось?.', required=True),
    #                   comment: Option(str, 'Введите коментарий к ивенту.', required=False)):
    #     await self.close_service.closeRequest(member=member, game_name=game_name, users_count=users_count,
    #                                           comment=comment, interaction=interaction)


def setup(bot):
    bot.add_cog(CloseMode(bot))
