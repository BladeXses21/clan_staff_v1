from discord import Embed, Colour

from config import PREFIX


class StaffCommandsEmbed(object):
    def __init__(self):
        self._embed = Embed(
            title='Clan Staff commands',
            description=f'\t***```Используйте префикс {PREFIX}staff [подкоманда]```***',
            color=3092790
        )
        self._embed.add_field(name='add', value='***```Добавить человека в clan staff```***')
        self._embed.add_field(name='kick', value='***```Убрать человека из clan staff```***')
        self._embed.add_field(name='list', value='***```Просмотреть список clan staff```***')
        self._embed.add_field(name='clear', value='***```Очистка статистики clan staff```***')
        self._embed.add_field(name='/event request', value='***```Запрос ивента в клан```***')
        self._embed.add_field(name='/staff profile', value='***```Профиль участников clan staff```***')

    @property
    def embed(self):
        return self._embed
