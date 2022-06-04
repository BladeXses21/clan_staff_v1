from systems.database_system import DatabaseSystem


# from utils.shop_item import Item


class CrossCloseSystem(DatabaseSystem):
    pass

    # ========================================= this request close system ======================================== $

    # def create_close(self, guild_id: int, message_id: int, event_name: str,
    #                  clan_send_name: str, clan_accept_name: int):
    #     close_request = CrossRequestModel(guild_id=guild_id, message_id=message_id, event_name=event_name)
    #
    #     close_request.guild_id = guild_id
    #     close_request.message_id = message_id
    #     close_request.event_num = event_name
    #     close_request.clan_send_name = clan_send_name
    #     close_request.clan_accept_name = clan_accept_name
    #     close_request.time_send_request = int(time.time())
    #     close_request.time_accept_request = 0
    #
    #     self.cross_clan_event_collection.insert_one(close_request.to_mongo())


close_system = CrossCloseSystem()
