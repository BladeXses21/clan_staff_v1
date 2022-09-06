import pymongo

from database.database_system import DatabaseSystem
from models.game_model.battle_types.battle import Battle
from models.game_model.lifeform_types.boss_type import Enemy


class BattleSystem(DatabaseSystem):

    def start_new_battle(self, enemy: Enemy):
        battle = Battle(enemy=enemy)
        self.game_battle_collection.insert_one({'battle': battle.dict()})
        return battle

    def get_current_battle(self) -> Battle:
        battle_date = self.game_battle_collection.find_one({}, sort=[('_id', pymongo.DESCENDING)])
        return Battle.parse_obj(battle_date['battle'])

    def update_current_battle(self, battle: Battle):
        self.game_battle_collection.find_one_and_update({}, sort=[('_id', pymongo.DESCENDING)], update={'$set': {'battle': battle.dict()}})
        return True


battle_system = BattleSystem()
