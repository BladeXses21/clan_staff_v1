import discord
from discord.ui import View, Button

from config import history_emoji, fault_emoji, quest_emoji, xp_emoji, UKI_EMOGI, time_emoji, butterfly_emoji, event_emoji


class StandartView:
    def __init__(self):
        self.button_trash = Button(style=discord.ButtonStyle.secondary, emoji='🗑')
        self.button_trash_two = Button(style=discord.ButtonStyle.secondary, emoji='🗑')

        self.button_shop = Button(style=discord.ButtonStyle.secondary, label='Магазин', emoji=UKI_EMOGI)
        self.button_history = Button(style=discord.ButtonStyle.secondary, label='История', emoji=history_emoji)
        self.button_fault = Button(style=discord.ButtonStyle.secondary, label='Выговоры', emoji=fault_emoji)
        self.button_quest = Button(style=discord.ButtonStyle.secondary, label='Квесты', emoji=quest_emoji)

        self.button_edit_time = Button(style=discord.ButtonStyle.grey, label='Время', emoji=time_emoji)
        self.button_edit_event = Button(style=discord.ButtonStyle.grey, label='Ивенты', emoji=event_emoji)
        self.button_edit_butterflies = Button(style=discord.ButtonStyle.grey, label='Бабочки', emoji=butterfly_emoji)
        self.button_edit_xp = Button(style=discord.ButtonStyle.grey, label='Опыт', emoji=xp_emoji)

    def standart_profile_view(self, drop_down) -> View:
        clan_staff_view = View(timeout=None)
        clan_staff_view.add_item(self.button_shop)
        clan_staff_view.add_item(self.button_history)
        clan_staff_view.add_item(self.button_fault)
        clan_staff_view.add_item(self.button_quest)
        clan_staff_view.add_item(drop_down)

        return clan_staff_view

    def admin_profile_view(self, drop_down) -> View:
        admin_view = View(timeout=None)
        admin_view.add_item(self.button_shop)
        admin_view.add_item(self.button_quest)
        admin_view.add_item(self.button_history)
        admin_view.add_item(self.button_fault)
        admin_view.add_item(self.button_trash)
        admin_view.add_item(self.button_edit_time)
        admin_view.add_item(self.button_edit_event)
        admin_view.add_item(self.button_edit_butterflies)
        admin_view.add_item(self.button_edit_xp)
        admin_view.add_item(self.button_trash_two)
        admin_view.add_item(drop_down)
        return admin_view


clan_staff_view = StandartView()
