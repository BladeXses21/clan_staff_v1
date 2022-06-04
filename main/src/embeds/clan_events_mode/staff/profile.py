from discord import Embed

from extensions.funcs import sum_time


class StaffProfile(object):
    def __init__(self, member, total_event, total_time, butterfly, fault, little_fault, add_time, guild, icon, avatar):
        self._embed = Embed(
            description=f'**Пользователь:** {member.mention}',
            color=3092790
        )
        self._embed.add_field(name='Суммарно ивентов:', value=total_event, inline=False)
        self._embed.add_field(name='Cуммарно времени:', value=sum_time(total_time), inline=False)
        self._embed.add_field(name='Бабочек:', value=butterfly, inline=False)
        self._embed.add_field(name='Выговоров:', value=fault, inline=False)
        self._embed.add_field(name='Устников:', value=little_fault, inline=False)
        self._embed.add_field(name='На должности:', value=f'<t:{add_time}:R>', inline=False)
        self._embed.set_author(name=f'клановый ивентер | {guild}', icon_url=icon)
        self._embed.set_thumbnail(url=avatar)

    @property
    def embed(self):
        return self._embed
