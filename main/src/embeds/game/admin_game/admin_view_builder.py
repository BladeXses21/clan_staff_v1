from discord.ui import View


class AdminMenuView(View):
    def __init__(self, enemies_callback, items_callback, heroes_callback):
        super().__init__(timeout=None)
        pass
