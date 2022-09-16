from discord import Colour, Embed

from extensions.funcs import equipped_item_string
from models.game_model.lifeform_types.hero_type import Hero


class HeroInventoryEmbed(Embed):
    def __init__(self, hero: Hero, selected: int):
        super().__init__(title=f'{hero.name} inventory: ', color=Colour(0x292b2f))
        self.cursor = '<:arrow:959084748796465222>'
        inventory = hero.inventory
        equipped = inventory.equipped

        items_string = equipped_item_string(equipped)

        i = 1
        for item in inventory.items:
            if i == selected:
                items_string = f'{items_string}\n{self.cursor} {i}.  {item}'
            else:
                items_string = f"{items_string}\n{i}.  {item}"
            i = i + 1
        self.description = f"{items_string}"
