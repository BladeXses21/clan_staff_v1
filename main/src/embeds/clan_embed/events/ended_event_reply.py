import time

from discord import Embed, Colour

from config import png_strip_for_embed, png_butterfly_gif


class EndedEventReplyEmbed(object):
    def __init__(self, event_name, event_mode, event_start_time):
        self._embed = Embed(
            description=f'**Название ивента:**```{event_name}```\n'
                        f'**Ивентер:**```{event_mode}```\n'
                        f'**Время начала:**```{event_start_time}```\n'
                        f'**Время конца:**```<t:{int(time.time())}>```',
            color=Colour(0x1FFF00)
        )
        self._embed.set_author(name='ивент был проведен, спасибо за участие',
                               icon_url=png_butterfly_gif),
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed
