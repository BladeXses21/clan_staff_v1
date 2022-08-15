import discord
from discord import Embed, Colour, Member, TextChannel, Message

from config import png_strip_for_embed, png_butterfly_gif
from embeds.base import DefaultEmbed


async def accept_enemy_embed(member_send: Member, request_msg: Message, clan_name: str, member_enemy: Member, view, event_channel: TextChannel, event_name: str, clan_enemy: str,
                             staff_view):
    try:
        await member_send.send(embed=DefaultEmbed(f'***```{member_enemy.name}, принял ваш запрос.\nОжидайте ответа ивентера.```***'))
        await request_msg.edit(embed=AcceptedEnemyClanEmbed(clan_name=clan_name).embed, view=view)
        event_channel_msg = await event_channel.send(embed=RequestToTheEventChannel(event_name=event_name, clan_send=clan_name, clan_enemy=clan_enemy).embed, view=staff_view)
    except discord.Forbidden:
        await request_msg.edit(embed=AcceptedEnemyClanEmbed(clan_name=clan_name).embed, view=view)
        event_channel_msg = await event_channel.send(embed=RequestToTheEventChannel(event_name=event_name, clan_send=clan_name, clan_enemy=clan_enemy).embed, view=staff_view)
    return event_channel_msg


class AcceptedEnemyClanEmbed(object):
    def __init__(self, clan_name):
        self._embed = Embed(
            description=f'***```Вы успешно приняли запрос на клоз\nОжидайте ответ ивентера.```***',
            color=Colour(0x1FFF00)
        )
        self._embed.set_author(
            name=f'Ваш противник {clan_name}',
            icon_url=png_butterfly_gif),
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed


class RequestToTheEventChannel(object):
    def __init__(self, event_name, clan_send, clan_enemy):
        self._embed = Embed(
            description=f'**Название клоза:**```{event_name}```\n'
                        f'**Клозер:**```ивент еще никто не взял```\n'
                        '**Время начала:**```xxx```\n'
                        '**Время конца:**```xxx```',
            color=Colour(0x36393F)
        )
        self._embed.set_author(
            name=f'Кланы {clan_send} и {clan_enemy} запросили клоз по игре {event_name}',
            icon_url=png_butterfly_gif),
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed
