from . import DatabaseSystem


class HistorySystem(DatabaseSystem):
    def create_history_list(self, guild_id: int, clan_staff_id: int):
        self.events_history.insert_one(
            {
                'guild_id': guild_id,
                'clan_staff_id': clan_staff_id,
                'event_history': [
                    {
                    }
                ]
            }
        )

    def remove_history_list(self, guild_id: int, clan_staff_id: int):
        self.events_history.delete_one({'guild_id': guild_id, 'clan_staff_id': clan_staff_id})

    def note_history(self, guild_id: int, clan_staff_id: int, name: str, time: int, date_end: int, clan_name):
        self.events_history.update_one({'guild_id': guild_id, 'clan_staff_id': clan_staff_id}, {
            '$push':
                {
                    'event_history':
                        {
                            'name': name,
                            'time': time,
                            'date_end': date_end,
                            'clan': clan_name
                        }}
        })

    def clear_history(self, guild_id: int):
        self.events_history.update_many({"guild_id": guild_id}, {'$pull': {'event_history': {}}})

    def get_history(self, guild_id: int, clan_staff_id: int):
        res = self.events_history.find_one({'guild_id': guild_id, 'clan_staff_id': clan_staff_id}, projection={'_id': False})
        return res['event_history']


event_history = HistorySystem()
