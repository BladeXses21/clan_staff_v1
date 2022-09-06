from pymongo import MongoClient
from config import MONGO_TOKEN


class DatabaseSystem(object):
    def __init__(self):
        self.client = MongoClient(MONGO_TOKEN)
        self._db = self.client.clan_staff_base

    @property
    def db(self):
        return self._db

    @property
    def cross_event_mode_collection(self):
        return self.db.cross_event_mode_collection

    @property
    def cross_clan_event_collection(self):
        return self.db.cross_clan_event_collection

    @property
    def close_collection(self):
        return self.db.close_collection

    @property
    def cross_guild_collection(self):
        return self.db.cross_guild_collection

    @property
    def cross_stats_collection(self):
        return self.db.cross_stats_collection

    @property
    def events_history(self):
        return self.db.events_history

    @property
    def fault_collection(self):
        return self.db.fault_collection

    @property
    def quest_collection(self):
        return self.db.quest_collection

    @property
    def clan_warn_collection(self):
        return self.db.clan_warn_collection

    @property
    def game_boss_collection(self):
        return self.db.boss_collection

    @property
    def item_collection(self):
        return self.db.item_collection

    @property
    def game_battle_collection(self):
        return self.db.battle_collection

    @property
    def game_hero_collection(self):
        return self.db.hero_collection
