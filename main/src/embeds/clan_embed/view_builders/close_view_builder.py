import discord
from discord.ui import View, Button


class CloseViewBuilder:
    def __init__(self):
        self.first_clan = Button(style=discord.ButtonStyle.secondary, label='Clan first', emoji='')
        self.second_clan = Button(style=discord.ButtonStyle.secondary, label='Clan second', emoji='')
        self.draw_close = Button(style=discord.ButtonStyle.green, label='Ничья', emoji='<:freeiconhandshake7195325:960536938639659089>')
        self.reject_close = Button(style=discord.ButtonStyle.red, label='Убрать клоз', emoji='<:icons8100:933511914707906590>')

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
