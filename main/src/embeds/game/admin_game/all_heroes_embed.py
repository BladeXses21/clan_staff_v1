from discord import Embed, Colour
import numpy as np
from database.game_system.hero_system import hero_system
from extensions.funcs import equipped_item_string


class AllHeroesEmbed(object):
    def __init__(self, selected: int, set_index: int = 10):
        self._embed = Embed(title=f'all heroes:', color=Colour(0x292b2f))
        self.cursor = '<:arrow:959084748796465222>'

        heroes = hero_system.get_all_heroes()
        var = []
        if heroes is None:
            return

        heroes_string = ''
        all_items = 'all items:\n'
        count = 1

        for i in range(0, len(heroes), set_index):
            var = heroes[i:i + set_index]
        for hero in var:
            inventory = hero.inventory
            equipped = inventory.equipped

            items_string = equipped_item_string(equipped)

            if count == selected:
                try:
                    for item in inventory.items:
                        all_items += f'{item.name} | {item.type} | {item.rarity}\n'
                    heroes_string = f"{heroes_string}\n{self.cursor}**{count}.** name: **`{hero.name}`**\n {all_items} \nmax_size:{inventory.max_size} \n{items_string}"
                except IndexError:
                    heroes_string = f"{heroes_string}\n{self.cursor}**{count}.** name: **`{hero.name}`**\n {inventory.items} {inventory.max_size} {inventory.equipped}"
            else:
                heroes_string = f"{heroes_string}\n**{count}.** name: **`{hero.name}`**"
            np.delete(hero, count)
            count = count + 1
            if count > set_index:
                break

        self._embed.description = str(heroes_string)

    @property
    def embed(self):
        return self._embed
