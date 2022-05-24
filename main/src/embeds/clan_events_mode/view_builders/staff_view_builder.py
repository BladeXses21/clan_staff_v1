import discord
from discord.ui import View, Button


class StaffViewBuilder:
    def __init__(self):
        self.button_tenderly = Button(style=discord.ButtonStyle.secondary,
                                      emoji='<:tenderly:970112564564459530>')
        self.button_meta = Button(style=discord.ButtonStyle.secondary,
                                  emoji='<:meta:970111815591804989>')
        self.button_darkness = Button(style=discord.ButtonStyle.secondary,
                                      emoji='<:darkness:970112958120218655>')
        self.button_hatory = Button(style=discord.ButtonStyle.secondary,
                                    emoji='<:hatory:970112576732143748>')
        self.button_guild = Button(style=discord.ButtonStyle.secondary,
                                   emoji='<:freeicon3dforwardarrow64844:960536938782285894>')

        self.button_guild_tenderly = Button(style=discord.ButtonStyle.secondary,
                                            emoji='<:tenderly:970112564564459530>')
        self.button_guild_meta = Button(style=discord.ButtonStyle.secondary,
                                        emoji='<:meta:970111815591804989>')
        self.button_guild_darkness = Button(style=discord.ButtonStyle.secondary,
                                            emoji='<:darkness:970112958120218655>')
        self.button_guild_hatory = Button(style=discord.ButtonStyle.secondary,
                                          emoji='<:hatory:970112576732143748>')
        self.button_guild_back = Button(style=discord.ButtonStyle.secondary,
                                        emoji='<:freeicon3dforwardarrow64844remov:960538574250471424>')

    def create_staff_list_view(self) -> View:
        view = self.__create_view([
            self.button_tenderly,
            self.button_meta,
            self.button_darkness,
            self.button_hatory,
            self.button_guild
        ])
        return view

    def create_guild_list_view(self) -> View:
        view = self.__create_view([
            self.button_guild_tenderly,
            self.button_guild_meta,
            self.button_guild_darkness,
            self.button_guild_hatory,
            self.button_guild_back
        ])
        return view

    def __create_view(self, buttons: list) -> View:
        view = View(timeout=None)
        for btn in buttons:
            view.add_item(btn)
        return view


staff_view_builder = StaffViewBuilder()
