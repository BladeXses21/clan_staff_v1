from discord import Embed, Colour

from config import PREFIX


class ClanCommandsEmbed(object):
    def __init__(self):
        self._embed = Embed(
            title='Commands for managing clans',
            description=f'\t***```Используйте префикс {PREFIX}clan [подкоманда]```***',
            color=3092790
        )
        self._embed.add_field(name='guild', value='***```Добавить сервер в бота```***')
        self._embed.add_field(name='auction', value='***```Выставить клан на аукцион```***')
        self._embed.add_field(name='send', value='***```Рассылка сообщения по кланам```***')

    @property
    def embed(self):
        return self._embed
