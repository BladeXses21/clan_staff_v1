from models.mongo_type import SavedStatModel
from database.database_system import DatabaseSystem


class CrossSaveStatsSystem(DatabaseSystem):

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

    def get_butterfly(self, guild_id: int, clan_staff_id: int) -> SavedStatModel.butterfly:
        st = SavedStatModel(guild_id=guild_id, clan_staff_id=clan_staff_id)
        res = self.cross_stats_collection.find_one(st.to_mongo())

        return res['butterfly']


save_stats_system = CrossSaveStatsSystem()
