from discord import Interaction, ApplicationContext

from database.game_system.boss_system import boss_system
from extensions.logger import staff_logger


class GameAdminService:
    def __init__(self, client):
        self.client = client

    async def adminMenu(self, interaction: Interaction):
        staff_logger.info(f'{interaction.user} вызвал adminMenu')

        async def boss_callback(interact: Interaction):
            await self.gameBoss(interact)

        if interaction.message is None:
            await interaction.response.send_message(embed=None, view=None, ephemeral=True)
        else:
            await interaction.response.edit_message(embed=None, view=None)

    async def gameBoss(self, interaction: Interaction, index: int = 1):
        bosses = boss_system.get_all_bosses()
        index = len(bosses) if index < 1 else 1 if index > len(bosses) else index

        async def up_callback(interact: Interaction):
            await self.gameBoss(interact, index - 1)

        async def down_callback(interact: Interaction):
            await self.gameBoss(interact, index + 1)

        async def back_callback(interact: Interaction):
            await self.adminMenu(interact)
