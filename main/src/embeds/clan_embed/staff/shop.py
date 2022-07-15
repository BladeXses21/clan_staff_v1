from discord import Embed

from config import png_strip_for_embed
from models.shop import shop_item


class StaffShop(object):
    def __init__(self, msg_author, color):
        self._embed = Embed(
            title=f"Магазин бабочек",
            color=color
        )
        self._embed.add_field(name='``                   услуга                   ``',
                              value='**#1** смена никнейма любому из наставников'
                                    '\n**#2** смена аватарки любому из наставников'
                                    '\n**#3** смена гиф любому из наставников'
                                    '\n**#4** покупка ста конфет'
                                    '\n**#5** покупка клана'
                                    '\n**#6** досрочное снятие письменного выговора'
                                    '\n**#7** досрочное снятие устного выговора'
                                    '\n**#8** покупка 60 минут к норме'
                                    '\n**#9** смена названия чата ветки на неделю'
                                    '\n**#10** смена названия войса ветки на неделю'
                                    '\n**#11** оплата лаврумы'
                                    '\n**#12** освобождение от нормы на неделю'
                                    '\n**#13** роль sponsor на месяц'
                                    '\n**#14** кастомная роль в маркете на месяц'
                                    '\n**#15** кот в мешке(???)'
                                    '\n**#16** рандомная роль из маркета'
                                    '\n**#17** смена никнейма в вашем профиле'
                                    '\n**#18** смена аватарки в вашем профиле'
                                    '\n**#19** смена гиф в вашем профиле'
                                    '\n**#20** сигна от Руcи')
        self._embed.add_field(name='``     цена     ``',
                              value=f'**{shop_item.SHOP_ITEM_AMOUNT[1]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[2]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[3]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[4]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[5]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[6]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[7]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[8]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[9]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[10]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[11]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[12]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[13]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[14]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[15]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[16]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[17]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[18]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[19]}** бабочек'
                                    f'\n**{shop_item.SHOP_ITEM_AMOUNT[20]}** бабочек', inline=True)
        self._embed.set_footer(text=f'выполнил {msg_author.name}')
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed


# class StaffShopTwo(object):
#     def __init__(self, msg_author):
#         self._embed = Embed(
#             title=f"Магазин бабочек",
#             color=15222085
#         )
#         self._embed.add_field(name='``                   услуга                   ``',
#                               value='**#11** оплата лаврумы'
#                                     '\n**#12** освобождение от нормы на неделю'
#                                     '\n**#13** роль sponsor на месяц'
#                                     '\n**#14** кастомная роль в маркете на месяц'
#                                     '\n**#15** кот в мешке(???)'
#                                     '\n**#16** рандомная роль из маркета'
#                                     '\n**#17** смена никнейма в вашем профиле'
#                                     '\n**#18** смена аватарки в вашем профиле'
#                                     '\n**#19** смена гиф в вашем профиле'
#                                     '\n**#20** сигна от Руcи', inline=True)
#         self._embed.add_field(name='``     цена     ``',
#                               value='400 <a:XX_Tenderly_33:933249467023499314>'
#                                     '\n260 <a:XX_Tenderly_33:933249467023499314>'
#                                     '\n800 <a:XX_Tenderly_33:933249467023499314>'
#                                     '\n1600 <a:XX_Tenderly_33:933249467023499314>'
#                                     '\n150 <a:XX_Tenderly_33:933249467023499314>'
#                                     '\n250 <a:XX_Tenderly_33:933249467023499314>'
#                                     '\n100 <a:XX_Tenderly_33:933249467023499314>'
#                                     '\n100 <a:XX_Tenderly_33:933249467023499314>'
#                                     '\n100 <a:XX_Tenderly_33:933249467023499314>'
#                                     '\n3000 <a:XX_Tenderly_33:933249467023499314>', inline=True)
#         self._embed.set_footer(text=f'выполнил {msg_author.name} | лист 2/2')
#         self._embed.set_image(url='https://cdn.discordapp.com/attachments/823681920411107348/825483461040799784/1111.png')
#
#     @property
#     def embed(self):
#         return self._embed
