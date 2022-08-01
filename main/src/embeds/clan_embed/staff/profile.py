from discord import Embed
from math import ceil
from config import LEVEL_MULTIPLIER, XP_INCREMENT
from extensions.funcs import sum_time, total_amount
from models.xp_bar import XpBarController


class StaffProfile(object):
    def __init__(self, member, total_event, total_time, butterfly, add_time, curator, xp, background_img, avatar_img, birthday, color, lvl):

        xp_lenght = 10
        green_pool = ceil(xp / XP_INCREMENT[4] * 100 / xp_lenght)

        xp_pool = XpBarController(green_pool, xp_lenght)

        self._embed = Embed(
            title=f"профиль пользователя: {member.name} | {birthday}",
            color=color
        )
        self._embed.add_field(name='``всего ивентов:``', value=total_event, inline=True)
        self._embed.add_field(name='``всего минут:``', value=sum_time(total_time), inline=True)
        self._embed.add_field(name='``зарплата:``', value=f"{total_amount(total_time, lvl)}", inline=True)
        self._embed.add_field(name='``бабочек:``', value=butterfly, inline=True)
        self._embed.add_field(name='``на должности:``', value=f'<t:{add_time}:R>', inline=True)
        self._embed.add_field(name='``принял:``', value=curator, inline=True)
        self._embed.add_field(name='``уровень:``', value=f"{lvl} | [множ. x{LEVEL_MULTIPLIER[lvl]}]", inline=True)
        self._embed.add_field(name='``количество xp:``', value=f"{xp} | [квесты]", inline=True)
        self._embed.add_field(name='``особая минималка:``', value='нет', inline=True)
        self._embed.add_field(name='``Полоса опыта:``', value=str(xp_pool.__str__()), inline=False)
        self._embed.set_footer(text='улучшить свой профиль можно за бабочки в шопе')
        self._embed.set_image(url=background_img)
        self._embed.set_thumbnail(url=avatar_img)

    @property
    def embed(self):
        return self._embed
