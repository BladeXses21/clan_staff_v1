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
        self._embed.add_field(name='auction [role_id] [amount] [end_time]', value='***```Выставить клан на аукцион```***')
        self._embed.add_field(name='send [message]', value='***```Рассылка сообщения по кланам```***')
        self._embed.add_field(name='emb {embed}', value='***```Отправка ботом эмбела с json```***')

    @property
    def embed(self):
        return self._embed
