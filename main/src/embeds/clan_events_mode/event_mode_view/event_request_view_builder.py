import discord
from discord.ui import View, Button


class EventRequestViewBuilder:
    def __init__(self):
        self.button_accept = Button(style=discord.ButtonStyle.secondary, label='Взять ивент', emoji='<:freeiconplaybutton64597:960536938752925716>')
        self.button_pass = Button(style=discord.ButtonStyle.secondary, label='Сдать ивент', emoji='<:933511914384920577:960339396350050406>')
        self.button_decline = Button(style=discord.ButtonStyle.secondary, label='Отказ от ивента', emoji='<:933511914707906590:960339513765429278>')

    def create_event_request_view(self) -> View:
        create_event_view = View(timeout=None)
        create_event_view.add_item(self.button_accept)
        create_event_view.add_item(self.button_decline)
        return create_event_view

    def pass_event_request_view(self) -> View:
        pass_event_view = View(timeout=None)
        pass_event_view.add_item(self.button_pass)
        return pass_event_view


event_request_view_builder = EventRequestViewBuilder()
