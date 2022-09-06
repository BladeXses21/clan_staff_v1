from typing import List

from database.database_system import DatabaseSystem
from models.game_model.inventory_types.item_types import Item


class ItemsSystem(DatabaseSystem):

    def create_new_item(self, item: Item):
        self.item_collection.insert_one({
            'name': item.name,
            'type': item.type,
            'rarity': item.rarity
        })
        return True

    def find_by_name(self, item_name: str):
        item_data = self.item_collection.find_one({"name": item_name})
        if item_data is None:
            print("This item doesnt exist")
            return None

        return Item.parse_obj(item_data)

    def all_items(self) -> list[Item] | None:
        items_data = self.item_collection.find({})
        if items_data is None:
            print("There arent any items in a game!!!!")
            return None
        items = []
        for i in items_data:
            items.append(Item.parse_obj(i))
        return items

    def delete_item(self, item: Item):
        self.item_collection.delete_one({"name": item.name})


items_system = ItemsSystem()
