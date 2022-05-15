import time

import discord
from discord.ext import commands, tasks

from base.funcs import get_clan_stats
from config import PREFIX, STATS_CHAT, TENDERLY_CATEGORY, META_CATEGORY, TENDERLY_CATEGORY_NAME, META_CATEGORY_NAME, TENDERLY_ID, META_ID, DARKNESS_ID, HATORY_ID, DARKNESS_CATEGORY_NAME, \
    HATORY_CATEGORY_NAME
from cogs.base import BaseCog
from embeds.def_embed import DefaultEmbed

desire_bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())


class CheckAllMemberOnClan(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        self.client = client
        self.stats_chat = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.stats_chat = self.client.get_channel(STATS_CHAT)

        if not self.check_all_member_voice.is_running():
            self.check_all_member_voice.start()

    @tasks.loop(minutes=5)
    async def check_all_member_voice(self):
        tenderly = get_clan_stats(self.client.get_guild(TENDERLY_ID), TENDERLY_CATEGORY_NAME)
        meta = get_clan_stats(self.client.get_guild(META_ID), META_CATEGORY_NAME)
        darkness = get_clan_stats(self.client.get_guild(DARKNESS_ID), DARKNESS_CATEGORY_NAME)
        hatory = get_clan_stats(self.client.get_guild(HATORY_ID), HATORY_CATEGORY_NAME)
        await self.stats_chat.send(embed=DefaultEmbed(
            f'<:tenderly:970112564564459530> {tenderly}\n\n<:meta:970111815591804989> {meta}\n\n<:darkness:970112958120218655> {darkness}'
            f'\n\n<:hatory:970112576732143748> {hatory}\n\n<t:{int(time.time())}:R>'))


def setup(bot):
    bot.add_cog(CheckAllMemberOnClan(bot))
    print("Cog 'voice check' connected!")
