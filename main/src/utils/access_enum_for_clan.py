from enum import Enum, unique


@unique
class AccessEnum(str, Enum):
    open = 'Open'
    close = 'Close'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
