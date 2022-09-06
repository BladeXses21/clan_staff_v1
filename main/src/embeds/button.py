from discord.ui import Button
from discord import ButtonStyle

from config import png_heart_icon, png_signal_icon, UKI_EMOGI, history_emoji, fault_emoji, time_emoji, quest_emoji, \
    event_emoji, butterfly_emoji, xp_emoji, tenderly_heart_emoji, meta_heart_emoji, darkness_heart_emoji, \
    sweetness_heart_emoji, right_arrow_emoji, left_arrow_emoji


class Buttons:
    def __init__(self):
        # region BUTTON CHOICE
        self.accept_btn = Button(style=ButtonStyle.secondary, emoji='<:gal:970365886076715128>')
        self.decline_btn = Button(style=ButtonStyle.secondary, emoji='<:krest:970365794707980398>')
        # endregion
        # region CLOSE REQUEST BUTTON
        self.clan_first = Button(style=ButtonStyle.secondary, label='Clan first', emoji='')
        self.clan_second = Button(style=ButtonStyle.secondary, label='Clan second', emoji='')
        self.close_draw = Button(style=ButtonStyle.green, label='Ничья',
                                 emoji='<:freeiconhandshake7195325:960536938639659089>')
        self.close_reject = Button(style=ButtonStyle.red, label='Убрать клоз',
                                   emoji='<:icons8100:933511914707906590>')
        # endregion
        # region EVENT REQUEST BUTTON
        self.button_accept = Button(style=ButtonStyle.secondary,
                                    label='Взять ивент',
                                    emoji='<:freeiconplaybutton64597:960536938752925716>')
        self.button_pass = Button(style=ButtonStyle.secondary,
                                  label='Сдать ивент',
                                  emoji='<:933511914384920577:960339396350050406>')
        self.button_decline = Button(style=ButtonStyle.secondary,
                                     label='Отказ от ивента',
                                     emoji='<:933511914707906590:960339513765429278>')
        # endregion
        # region HELP BUTTON FOR REQUEST STAFF
        self.button_staff = Button(style=ButtonStyle.secondary, label='Подать заявку на клан стафф',
                                   emoji=png_heart_icon)
        self.button_clan = Button(style=ButtonStyle.secondary, label='Подать заявку на создание клана',
                                  emoji=png_signal_icon)
        # endregion
        # region STAFF PROFILE BUTTON
        # self.button_trash = Button(style=discord.ButtonStyle.secondary, emoji='🗑')
        # self.button_trash_two = Button(style=discord.ButtonStyle.secondary, emoji='🗑')
        #
        # self.button_shop = Button(style=discord.ButtonStyle.secondary, label='Магазин', emoji=UKI_EMOGI)
        # self.button_history = Button(style=discord.ButtonStyle.secondary, label='История', emoji=history_emoji)
        # self.button_fault = Button(style=discord.ButtonStyle.secondary, label='Выговоры', emoji=fault_emoji)
        # self.button_quest = Button(style=discord.ButtonStyle.secondary, label='Квесты', emoji=quest_emoji)
        #
        # self.button_edit_time = Button(style=discord.ButtonStyle.grey, label='Время', emoji=time_emoji)
        # self.button_edit_event = Button(style=discord.ButtonStyle.grey, label='Ивенты', emoji=event_emoji)
        # self.button_edit_butterflies = Button(style=discord.ButtonStyle.grey, label='Бабочки', emoji=butterfly_emoji)
        # self.button_edit_xp = Button(style=discord.ButtonStyle.grey, label='Опыт', emoji=xp_emoji)
        # endregion
        # region STAFF LIST BUTTON | GUILD BUTTON
        self.button_tenderly = Button(style=ButtonStyle.secondary,
                                      emoji=tenderly_heart_emoji)
        self.button_meta = Button(style=ButtonStyle.secondary,
                                  emoji=meta_heart_emoji)
        self.button_darkness = Button(style=ButtonStyle.secondary,
                                      emoji=darkness_heart_emoji)
        self.button_sweetness = Button(style=ButtonStyle.secondary,
                                       emoji=sweetness_heart_emoji)
        self.button_guild = Button(style=ButtonStyle.secondary,
                                   emoji=right_arrow_emoji)

        self.button_guild_tenderly = Button(style=ButtonStyle.secondary,
                                            emoji=tenderly_heart_emoji)
        self.button_guild_meta = Button(style=ButtonStyle.secondary,
                                        emoji=meta_heart_emoji)
        self.button_guild_darkness = Button(style=ButtonStyle.secondary,
                                            emoji=darkness_heart_emoji)
        self.button_guild_sweetness = Button(style=ButtonStyle.secondary,
                                             emoji=sweetness_heart_emoji)
        self.button_guild_back = Button(style=ButtonStyle.secondary,
                                        emoji=left_arrow_emoji)
        # endregion
        # region BUTTON ADMIN MENU | GAME BOSS
        self.enemies_btn = Button(style=ButtonStyle.secondary, label='Enemies')
        self.items_btn = Button(style=ButtonStyle.secondary, label='Items')
        self.heroes_btn = Button(style=ButtonStyle.secondary, label='Heroes')
        # endregion
        # region BOSSES VIEW BUILDER
        self.back_btn = Button(style=ButtonStyle.blurple, emoji='<:freeicon3dforwardarrow64844remov:960538574250471424>')
        self.up_btn = Button(style=ButtonStyle.gray, emoji='<:up_arrow:960549187261460510>')
        self.down_btn = Button(style=ButtonStyle.grey, emoji='<:down_arrow:960549187194351706>')
        self.choose_btn = Button(style=ButtonStyle.blurple, label='Choose')
        # endregion
        # region BOSS VIEW BUILDER
        self.add_items_btn = Button(style=ButtonStyle.secondary, label='Add items')
        self.delete_btn = Button(style=ButtonStyle.red, label='Delete')
        # endregion
        # region ADD ITEMS VIEW BUILDER
        self.detail_btn = Button(style=ButtonStyle.secondary, label='', emoji='ℹ')
        self.add_item_btn = Button(style=ButtonStyle.blurple, label='', emoji='➕')
        self.attack_btn = Button(style=ButtonStyle.green, label='Attack', emoji="<:933511914707906590:960339513765429278>")
        # endregion
        # region FIGHT VIEW BUILDER
        self.profile_btn = Button(style=ButtonStyle.blurple, label='Profile', emoji="<:933511914384920577:960339396350050406>")
        # endregion
        # region INVENTORY VIEW BUILDER
        self.equip_btn = Button(style=ButtonStyle.green, emoji='<:icons896:960344174551502858>')
        self.remove_item_btn = Button(style=ButtonStyle.red, label='', emoji='➖')
        self.inventory_btn = Button(style=ButtonStyle.blurple, label='Inventory',
                                    emoji='<:premiumiconbackpack4672563:960536938631270450>')
        # endregion


buttons = Buttons()
