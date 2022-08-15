from discord import Embed, Colour

from config import PREFIX, TENDERLY_ID, AUCTION_TENDERLY_IMAGE, \
    META_ID, DARKNESS_ID, AUCTION_DARKNESS_IMAGE, AUCTION_META_IMAGE


class AuctionEmbed(object):
    def __init__(self, clan, amount, guild, end_date: str):
        self._embed = Embed(
            title="<:auction_lot:973729039846088734> Клановый аукцион",
            colour=Colour(0xa9a9ea),
            description=f"Это настоящий аукцион, где вы можете выкупить полноценный клан!"
                        "\nВ аукцион будут попадать неактивные кланы."
                        f"\n\nЛотом на данном аукционе является клан: {clan}"
                        "\n\n**Делайте свои ставки!**"
                        "\n**Может именно ты станешь будущем лидером этого клана!**"
                        "\n\n**<:regulations:973729144816959539> Правила:**"
                        f"\n**1.** Торги начинаются с **{amount}** <a:raduga:959419537168683008>, шаг повышения ставки от **100 до 500** "
                        '\n**2.** Указывать нужно только сумму к которой хотите повысить цену лота'
                        '\n**3.** У вас на балансе должна быть нужная сумма <a:raduga:959419537168683008> для ставки'
                        '\n**4.** Вы не должи быть участником клана на момент ставки'
                        '\n**5.** Перепродажа клана после покупки, заморожена на две недели'
                        "\n**4.** Клан достается участнику, предложившему самую высокую цену"
                        "\n**5.** Победитель торгов платит сумму равную своей ставке"
                        "\n**6.** Чат модерируется по всем правилам сервера"
                        "\n**7.** Нарушения правил аукциона влечет за собой получения мута или варна")
        self._embed.set_footer(text=end_date)
        if guild.id == TENDERLY_ID:
            self._embed.set_image(url=AUCTION_TENDERLY_IMAGE)
        if guild.id == META_ID:
            self._embed.set_image(url=AUCTION_META_IMAGE)
        if guild.id == DARKNESS_ID:
            self._embed.set_image(url=AUCTION_DARKNESS_IMAGE)
        if guild.id == HATORY_ID:
            self._embed.set_image(url=AUCTION_HATORY_IMAGE)

    @property
    def embed(self):
        return self._embed
