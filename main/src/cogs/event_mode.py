import datetime

from discord.ext import tasks

from cogs.base import BaseCog


class EventsMode(BaseCog):
    def __init__(self, client):
        super().__init__(client)

    # @tasks.loop(time=datetime.time(0, 0, 1, 0))
    # def hello_negr(self):
    #     pass

def setup(bot):
    bot.add_cog(EventsMode(bot))
    print("Cog 'event mode' connected!")
