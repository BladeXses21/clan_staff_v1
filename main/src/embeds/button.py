import discord
from discord.ui import Button

from config import png_heart_icon, png_signal_icon, UKI_EMOGI, history_emoji, fault_emoji, time_emoji, quest_emoji, \
    event_emoji, butterfly_emoji, xp_emoji, tenderly_heart_emoji, meta_heart_emoji, darkness_heart_emoji, \
    sweetness_heart_emoji, right_arrow_emoji, left_arrow_emoji


class Buttons:
    def __init__(self):
        # region BUTTON CHOICE
        self.accept_btn = Button(style=discord.ButtonStyle.secondary, emoji='<:gal:970365886076715128>')
        self.decline_btn = Button(style=discord.ButtonStyle.secondary, emoji='<:krest:970365794707980398>')
        # endregion
        # region CLOSE REQUEST BUTTON
        self.clan_first = Button(style=discord.ButtonStyle.secondary, label='Clan first', emoji='')
        self.clan_second = Button(style=discord.ButtonStyle.secondary, label='Clan second', emoji='')
        self.close_draw = Button(style=discord.ButtonStyle.green, label='Ничья',
                                 emoji='<:freeiconhandshake7195325:960536938639659089>')
        self.close_reject = Button(style=discord.ButtonStyle.red, label='Убрать клоз',
                                   emoji='<:icons8100:933511914707906590>')
        # endregion
        # region EVENT REQUEST BUTTON
        self.button_accept = Button(style=discord.ButtonStyle.secondary,
                                    label='Взять ивент',
                                    emoji='<:freeiconplaybutton64597:960536938752925716>')
        self.button_pass = Button(style=discord.ButtonStyle.secondary,
                                  label='Сдать ивент',
                                  emoji='<:933511914384920577:960339396350050406>')
        self.button_decline = Button(style=discord.ButtonStyle.secondary,
                                     label='Отказ от ивента',
                                     emoji='<:933511914707906590:960339513765429278>')
        # endregion
        # region HELP BUTTON FOR REQUEST STAFF
        self.button_staff = Button(style=discord.ButtonStyle.secondary, label='Подать заявку на клан стафф',
                                   emoji=png_heart_icon)
        self.button_clan = Button(style=discord.ButtonStyle.secondary, label='Подать заявку на создание клана',
                                  emoji=png_signal_icon)
        # endregion
        # region STAFF PROFILE BUTTON
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
        # endregion
        # region STAFF LIST BUTTON | GUILD BUTTON
        self.button_tenderly = Button(style=discord.ButtonStyle.secondary,
                                      emoji=tenderly_heart_emoji)
        self.button_meta = Button(style=discord.ButtonStyle.secondary,
                                  emoji=meta_heart_emoji)
        self.button_darkness = Button(style=discord.ButtonStyle.secondary,
                                      emoji=darkness_heart_emoji)
        self.button_sweetness = Button(style=discord.ButtonStyle.secondary,
                                       emoji=sweetness_heart_emoji)
        self.button_guild = Button(style=discord.ButtonStyle.secondary,
                                   emoji=right_arrow_emoji)

        self.button_guild_tenderly = Button(style=discord.ButtonStyle.secondary,
                                            emoji=tenderly_heart_emoji)
        self.button_guild_meta = Button(style=discord.ButtonStyle.secondary,
                                        emoji=meta_heart_emoji)
        self.button_guild_darkness = Button(style=discord.ButtonStyle.secondary,
                                            emoji=darkness_heart_emoji)
        self.button_guild_sweetness = Button(style=discord.ButtonStyle.secondary,
                                             emoji=sweetness_heart_emoji)
        self.button_guild_back = Button(style=discord.ButtonStyle.secondary,
                                        emoji=left_arrow_emoji)
        # endregion


buttons = Buttons()
