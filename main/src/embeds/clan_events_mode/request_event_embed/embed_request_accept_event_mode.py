import time

import discord
from discord import Embed, Colour

from embeds.def_embed import DefaultEmbed


class RequestAcceptEventMode(object):
    def __init__(self, event_num, clan_name, event_mode):
        self._embed = Embed(
            description=f'**Название ивента:**```{event_num}```\n**Клан:**```{clan_name}```\n**Ивентер:**```{event_mode}```\n**Время начала:**\n<t:{int(time.time())}>',
            color=Colour(0x36393F)
        )
        self._embed.set_author(name='запрос на ивент',
                               icon_url='https://images-ext-2.discordapp.net/external/ZtDftGSI1KwmT7ML9u9R23RJqJHQv8cx1TPHxsQY2q0/%3Fsize%3D80%26quality%3Dlossless/https/cdn.discordapp.com/emojis/936017706480717825.gif'),
        self._embed.set_image(url='https://cdn.discordapp.com/attachments/823681920411107348/825483461040799784/1111.png')

    @property
    def embed(self):
        return self._embed


async def accept_event_embed(user, request_msg, clan_name, event_num, clan_staff, pass_view):
    try:
        await user.send(embed=DefaultEmbed(f'***```{clan_staff.name}, принял запрос ивента;\nОжидайте в ближайшее время.```***'))
        await request_msg.edit(embed=RequestAcceptEventMode(clan_name=clan_name, event_num=event_num, event_mode=clan_staff.name).embed,
                               view=pass_view)
    except discord.Forbidden:
        await request_msg.edit(embed=RequestAcceptEventMode(clan_name=clan_name, event_num=event_num, event_mode=clan_staff.name).embed,
                               view=pass_view)

