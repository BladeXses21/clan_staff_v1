import discord
from discord import Embed, Colour, Member, TextChannel, Interaction

from config import png_strip_for_embed, png_butterfly_gif
from embeds.base import DefaultEmbed


async def request_to_the_enemy(interaction: Interaction, member_send: Member, enemy_channel: TextChannel, event_name: str, clan_name: str, comment: str, view):
    try:
        await member_send.send(embed=DefaultEmbed(f'***```Запрос был успешно отпрален и противник получил вызов.\nОжидайте ответа.```***'))
        await enemy_channel.send(embed=ClanCloseEmbed(event_name, clan_name, comment).embed, view=view)
    except discord.Forbidden:
        await interaction.response.send_message(embed=DefaultEmbed(f'***```Запрос был успешно отпрален и противник получил вызов.\nОжидайте ответа.```***'))
        await enemy_channel.send(embed=ClanCloseEmbed(event_name, clan_name, comment).embed, view=view)


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
