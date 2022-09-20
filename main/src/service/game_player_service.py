from discord import Interaction, ApplicationContext

from config import HERO_CLASS_BY_INDEX, HERO_CLASS_ARRAY
from database.game_system.battle_system import battle_system
from database.game_system.hero_system import hero_system
from embeds.base import DefaultEmbed
from embeds.game.game_view_builder.choose_class_view_builder import ChooseClassView
from embeds.game.game_view_builder.fight_view_builder import FightView
from embeds.game.game_view_builder.inventory_view_builder import InventoryView
from embeds.game.game_view_builder.profile_view_builder import ProfileView
from embeds.game.player_game.battle_embed import BattleEmbed
from embeds.game.player_game.choice_class_embed import ChoiceClassEmbed
from embeds.game.player_game.hero_embed import HeroStatsEmbed
from embeds.game.player_game.hit_embed import HitEmbed
from embeds.game.player_game.inventory_embed import HeroInventoryEmbed


class GameService:

    def __init__(self, client):
        self.client = client

    async def boss(self, interaction: Interaction, ctx: ApplicationContext = None):
        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        hero_system.get_hero_by_user(ctx.user)
        battle = battle_system.get_current_battle()

        async def attack_callback(interact: Interaction):
            fight_view.disable_attack(battle.is_over())

            await self.attack_enemy(interaction=interact, ctx=ctx)

        async def profile_callback(interact: Interaction):
            await self.profile(interaction=interact, ctx=ctx)

        fight_view = FightView(attack_callback, profile_callback)
        fight_view.disable_attack(battle.is_over())

        if interaction.message is None:
            await interaction.response.send_message(embed=BattleEmbed(battle, interaction.user.id),
                                                    view=fight_view, ephemeral=True)
        else:
            await interaction.response.edit_message(embed=BattleEmbed(battle, interaction.user.id),
                                                    view=fight_view)

    async def profile(self, interaction: Interaction, ctx: ApplicationContext = None):
        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        hero = hero_system.get_hero_by_user(ctx.user)

        async def inventory_callback(interact: Interaction):
            await self.inventory(interact, ctx)  # inventory command update view by yourself

        async def back_callback(interact: Interaction):
            await self.boss(interact, ctx)

        async def choose_class_callback(interact: Interaction):
            if hero_system.check_hero_on_the_class_by_user(ctx.user) is True:
                return False
            await self.choice_class(interact, ctx)
            return True

        profile_view = ProfileView(back_callback, inventory_callback, choose_class_callback)
        profile_view.disable_choice_class(hero_system.check_hero_on_the_class_by_user(ctx.user))

        if interaction.message is None:
            await interaction.response.send_message(embed=HeroStatsEmbed(hero), view=profile_view, ephemeral=True)
        else:
            print(interaction.message.to_message_reference_dict())
            await interaction.response.edit_message(embed=HeroStatsEmbed(hero), view=profile_view)

    async def choice_class(self, interaction: Interaction, ctx: ApplicationContext = None, index: int = 1):
        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        hero = hero_system.get_hero_by_user(ctx.user)

        index = len(HERO_CLASS_ARRAY) if index < 1 else 1 if index > len(HERO_CLASS_ARRAY) else index

        async def back_callback(interact: Interaction):
            await self.inventory(interact, ctx)

        async def up_callback(interact: Interaction):
            await self.choice_class(interact, ctx, index - 1)

        async def down_callback(interact: Interaction):
            await self.choice_class(interact, ctx, index + 1)

        async def choose_callback(interact: Interaction):
            await self.choose_class(interact, ctx, index)

        choose_class_view = ChooseClassView(back_callback, up_callback, down_callback, choose_callback, index)

        if interaction.message is None:
            await interaction.response.send_message(embed=ChoiceClassEmbed(hero, index),
                                                    view=choose_class_view, ephemeral=True)
        else:
            await interaction.response.edit_message(embed=ChoiceClassEmbed(hero, index),
                                                    view=choose_class_view)

    async def inventory(self, interaction: Interaction, ctx: ApplicationContext = None, index: int = 1):
        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        hero = hero_system.get_hero_by_user(ctx.user)
        inventory = hero.inventory

        index = len(inventory.items) if index < 1 else 1 if index > len(inventory.items) else index

        async def back_callback(interact: Interaction):
            await self.profile(interact, ctx)

        async def up_callback(interact: Interaction):
            await self.inventory(interact, ctx, index - 1)

        async def down_callback(interact: Interaction):
            await self.inventory(interact, ctx, index + 1)

        async def equip_callback(interact: Interaction):
            await self.equip(interact, ctx, index)

        async def remove_item_callback(interact: Interaction):
            await self.remove_item(interact, ctx, index)

        inventory_view = InventoryView(back_callback, up_callback, down_callback, equip_callback, remove_item_callback)

        if interaction.message is None:
            await interaction.response.send_message(embed=HeroInventoryEmbed(hero, index),
                                                    view=inventory_view, ephemeral=True)
        else:
            await interaction.response.edit_message(embed=HeroInventoryEmbed(hero, index),
                                                    view=inventory_view)

    async def attack_enemy(self, interaction: Interaction, ctx: ApplicationContext = None):
        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        hero = hero_system.get_hero_by_user(ctx.user)

        if hero_system.check_hero_on_the_class_by_user(ctx.user) is False:
            return await self.choice_class(interaction, ctx)

        if hero.is_dead():
            return await interaction.response.send_message(embed=DefaultEmbed(f'***```You cant attack being dead !!!```***'),
                                                           delete_after=5,
                                                           ephemeral=True)
        battle = battle_system.get_current_battle()

        if not battle.fight_with(hero):
            return await interaction.response.send_message(embed=DefaultEmbed(description="***```Boss already dead```***"),
                                                           delete_after=3,
                                                           ephemeral=True)

        battle_system.update_current_battle(battle)
        hero_system.health_change(hero)

        if interaction.message is None:
            await interaction.channel.send(embed=HitEmbed(battle, hero))
        else:
            await interaction.response.edit_message(embed=HitEmbed(battle, hero))

        await self.boss(interaction, ctx)

    async def equip(self, interaction: Interaction, ctx: ApplicationContext = None, index: int = 1):
        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        hero = hero_system.get_hero_by_user(ctx.user)
        item_by_index = hero.inventory.item_by_index(index)

        if item_by_index is not None:
            hero.inventory.equip(item_by_index)
            hero_system.modify_inventory(hero)

        if interaction.message is None:
            await interaction.response.send_message(embed=HeroInventoryEmbed(hero, index), ephemeral=True)
        else:
            await interaction.response.edit_message(embed=HeroInventoryEmbed(hero, index))

    async def choose_class(self, interaction: Interaction, ctx: ApplicationContext = None, index: int = 1):
        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        hero = hero_system.get_hero_by_user(ctx.user)

        hero_system.add_class_to_hero(ctx.user, HERO_CLASS_BY_INDEX[index])
        await self.boss(interaction, ctx)
        await ctx.followup.send(embed=DefaultEmbed(f"***```class {HERO_CLASS_BY_INDEX[index]} selected```***"), ephemeral=True)

    async def remove_item(self, interaction: Interaction, ctx: ApplicationContext = None, index: int = 1):
        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        hero = hero_system.get_hero_by_user(ctx.user)

        hero.inventory.remove_item(index)
        hero_system.modify_inventory(hero)

        if interaction.message is None:
            await interaction.response.send_message(embed=HeroInventoryEmbed(hero, index), ephemeral=True)
        else:
            await interaction.response.edit_message(embed=HeroInventoryEmbed(hero, index))
