import time

from discord import Embed, Colour

from config import png_strip_for_embed, png_butterfly_gif


class AcceptedEventReplyEmbed(object):
    def __init__(self, event_name, event_mode):
        self._embed = Embed(
            description=f'**Название ивента:**```{event_name}```\n'
                        f'**Ивентер:**```{event_mode}```\n'
                        f'**Время начала:**<t:{int(time.time())}>\n'
                        f'**Время конца:**```xxx```',
            color=Colour(0x1FFF00)
        )
        self._embed.set_author(name='спасибо за ожидание, ивент был принят',
                               icon_url=png_butterfly_gif),
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed
