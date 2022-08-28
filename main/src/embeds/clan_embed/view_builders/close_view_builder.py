from discord.ui import View

from embeds.button import buttons


class CloseViewBuilder:
    def __init__(self):
        self.first_clan = buttons.clan_first
        self.second_clan = buttons.clan_second
        self.draw_close = buttons.close_draw
        self.reject_close = buttons.close_reject

    def wining_close(self, clan_one, clan_two) -> View:
        two_clans = View(timeout=None)
        self.first_clan.label = str(clan_one)
        self.second_clan.label = str(clan_two)
        two_clans.add_item(self.first_clan)
        two_clans.add_item(self.second_clan)
        two_clans.add_item(self.draw_close)
        two_clans.add_item(self.reject_close)
        return two_clans


close_view_builder = CloseViewBuilder()
