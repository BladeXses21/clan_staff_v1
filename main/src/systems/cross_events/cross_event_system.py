import time

from systems.database_system import DatabaseSystem
from models.models import ClanStaffModel, CrossGuildModel, RequestModel, CrossRequestModel, SavedStatModel


# from utils.shop_item import Item


class CrossEventsSystem(DatabaseSystem):

    def add_clan_staff(self, guild_id: int, clan_staff_id: int) -> bool:
        dbm = ClanStaffModel(guild_id=guild_id, clan_staff_id=clan_staff_id)
        if self.cross_event_mode_collection.find_one(dbm.to_mongo()):
            return False

        dbm.add_time = int(time.time())
        dbm.member_work_this_request = 0
        dbm.sum_event_ends = 0
        dbm.butterfly = 0
        dbm.fault = 0
        dbm.wasting_time = 0

        self.cross_event_mode_collection.insert_one(dbm.to_mongo())
        return True

    def delete_clan_staff(self, clan_staff_id: int, guild_id: int):
        dbm = ClanStaffModel(guild_id=guild_id, clan_staff_id=clan_staff_id)
        self.cross_event_mode_collection.delete_one(dbm.to_mongo())

    def is_clan_staff(self, guild_id: int, clan_staff_id: int) -> bool:
        dbm = ClanStaffModel(guild_id=guild_id, clan_staff_id=clan_staff_id)
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
        dbm = ClanStaffModel(guild_id=guild_id)
        return self.cross_event_mode_collection.find(dbm.to_mongo(), {'clan_staff_id': 1, 'sum_event_ends': 1}).sort('sum_event_ends')

    def get_clan_staff(self, guild_id: int, clan_staff_id: int):
        dbm = ClanStaffModel(guild_id=guild_id, clan_staff_id=clan_staff_id)
        res = self.cross_event_mode_collection.find_one(dbm.to_mongo())

        return res['clan_staff_id'], res['sum_event_ends'], res['wasting_time'], res['add_time']

    # достает всех ивентеров с базы для таблицы
    def get_event_organizers(self, guild_id: int):
        dbm = ClanStaffModel(guild_id=guild_id)
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
        dbm = ClanStaffModel(guild_id=guild_id)

        self.cross_event_mode_collection.update_many(dbm.to_mongo(), {'$set': {'sum_event_ends': 0, 'wasting_time': 0}})

    def update_wasting_time(self, guild_id: int, clan_staff_id: int, waisting_time: int):
        dbm = ClanStaffModel(guild_id=guild_id, clan_staff_id=clan_staff_id)

        self.cross_event_mode_collection.update_one(dbm.to_mongo(), {'$inc': {'wasting_time': waisting_time}})

    def update_number_event(self, guild_id: int, clan_staff_id: int, sum_event_ends: int):
        dbm = ClanStaffModel(guild_id=guild_id, clan_staff_id=clan_staff_id)

        self.cross_event_mode_collection.update_one(dbm.to_mongo(), {'$inc': {'sum_event_ends': sum_event_ends}})

    def update_fault(self, guild_id: int, clan_staff_id: int, fauld: int):
        dbm = ClanStaffModel(guild_id=guild_id, clan_staff_id=clan_staff_id)

        self.cross_event_mode_collection.update_one(dbm.to_mongo(), {'$inc': {'fault': fauld}})

    # ========================================= this cross clan system ======================================== $

    def add_guild(self, guild_id: int, event_channel_id: int, text_category_id: int,
                  voice_category_id: int, clan_staff_role_id: int, auction_channel_id: int, trash_channel_id: int,
                  leader_role_id: int, consliger_role_id: int, find_clan_channel_id: int, clan_info_channel_id: int,
                  create_clan_url: str, verify_url: str, clan_staff_url: str, team_lead_id: int, senior_lead_id: int) -> bool:
        cgm = CrossGuildModel(
            guild_id=guild_id, event_channel_id=event_channel_id,
            text_category_id=text_category_id, voice_category_id=voice_category_id,
            clan_staff_role_id=clan_staff_role_id, auction_channel_id=auction_channel_id, trash_channel_id=trash_channel_id
        )

        if self.cross_guild_collection.find_one(cgm.to_mongo()):
            return False

        cgm.guild_id = guild_id
        cgm.event_channel_id = event_channel_id
        cgm.text_category_id = text_category_id
        cgm.voice_category_id = voice_category_id
        cgm.clan_staff_role_id = clan_staff_role_id
        cgm.auction_channel_id = auction_channel_id
        cgm.trash_channel_id = trash_channel_id
        cgm.leader_role_id = leader_role_id
        cgm.consliger_role_id = consliger_role_id
        cgm.find_clan_channel_id = find_clan_channel_id
        cgm.clan_info_channel_id = clan_info_channel_id
        cgm.create_clan_url = create_clan_url
        cgm.verify_url = verify_url
        cgm.clan_staff_url = clan_staff_url
        cgm.team_lead_id = team_lead_id
        cgm.senior_lead_id = senior_lead_id

        self.cross_guild_collection.insert_one(cgm.to_mongo())
        return True

    def get_help_fields(self, guild_id: int):
        cgm = CrossGuildModel(guild_id=guild_id)
        res = self.cross_guild_collection.find_one(cgm.to_mongo())
        return res['leader_role_id'], res['consliger_role_id'], res['find_clan_channel_id'], res['clan_info_channel_id'], res['create_clan_url'], res['verify_url'], res['clan_staff_url'], \
               res['team_lead_id'], res['senior_lead_id']

    def get_trash_channel(self, guild_id: int):
        cgm = CrossGuildModel(guild_id=guild_id)
        res = self.cross_guild_collection.find_one(cgm.to_mongo())

        return res['trash_channel_id']

    def get_auction_channel(self, guild_id: int):
        cgm = CrossGuildModel(guild_id=guild_id)
        res = self.cross_guild_collection.find_one(cgm.to_mongo())

        return res['auction_channel_id']

    def get_role_by_guild_id(self, guild_id: int):
        cgm = CrossGuildModel(guild_id=guild_id)
        res = self.cross_guild_collection.find_one(cgm.to_mongo())

        return res['clan_staff_role_id']

    def get_event_channel_by_guild_id(self, guild_id: int):
        cgm = CrossGuildModel(guild_id=guild_id)
        res = self.cross_guild_collection.find_one(cgm.to_mongo())

        return res['event_channel_id']

    def get_text_category_by_guild_id(self, guild_id: int):
        cgm = CrossGuildModel(guild_id=guild_id)
        res = self.cross_guild_collection.find_one(cgm.to_mongo())

        return res['text_category_id']

    def get_voice_category_by_guild_id(self, guild_id: int):
        cgm = CrossGuildModel(guild_id=guild_id)
        res = self.cross_guild_collection.find_one(cgm.to_mongo())

        return res['voice_category_id']

    def get_cross_guild(self, guild_id: int):
        cgm = CrossGuildModel(guild_id=guild_id)
        res = self.cross_guild_collection.find_one(cgm.to_mongo())

        return res['event_channel_id'], res['clan_staff_role_id'], res['text_category_id'], res['voice_category_id']

    def find_guild_id(self, guild_id: int) -> bool:
        cgm = CrossGuildModel(guild_id=guild_id)
        if self.cross_guild_collection.find_one(cgm.to_mongo()):
            return True
        return False

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
        dbm = ClanStaffModel(guild_id=guild_id, clan_staff_id=clan_staff_id)

        self.cross_clan_event_collection.update_one(crm.to_mongo(), {'$set': {'clan_staff_id': clan_staff_id,
                                                                              'time_accept_request': int(time.time())}})
        self.cross_event_mode_collection.update_one(dbm.to_mongo(), {'$set': {'member_work_this_request': message_id}})

    def delete_clan_event(self, guild_id: int, message_id: int):
        self.cross_clan_event_collection.delete_one({'guild_id': guild_id, 'message_id': message_id})

    def set_member_request(self, guild_id: int, clan_staff_id: int):
        dbm = ClanStaffModel(guild_id=guild_id, clan_staff_id=clan_staff_id)
        self.cross_event_mode_collection.update_one(dbm.to_mongo(), {'$set': {'member_work_this_request': 0}})

    def pass_clan_event(self, guild_id: int, clan_staff_id: int, waisting_time: int):
        dbm = ClanStaffModel(guild_id=guild_id, clan_staff_id=clan_staff_id)
        self.cross_event_mode_collection.update_one(dbm.to_mongo(), {'$inc': {'sum_event_ends': 1,
                                                                              'wasting_time': waisting_time}})
        self.cross_event_mode_collection.update_one(dbm.to_mongo(), {'$set': {'member_work_this_request': 0}})

    # ========================================= this save stat system ============================================= $

    def create_stat(self, guild_id: int, clan_staff_id: int):
        st = SavedStatModel(guild_id=guild_id, clan_staff_id=clan_staff_id)
        if self.cross_stats_collection.find_one(st.to_mongo()):
            return False
        st.total_time_events = 0
        st.total_event_ends = 0
        st.butterfly = 0

        self.cross_stats_collection.insert_one(st.to_mongo())

    def add_stat(self, guild_id: int, clan_staff_id: int, waisting_time: int):
        st = SavedStatModel(guild_id=guild_id, clan_staff_id=clan_staff_id)
        self.cross_stats_collection.update_one(st.to_mongo(), {'$inc': {'sum_event_ends': 1,
                                                                        'wasting_time': waisting_time}})

    def update_butterfly(self, guild_id: int, clan_staff_id: int, butterfly: int):
        st = SavedStatModel(guild_id=guild_id, clan_staff_id=clan_staff_id)

        self.cross_stats_collection.update_one(st.to_mongo(), {'$inc': {'butterfly': butterfly}})

    def get_butterfly(self, guild_id: int, clan_staff_id: int):
        st = SavedStatModel(guild_id=guild_id, clan_staff_id=clan_staff_id)
        res = self.cross_stats_collection.find_one(st.to_mongo())

        return res['butterfly']

    # ========================================= this item system ======================================== $
    #
    # def create_new_item(self, item: Item):
    #     if self.cross_item_collection.find_one(item.name):
    #         return False
    #
    #     self.cross_item_collection.insert_one({
    #         'name': item.name,
    #         'rarity': item.rarity
    #     })
    #     return True

    # def get_item_by_rarity(self, item: Item.rarity):
    #     return self.cross_item_mollection.find({
    #         'rarity': item
    #     })

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


cross_event_system = CrossEventsSystem()
