from discord import Embed, Colour

from config import png_strip_for_embed, png_butterfly_gif
from embeds.base import DefaultEmbed


class ClanEventEmbed(object):
    def __init__(self, event_name: str, clan_name: str, users_count: str, comment: str):
        self._embed = Embed(
            description=f'**Название ивента:**```{event_name}```\n'
                        f'**Клан:**```{clan_name}```\n'
                        f'**Количество человек:**```{users_count}```\n'
                        f'**Коментарий:**```{comment}```\n'
                        f'**Ивентер:**```ивент еще никто не взял```',
            color=Colour(0x36393F)
        )
        self._embed.set_author(name='запрос на ивент',
                               icon_url=png_butterfly_gif),
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed


async def full_request_respons(interaction, event_channel, role_id, event_num, users_count, comment, event_request_view):
    await event_channel.send(f'<@&{role_id}>')
    request_msg = await event_channel.send(
        embed=ClanEventEmbed(event_name=event_num, clan_name=interaction.user.voice.channel.name, users_count=users_count, comment=comment).embed,
        view=event_request_view)
    await interaction.response.send_message(
        embed=DefaultEmbed(f'***```{interaction.user.name}, запрос на ивент был успешно отправлен;\nПожалуйста дождитесь ответа ивентера.```***'), ephemeral=True)
    return request_msg
