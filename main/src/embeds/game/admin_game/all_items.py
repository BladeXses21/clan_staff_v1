from discord import Embed, Colour

from database.game_system.items_system import items_system


class AllItemEmbed(object):
    def __init__(self):
        self._embed = Embed(title=f'all items:', color=Colour(0x292b2f))

        items = items_system.all_items()
        if items is None:
            return

        items_string = ''
        for i in range(0, items.__len__()):
            items_string = f"{items_string}\n{i + 1}. {items.__getitem__(i).name}"
        self._embed.description = f"{items_string}"

    @property
    def embed(self):
        return self._embed
