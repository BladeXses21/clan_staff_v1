import discord
from discord import ApplicationContext
from discord.ui import InputText, Modal
from config import REQUEST_STAFF_CHANNEL, CURATOR_ROLE_BY_SERVER_ID, png_strip_for_embed, BLADEXSES_ID, CLAN_CREATE_REQUEST_CHANNEL


class StaffModal(Modal):
    def __init__(self, ctx: ApplicationContext) -> None:
        super().__init__(title="Заполнение формы Клан Стаффа")
        self.ctx = ctx
        self.add_item(InputText(label='ID/НИК/ИМЯ И ВОЗРАСТ', placeholder='9541302791235454545, BladeXses#6699, Артур, 20'))
        self.add_item(InputText(label='ПОЧЕМУ МЫ ДОЛЖНЫ ВЗЯТЬ ТЕБЯ?', placeholder='...', style=discord.InputTextStyle.long))
        self.add_item(InputText(label='НА КАКУЮ ИЗ ДВУХ ВЕТОК ТЫ ХОЧЕШЬ ВСТАТЬ?', placeholder='Например: Clan Manager или Clan EventMod'))
        self.add_item(InputText(label='УКАЖИ СВОЙ ЧАСОВОЙ ПОЯС.', placeholder='Например: (UTS +3) или +1 от МСК'))
        self.add_item(InputText(label='КОЛИЧЕСТВО НАРУШЕНИЙ и ОНЛАЙН НА СЕРВЕРЕ', placeholder='0 нарушений | 00 ч. 00 м.'))

    async def callback(self, interaction: discord.Interaction):
        emb = discord.Embed(title='Набор на Клан Стафф')
        emb.add_field(name='ID/Ник/Имя и возраст:', value=self.children[0].value, inline=False)
        emb.add_field(name='Почему мы должны взять тебя?:', value=self.children[1].value, inline=False)
        emb.add_field(name='На какую из двух должностей ты хочешь встать:', value=self.children[2].value, inline=False)
        emb.add_field(name='Укажи свой часовой пояс:', value=self.children[3].value, inline=False)
        emb.add_field(name='Количество нарушений и онлайн на сервере:', value=self.children[4].value, inline=False)
        emb.set_image(url=png_strip_for_embed)
        await interaction.response.send_message(content=f'{interaction.user.mention}, заявка успешно отправлена', embed=emb, ephemeral=True)
        await interaction.client.get_channel(REQUEST_STAFF_CHANNEL[interaction.guild.id]).send(content=f'<@&{CURATOR_ROLE_BY_SERVER_ID[interaction.guild.id]}>', embed=emb)


class ClanModal(Modal):
    def __init__(self, ctx: ApplicationContext, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ctx = ctx
        self.add_item(InputText(label='ВВЕДИ БУДУЩИХ УЧАСТНИКОВ СВОЕГО КЛАНА мин.10', placeholder='Если ты заполняешь это на Tenderly, то этих людей ты должен пригласить на сервер.',
                                style=discord.InputTextStyle.long))
        self.add_item(InputText(label='УКАЖИ ЛИДЕРА КЛАНА ЕГО НИК + ID', placeholder='Например: BladeXses#6699 | 045045400656544'))
        self.add_item(InputText(label='БЫЛ ЛИ У ТЕБЯ КЛАН В ПРОШЛОМ?', placeholder='Да/Нет, если да то какой?'))
        self.add_item(InputText(label='НАПИШИ НАЗВАНИЕ любой шрифт И ЦВЕТ КЛАНА #hex', placeholder='Например: ᴅᴇᴠɪʟᴅʏɴᴀꜱᴛʏ | #020202'))

    async def callback(self, interaction: discord.Interaction):
        emb = discord.Embed(title=f'Заявка на создание клана | {interaction.guild.name}')
        emb.add_field(name='Будущие участники клана:', value=self.children[0].value, inline=False)
        emb.add_field(name='Лидер клана:', value=self.children[1].value, inline=False)
        emb.add_field(name='Был ли клан в прошлом:', value=self.children[2].value, inline=False)
        emb.add_field(name='Название клана и цвет:', value=self.children[3].value, inline=False)
        emb.set_image(url=png_strip_for_embed)
        await interaction.response.send_message(content=f'{interaction.user.mention}, заявка успешно отправлена', embed=emb, ephemeral=True)
        await interaction.client.get_channel(CLAN_CREATE_REQUEST_CHANNEL).send(content=f'<@{BLADEXSES_ID}>', embed=emb)
