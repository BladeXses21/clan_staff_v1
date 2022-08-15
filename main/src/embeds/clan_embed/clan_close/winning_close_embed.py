import time
from discord import Embed, Colour, Message, Member
from config import png_butterfly_gif, png_strip_for_embed


async def pass_close_embed(reques_msg: Message, event_name: str, team_win: str, team_lose: str, clan_staff: Member, time_start, sum_time, end_result):
    await reques_msg.edit(content=end_result, embed=WinningCloseEmbed(event_name=event_name, team_win=team_win, team_lose=team_lose, clan_staff=clan_staff.name, time_start=time_start, sum_time=sum_time).embed)


class WinningCloseEmbed(object):
    def __init__(self, event_name: str, team_win: str, clan_staff: str, time_start, sum_time, team_lose):
        self._embed = Embed(
            description=f'**Название клоза:**```{event_name}```\n'
                        f'**Клозер:**```{clan_staff}```\n'
                        f'**Команда победителя:**```{team_win}```\n'
                        f'**Команда проигравшего:**```{team_lose}```\n'
                        f'**Суммарное время:**```{sum_time}```\n'
                        f'**Время начала:**```{time_start}```\n'
                        f'**Время конца:**```<t:{int(time.time())}>```',
            color=Colour(0x36393F)
        )
        self._embed.set_author(
            name=f'клоз завершен.',
            icon_url=png_butterfly_gif),
        self._embed.set_image(url=png_strip_for_embed)

    @property
    def embed(self):
        return self._embed
