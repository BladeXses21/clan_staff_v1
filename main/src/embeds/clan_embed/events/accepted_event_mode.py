import time

import discord
from discord import Embed, Colour

from config import png_strip_for_embed, png_butterfly_gif
from embeds.base import DefaultEmbed


class AcceptedEventMode(object):
    def __init__(self, event_num, clan_name, event_mode):
        self._embed = Embed(
            description=f'**Название ивента:**```{event_num}```\n'
                        f'**Клан:**```{clan_name}```\n'
                        f'**Ивентер:**```{event_mode}```\n'
                        f'**Время начала:**\n<t:{int(time.time())}>',
            color=Colour(0x36393F)
        )
        self._embed.set_author(name='запрос на ивент',
                               icon_url=png_butterfly_gif),
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed


async def accept_event_embed(user, request_msg, clan_name, event_num, clan_staff, pass_view):
    try:
        await user.send(embed=DefaultEmbed(f'***```{clan_staff.name}, принял запрос ивента;\nОжидайте в ближайшее время.```***'))
        await request_msg.edit(embed=AcceptedEventMode(clan_name=clan_name, event_num=event_num,
                                                       event_mode=clan_staff.name).embed,
                               view=pass_view)
    except discord.Forbidden:
        await request_msg.edit(embed=AcceptedEventMode(clan_name=clan_name, event_num=event_num, event_mode=clan_staff.name).embed,
                               view=pass_view)

