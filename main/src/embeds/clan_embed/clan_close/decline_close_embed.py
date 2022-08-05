from discord import Embed, Colour

from config import png_strip_for_embed, png_butterfly_gif


class DeclinedCloseReply(object):
    def __init__(self, event_name, decline_user):
        self._embed = Embed(
            description=f'**Название клоза:**```{event_name}```\n'
                        f'**Статус:**```ивент не был принят```\n'
                        f'**Пользователь отклонивший:**```{decline_user}```\n',
            color=Colour(0x1FFF00)
        )
        self._embed.set_author(name='ивент был проведен, спасибо за участие',
                               icon_url=png_butterfly_gif),
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed


