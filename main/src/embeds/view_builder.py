import discord
from discord.ui import View, Button

from embeds.button import buttons


class DefaultViewBuilder:
    def __init__(self):
        self.button_accept = buttons.accept_btn
        self.button_decline = buttons.decline_btn

    def create_choice_view(self) -> View:
        view = View(timeout=None)
        view.add_item(self.button_accept)
        view.add_item(self.button_decline)
        return view

    def create_view(self) -> View:
        view = View(timeout=None)
        view.remove_item(self.button_accept)
        view.remove_item(self.button_decline)
        return view


default_view_builder = DefaultViewBuilder()
