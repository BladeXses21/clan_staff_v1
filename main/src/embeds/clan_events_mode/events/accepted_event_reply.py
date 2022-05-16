import time

from discord import Embed, Colour


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
                               icon_url='https://images-ext-2.discordapp.net/external/ZtDftGSI1KwmT7ML9u9R23RJqJHQv8cx1TPHxsQY2q0/%3Fsize%3D80%26quality%3Dlossless/https/cdn.discordapp.com/emojis/936017706480717825.gif'),
        self._embed.set_image(url='https://cdn.discordapp.com/attachments/823681920411107348/825483461040799784/1111.png')

    @property
    def embed(self):
        return self._embed