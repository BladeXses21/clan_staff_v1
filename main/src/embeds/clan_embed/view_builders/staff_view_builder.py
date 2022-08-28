from discord.ui import View

from embeds.button import buttons


class StaffViewBuilder:
    def __init__(self):
        self.button_tenderly = buttons.button_tenderly
        self.button_meta = buttons.button_meta
        self.button_darkness = buttons.button_darkness
        self.button_sweetness = buttons.button_sweetness
        self.button_guild = buttons.button_guild

        self.button_guild_tenderly = buttons.button_guild_tenderly
        self.button_guild_meta = buttons.button_guild_meta
        self.button_guild_darkness = buttons.button_guild_darkness
        self.button_guild_sweetness = buttons.button_guild_sweetness
        self.button_guild_back = buttons.button_guild_back

    def create_staff_list_view(self) -> View:
        view = self.__create_view([
            self.button_tenderly,
            self.button_meta,
            self.button_darkness,
            self.button_sweetness,
            self.button_guild
        ])
        return view

    def create_guild_list_view(self) -> View:
        view = self.__create_view([
            self.button_guild_tenderly,
            self.button_guild_meta,
            self.button_guild_darkness,
            self.button_guild_sweetness,
            self.button_guild_back
        ])
        return view

    def __create_view(self, buttons: list) -> View:
        view = View(timeout=None)
        for btn in buttons:
            view.add_item(btn)
        return view


staff_view_builder = StaffViewBuilder()
