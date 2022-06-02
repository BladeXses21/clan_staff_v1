from discord import Embed, Colour


class AuctionLot(object):
    def __init__(self, user, amount):
        self._embed = Embed(colour=Colour(0xa9a9ea),
                            description=f"<:auction_lot:973729039846088734> ***{user.mention}, повысил цену лота до {amount}*** <a:raduga:959419537168683008>")

    @property
    def embed(self):
        return self._embed
