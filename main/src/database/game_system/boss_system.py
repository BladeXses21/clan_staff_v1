import random

from database.database_system import DatabaseSystem
from models.game_model.inventory_types.boss_inventory import EnemyInventory
from models.game_model.lifeform_types.boss_type import Enemy


class BossSystem(DatabaseSystem):

    def create_boss(self, name: str, health: int, attack_dmg: int, image: str):
        if self.game_boss_collection.find_one({"name": name}):
            return False

        self.game_boss_collection.insert_one({
            "name": name,
            "current_health": health,
            "max_health": health,
            "attack_dmg": attack_dmg,
            "image": image,
            "inventory": EnemyInventory().dict()
        })
        return True

    def get_random_boss(self):
        random_number = random.randint(0, self.game_boss_collection.count_documents({}) - 1)
        random_enemy_data = self.game_boss_collection.find().limit(-1).skip(random_number).next()
        return Enemy.parse_obj(random_enemy_data)

    def get_by_name(self, boss_name: str):
        boss_data = self.game_boss_collection.find_one({"name": boss_name})
        if boss_data is None:
            return
        return Enemy.parse_obj(boss_data)

    def modify_inventory(self, enemy: Enemy):
        self.game_boss_collection.update_one({"name": enemy.name}, {"$set": {'inventory': enemy.inventory.dict()}})
        return True

    def all_bosses(self) -> list[Enemy]:
        bosses_date = self.game_boss_collection.find({})
        bosses = []
        for i in bosses_date:
            print(i)
            bosses.append(Enemy.parse_obj(i))
        return bosses

    def remove_by_name(self, boss_name: str):
        self.game_boss_collection.delete_one({"name": boss_name})


boss_system = BossSystem()
