from discord import Embed

from config import NEXT_STEP_EMOJI, NEXT_STEP_PINK_EMOJI, BARRETTE_BLUE_EMOJI, BARRETTE_PINK_EMOJI, UKI_EMOGI


class HelpEmbed(object):
    def __init__(self, guild_name, leader_role, consliger_role, find_clan_channel, create_clan_url, verify_url, clan_info, clan_staff_url, lead, senior):
        self._embed = Embed(
            title=f'Клановый помощник | {guild_name}',
            description=f'Для вступления в клан, вы должны получить приглашение от Лидера или Заместителя клана.'
                        f'\n\n> **Определить их вы можете по наличию у них роли:**'
                        f'\n{NEXT_STEP_EMOJI} {leader_role} или {consliger_role}.'
                        f'\n\n> **Для их поиска можете воспользоваться чатом:**'
                        f'\n{NEXT_STEP_EMOJI} {find_clan_channel}'
                        f'\n\n **Так же у вас** есть возможность **создать свой клан**, для этого нужно заполнить - [**заявку для создания**]({create_clan_url}) и если она будет одобрена, вам ответят в личные сообщения.'
                        f'\n\nПосле **завершения создания** клана, вам **не будут доступны** все внутри клановые возможности, чтобы это исправить вам нужно верифицировать клан [**заполнив заявку**]({verify_url}).'
                        f'\n\n{BARRETTE_PINK_EMOJI}**Верификация** - это процесс после которого у клана появляется доступ к полному функционалу.'
                        f'\n{BARRETTE_BLUE_EMOJI}**Требования:** 20.000{UKI_EMOGI} (Юки) в казне и 500 часов онлайна.'
                        f'\n{UKI_EMOGI}**Юки** - клановая валюта. Её можно получить за онлайн в клановом войсе, а так же за проведение ивента внутри клана запросив его по команде: **/event request.**'
                        f'\n\n> **Вся информация о кланах, их правила и команды находятся здесь:**'
                        f'\n{NEXT_STEP_PINK_EMOJI} {clan_info}'
                        f'\n> **Для подачи заявки на clan staff заполните эту форму:**'
                        f'\n{NEXT_STEP_PINK_EMOJI} [**тыкни чтобы заполнить**]({clan_staff_url})'
                        f'\n> **По техническим вопросам найденным багам и предложениям по кланам:**'
                        f'\n{NEXT_STEP_PINK_EMOJI} {lead}'
                        f'\n> **Вопросы, жалобы, идеи и предложения по Clan Staff:**'
                        f'\n{NEXT_STEP_PINK_EMOJI} {senior}\n',
            color=16749794
        )

    @property
    def embed(self):
        return self._embed
