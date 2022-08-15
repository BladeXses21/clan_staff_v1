from discord import Embed, Colour, Forbidden, Member, Message
from discord.ui import View

from config import png_strip_for_embed, png_butterfly_gif
from embeds.base import DefaultEmbed


async def decline_enemy_embed(member_send: Member, request_msg: Message, event_name: str, member_enemy: Member):
    try:
        await member_send.send(embed=DefaultEmbed(f'***```{member_enemy.name}, отклонил ваш запрос.```***'))
        await request_msg.edit(embed=DeclinedCloseReply(event_name=event_name, decline_user=member_enemy).embed, view=View())
    except Forbidden:
        await request_msg.edit(embed=DeclinedCloseReply(event_name=event_name, decline_user=member_enemy).embed, view=View())


class DeclinedCloseReply(object):
    def __init__(self, event_name, decline_user):
        self._embed = Embed(
            description=f'**Название клоза:**```{event_name}```\n'
                        f'**Статус:**```ивент не был принят```\n'
                        f'**Пользователь отклонивший:**```{decline_user}```\n',
            color=Colour(0x1FFF00)
        )
        self._embed.set_author(name='ивент был отклонен.',
                               icon_url=png_butterfly_gif),
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed
