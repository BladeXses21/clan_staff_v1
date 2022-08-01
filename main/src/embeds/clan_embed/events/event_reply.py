from discord import Embed, Colour

from config import png_strip_for_embed, png_butterfly_gif


class EventReplyEmbed(object):
    def __init__(self, event_name):
        self._embed = Embed(
            description=f'**Название ивента:**```{event_name}```\n'
                        f'**Ивентер:**```ивент еще никто не взял```\n'
                        '**Время начала:**```xxx```\n'
                        '**Время конца:**```xxx```',
            color=Colour(0x36393F)
        )
        self._embed.set_author(name='вы запросили ивент, ожидайте...',
                               icon_url=png_butterfly_gif),
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed
