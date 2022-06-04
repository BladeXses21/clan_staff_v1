from models.mongo_type import InventoryModel
from models.shop_type import Item
from systems.database_system import DatabaseSystem


class CrossItemSystem(DatabaseSystem):

    # ======================================== this item system ======================================== $
    def create_new_item(self, name: str, rarity: str):
        itc = InventoryModel(name=name, rarity=rarity)
        if self.cross_item_collection.find_one(itc.to_mongo()):
            return False

        itc.name = name
        itc.rarity = rarity

        self.cross_item_collection.insert_one(itc.to_mongo())
        return True


item_system = CrossItemSystem()
