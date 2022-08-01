from discord import Embed, Colour

from config import png_strip_for_embed, png_butterfly_gif


class AcceptedClanCloseEmbed(object):
    def __init__(self, clan_name):
        self._embed = Embed(
            description=f'***```Вы успешно приняли запрос на клоз\nОжидайте ответ ивентера...```***',
            color=Colour(0x1FFF00)
        )
        self._embed.set_author(
            name=f'Ваш противник {clan_name}',
            icon_url=png_butterfly_gif),
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed


