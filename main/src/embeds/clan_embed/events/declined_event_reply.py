from discord import Embed, Colour

from config import png_strip_for_embed, png_butterfly_gif


class DeclinedEventReplyEmbed(object):
    def __init__(self, event_name):
        self._embed = Embed(
            description=f'**Название ивента:**```{event_name}```\n'
                        f'**Ивентер:**```ивент не был принят```\n'
                        f'**Время начала:**```ххх```\n'
                        f'**Время конца:**```ххх```',
            color=Colour(0x1FFF00)
        )
        self._embed.set_author(name='ивент был проведен, спасибо за участие',
                               icon_url=png_butterfly_gif),
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed
