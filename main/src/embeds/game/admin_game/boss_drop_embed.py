from discord import Colour, Embed

from models.game_model.lifeform_types.boss_type import Enemy


class BossDropEmbed(object):
    def __init__(self, enemy: Enemy):
        self._embed = Embed(title=f'{enemy.name} can drop: ', color=Colour(0x292b2f))
        inventory = enemy.inventory

        items_string = ''
        for i in range(0, inventory.items.__len__()):
            items_string = f"{items_string}\n{i + 1}. {inventory.items.__getitem__(i).name}"
        self._embed.description = f"{items_string}"

    @property
    def embed(self):
        return self._embed
