import time
from random import choice
from typing import List, Any

from PIL import Image, ImageDraw, ImageChops
from discord import Member
from discord.ext import tasks

from config import DAY_IN_SECONDS, LEVEL_MULTIPLIER, XP_INCREMENT, META_ID, PAYMENT
from embeds.clan_embed.auction.trash_channel_embed import AuctionTrashEmbed
from embeds.clan_embed.staff.staff import StaffEmbed, GuildListEmbed
from database.systems.event_history_system import event_history
from database.systems.event_system import cross_event_system
from database.systems.fault_system import fault_system
from database.systems.quest_system import quest_system
from database.systems.server_system import cross_server_system
from main import client


def add_clan_staff_response(member: Member) -> str:
    response_list = (
        'был пропущен(а) в рай!',
        'успешно добавлен(а) в список клан челиксов!',
        'теперь новый крутейший учасник clan staff!',
        'был успешно добавлен! Не упускай его из виду!',
        'назначен(а) самым милым участником clan staff',
        'этот супер пупс теперь в команде clan staff',
        'успешно прибыл к нашей команде clan staff',
        'добавлен в нашу колекцию клан ивентеров'
    )
    return f'***```{member.name}, {choice(response_list)}```***'


def remove_clan_staff_response(member: Member) -> str:
    response_list = (
        'был изгнан из рая прямиком в ад',
        'успешно убран(а) из списка клан челиксов',
        'теперь не крутой участник clan staff',
        'был успешно удален! Мы будет грустить без него(нет)',
        'теперь не является самым милым участником',
        'пупс был убран из clan staff',
        'успешно отплыл от нашей команды clan staff',
        'был поддожен и случайно сгорел',
        'был убран из нашей колекции'
    )
    return f'***```{member.name}, {choice(response_list)}```***'


def sum_time(secs: int) -> str:
    days = 0
    if secs >= DAY_IN_SECONDS:
        secs -= DAY_IN_SECONDS
        days += 1
    result = time.strftime(f"0{days}:%H:%M:%S", time.gmtime(secs))
    return result


def get_staff_event_list(members, guild_id) -> str:
    counter = 1
    description = ''
    for member in members:
        lvl = cross_event_system.get_lvl_count(guild_id=guild_id, clan_staff_id=member["clan_staff_id"])
        description += f'{counter}. <@{member["clan_staff_id"]}> — {str(member["sum_event_ends"])} ивентов' \
                       f' — {sum_time(member["wasting_time"])} времени — {total_amount(guild_id=guild_id, seconds=member["wasting_time"], lvl=lvl)} зарплата\n'
        counter += 1
    return description


def get_guild_list(guild) -> str:
    counter = 1
    description = ''
    client_category = client.get_channel(cross_server_system.get_text_category(guild.id))
    for category in guild.categories:
        if category.name == client_category.name:
            for channel in category.text_channels:
                description += f'**{counter}.** — {channel.mention} — ' + \
                               f'**{channel.created_at.strftime("%m/%d/%Y")}**\n'
                counter += 1
    return description


def sum_event_time(guild: int, message_id: int):
    time_accept_request = cross_event_system.get_time_accept_clan_event(guild_id=guild, message_id=message_id)
    result = time.gmtime(int(time.time()) - int(time_accept_request))
    return str(time.strftime("%H:%M:%S", result))


def get_event_history(guild_id: int, member_id: int):
    counter = 1
    description = ''
    for history in event_history.get_history(guild_id=guild_id, clan_staff_id=member_id):
        description += f'**#{counter}** {history["name"]} | {int(history["time"] / 60)} m. | {history["clan"]} | <t:{history["date_end"]}>\n'
        counter += 1

    return description


def get_fault(guild_id: int, member_id: int):
    date = ''
    reason = ''
    f_type = ''
    for fault in fault_system.get_fault(guild_id=guild_id, clan_staff_id=member_id):
        str(fault['index']) + '\n'
        date += f"**#{str(fault['index'])}**<t:{fault['add_date']}:R>" + '\n'
        reason += fault['reason'] + '\n'
        f_type += fault['type'] + '\n'
    return date, reason, f_type


def quest_info(guild_id: int, member_id: int):
    res = quest_system.get_quest_xp(guild_id=guild_id, clan_staff_id=member_id)
    xp_ = {}
    quest_time = {}
    for quest in res["quest_list"]:
        xp_[quest["name"]] = quest['xp']
        quest_time[quest['name']] = quest['timer']

    return xp_, quest_time


def get_quest_list(guild_id: int, member_id: int):
    counter = 1
    description = ''
    for quest in quest_system.get_quest_list(guild_id=guild_id, clan_staff_id=member_id):
        description += f'> **#{counter}** {quest["name"]} | {int(quest["timer"])} m.***```награда: {quest["xp"]} xp```***\n'
        counter += 1

    return description


def quest_limit(guild_id: int, member_id: int):
    if len(quest_system.get_quest_list(guild_id=guild_id, clan_staff_id=member_id)) <= 8:
        return True


def total_amount(guild_id: int, seconds: int, lvl):
    total_minutes = int(seconds / 60)
    amount, butterfly = 0, 0
    description = ''
    if total_minutes < PAYMENT[guild_id]['right_time']:
        amount += total_minutes
        return amount
    if total_minutes >= PAYMENT[guild_id]['right_time']:
        amount += PAYMENT[guild_id]['right_payment']
        total_minutes -= PAYMENT[guild_id]['right_time']
        while True:
            if total_minutes < PAYMENT[guild_id]['overtime']:
                description += f'{amount} | {int(butterfly)}'
                return description
            else:
                total_minutes -= PAYMENT[guild_id]['overtime']
                butterfly += LEVEL_MULTIPLIER[lvl] * PAYMENT[guild_id]['bonus_payment']


def xp_to_lvl(xp: int):
    if xp < XP_INCREMENT[1]:
        return 1
    if xp < XP_INCREMENT[2]:
        return 2
    if xp < XP_INCREMENT[3]:
        return 3
    if xp > XP_INCREMENT[4]:
        return 4


def is_member_in_voice(interaction, category_name) -> list[int]:
    members_id = []
    for category in interaction:
        if category.name == category_name:
            for channel in category.voice_channels:
                for member in channel.members:
                    members_id.append(member.id)
    return members_id


def get_clan_channel_names(interaction, category_name) -> list:
    clan_channel_names = []
    for category in interaction.guild.categories:
        if category.name == category_name:
            for channel in category.text_channels:
                clan_channel_names.append(channel.name)
    return clan_channel_names


def get_clan_stats(guild, category_name):
    member_self_mute = 0
    member_self_deaf = 0
    members = 0
    for category in guild.categories:
        if category.name == category_name:
            for channel in category.voice_channels:
                for member in channel.members:
                    if member.voice.self_mute:
                        member_self_mute += 1
                    if member.voice.self_deaf:
                        member_self_deaf += 1
                    else:
                        members += 1
    result = f'<:micro:971837362302771280> **{member_self_mute}** ' \
             f'<:hs:971837386503913552> **{member_self_deaf}** ' \
             f'<:peope:971837376454336552> **{members}**'
    return result


def number_of_people_in_clan(guild, category_name):
    response = ''
    for category in guild.categories:
        if category.name == category_name:
            for channel in category.voice_channels:
                response += f'**{str(channel.name)}**  |  количество человек в войсе: **{str(len(channel.members))}** | \n'
    return response


async def get_staff_list_async(interaction, ctx, server_id, list_response, button):
    if interaction.user.id != ctx.author.id:
        return False
    get_guild = client.get_guild(server_id)
    _members = cross_event_system.get_event_organizers(guild_id=server_id)
    event_list = get_staff_event_list(_members, guild_id=server_id)
    await list_response.edit(
        embed=StaffEmbed(event_list, guild=get_guild.name, user=interaction.user.id, icon=get_guild.icon).embed,
        view=button, delete_after=160)


async def get_guilds_list_async(interaction, ctx, clan_id, list_response, button):
    if interaction.user.id != ctx.author.id:
        return False
    client_guild = client.get_guild(clan_id)
    description = get_guild_list(client_guild)
    await list_response.edit(
        embed=GuildListEmbed(
            description=description,
            guild=client_guild.name,
            user=interaction.user.name,
            icon=client_guild.icon
        ).embed,
        view=button,
        delete_after=160
    )


@tasks.loop(minutes=60)
async def send_trash_auction(ctx, role):
    guild = ctx.guild
    auction_channl_id = cross_server_system.get_auction_channel(guild.id)
    trash_channel_id = cross_server_system.get_trash_channel(guild.id)
    get_auction_channel = client.get_channel(auction_channl_id)
    get_trash_channel = client.get_channel(trash_channel_id)
    await get_trash_channel.send(embed=AuctionTrashEmbed(get_auction_channel, role).embed)
