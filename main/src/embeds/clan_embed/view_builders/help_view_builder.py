from discord.ui import View

from embeds.button import buttons


class HelpViewBuilder:
    def __init__(self):
        self.button_staff = buttons.button_staff
        self.button_clan = buttons.button_clan

    def create_staff_view(self) -> View:
        view = View(timeout=None)
        view.add_item(self.button_staff)
        view.add_item(self.button_clan)
        return view


help_view_builder = HelpViewBuilder()
