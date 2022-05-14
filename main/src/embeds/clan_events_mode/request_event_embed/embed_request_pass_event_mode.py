import time

from discord import Embed, Colour


class RequestPassEventMode(object):
    def __init__(self, event_num, clan_name, clan_staff, sum_time_event, time_accept_request, comment, end_result):
        self._embed = Embed(
            description=f'**Название ивента:**```{event_num}```\n**Клан:**```{clan_name}```\n**Коментарий:**```{comment}```\n**Ивентер:**```{clan_staff}```\n**Сумарное время:** ```{sum_time_event}```'
                        f'\n**Время начала ивента:**<t:{time_accept_request}:R>\n**Время конца:**<t:{int(time.time())}:R>\n\n{end_result}',
            color=Colour(0x36393F)
        )
        self._embed.set_author(name='запрос на ивент',
                               icon_url='https://images-ext-2.discordapp.net/external/ZtDftGSI1KwmT7ML9u9R23RJqJHQv8cx1TPHxsQY2q0/%3Fsize%3D80%26quality%3Dlossless/https/cdn.discordapp.com/emojis/936017706480717825.gif'),
        self._embed.set_image(url='https://cdn.discordapp.com/attachments/823681920411107348/825483461040799784/1111.png')

    @property
    def embed(self):
        return self._embed


async def pass_event_embed(request_msg, event_num, clan_name, clan_staff, sum_time_event, time_accept_request, comment, pass_view, end_result):
    await request_msg.edit(
        embed=RequestPassEventMode(event_num=event_num, clan_name=clan_name, clan_staff=clan_staff.name, sum_time_event=sum_time_event,
                                   time_accept_request=time_accept_request, comment=comment, end_result=end_result).embed, view=pass_view)
