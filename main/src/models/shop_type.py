import random

from pydantic import BaseModel

from config import chances_for_items
from systems.cross_events.cross_event_system import cross_event_system
from utils.item_rarity_enum import EnumItemRarity

things_chance = [EnumItemRarity.common] * chances_for_items['common'] + \
                [EnumItemRarity.rare] * chances_for_items['rare'] + \
                [EnumItemRarity.mythical] * chances_for_items['mythical'] + \
                [EnumItemRarity.legendary] * chances_for_items['legendary'] + \
                [EnumItemRarity.immortal] * chances_for_items['immortal']


def get_random_item():
    random_things = random.choice(things_chance)
    remaining_item = cross_event_system.get_item_by_rarity(random_things)
    return random.choice(remaining_item)


class Item(BaseModel):
    name: str
    rarity: EnumItemRarity = EnumItemRarity.common

    def __str__(self):
        return f"{self.rarity.rarityIcon()} {self.name}"

# todo - сдлеать drop down menu с выбокой item rarity и указанием его названия через wait for в панели управления clan staff
