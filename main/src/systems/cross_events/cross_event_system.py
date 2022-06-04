import time

from systems.database_system import DatabaseSystem
from models.mongo_type import CrossStafModel, RequestModel


class CrossEventsSystem(DatabaseSystem):

    def add_clan_staff(self, guild_id: int, clan_staff_id: int) -> bool:
        dbm = CrossStafModel(guild_id=guild_id, clan_staff_id=clan_staff_id)
        if self.cross_event_mode_collection.find_one(dbm.to_mongo()):
            return False

        dbm.add_time = int(time.time())
        dbm.member_work_this_request = 0
        dbm.sum_event_ends = 0
        dbm.butterfly = 0
        dbm.fault = 0
        dbm.little_fault = 0
        dbm.wasting_time = 0

        self.cross_event_mode_collection.insert_one(dbm.to_mongo())
        return True

    def delete_clan_staff(self, clan_staff_id: int, guild_id: int):
        dbm = CrossStafModel(guild_id=guild_id, clan_staff_id=clan_staff_id)
        self.cross_event_mode_collection.delete_one(dbm.to_mongo())

    def is_clan_staff(self, guild_id: int, clan_staff_id: int) -> bool:
        dbm = CrossStafModel(guild_id=guild_id, clan_staff_id=clan_staff_id)
        if self.cross_event_mode_collection.find_one(dbm.to_mongo()):
            return True
        return False

    def is_event_completed(self, guild_id: int, clan_staff_id: int) -> bool:
        res = self.cross_event_mode_collection.find_one({'guild_id': guild_id, 'clan_staff_id': clan_staff_id})

        if res['member_work_this_request'] == 0:
            return True

        return False

    def get_request_msg_id(self, guild_id: int, clan_staff_id: int):
        res = self.cross_event_mode_collection.find_one({'guild_id': guild_id, 'clan_staff_id': clan_staff_id})

        if res['member_work_this_request'] == 0:
            return 0
        return res['member_work_this_request']

    def enumeration_events_mode(self, guild_id: int):
        dbm = CrossStafModel(guild_id=guild_id)
        return self.cross_event_mode_collection.find(dbm.to_mongo(), {'clan_staff_id': 1, 'sum_event_ends': 1}).sort('sum_event_ends')

    def get_clan_staff(self, guild_id: int, clan_staff_id: int):
        dbm = CrossStafModel(guild_id=guild_id, clan_staff_id=clan_staff_id)
        res = self.cross_event_mode_collection.find_one(dbm.to_mongo())

        return res['clan_staff_id'], res['sum_event_ends'], res['wasting_time'], res['fault'], res['little_fault'], res['add_time']

    # достает всех ивентеров с базы для таблицы
    def get_event_organizers(self, guild_id: int):
        dbm = CrossStafModel(guild_id=guild_id)
        return self.cross_event_mode_collection.find(
            dbm.to_mongo(),
            {
                '_id': 0,
                'clan_staff_id': 1,
                'sum_event_ends': 1,
                'wasting_time': 1,
                'add_time': 1
            }
        ).sort('wasting_time', -1)

    def reset_staff_stats(self, guild_id: int):
        dbm = CrossStafModel(guild_id=guild_id)

        self.cross_event_mode_collection.update_many(dbm.to_mongo(), {'$set': {'sum_event_ends': 0, 'wasting_time': 0}})

    def update_wasting_time(self, guild_id: int, clan_staff_id: int, waisting_time: int):
        dbm = CrossStafModel(guild_id=guild_id, clan_staff_id=clan_staff_id)

        self.cross_event_mode_collection.update_one(dbm.to_mongo(), {'$inc': {'wasting_time': waisting_time}})

    def update_number_event(self, guild_id: int, clan_staff_id: int, sum_event_ends: int):
        dbm = CrossStafModel(guild_id=guild_id, clan_staff_id=clan_staff_id)

        self.cross_event_mode_collection.update_one(dbm.to_mongo(), {'$inc': {'sum_event_ends': sum_event_ends}})

    def update_fault(self, guild_id: int, clan_staff_id: int, fault: int):
        dbm = CrossStafModel(guild_id=guild_id, clan_staff_id=clan_staff_id)

        self.cross_event_mode_collection.update_one(dbm.to_mongo(), {'$inc': {'fault': fault}})

    def update_little_fault(self, guild_id: int, clan_staff_id: int, little_fault: int):
        dbm = CrossStafModel(guild_id=guild_id, clan_staff_id=clan_staff_id)

        self.cross_event_mode_collection.update_one(dbm.to_mongo(), {'$inc': {'little_fault': little_fault}})

    # ========================================= this request system ======================================== $

    def create_request(self, guild_id: int, message_id: int, event_num: int,
                       clan_name: str, member_send_request: int, comment: str):
        event_request = RequestModel(
            guild_id=guild_id,
            message_id=message_id,
            event_num=event_num,
            member_send_request=member_send_request
        )

        event_request.guild_id = guild_id
        event_request.message_id = message_id
        event_request.event_num = event_num
        event_request.comment = comment
        event_request.clan_name = clan_name
        event_request.time_send_request = int(time.time())
        event_request.member_send_request = member_send_request
        event_request.time_accept_request = 0

        self.cross_clan_event_collection.insert_one(event_request.to_mongo())

    def get_clan_event(self, guild_id: int, message_id: int):
        res = self.cross_clan_event_collection.find_one({'guild_id': guild_id, "message_id": message_id})
        return res['event_num'], res['comment'], res['clan_name'], res['member_send_request']

    def get_time_accept_clan_event(self, guild_id: int, message_id: int):
        res = self.cross_clan_event_collection.find_one({'guild_id': guild_id, "message_id": message_id})

        if res is None:
            return ()

        return res['time_accept_request']

    def accept_clan_event(self, guild_id: int, message_id: int, clan_staff_id: int):
        crm = RequestModel(guild_id=guild_id, message_id=message_id)
        dbm = CrossStafModel(guild_id=guild_id, clan_staff_id=clan_staff_id)

        self.cross_clan_event_collection.update_one(crm.to_mongo(), {'$set': {'clan_staff_id': clan_staff_id,
                                                                              'time_accept_request': int(time.time())}})
        self.cross_event_mode_collection.update_one(dbm.to_mongo(), {'$set': {'member_work_this_request': message_id}})

    def delete_clan_event(self, guild_id: int, message_id: int):
        self.cross_clan_event_collection.delete_one({'guild_id': guild_id, 'message_id': message_id})

    def set_member_request(self, guild_id: int, clan_staff_id: int):
        dbm = CrossStafModel(guild_id=guild_id, clan_staff_id=clan_staff_id)
        self.cross_event_mode_collection.update_one(dbm.to_mongo(), {'$set': {'member_work_this_request': 0}})

    def pass_clan_event(self, guild_id: int, clan_staff_id: int, waisting_time: int):
        dbm = CrossStafModel(guild_id=guild_id, clan_staff_id=clan_staff_id)
        self.cross_event_mode_collection.update_one(dbm.to_mongo(), {'$inc': {'sum_event_ends': 1,
                                                                              'wasting_time': waisting_time}})
        self.cross_event_mode_collection.update_one(dbm.to_mongo(), {'$set': {'member_work_this_request': 0}})


cross_event_system = CrossEventsSystem()
