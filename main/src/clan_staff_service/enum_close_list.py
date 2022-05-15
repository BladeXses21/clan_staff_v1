from enum import Enum, unique


@unique
class EnumCloseList(Enum):
    # events
    dota_close = 'Dota 2 5x5'
    cs_go_close = 'CS:GO 5x5'
    valorant_close = 'VALORANT 5x5'
    brawl_stars = 'Brawl Stars'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
