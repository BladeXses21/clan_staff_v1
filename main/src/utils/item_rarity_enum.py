from enum import unique, Enum


@unique
class EnumItemRarity(str, Enum):
    common = 'common'
    rare = 'rare'
    mythical = 'mythical'
    legendary = 'legendary'
    immortal = 'immortal'

    def rarityIcon(self) -> str:
        if EnumItemRarity.common is self:
            return ":white_circle:"
        elif EnumItemRarity.rare is self:
            return ":blue_circle:"
        elif EnumItemRarity.mythical is self:
            return ":purple_circle:"
        elif EnumItemRarity.legendary is self:
            return ":yellow_circle:"
        elif EnumItemRarity.immortal is self:
            return ":red_circle:"
