import discord
from discord import Embed, Colour, Member

from config import png_strip_for_embed, png_butterfly_gif
from embeds.base import DefaultEmbed
from embeds.clan_embed.clan_close.accepted_close import AcceptedClanCloseEmbed


class ClanCloseEmbed(object):
    def __init__(self, event_name, clan_name, comment):
        self._embed = Embed(
            description=f'***```Ожидание ответа...```***\n' +
                        f'**Название игры:**```{event_name}```\n' +
                        f'**Коментарий:**```{comment}```',
            color=Colour(0x1FFF00)
        )
        self._embed.set_author(
            name=f'Клан {clan_name}, бросил вам вызов.',
            icon_url=png_butterfly_gif),
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed

    async def accept_enemy_embed(member: Member, request_msg, clan_name, event_num, clan_staff, decline_view):
        try:
            await member.send(embed=DefaultEmbed(f'***```{clan_staff.name}, принял запрос на проведение клоза```***'))
            await request_msg.edit(
                embed=AcceptedClanCloseEmbed().embed, view=decline_view)
        except discord.Forbidden:
            await request_msg.edit(
                embed=AcceptedClanCloseEmbed().embed, view=decline_view)
