from enum import Enum, unique


@unique
class CloseEnumList(Enum):
    # events
    dota = 'Dota 2 5x5'
    cs_go = 'CS:GO 5x5'
    valorant = 'VALORANT 5x5'
    brawl_stars = 'Brawl Stars'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
