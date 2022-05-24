from discord import Embed, Colour

from config import PREFIX, TENDERLY_ID, AUCTION_TENDERLY_IMAGE, \
    META_ID, DARKNESS_ID, AUCTION_DARKNESS_IMAGE, AUCTION_META_IMAGE, HATORY_ID


class AuctionEmbed(object):
    def __init__(self, clan, amount, guild):
        self._embed = Embed(
            title="<:auction_lot:973729039846088734> Клановый аукцион",
            colour=Colour(0xa9a9ea),
            description=f"Это настоящий аукцион, где вы можете выкупить полноценный клан!"
                        "\nВ аукцион будут попадать неактивные кланы."
                        f"\n\nЛотом на данном аукционе является клан: {clan}"
                        "\n\n**Делайте свои ставки!**"
                        "\n**Может именно ты станешь будущем лидером этого клана!**"
                        "\n\n**<:regulations:973729144816959539> Правила:**"
                        f"\n**1.** Торги начинаются с **{amount}** <a:raduga:959419537168683008> , шаг повышения ставки от **1 до 500.** "
                        "\n**2.** Клан достается участнику, предложившему самую высокую цену."
                        "\n**3.** Победитель торгов платит сумму равную своей ставке."
                        "\n**4.** Чат модерируется по всем правилам сервера."
                        "\n**5.** Нарушения правил аукциона влечет за собой получения мута или варна.")
        if guild.id == TENDERLY_ID:
            self._embed.set_image(url=AUCTION_TENDERLY_IMAGE)
        if guild.id == META_ID:
            self._embed.set_image(url=AUCTION_META_IMAGE)
        if guild.id == DARKNESS_ID:
            self._embed.set_image(url=AUCTION_DARKNESS_IMAGE)
        if guild.id == HATORY_ID:
            pass

    @property
    def embed(self):
        return self._embed


class AuctionLot(object):
    def __init__(self, user, amount):
        self._embed = Embed(colour=Colour(0xa9a9ea),
                            description=f"<:auction_lot:973729039846088734> ***{user.mention}, повысил цену лота до {amount}*** <a:raduga:959419537168683008>")

    @property
    def embed(self):
        return self._embed
