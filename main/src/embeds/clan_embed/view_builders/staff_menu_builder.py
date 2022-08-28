from discord.ui import View

from embeds.button import buttons


class StandardView:
    def __init__(self):
        self.button_trash = buttons.button_trash
        self.button_trash_two = buttons.button_trash_two

        self.button_shop = buttons.button_shop
        self.button_history = buttons.button_history
        self.button_fault = buttons.button_fault
        self.button_quest = buttons.button_quest

        self.button_edit_time = buttons.button_edit_time
        self.button_edit_event = buttons.button_edit_event
        self.button_edit_butterflies = buttons.button_edit_butterflies
        self.button_edit_xp = buttons.button_edit_xp

    def standard_profile_view(self, drop_down) -> View:
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


clan_staff_view = StandardView()
