from discord import Embed, Colour


class AuctionTrashEmbed(object):
    def __init__(self, channel, role):
        self._embed = Embed(colour=Colour(0xa9a9ea),
                            title="<:auction_lot:973729039846088734> Клановый аукцион",
                            description=f"**Прямо сейчас в канале {channel.mention}, проводится клановый аукцион.\nЛотом на данном аукционе выступает клан {role}**")

    @property
    def embed(self):
        return self._embed
