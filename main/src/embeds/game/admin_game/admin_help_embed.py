from discord import Embed, Colour

from config import PREFIX


class AdminHelpEmbed(object):
    def __init__(self):
        self._embed = Embed(
            title='Commands for game admin',
            description=f'\t***```Используйте префикс {PREFIX}game [подкоманда]```***',
            color=3092790
        )
        self._embed.add_field(name='admin_menu', value='***```admin menu for game```***')

    @property
    def embed(self):
        return self._embed
