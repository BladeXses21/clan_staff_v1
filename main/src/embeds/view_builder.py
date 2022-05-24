import discord
from discord.ui import View, Button


class DefaultViewBuilder:
    def __init__(self):
        self.button_accept = Button(style=discord.ButtonStyle.secondary, emoji='<:gal:970365886076715128>')
        self.button_decline = Button(style=discord.ButtonStyle.secondary, emoji='<:krest:970365794707980398>')

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
