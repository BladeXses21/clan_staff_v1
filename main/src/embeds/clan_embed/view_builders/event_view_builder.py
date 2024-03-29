import discord
from discord.ui import View, Button


class EventViewBuilder:
    def __init__(self):
        self.button_accept = Button(style=discord.ButtonStyle.secondary,
                                    label='Взять ивент',
                                    emoji='<:freeiconplaybutton64597:960536938752925716>')
        self.button_pass = Button(style=discord.ButtonStyle.secondary,
                                  label='Сдать ивент',
                                  emoji='<:933511914384920577:960339396350050406>')
        self.button_decline = Button(style=discord.ButtonStyle.secondary,
                                     label='Отказ от ивента',
                                     emoji='<:933511914707906590:960339513765429278>')

    def create_event_request_view(self) -> View:
        view = View(timeout=None)
        view.add_item(self.button_accept)
        view.add_item(self.button_decline)
        return view

    def pass_event_request_view(self) -> View:
        view = View(timeout=None)
        view.add_item(self.button_pass)
        return view


event_view_builder = EventViewBuilder()
