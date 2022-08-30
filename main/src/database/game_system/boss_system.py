import random

from database.database_system import DatabaseSystem
from models.game_model.inventory_types.boss_inventory import EnemyInventory
from models.game_model.lifeform_types.boss_type import Enemy
from models.mongo_type import BossModal


class BossSystem(DatabaseSystem):

    def create_boss(self, name: str, health: int, attack_dmg: int, image: str):
        bm = BossModal(name=name)
        if self.game_boss_collection.find_one(bm.to_mongo()):
            return False

        bm.name = name
        bm.current_health = health
        bm.max_health = health
        bm.attack_dmg = attack_dmg
        bm.boss_img = image
        bm.inventory = EnemyInventory().dict()
        return True

    def get_random_boss(self):
        random_number = random.randint(0, self.game_boss_collection.count_documents({}) - 1)
        random_enemy_data = self.game_boss_collection.find().limit(-1).skip(random_number).next()
        return Enemy.parse_obj(random_enemy_data)

    def all_bosses(self) -> list[Enemy]:
        bosses_date = self.game_boss_collection.find({})
        bosses = []
        for i in bosses_date:
            bosses.append(Enemy.parse_obj(i))
        return bosses


boss_system = BossSystem()
