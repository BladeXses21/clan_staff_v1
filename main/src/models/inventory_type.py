from pydantic import BaseModel
from typing import List

from models.shop_type import Item


class Inventory(BaseModel):
    items: List[Item] = []
    max_size: int = 10

    def add_item(self, item: Item):
        self.items.append(item)

    def item_by_index(self, index: int) -> Item | None:
        if index > self.items.__len__() or index < 1:
            return None
        return self.items.__getitem__(index-1)

    def rem_item(self, index: int):
        if len(self.items) <= 0:
            return

        self.items.__delitem__(index-1)

