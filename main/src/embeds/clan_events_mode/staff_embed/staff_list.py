from discord import Embed


class StaffListEmbed(object):
    def __init__(self, description, guild, user, icon):
        self._embed = Embed(
            description=f'{description}',
            color=3092790
        )
        self._embed.set_author(name=f'клановые ивентеры | {guild}', icon_url=icon)
        self._embed.set_footer(text=f'запросил(a): {user}')

    @property
    def embed(self):
        return self._embed


class GuildListEmbed(object):
    def __init__(self, description, guild, user, icon):
        self._embed = Embed(
            description=f'{description}',
            color=3092790
        )
        self._embed.set_author(name=f'список кланов | {guild}', icon_url=icon)
        self._embed.set_footer(text=f'запросил(а): {user}')

    @property
    def embed(self):
        return self._embed
