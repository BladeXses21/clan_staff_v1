import time

from discord import Embed, Colour

from config import png_strip_for_embed, png_butterfly_gif


class PassedEventModeEmbed(object):
    def __init__(self, event_num, clan_name, clan_staff, sum_time_event, time_accept_request, comment, end_result):
        self._embed = Embed(
            description=f'**Название ивента:**```{event_num}```\n'
                        f'**Клан:**```{clan_name}```\n'
                        f'**Коментарий:**```{comment}```\n'
                        f'**Ивентер:**```{clan_staff}```\n'
                        f'**Сумарное время:** ```{sum_time_event}```\n'
                        f'**Время начала ивента:**<t:{time_accept_request}>\n'
                        f'**Время конца:**<t:{int(time.time())}>\n\n{end_result}',
            color=Colour(0x36393F)
        )
        self._embed.set_author(name='запрос на ивент',
                               icon_url=png_butterfly_gif),
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed


async def pass_event_embed(request_msg, event_num, clan_name, clan_staff,
                           sum_time_event, time_accept_request, comment, pass_view, end_result):
    await request_msg.edit(
        embed=PassedEventModeEmbed(event_num=event_num, clan_name=clan_name, clan_staff=clan_staff.name,
                                   sum_time_event=sum_time_event, time_accept_request=time_accept_request,
                                   comment=comment, end_result=end_result).embed, view=pass_view)
