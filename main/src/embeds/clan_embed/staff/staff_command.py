from discord import Embed

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
        self._embed.add_field(name='warn [id/@link] [reason] [type]', value='***```Выдать выговор участнику```***')
        self._embed.add_field(name='unwarn [id/@link] [index]', value='***```Снять выговор с участника```***')
        self._embed.add_field(name='fault [id/@link]', value='***```Просмотреть список выговоров участника```***')
        self._embed.add_field(name='his [id/@link]', value='***```Просмотреть историю ивентов участника```***')
        self._embed.add_field(name='clear_his', value='***```Очистка истории ивентов на сервере```***')
        self._embed.add_field(name='dr [id/link] [date]', value='***```Назничить день рождения участника```***')
        self._embed.add_field(name='av [id/link] [image_url]', value='***```Изменить аватарку в профиле участника```***')
        self._embed.add_field(name='back [id/link] [image_url]', value='***```Изменить фон в профиле участника```***')
        self._embed.add_field(name='quest [id/link]', value='***```Просмотреть действующие квесты участника```***')
        self._embed.add_field(name='new_quest [timer] [xp] [event_name]', value='***```Создать новый квест для всех участников```***', inline=False)
        self._embed.add_field(name='rem_quest [event_name] [id/@link]', value='***```Удалить квест определенному участнику | Если не указать человека, квест удалиться всем```***', inline=False)
        self._embed.add_field(name='refresh [id/@link]', value='***```Используется в случае если человек не смог завершить ивент | сбрасывает ивент с человека.```***', inline=False)

    @property
    def embed(self):
        return self._embed
