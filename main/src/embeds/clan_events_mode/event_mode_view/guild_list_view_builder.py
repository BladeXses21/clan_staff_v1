import discord
from discord.ui import View, Button


class CrossStaffListViewBuilder:
    def __init__(self):
        self.button_tenderly = Button(style=discord.ButtonStyle.secondary, emoji='<:tenderly:970112564564459530>')
        self.button_meta = Button(style=discord.ButtonStyle.secondary, emoji='<:meta:970111815591804989>')
        self.button_darkness = Button(style=discord.ButtonStyle.secondary, emoji='<:darkness:970112958120218655>')
        self.button_hatory = Button(style=discord.ButtonStyle.secondary, emoji='<:hatory:970112576732143748>')
        self.button_guild = Button(style=discord.ButtonStyle.secondary, emoji='<:freeicon3dforwardarrow64844:960536938782285894>')

        self.button_guild_tenderly = Button(style=discord.ButtonStyle.secondary, emoji='<:tenderly:970112564564459530>')
        self.button_guild_meta = Button(style=discord.ButtonStyle.secondary, emoji='<:meta:970111815591804989>')
        self.button_guild_darkness = Button(style=discord.ButtonStyle.secondary, emoji='<:darkness:970112958120218655>')
        self.button_guild_hatory = Button(style=discord.ButtonStyle.secondary, emoji='<:hatory:970112576732143748>')
        self.button_guild_back = Button(style=discord.ButtonStyle.secondary, emoji='<:freeicon3dforwardarrow64844remov:960538574250471424>')

    def staff_list_view(self) -> View:
        staff_list_view = View(timeout=None)
        staff_list_view.add_item(self.button_tenderly)
        staff_list_view.add_item(self.button_meta)
        staff_list_view.add_item(self.button_darkness)
        staff_list_view.add_item(self.button_hatory)
        staff_list_view.add_item(self.button_guild)
        return staff_list_view

    def guild_list_view(self) -> View:
        guild_list_view = View(timeout=None)
        guild_list_view.add_item(self.button_guild_tenderly)
        guild_list_view.add_item(self.button_guild_meta)
        guild_list_view.add_item(self.button_guild_darkness)
        guild_list_view.add_item(self.button_guild_hatory)
        guild_list_view.add_item(self.button_guild_back)
        return guild_list_view


cross_staff_view_builder = CrossStaffListViewBuilder()
