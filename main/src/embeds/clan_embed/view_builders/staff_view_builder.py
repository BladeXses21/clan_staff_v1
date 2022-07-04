import discord
from discord.ui import View, Button

from config import tenderly_heart_emoji, meta_heart_emoji, darkness_heart_emoji, hatory_heart_emoji, sweetness_heart_emoji, right_arrow_emoji, left_arrow_emoji


class StaffViewBuilder:
    def __init__(self):
        self.button_tenderly = Button(style=discord.ButtonStyle.secondary,
                                      emoji=tenderly_heart_emoji)
        self.button_meta = Button(style=discord.ButtonStyle.secondary,
                                  emoji=meta_heart_emoji)
        self.button_darkness = Button(style=discord.ButtonStyle.secondary,
                                      emoji=darkness_heart_emoji)
        self.button_hatory = Button(style=discord.ButtonStyle.secondary,
                                    emoji=hatory_heart_emoji)
        self.button_sweetness = Button(style=discord.ButtonStyle.secondary,
                                       emoji=sweetness_heart_emoji)
        self.button_guild = Button(style=discord.ButtonStyle.secondary,
                                   emoji=right_arrow_emoji)

        self.button_guild_tenderly = Button(style=discord.ButtonStyle.secondary,
                                            emoji=tenderly_heart_emoji)
        self.button_guild_meta = Button(style=discord.ButtonStyle.secondary,
                                        emoji=meta_heart_emoji)
        self.button_guild_darkness = Button(style=discord.ButtonStyle.secondary,
                                            emoji=darkness_heart_emoji)
        self.button_guild_hatory = Button(style=discord.ButtonStyle.secondary,
                                          emoji=hatory_heart_emoji)
        self.button_guild_sweetness = Button(style=discord.ButtonStyle.secondary,
                                             emoji=sweetness_heart_emoji)
        self.button_guild_back = Button(style=discord.ButtonStyle.secondary,
                                        emoji=left_arrow_emoji)

    def create_staff_list_view(self) -> View:
        view = self.__create_view([
            self.button_tenderly,
            self.button_meta,
            self.button_darkness,
            self.button_hatory,
            self.button_sweetness,
            self.button_guild
        ])
        return view

    def create_guild_list_view(self) -> View:
        view = self.__create_view([
            self.button_guild_tenderly,
            self.button_guild_meta,
            self.button_guild_darkness,
            self.button_guild_hatory,
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
