import discord
from discord import ApplicationContext
from discord.ui import Select
from discord import errors
from config import OWNER_IDS, STOP_WORD
from embeds.base import DefaultEmbed
from embeds.clan_events_mode.staff.profile import StaffProfile
from embeds.clan_events_mode.view_builders.profile_view_builder import edit_profile_view
from extensions.logger import staff_logger
from main import client
from systems.cross_events.cross_event_system import cross_event_system


class ClanService:
    def __init__(self, client):
        self.client = client

    async def drop_menu(self, interaction: discord.Interaction, ctx: ApplicationContext = None):
        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        clan_staff_options = []

        for i in cross_event_system.enumeration_events_mode(ctx.guild.id):
            member = ctx.guild.get_member(i['clan_staff_id'])
            clan_staff_options.append(discord.SelectOption(label=i['clan_staff_id'], description=member.name, emoji='<a:_an:967471171480207420>'))

        drop_down_menu = Select(options=clan_staff_options, placeholder='Выберите человека для отображения')

        view = discord.ui.View(timeout=None)
        view.add_item(drop_down_menu)
        try:
            author_id, my_total_events, my_total_times, my_add_time = cross_event_system.get_clan_staff(ctx.guild.id, ctx.author.id)
            my_butterfly = cross_event_system.get_butterfly(ctx.guild.id, ctx.author.id)

            if ctx.message is None:
                await ctx.response.send_message(embed=StaffProfile(member=ctx.author, total_event=my_total_events, total_time=my_total_times, butterfly=my_butterfly, add_time=my_add_time,
                                                                   guild=ctx.guild.name, fault='0', icon=ctx.guild.icon, avatar=ctx.author.display_avatar).embed, view=view, ephemeral=True)
            else:
                await ctx.response.edit_message(embed=StaffProfile(member=ctx.author, total_event=my_total_events, total_time=my_total_times, butterfly=my_butterfly, add_time=my_add_time,
                                                                   guild=ctx.guild.name, fault='0', icon=ctx.guild.icon, avatar=ctx.author.display_avatar).embed, view=view)
        except TypeError:
            if ctx.message is None:
                await ctx.response.send_message(embed=DefaultEmbed('***```Выберите пользователя```***'), view=view, ephemeral=True)
            else:
                await ctx.response.edit_message(embed=DefaultEmbed('***```Выберите пользователя```***'), view=view)

        async def menu_callback(interact: discord.Interaction):
            create_profile_view = edit_profile_view.edit_clan_staff_profile()
            member_id, total_event, total_time, add_time = cross_event_system.get_clan_staff(interact.guild.id, drop_down_menu.values[0])
            try:
                get_butterfly = cross_event_system.get_butterfly(interact.guild.id, drop_down_menu.values[0])
            except TypeError:
                get_butterfly = 0
            get_member = interact.guild.get_member(member_id)

            if interact.user.id not in OWNER_IDS:
                await interact.response.edit_message(
                    embed=StaffProfile(member=get_member, total_event=total_event, total_time=total_time, butterfly=get_butterfly, add_time=add_time,
                                       guild=interact.guild.name, fault='0', icon=interact.guild.icon, avatar=get_member.display_avatar).embed, view=view)
            else:
                await interact.response.edit_message(
                    embed=StaffProfile(member=get_member, total_event=total_event, total_time=total_time, butterfly=get_butterfly, add_time=add_time,
                                       guild=interact.guild.name, fault='0', icon=interact.guild.icon, avatar=get_member.display_avatar).embed, view=create_profile_view)

            async def edit_time_callback(inter: discord.Interaction):
                await inter.response.send_message(embed=DefaultEmbed(
                    f'{inter.user.name}, введите суммарное количество времени в секундах, которое хотите прибавить. __3600 с. = 1 ч.__\nИспользуйте (-) чтобы убавить.'), ephemeral=True)

                def check(m):
                    if m.channel == inter.channel:
                        if not m.author.bot:
                            return m

                msg = await client.wait_for('message', check=check)

                if msg.author.id == inter.user.id:
                    try:
                        number = int(msg.content)
                        cross_event_system.update_wasting_time(guild_id=inter.guild.id, clan_staff_id=member_id, waisting_time=number)
                        await inter.followup.send(embed=DefaultEmbed(f'Успешно изменено на: {msg.content} с. пользователю <@{member_id}>'), ephemeral=True)
                        await msg.delete()

                        staff_logger.info(f'{msg.author} изменил время ивентов {member_id} на {msg.content}')

                    except ValueError:
                        staff_logger.warn(f'{msg.author}, ввів погане значення для часу.')
                        await inter.followup.send(embed=DefaultEmbed('Не коректное число.'), ephemeral=True)
                        await msg.delete()
                else:
                    pass

            async def edit_event_callback(inter: discord.Interaction):
                await inter.response.send_message(embed=DefaultEmbed(
                    f'{inter.user.name}, введите количество ивентов, которое хотите прибавить.\nИспользуйте (-) чтобы убавить.'), ephemeral=True)

                def check(m):
                    if m.channel == inter.channel:
                        if not m.author.bot:
                            return m

                msg = await client.wait_for('message', check=check)

                if msg.author.id == inter.user.id:
                    try:
                        number = int(msg.content)
                        cross_event_system.update_number_event(guild_id=inter.guild.id, clan_staff_id=member_id, sum_event_ends=number)
                        await inter.followup.send(embed=DefaultEmbed(f'Успешно изменено на: {msg.content} ивентов. пользователю <@{member_id}>'), ephemeral=True)
                        await msg.delete()

                        staff_logger.info(f'{msg.author} изменил ивенты {member_id} на {msg.content}')

                    except ValueError:
                        await inter.followup.send(embed=DefaultEmbed('Не коректное число.'), ephemeral=True)
                        await msg.delete()
                else:
                    pass

            async def edit_butterfly_callback(inter: discord.Interaction):
                await inter.response.send_message(embed=DefaultEmbed(
                    f'{inter.user.name}, введите количество бабочек, которое хотите прибавить.\nИспользуйте (-) чтобы убавить.'), ephemeral=True)

                def check(m):
                    if m.channel == inter.channel:
                        if not m.author.bot:
                            return m

                msg = await client.wait_for('message', check=check)

                if msg.author.id == inter.user.id:
                    try:
                        number = int(msg.content)
                        cross_event_system.update_butterfly(guild_id=inter.guild.id, clan_staff_id=member_id, butterfly=number)
                        await inter.followup.send(embed=DefaultEmbed(f'Успешно изменено на: {msg.content} бабочек. пользователю <@{member_id}>'), ephemeral=True)
                        await msg.delete()

                        staff_logger.info(f'{msg.author} изменил бабочки {member_id} на {msg.content}')

                    except ValueError:
                        await inter.followup.send(embed=DefaultEmbed('Не коректное число.'), ephemeral=True)
                        await msg.delete()
                else:
                    pass

            async def edit_fault_callback(inter: discord.Interaction):
                pass

            async def back_callback(inter: discord.Interaction, context: ApplicationContext = None):
                await self.drop_menu(inter, context)

            edit_profile_view.button_time.callback = edit_time_callback
            edit_profile_view.button_event.callback = edit_event_callback
            edit_profile_view.button_butterflies.callback = edit_butterfly_callback
            edit_profile_view.button_back.callback = back_callback

        drop_down_menu.callback = menu_callback

    async def inventory(self, interaction: discord.Interaction, ctx: ApplicationContext = None, index: int = 1):
        if ctx is None:
            ctx = await self.client.get_application_context(interaction)
