from discord import Embed

from config import png_strip_for_embed


class FaultEmbed(object):
    def __init__(self, clan_name: str, description: str):
        self._embed = Embed(
            title=f'Список доступов в голосовой канал {clan_name}',
            description=description
        )
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed
