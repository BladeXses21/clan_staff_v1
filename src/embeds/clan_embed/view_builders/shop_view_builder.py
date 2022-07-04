from typing import Any

import discord
from discord.ui import View, Button, Select


class ShopEditView:
    def __init__(self):
        self.button_back_menu = Button(style=discord.ButtonStyle.secondary, label='Назад', emoji='<a:uki2:959118514814324788>')

        self.option_one = discord.SelectOption(label='1', description='смена никнейма любому из наставников | 7 дней', emoji='<a:_an:967471171480207420>')
        self.option_two = discord.SelectOption(label='2', description='смена аватарки любому из наставников | 7 дней', emoji='<a:_an:967471171480207420>')
        self.option_three = discord.SelectOption(label='3', description='смена гиф любому из наставников | 7 дней', emoji='<a:_an:967471171480207420>')
        self.option_four = discord.SelectOption(label='4', description='покупка ста конфет', emoji='<a:_an:967471171480207420>')
        self.option_five = discord.SelectOption(label='5', description='покупка клана', emoji='<a:_an:967471171480207420>')
        self.option_six = discord.SelectOption(label='6', description='досрочное снятие письменного выговора', emoji='<a:_an:967471171480207420>')
        self.option_seven = discord.SelectOption(label='7', description='досрочное снятие устного выговора', emoji='<a:_an:967471171480207420>')
        self.option_eight = discord.SelectOption(label='8', description='покупка 60 минут к норме', emoji='<a:_an:967471171480207420>')
        self.option_nive = discord.SelectOption(label='9', description='смена названия чата ветки на неделю', emoji='<a:_an:967471171480207420>')
        self.option_ten = discord.SelectOption(label='10', description='смена названия войса ветки на неделю', emoji='<a:_an:967471171480207420>')

        self.option_eleven = discord.SelectOption(label='11', description='оплата лаврумы', emoji='<a:_an:967471171480207420>')
        self.option_twelve = discord.SelectOption(label='12', description='освобождение от нормы на неделю', emoji='<a:_an:967471171480207420>')
        self.option_thirteen = discord.SelectOption(label='13', description='роль sponsor на месяц', emoji='<a:_an:967471171480207420>')
        self.option_fourteen = discord.SelectOption(label='14', description='кастомная роль в маркете на месяц', emoji='<a:_an:967471171480207420>')
        self.option_fifteen = discord.SelectOption(label='15', description='кот в мешке(???)', emoji='<a:_an:967471171480207420>')
        self.option_sixteeen = discord.SelectOption(label='16', description='рандомная роль из маркета', emoji='<a:_an:967471171480207420>')
        self.option_seventeen = discord.SelectOption(label='17', description='смена никнейма в вашем профиле', emoji='<a:_an:967471171480207420>')
        self.option_eighteen = discord.SelectOption(label='18', description='смена аватарки в вашем профиле', emoji='<a:_an:967471171480207420>')
        self.option_nineteen = discord.SelectOption(label='19', description='смена гиф в вашем профиле', emoji='<a:_an:967471171480207420>')
        self.option_twenty = discord.SelectOption(label='20', description='сигна от Русланы', emoji='<a:_an:967471171480207420>')

    def create_shop_list_view(self) -> tuple[View, Select[View | Any]]:
        view, select_menu = self.__create_shop_menu_view([
            self.option_one,
            self.option_two,
            self.option_three,
            self.option_four,
            self.option_five,
            self.option_six,
            self.option_seven,
            self.option_eight,
            self.option_nive,
            self.option_ten,
            self.option_eleven,
            self.option_twelve,
            self.option_thirteen,
            self.option_fourteen,
            self.option_fifteen,
            self.option_sixteeen,
            self.option_seventeen,
            self.option_eighteen,
            self.option_nineteen,
            self.option_twenty
        ])
        return view, select_menu

    def __create_shop_menu_view(self, drop_menu: list) -> tuple[View, Select[View | Any]]:
        view = View(timeout=None)
        list_option = []
        for i in drop_menu:
            list_option.append(i)
        select_menu = Select(options=list_option, placeholder='Выберите человека для отображения')
        view.add_item(select_menu)
        view.add_item(self.button_back_menu)
        return view, select_menu


shop_edit_view = ShopEditView()
