import time

from database.database_system import DatabaseSystem
from models.mongo_type import RequestCloseModel


class CloseSystem(DatabaseSystem):

    def create_close(self, guild_id: int, event_name: str, member_send_request: int, clan_send_request: str, comment: str, enemy_msg_id: int):
        close_request = RequestCloseModel(guild_id=guild_id, member_send_request=member_send_request)

        if self.close_collection.find_one(close_request.to_mongo()):
            return False

        close_request.enemy_msg_id = enemy_msg_id
        close_request.event_name = event_name
        close_request.clan_send_request = clan_send_request
        close_request.comment = comment
        close_request.clan_staff_id = 0
        close_request.time_send_request = int(time.time())
        close_request.time_accept_request = 0

        self.close_collection.insert_one(close_request.to_mongo())

    def remove_close(self, guild_id: int, member_send_request: int):
        close_request = RequestCloseModel(guild_id=guild_id, member_send_request=member_send_request)
        self.close_collection.delete_one(close_request.to_mongo())

    def enemy_accept_close(self, guild_id: int, enemy_msg_id: int, close_message_id: int):
        close_request = RequestCloseModel(guild_id=guild_id, enemy_msg_id=enemy_msg_id)

        self.close_collection.update_one(close_request.to_mongo(),
                                         {'$set': {'close_message_id': close_message_id}})

    def staff_accept_close(self, guild_id: int, close_message_id: int, clan_staff_id: int):
        close_request = RequestCloseModel(guild_id=guild_id, close_message_id=close_message_id)

        self.close_collection.update_one(close_request.to_mongo(),
                                         {'$set': {'clan_staff_id': clan_staff_id, 'time_accept_request': int(time.time())}})

    def get_time_send(self, guild_id: int, close_message_id: int) -> RequestCloseModel.time_send_request:
        res = self.close_collection.find_one({'guild_id': guild_id, "close_message_id": close_message_id})
        return res['time_send_request']

    def get_member_send_request(self, guild_id: int, close_message_id: int) -> RequestCloseModel.time_send_request:
        res = self.close_collection.find_one({'guild_id': guild_id, "close_message_id": close_message_id})
        return res['member_send_request']
    
# event_name, team_one, team_two, comment, member_send_request


close_system = CloseSystem()
