import discord
from discord.ext import commands
import urllib.request

from cogs.base import BaseCog
from discord import slash_command, Interaction, Bot, ApplicationContext, Option

from config import PERMISSION_ROLE, OWNER_IDS, YUKI_ID
from database.game_system.battle_system import battle_system
from database.game_system.boss_system import boss_system
from database.game_system.items_system import items_system
from embeds.base import DefaultEmbed
from embeds.game.admin_game.admin_help_embed import AdminHelpEmbed
from embeds.game.admin_game.boss_drop_embed import BossDropEmbed
from extensions.logger import staff_logger
from models.game_model.inventory_types.item_types import EnumItemTypes, EnumItemRarity, Item
from service.game_admin_service import GameAdminService


class GameAdmin(BaseCog):
    def __init__(self, client: Bot):
        super().__init__(client)
        self.game_admin_service = GameAdminService(client)
        print('Cog "GameAdmin connected"')

    admins = discord.SlashCommandGroup('admin', 'commands to game for admin', guild_ids=[YUKI_ID])

    @commands.group(aliases=['админ'])
    @commands.has_any_role(*PERMISSION_ROLE)
    async def admin(self, ctx):
        if not ctx.invoked_subcommand:
            staff_logger.info(f'{ctx.author} use !admin command')
            if ctx.author.id in OWNER_IDS:
                return await ctx.send(embed=AdminHelpEmbed().embed, delete_after=60)
            else:
                pass

    # region ADMIN MENU COMMAND - FOR ADMIN
    @admins.command(name='admin_menu', description='Вызывает меню админа')
    @commands.has_any_role(*PERMISSION_ROLE)
    async def admin_menu(self, interaction: Interaction):
        await self.game_admin_service.adminMenu(interaction)

    # endregion
    # region START GAME COMMAND - FOR ADMIN
    @admins.command(name='start', description='start game', guild_ids=[YUKI_ID])
    @commands.has_any_role(*PERMISSION_ROLE)
    async def start(self, interaction: Interaction):
        boss = boss_system.get_random_boss()
        battle_system.start_new_battle(boss)
        #   - todo event start embed
        await interaction.response.send_message(
            embed=DefaultEmbed(description=f'***```Boss {boss.name} was born in hell to destroy the world!```***'))

    # endregion
    # region CREATE ENEMY COMMAND - FOR ADMIN
    @admin.command(description='Создать боса для игры | Create enemy for game')
    @commands.has_any_role(*PERMISSION_ROLE)
    async def create_enemy(self, interaction: Interaction, name: str, health: int, attack_dmg: int, image: str):
        try:
            urllib.request.urlopen(image)
        except ValueError | TypeError as e:
            return await interaction.response.send_message(embed=DefaultEmbed(f'***```{interaction.user.name}, check link.\n{str(e)}.```***'),
                                                           delete_after=20)
        boss_system.create_boss(name=name, health=health, attack_dmg=attack_dmg, image=image)
        await interaction.response.send_message(
            embed=DefaultEmbed(f'***```boss {name} has been created```***\nhis argument n:{name} h:{health} a:{attack_dmg} i:{image}'))

    # endregion
    # region CREATE ITEM COMMAND - FOR ADMIN
    @admins.command(name='create_item', description='Создать предмет для игры | Create new item in game')
    @commands.has_any_role(*PERMISSION_ROLE)
    async def create_item(self, interaction: Interaction, name: str,
                          item_type: Option(EnumItemTypes, 'chose item type', choices=EnumItemTypes.list(), required=True),
                          rarity: Option(str, 'chose item rarity', choices=EnumItemRarity.list(), required=True) = EnumItemRarity.common):
        items_system.create_new_item(item=Item(name=name, type=item_type, rarity=rarity))
        await interaction.response.send_message(embed=DefaultEmbed(f'***```{interaction.user.name}, вы добавили {name} типу {item_type}```***'))

    # endregion
    # region ADD BOSS DROP COMMAND - FOR ADMIN
    @admins.command(name='add_boss_drop', description='add item drop for boss')
    @commands.has_any_role(*PERMISSION_ROLE)
    async def add_boss_drop(self, interaction: Interaction, boss_name: str, item_name: str):
        await self.game_admin_service.add_drop(interaction, boss_name, item_name)

    # endregion
    # region REMOVE BOSS DROP - FOR ADMIN
    @admins.command(name='remove_boss_drop', description='remove item drop from boss')
    @commands.has_any_role(*PERMISSION_ROLE)
    async def remove_boss_drop(self, interaction: Interaction, boss_name: str, item_index: int):
        boss = boss_system.get_by_name(boss_name)
        boss.inventory.remove_item(item_index)
        boss_system.modify_inventory(boss)
        return await interaction.response.send_message(embed=BossDropEmbed(boss).embed)

    # endregion
    # region SEE BOSS INVENTORY - FOR ADMIN
    @admins.command(name='see_boss_inventory', description='show boss inventory')
    @commands.has_any_role(*PERMISSION_ROLE)
    async def see_boss_inventory(self, interaction: Interaction, boss_name: str):
        boss = boss_system.get_by_name(boss_name)
        return await interaction.response.send_message(embed=BossDropEmbed(boss).embed)
    # endregion


def setup(bot):
    bot.add_cog(GameAdmin(bot))
