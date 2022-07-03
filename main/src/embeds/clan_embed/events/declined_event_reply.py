from discord import Embed, Colour

from config import png_strip_for_embed


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
                               icon_url='https://images-ext-2.discordapp.net/external/ZtDftGSI1KwmT7ML9u9R23RJqJHQv8cx1TPHxsQY2q0/%3Fsize%3D80%26quality%3Dlossless/https/cdn.discordapp.com/emojis/936017706480717825.gif'),
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed
