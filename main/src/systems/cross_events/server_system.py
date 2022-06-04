from models.mongo_type import CrossGuildModel
from systems.database_system import DatabaseSystem


class CrossServerSystem(DatabaseSystem):
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


cross_server_system = CrossServerSystem()
