from discord.ui import View

from embeds.button import buttons


class ChooseClassView(View):
    def __init__(self, back_callback, up_callback, down_callback, choose_class, index: int = 1):
        super().__init__(timeout=None)
        buttons.back_btn.callback = back_callback
        buttons.up_btn.callback = up_callback
        buttons.down_btn.callback = down_callback

        buttons.choose_class_fighter.callback = choose_class
        buttons.choose_class_archer.callback = choose_class
        buttons.choose_class_barbarian.callback = choose_class
        buttons.choose_class_druid.callback = choose_class
        buttons.choose_class_ranger.callback = choose_class
        buttons.choose_class_rogue.callback = choose_class
        buttons.choose_class_wizard.callback = choose_class

        self.add_item(buttons.back_btn)
        self.add_item(buttons.up_btn)
        self.add_item(buttons.down_btn)
        self.add_item(buttons.choose_class_fighter)

        match index:
            case 2:
                self.remove_item(buttons.choose_class_fighter)
                self.add_item(buttons.choose_class_archer)
            case 3:
                self.remove_item(buttons.choose_class_fighter)
                self.add_item(buttons.choose_class_barbarian)
            case 4:
                self.remove_item(buttons.choose_class_fighter)
                self.add_item(buttons.choose_class_druid)
            case 5:
                self.remove_item(buttons.choose_class_fighter)
                self.add_item(buttons.choose_class_ranger)
            case 6:
                self.remove_item(buttons.choose_class_fighter)
                self.add_item(buttons.choose_class_rogue)
            case 7:
                self.remove_item(buttons.choose_class_fighter)
                self.add_item(buttons.choose_class_wizard)
