from discord import Embed, Color

from config import png_strip_for_embed


class FaultEmbed(object):
    def __init__(self, member, command_use, date, reason, fault_type, color, avatar):
        self._embed = Embed(
            title=f'выговоры: {member.name}',
            description="**2** устных выговора по одной причине = **1** письменный"
                        "\n**2** письменных выговора = **снятие** (если один из выговоров из-за нормы, то снятие по 3 выговорам)",
            color=color
        )
        self._embed.add_field(name='``    дата    ``', value=f"{date}⠀", inline=True)
        self._embed.add_field(name='``  причина  ``', value=f"{reason}⠀", inline=True)
        self._embed.add_field(name='``    тип    ``', value=f"{fault_type}⠀", inline=True)
        self._embed.set_footer(text=f'выполнил {command_use.name}')
        self._embed.set_image(url=png_strip_for_embed)
        self._embed.set_thumbnail(url=avatar)

    @property
    def embed(self):
        return self._embed
