import time

import discord
from discord.ext import commands, tasks

from cogs.base import BaseCog
from config import META_ID, DARKNESS_ID, HATORY_ID, DARKNESS_CATEGORY_NAME
from config import PREFIX, STATS_SERVER_CHAT, HATORY_CATEGORY_NAME, SWEETNESS_ID, SWEETNESS_CATEGORY_NAME, SERVER_EMOGI, STATS_CLAN_CHAT, png_strip_for_embed
from config import TENDERLY_CATEGORY_NAME, META_CATEGORY_NAME, TENDERLY_ID
from embeds.base import DefaultEmbed
from extensions.funcs import get_clan_stats, number_of_people_in_clan

desire_bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())


class ClanStats(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        self.client = client
        self.stats_server_chat = None
        self.stats_clan_chat = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.stats_server_chat = self.client.get_channel(STATS_SERVER_CHAT)
        self.stats_clan_chat = self.client.get_channel(STATS_CLAN_CHAT)

        if not self.servers_stats.is_running():
            self.servers_stats.start()
        if not self.servers_clan_stats.is_running():
            self.servers_clan_stats.start()

    @tasks.loop(minutes=5)
    async def servers_stats(self):
        tenderly = get_clan_stats(self.client.get_guild(TENDERLY_ID), TENDERLY_CATEGORY_NAME)
        meta = get_clan_stats(self.client.get_guild(META_ID), META_CATEGORY_NAME)
        darkness = get_clan_stats(self.client.get_guild(DARKNESS_ID), DARKNESS_CATEGORY_NAME)
        sweetness = get_clan_stats(self.client.get_guild(SWEETNESS_ID), SWEETNESS_CATEGORY_NAME)
        await self.stats_server_chat.send(embed=DefaultEmbed(
            f'{SERVER_EMOGI[TENDERLY_ID]} {tenderly}\n\n'
            f'{SERVER_EMOGI[META_ID]} {meta}\n\n'
            f'{SERVER_EMOGI[DARKNESS_ID]} {darkness}\n\n'
            f'{SERVER_EMOGI[SWEETNESS_ID]} {sweetness}\n\n'
            f'<t:{int(time.time())}:R>'))

    @tasks.loop(minutes=10)
    async def servers_clan_stats(self):
        tenderly_members = number_of_people_in_clan(self.client.get_guild(TENDERLY_ID), TENDERLY_CATEGORY_NAME)
        meta_members = number_of_people_in_clan(self.client.get_guild(META_ID), META_CATEGORY_NAME)
        darkness_members = number_of_people_in_clan(self.client.get_guild(DARKNESS_ID), DARKNESS_CATEGORY_NAME)
        sweetness_members = number_of_people_in_clan(self.client.get_guild(SWEETNESS_ID), SWEETNESS_CATEGORY_NAME)
        await self.stats_clan_chat.send(embed=DefaultEmbed(f'{SERVER_EMOGI[TENDERLY_ID]} TENDERLY\n\n {tenderly_members}\n\n'f'<t:{int(time.time())}>').set_image(url=png_strip_for_embed))
        await self.stats_clan_chat.send(embed=DefaultEmbed(f'{SERVER_EMOGI[META_ID]} META\n\n {meta_members}\n\n'f'<t:{int(time.time())}>').set_image(url=png_strip_for_embed))
        await self.stats_clan_chat.send(embed=DefaultEmbed(f'{SERVER_EMOGI[DARKNESS_ID]} DARKNESS\n\n {darkness_members}\n\n'f'<t:{int(time.time())}>').set_image(url=png_strip_for_embed))
        await self.stats_clan_chat.send(embed=DefaultEmbed(f'{SERVER_EMOGI[SWEETNESS_ID]} SWEETNESS\n\n {sweetness_members}\n\n'f'<t:{int(time.time())}>').set_image(url=png_strip_for_embed))


def setup(bot):
    bot.add_cog(ClanStats(bot))
    print("Cog 'clan stats check' connected!")
