import discord
from discord.ui import View, Button

from config import png_heart_icon, png_signal_icon


class HelpViewBuilder:
    def __init__(self):
        self.button_staff = Button(style=discord.ButtonStyle.secondary, label='Подать заявку на клан стафф', emoji=png_heart_icon)
        self.button_clan = Button(style=discord.ButtonStyle.secondary, label='Подать заявку на создание клана', emoji=png_signal_icon)

    def create_staff_view(self) -> View:
        view = View(timeout=None)
        view.add_item(self.button_staff)
        view.add_item(self.button_clan)
        return view


help_view_builder = HelpViewBuilder()
