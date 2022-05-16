import time

from discord import Embed, Colour


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
                               icon_url='https://images-ext-2.discordapp.net/external/ZtDftGSI1KwmT7ML9u9R23RJqJHQv8cx1TPHxsQY2q0/%3Fsize%3D80%26quality%3Dlossless/https/cdn.discordapp.com/emojis/936017706480717825.gif'),
        self._embed.set_image(url='https://cdn.discordapp.com/attachments/823681920411107348/825483461040799784/1111.png')

    @property
    def embed(self):
        return self._embed
