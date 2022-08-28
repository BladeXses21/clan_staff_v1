from discord.ui import View

from embeds.button import buttons


class EventViewBuilder:
    def __init__(self):
        self.button_accept = buttons.button_accept
        self.button_pass = buttons.button_pass
        self.button_decline = buttons.button_decline

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
