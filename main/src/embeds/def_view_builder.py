import discord
from discord.ui import View, Button


class DedaultViewBuilder:
    def __init__(self):
        self.button_accept = Button(style=discord.ButtonStyle.secondary, emoji='<:gal:970365886076715128>')
        self.button_decline = Button(style=discord.ButtonStyle.secondary, emoji='<:krest:970365794707980398>')

    def chose_puth(self) -> View:
        your_puth = View(timeout=None)
        your_puth.add_item(self.button_accept)
        your_puth.add_item(self.button_decline)
        return your_puth

    def remove_chose(self) -> View:
        your_puth = View(timeout=None)
        your_puth.remove_item(self.button_accept)
        your_puth.remove_item(self.button_decline)
        return your_puth


default_view_builder = DedaultViewBuilder()
