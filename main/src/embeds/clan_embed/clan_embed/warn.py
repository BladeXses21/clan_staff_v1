import discord
from discord import Embed

from config import png_strip_for_embed


class ClanWarnEmbed(object):
    def __init__(self, guild: discord.Guild, clan_role, command_use, remove_date, reason):
        self._embed = Embed(
            title=f'выговоры кланов | {guild.name}',
        )
        self._embed.add_field(name='``    клан    ``', value=f"{clan_role}", inline=True)
        self._embed.add_field(name='``  причина  ``', value=f"{reason}", inline=True)
        self._embed.add_field(name='``    истекает    ``', value=f"{remove_date}", inline=True)
        self._embed.set_footer(text=f'выполнил {command_use.name}')
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed
