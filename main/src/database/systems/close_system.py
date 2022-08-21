import time

from database.database_system import DatabaseSystem
from models.mongo_type import RequestCloseModel


class CloseSystem(DatabaseSystem):

    def create_close(self, guild_id: int, event_name: str, member_send_request: int, teamOneId: int,
                     comment: str, enemy_msg_id: int, teamTwoId: int):
        close_request = RequestCloseModel(guild_id=guild_id, member_send_request=member_send_request)

        if self.close_collection.find_one(close_request.to_mongo()):
            return False

        close_request.guild_id = guild_id
        close_request.clan_staff_id = 0
        close_request.eventName = event_name
        close_request.memberSendRequest_Id = member_send_request
        close_request.teamTwoMsg_Id = enemy_msg_id
        close_request.closeMsg_Id = 0
        close_request.teamOne_Id = teamOneId
        close_request.teamTwo_Id = teamTwoId
        close_request.comment = comment
        close_request.timeSendRequest = int(time.time())
        close_request.timeAcceptRequest = 0

        self.close_collection.insert_one(close_request.to_mongo())

    def remove_close(self, guild_id: int, member_send_request: int):
        close_request = RequestCloseModel(guild_id=guild_id, member_send_request=member_send_request)
        self.close_collection.delete_one(close_request.to_mongo())

    def enemy_accept_close(self, guild_id: int, enemy_msg_id: int, close_message_id: int):
        close_request = RequestCloseModel(guild_id=guild_id, enemy_msg_id=enemy_msg_id)

        self.close_collection.update_one(close_request.to_mongo(),
                                         {'$set': {'closeMsg_Id': close_message_id}})

    def staff_accept_close(self, guild_id: int, close_message_id: int, clan_staff_id: int):
        close_request = RequestCloseModel(guild_id=guild_id, close_message_id=close_message_id)

        self.close_collection.update_one(close_request.to_mongo(),
                                         {'$set': {'clan_staff_id': clan_staff_id,
                                                   'timeAcceptRequest': int(time.time())}})

    def get_time_send(self, guild_id: int, close_message_id: int) -> RequestCloseModel.timeSendRequest:
        res = self.close_collection.find_one({'guild_id': guild_id, "close_message_id": close_message_id})
        return res['timeSendRequest']

    def get_member_send_request(self, guild_id: int, close_message_id: int) -> RequestCloseModel.memberSendRequest_Id:
        res = self.close_collection.find_one({'guild_id': guild_id, "close_message_id": close_message_id})
        return res['memberSendRequest_Id']

    def get_res(self, guild_id: int, close_message_id: int) -> tuple[str, int, int, str, int]:
        res = self.close_collection.find_one({'guild_id': guild_id, "close_message_id": close_message_id})
        return res['eventName'], res['teamOne_Id'], res['teamTwo_Id'], res['comment'], res['memberSendRequest_Id']


close_system = CloseSystem()
