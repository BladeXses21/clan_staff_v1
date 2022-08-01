from discord import Embed, Colour

from config import png_strip_for_embed


class ProfileClose(object):
    def __init__(self, user_avatar, user_name: str, game_counter, rating: str, winrate: str, first_game: int, last_game: int, clan: str):
        self._embed = Embed(
            title=f'Профиль пользователя: {user_name}',
            color=Colour(0x36393F)
        )
        self._embed.add_field(name='``всего игр:``', value=game_counter)
        self._embed.add_field(name='``всего рейтинга:``', value=rating)
        self._embed.add_field(name='``винрейт:``', value=winrate + '%')
        self._embed.add_field(name='``первая игра:``', value=f"<t:{first_game}:R>")
        self._embed.add_field(name='``последняя игра:``', value=f"<t:{last_game}:R>")
        self._embed.add_field(name='``участник клана:``', value=clan)
        self._embed.set_thumbnail(url=user_avatar)
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed
