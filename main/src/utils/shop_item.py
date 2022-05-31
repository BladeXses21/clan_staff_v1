from enum import Enum, unique
import random

from pydantic import BaseModel

from systems.cross_events.cross_event_system import cross_event_system


@unique
class EnumItemRarity(str, Enum):
    common = 'common'
    rare = 'rare'
    mythical = 'mythical'
    legendary = 'legendary'
    immortal = 'immortal'


things_chance = [EnumItemRarity.common] * 50 + [EnumItemRarity.rare] * 20 + [EnumItemRarity.mythical] * 15 + [EnumItemRarity.legendary] * 10 + [EnumItemRarity.immortal]


def get_random_item():
    random_things = random.choice(things_chance)
    remaining_item = cross_event_system.get_item_by_rarity(random_things)
    return random.choice(remaining_item)


class Item(BaseModel):
    name: str
    rarity: EnumItemRarity = EnumItemRarity.common

    def __str__(self):
        return f"{self.rarity.rarity_by()} {self.name}"

# todo - сдлеать drop down menu с выбокой item rarity и указанием его названия через wait for в панели управления clan staff
