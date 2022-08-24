from database.database_system import DatabaseSystem
from models.mongo_type import QuestModel
import time


class QuestSystem(DatabaseSystem):

    def formation_doc(self, guild_id: int, clan_staff_id: int):
        quest = QuestModel(guild_id=guild_id, clan_staff_id=clan_staff_id)

        self.quest_collection.insert_one(quest.to_mongo())

    def remove_quest_doc(self, guild_id: int, clan_staff_id: int):
        quest = QuestModel(guild_id=guild_id, clan_staff_id=clan_staff_id)
        self.quest_collection.delete_one(quest.to_mongo())

    def create_new_quest(self, guild_id: int, member_id: int, name: str, timer: int, xp: int):
        self.quest_collection.update_one({'guild_id': guild_id, 'clan_staff_id': member_id}, {
            '$push':
                {
                    'quest_list':
                        {
                            'name': name,
                            'timer': timer,
                            'xp': xp,
                            'add_time': int(time.time())
                        }}
        })

    def get_quest_list(self, guild_id: int, clan_staff_id: int) -> list:
        res = self.quest_collection.find_one({'guild_id': guild_id, 'clan_staff_id': clan_staff_id})

        if res is None:
            return []

        return res['quest_list']

    def get_quest_xp(self, guild_id: int, clan_staff_id: int) -> dict[QuestModel.quest_list]:
        res = self.quest_collection.find_one({'guild_id': guild_id, 'clan_staff_id': clan_staff_id}, {"quest_list": 1})
        return res

    def remove_quest(self, guild_id: int, clan_staff_id: int, name: str):
        self.quest_collection.update_one({'guild_id': guild_id, 'clan_staff_id': clan_staff_id},
                                         {"$pull": {"quest_list": {"name": name}}})


quest_system = QuestSystem()
