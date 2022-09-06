import discord
from discord import Interaction

from cogs.base import BaseCog
from config import YUKI_ID
from database.game_system.hero_system import hero_system
from embeds.game.player_game.inventory_embed import HeroInventoryEmbed
from service.game_player_service import GameService


class BossGamePlayer(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        self.game_service = GameService(client)
        print("Cog 'boss-game player commands' connected!")

    games = discord.SlashCommandGroup('game', 'commands to game for user', guild_ids=[YUKI_ID])

    @games.command(name='boss', description='Show boss Embed')
    async def boss(self, interaction: Interaction):
        await self.game_service.boss(interaction)

    @games.command(name='attack_enemy', description='Attack enemy')
    async def attack_enemy(self, interaction: Interaction):
        await self.game_service.attack_enemy(interaction)

    @games.command(name='profile', description='Show user stats in boss event')
    async def profile(self, interaction: Interaction):
        await self.game_service.profile(interaction)

    @games.command(name='inventory', description='Show ur inventory')
    async def inventory(self, interaction: Interaction):
        await self.game_service.inventory(interaction)

    @games.command(name='equip_item', description='Equip item from ur inventory')
    async def equip_item(self, interaction: Interaction, item_index: int):
        await self.game_service.equip(interaction=interaction, index=item_index)

    @games.command(name='remove_item', description='remove item from ur inventory')
    async def remove_item(self, interaction: Interaction, item_index: int):
        hero = hero_system.get_hero_by_user(interaction.user)
        inventory = hero.inventory
        inventory.remove_item(item_index)

        hero_system.modify_inventory(hero)
        await interaction.response.send_message(embed=HeroInventoryEmbed(hero, item_index))


def setup(bot):
    bot.add_cog(BossGamePlayer(bot))
