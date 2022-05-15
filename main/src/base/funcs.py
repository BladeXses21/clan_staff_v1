import time
from random import choice
from discord import Member

from config import DAY_IN_SECONDS
from main import client
from embeds.clan_events_mode.staff_embed.staff_list import StaffListEmbed, GuildListEmbed
from systems.clan_staff.cross_event_request_system import cross_event_system


def add_clan_staff_response(member: Member) -> str:
    response_list = (
        'был пропущен(а) в рай!',
        'успешно добавлен(а) в список клан челиксов!',
        'теперь новый крутейший учасник clan staff!',
        'был успешно добавлен, не упускай его из виду!',
        'назначен(а) самым милым участником clan staff',
        'этот супер пупс теперь в команде clan staff',
        'успешно прибыл к нашей команде clan staff'
    )
    return f'***```{member.name}, {choice(response_list)}```***'


def remove_clan_staff_response(member: Member) -> str:
    response_list = (
        'был изгнан из рая прямиком в ад',
        'успешно убран(а) из списка клан челиксов',
        'теперь не крутой участник clan staff',
        'был успешно удален, грустно конечно',
        'теперь не является самым милым участником',
        'пупс был убран из clan staff',
        'успешно отплыл от нашей команды clan staff',
        'был поддожен и случайно сгорел'
    )
    return f'***```{member.name}, {choice(response_list)}```***'


def sum_time(secs: int) -> str:
    days = 0
    if secs >= DAY_IN_SECONDS:
        secs -= DAY_IN_SECONDS
        days += 1
    result = time.strftime(f"{days}:%H:%M:%S", time.gmtime(secs))
    return result


def get_staff_event_list(members) -> str:
    counter = 1
    description = ''
    for member in members:
        description += f'{counter}. <@{member["clan_staff_id"]}> — {str(member["sum_event_ends"])} ивентов' \
                       f' — {sum_time(member["wasting_time"])} времени — <t:{member["add_time"]}:R>\n'
        counter += 1
    return description


def get_guild_list(guild) -> str:
    counter = 1
    description = ''
    client_category = client.get_channel(cross_event_system.get_text_category_by_guild_id(guild.id))
    for category in guild.categories:
        if category.name == client_category.name:
            for channel in category.text_channels:
                description += f'**{counter}.** — {channel.mention} — ' + \
                               f'**{channel.created_at.strftime("%m/%d/%Y")}**\n'
                counter += 1
    return description


def sum_event_time(guild: int, message_id: int):
    time_accept_request = cross_event_system.get_time_accept_request(guild_id=guild, message_id=message_id)
    result = time.gmtime(int(time.time()) - int(time_accept_request))
    return str(time.strftime("%H:%M:%S", result))


# def check_member_on_voice(interaction, category_name) -> list[int]:
#     members = []
#     for category in interaction:
#         if category.name == category_name:
#             for channel in category.voice_channels:
#                 if len(channel.members) > 0:
#                     members.append(*channel.members)
#     return [member.id for member in members]

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


async def get_staff_list_async(interaction, ctx, clan_id, list_response, button):
    if interaction.user.id != ctx.author.id:
        return False
    get_tenderly_guild = client.get_guild(clan_id)
    server_members = cross_event_system.enumeration_events_mode(guild_id=clan_id)
    event_list = get_staff_event_list(server_members)
    await list_response.edit(
        embed=StaffListEmbed(event_list, guild=get_tenderly_guild.name, user=interaction.user.name, icon=get_tenderly_guild.icon).embed,
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
