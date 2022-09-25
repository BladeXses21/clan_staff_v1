from pydantic import BaseModel
from typing import List

from models.game_model.inventory_types.item_types import Item


class Inventory(BaseModel):
    items: List[Item] = []
    max_size: int = 7

    def add_item(self, item: Item):
        if len(self.items) >= int(self.max_size):
            return

        self.items.append(item)

    def remove_item(self, item_index: int):
        if len(self.items) <= 0:
            print("Inventory is empty already! Nothing to remove")
            return

        self.items.__delitem__(1 - 1)

    def item_by_index(self, item_index: int) -> Item | None:
        if item_index > self.items.__len__() or item_index < 1:
            return None
        return self.items.__getitem__(item_index - 1)
