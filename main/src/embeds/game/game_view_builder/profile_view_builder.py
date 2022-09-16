from discord.ui import View

from embeds.button import buttons


class ProfileView(View):
    def __init__(self, back_callback, inventory_callback, hero_class_callback):
        super().__init__(timeout=None)
        buttons.back_btn.callback = back_callback
        buttons.inventory_btn.callback = inventory_callback
        buttons.choice_hero_class.callback = hero_class_callback
        self.add_item(buttons.back_btn)
        self.add_item(buttons.inventory_btn)
        self.add_item(buttons.choice_hero_class)

    @staticmethod
    def disable_choice_class(disable: bool):
        buttons.choice_hero_class.disabled = disable
