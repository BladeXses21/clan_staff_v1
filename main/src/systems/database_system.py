from pymongo import MongoClient
from config import MongoToken


class DatabaseSystem(object):
    def __init__(self):
        self.client = MongoClient(MongoToken)
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
    def cross_guild_collection(self):
        return self.db.cross_guild_collection
