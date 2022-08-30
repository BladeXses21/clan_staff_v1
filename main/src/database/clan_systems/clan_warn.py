import time

from database.database_system import DatabaseSystem
from models.mongo_type import ClanWarnModal


class ClanWarnSystem(DatabaseSystem):

    def addGuildToWarnSystem(self, guild_id: int):
        cw = ClanWarnModal(guild_id=guild_id)
        if self.clan_warn_collection.find_one(cw.to_mongo()):
            return False

        self.clan_warn_collection.insert_one(cw.to_mongo())

    def addWarn(self, guild_id: int, clan_staff_id: int, clan_role_id: int, warn_days: int, reason: str):
        self.clan_warn_collection.update_one({'guild_id': guild_id}, {
            '$push': {
                'warn_list':
                    {
                        'clan_staff_id': clan_staff_id,
                        'clan_role_id': clan_role_id,
                        'reason': reason,
                        'warn_date': int(time.time()),
                        'unwarn_date': int(time.time()) + warn_days * 86400
                    }
            }
        })

    def getClanWarnList(self, guild_id: int) -> ClanWarnModal.warn_list:
        res = self.clan_warn_collection.find_one({'guild_id': guild_id}, projection={'_id': False})
        return res['warn_list']

    def removeClanWarn(self, guild_id: int, clan_role_id: int, reason: str, unwarn_date: int):
        self.clan_warn_collection.update_one({'guild_id': guild_id},
                                             {'$pull': {'warn_list': {'clan_role_id': clan_role_id, 'reason': reason, 'unwarn_date': unwarn_date}}})


clan_warn_system = ClanWarnSystem()
