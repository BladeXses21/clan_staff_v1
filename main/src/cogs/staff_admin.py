from discord.ext import commands

from cogs.base import BaseCog
from systems.cross_events.item_system import item_system


class AdminStaff(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        self.client = client

    @commands.command(name='add_item')
    async def add_item(self, name: str, rarity: str):
        item_system.create_new_item(name=name, rarity=rarity)


def setup(bot):
    bot.add_cog(AdminStaff(bot))
    print("Cog 'addmin cogs' connected!")

