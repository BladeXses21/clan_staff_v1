import time
from . import DatabaseSystem
from src.database.models import FaultModel, Number


class FaultSystem(DatabaseSystem):

    def create_fault_list(self, guild_id: int, clan_staff_id: int):
        ft = FaultModel()
        ft.guild_id = guild_id
        ft.clan_staff_id = clan_staff_id
        self.fault_collection.insert_one(ft.to_mongo())

    def remove_fault_list(self, guild_id: int, clan_staff_id: int):
        ft = FaultModel(guild_id=guild_id, clan_staff_id=clan_staff_id)
        self.fault_collection.delete_one(ft.to_mongo())

    def add_fault(self, guild_id: int, clan_staff_id: int, reason: str, fault_type: str):
        num = Number()
        self.fault_collection.update_one({'guild_id': guild_id, 'clan_staff_id': clan_staff_id}, {
            '$push':
                {
                    'fault_list':
                        {
                            'index': num.sequential_value,
                            'reason': reason,
                            'type': fault_type,
                            'add_date': int(time.time())
                        }}
        })

    def get_fault(self, guild_id: int, clan_staff_id: int):
        res = self.fault_collection.find_one({'guild_id': guild_id, 'clan_staff_id': clan_staff_id}, projection={'_id': False})
        return res['fault_list']

    def remove_the_fault(self, guild_id: int, clan_staff_id: int, warn_index: int):
        self.fault_collection.update_one({'guild_id': guild_id, 'clan_staff_id': clan_staff_id}, {"$pull": {"fault_list": {"index": warn_index}}})


fault_system = FaultSystem()
