from discord import Embed, Colour


class SendingMessagesClans(object):
    def __init__(self, args):
        self._embed = Embed(
            title=f'<:signal:973732570971897856> Оповещение!',
            description=f'\t***```{args}```***',
            color=3092790
        )

    @property
    def embed(self):
        return self._embed
