import random

from models.game_model.inventory_types.inventory_types import Inventory


class EnemyInventory(Inventory):

    def random_item(self):
        return self.items.__getitem__(random.randint(0, self.items.__len__() - 1))
