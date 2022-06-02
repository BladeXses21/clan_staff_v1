import discord
from discord.ui import View, Button


class EditProfileView:
    def __init__(self):
        self.button_time = Button(style=discord.ButtonStyle.secondary, emoji='<:add_time:975531795518988349>')
        self.button_event = Button(style=discord.ButtonStyle.secondary, emoji='<:add_event:975532477244395530>')
        self.button_butterflies = Button(style=discord.ButtonStyle.secondary, emoji='<:butterflies:975533294613573632>')
        self.button_back = Button(style=discord.ButtonStyle.secondary, emoji='<:down_arrow:960549187194351706>')
        self.button_fault = Button(style=discord.ButtonStyle.secondary, emoji='<:fault:981637605089230959>')

    def edit_clan_staff_profile(self) -> View:
        create_profile_view = View(timeout=None)
        create_profile_view.add_item(self.button_time)
        create_profile_view.add_item(self.button_event)
        create_profile_view.add_item(self.button_butterflies)
        create_profile_view.add_item(self.button_fault)
        create_profile_view.add_item(self.button_back)
        return create_profile_view


edit_profile_view = EditProfileView()
