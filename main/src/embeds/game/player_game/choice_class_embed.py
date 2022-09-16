from discord import Embed, Colour

from config import HERO_CLASS_BY_INDEX, HERO_CLASS_ARRAY
from models.game_model.lifeform_types.hero_type import Hero


class ChoiceClassEmbed(Embed):
    def __init__(self, hero: Hero, selected: int):
        super().__init__(title=f'{hero.name} choice hero: ', color=Colour(0x292b2f))
        self.cursor = '<:arrow:959084748796465222>'

        class_string = f''
        i = 1

        for c in HERO_CLASS_ARRAY:
            if i == selected:
                class_string = f'{class_string}\n{self.cursor} {i}.  {c}'
            else:
                class_string = f"{class_string}\n{i}.  {c}"
            i = i + 1
        self.description = f"{class_string}"
