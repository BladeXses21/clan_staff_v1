import discord
from discord import Embed, Colour, Message, Member
from config import png_butterfly_gif, png_strip_for_embed
from embeds.base import DefaultEmbed


async def take_close_embed(event_channel_msg: Message, event_name: str, team_one: str, team_two: str, clan_staff: Member, time_start, comment, member_send,
                           close_channel: discord.VoiceChannel, view):
    try:
        await member_send.send(embed=DefaultEmbed(f'***```Ивентер {clan_staff.name}, принял ваш запрос.\nСобирайтесь в комнате {close_channel.mention}.```***'))
        await event_channel_msg.edit(embed=RunningCloseEmbed(event_name=event_name, team_win=team_one, team_lose=team_two, clan_staff=clan_staff.name, time_start=time_start,
                                                             comment=comment).embed, view=view)
    except discord.Forbidden:
        await event_channel_msg.edit(embed=RunningCloseEmbed(event_name=event_name, team_win=team_one, team_lose=team_two, clan_staff=clan_staff.name, time_start=time_start,
                                                             comment=comment).embed, view=view)


class RunningCloseEmbed(object):
    def __init__(self, event_name: str, team_win: str, clan_staff: str, time_start, team_lose, comment):
        self._embed = Embed(
            description=f'**Название клоза:**```{event_name}```\n'
                        f'**Клозер:**```{clan_staff}```\n'
                        f'**Команда первая:**```{team_win}```\n'
                        f'**Команда вторая:**```{team_lose}```\n'
                        f'**Коментарий:**```{comment}```\n'
                        f'**Время начала:**```{time_start}```\n',
            color=Colour(0x36393F)
        )
        self._embed.set_author(
            name=f'клоз идёт.',
            icon_url=png_butterfly_gif),
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed
