from discord.ui import View

from embeds.button import buttons


class HeroesView(View):
    def __init__(self, back_callback, up_callback, down_callback, next_callback):
        super().__init__(timeout=None)
        buttons.back_btn.callback = back_callback
        buttons.up_btn.callback = up_callback
        buttons.down_btn.callback = down_callback
        buttons.next_page_btn.callback = next_callback
        self.add_item(buttons.back_btn)
        self.add_item(buttons.up_btn)
        self.add_item(buttons.down_btn)
        self.add_item(buttons.next_page_btn)
