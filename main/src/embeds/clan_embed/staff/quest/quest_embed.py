from discord import Embed

from config import png_strip_for_embed


class QuestEmbed(object):
    def __init__(self, member, description, msg_author, color, avatar):
        self._embed = Embed(
            title=f'квесты пользователя: {member.name}',
            description=description,
            color=color
        )
        self._embed.set_footer(text=f'выполнил {msg_author.name}')
        self._embed.set_image(url=png_strip_for_embed)
        self._embed.set_thumbnail(url=avatar)

    @property
    def embed(self):
        return self._embed
