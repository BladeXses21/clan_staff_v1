import discord
from discord import ApplicationContext, Interaction
from discord.ui import Select

from config import OWNER_IDS, SHOP_CHANNEL_ID, BLADEXSES_ID
from embeds.base import DefaultEmbed
from embeds.clan_embed.fault.fault_embed import FaultEmbed
from embeds.clan_embed.history.event_history import HistoryEmbed
from embeds.clan_embed.quest.quest_embed import QuestEmbed
from embeds.clan_embed.staff.profile import StaffProfile
from embeds.clan_embed.staff.shop import StaffShop
from embeds.clan_embed.view_builders.shop_view_builder import shop_edit_view
from embeds.clan_embed.view_builders.staff_menu_builder import clan_staff_view
from extensions.funcs import get_event_history, get_fault, get_quest_list
from extensions.logger import staff_logger
from main import client
from models.shop import shop_item
from database.systems.event_system import cross_event_system
from database.systems.saved_stats_system import save_stats_system


class ClanService:
    def __init__(self, client):
        self.client = client
        self.xp_lenght = 15

    async def drop_menu(self, interaction: Interaction, ctx: ApplicationContext = None):

        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        clan_staff_options = []

        for i in cross_event_system.enumeration_events_mode(ctx.guild.id):
            try:
                member = ctx.guild.get_member(i['clan_staff_id'])
                clan_staff_options.append(discord.SelectOption(label=i['clan_staff_id'], description=member.name, emoji='<a:_an:967471171480207420>'))
            except AttributeError:
                continue

        drop_down_menu = Select(options=clan_staff_options, placeholder='Выберите человека для отображения')

        view = discord.ui.View(timeout=None)
        view.add_item(drop_down_menu)

        try:
            author_id, t_events, t_times, my_add_time, my_curator, my_xp, my_avatar, my_background, my_birthday, my_color = cross_event_system.get_clan_staff(ctx.guild.id, ctx.author.id)
            my_lvl = cross_event_system.get_lvl_count(ctx.guild.id, ctx.author.id)
            my_butterfly = save_stats_system.get_butterfly(ctx.guild.id, ctx.author.id)
            if ctx.message is None:
                await ctx.response.send_message(
                    embed=StaffProfile(member=ctx.author, total_event=t_events, total_time=t_times, butterfly=my_butterfly, add_time=my_add_time, curator=f"<@{my_curator}>",
                                       xp=my_xp, avatar_img=my_avatar, background_img=my_background, birthday=my_birthday, color=my_color, lvl=my_lvl).embed, view=view, delete_after=160)
            else:
                await ctx.response.edit_message(
                    embed=StaffProfile(member=ctx.author, total_event=t_events, total_time=t_times, butterfly=my_butterfly, add_time=my_add_time, curator=f"<@{my_curator}>",
                                       xp=my_xp, avatar_img=my_avatar, background_img=my_background, birthday=my_birthday, color=my_color, lvl=my_lvl).embed, view=view, delete_after=160)
        except TypeError:
            if ctx.message is None:
                await ctx.response.send_message(embed=DefaultEmbed('***```Выберите пользователя```***'), view=view, delete_after=160)
            else:
                await ctx.response.edit_message(embed=DefaultEmbed('***```Выберите пользователя```***'), view=view, delete_after=160)

        async def delete_callback(intera: Interaction):
            if intera.user.id != ctx.author.id:
                return False
            await intera.message.delete()

        async def menu_callback(interact: Interaction):
            if interact.user.id != ctx.author.id:
                return False
            common_view = clan_staff_view.standart_profile_view(drop_down_menu)

            admin_view = clan_staff_view.admin_profile_view(drop_down_menu)

            member_id, total_event, total_time, add_time, curator, xp, avatar, background, birthday, color = cross_event_system.get_clan_staff(interact.guild.id, drop_down_menu.values[0])
            lvl = cross_event_system.get_lvl_count(interact.guild.id, drop_down_menu.values[0])
            try:
                get_butterfly = save_stats_system.get_butterfly(interact.guild.id, drop_down_menu.values[0])
            except TypeError:
                get_butterfly = 0
            get_member = interact.guild.get_member(member_id)

            if interact.user.id not in OWNER_IDS:
                # todo - подумать что делать с цветом профилей
                await interact.response.edit_message(
                    embed=StaffProfile(member=get_member, total_event=total_event, total_time=total_time, butterfly=get_butterfly, add_time=add_time, curator=f'<@{curator}>', xp=xp,
                                       avatar_img=avatar, background_img=background, birthday=birthday, color=color, lvl=lvl).embed,
                    view=common_view)
            else:
                await interact.response.edit_message(
                    embed=StaffProfile(member=get_member, total_event=total_event, total_time=total_time, butterfly=get_butterfly, add_time=add_time, curator=f'<@{curator}>', xp=xp,
                                       avatar_img=avatar, background_img=background, birthday=birthday, color=color, lvl=lvl).embed, view=admin_view)

            async def edit_time_callback(inter: Interaction):
                if inter.user.id != ctx.author.id:
                    return False

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
                        await inter.followup.send(embed=DefaultEmbed('Не коректное число.'), ephemeral=True, delete_after=10)
                        await msg.delete()
                else:
                    pass

            async def edit_event_callback(inter: Interaction):
                if inter.user.id != ctx.author.id:
                    return False
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

            async def edit_butterfly_callback(inter: Interaction):
                if inter.user.id != ctx.author.id:
                    return False
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
                        save_stats_system.update_butterfly(guild_id=inter.guild.id, clan_staff_id=member_id, butterfly=number)
                        await inter.followup.send(embed=DefaultEmbed(f'Успешно изменено на: {msg.content} бабочек. пользователю <@{member_id}>'), ephemeral=True)
                        await msg.delete()

                        staff_logger.info(f'{msg.author} изменил бабочки {member_id} на {msg.content}')

                    except ValueError:
                        await inter.followup.send(embed=DefaultEmbed('Не коректное число.'), ephemeral=True)
                        await msg.delete()
                else:
                    pass

            async def edit_xp_callback(inter: Interaction):
                if inter.user.id != ctx.author.id:
                    return False
                await inter.response.send_message(embed=DefaultEmbed(
                    f'{inter.user.name}, введите количество опыта, которое хотите прибавить.\nИспользуйте (-) чтобы убавить.'), ephemeral=True)

                def check(m):
                    if m.channel == inter.channel:
                        if not m.author.bot:
                            return m

                msg = await client.wait_for('message', check=check)

                if msg.author.id == inter.user.id:
                    try:
                        number = int(msg.content)
                        cross_event_system.update_xp_counter(guild_id=inter.guild.id, clan_staff_id=member_id, xp=number)
                        await inter.followup.send(embed=DefaultEmbed(f'Успешно изменено на: {msg.content} опыта. пользователю <@{member_id}>'), ephemeral=True)
                        await msg.delete()

                        staff_logger.info(f'{msg.author} изменил опыт {member_id} на {msg.content}')

                    except ValueError:
                        await inter.followup.send(embed=DefaultEmbed('Не коректное число.'), ephemeral=True)
                        await msg.delete()
                else:
                    pass

            async def quest_menu(inter: Interaction):
                if inter.user.id != ctx.author.id:
                    return False
                get_description = get_quest_list(guild_id=inter.guild.id, member_id=int(drop_down_menu.values[0]))
                clr, av = cross_event_system.get_color_and_avatar(guild_id=inter.guild.id, clan_staff_id=int(drop_down_menu.values[0]))
                await inter.response.edit_message(
                    embed=QuestEmbed(member=inter.guild.get_member(int(drop_down_menu.values[0])), description=get_description, msg_author=inter.user, color=clr, avatar=av).embed,
                    delete_after=90)

            async def history_menu(inter: Interaction):
                if inter.user.id != ctx.author.id:
                    return False
                clr, av = cross_event_system.get_color_and_avatar(guild_id=inter.guild.id, clan_staff_id=int(drop_down_menu.values[0]))
                get_description = get_event_history(guild_id=inter.guild.id, member_id=int(drop_down_menu.values[0]))
                await inter.response.edit_message(
                    embed=HistoryEmbed(member=inter.guild.get_member(int(drop_down_menu.values[0])), description=get_description, msg_author=inter.user, color=clr, avatar=av).embed,
                    delete_after=90)

            async def fault_menu(inter: Interaction):
                if inter.user.id != ctx.author.id:
                    return False
                clr, av = cross_event_system.get_color_and_avatar(guild_id=inter.guild.id, clan_staff_id=int(drop_down_menu.values[0]))
                date, reason, f_type = get_fault(guild_id=inter.guild.id, member_id=int(drop_down_menu.values[0]))
                await inter.response.edit_message(
                    embed=FaultEmbed(
                        member=inter.guild.get_member(int(drop_down_menu.values[0])), command_use=inter.user, date=date, reason=reason, fault_type=f_type,
                        color=clr, avatar=av).embed, delete_after=90)

            async def shop_menu(inter: Interaction):
                if inter.user.id != ctx.author.id:
                    return False
                view_1, select_menu = shop_edit_view.create_shop_list_view()
                await inter.response.edit_message(embed=StaffShop(inter.user, color=color).embed, view=view_1, delete_after=90)

                async def select_option(inte: Interaction):
                    if inte.user.id != ctx.author.id:
                        return False
                    user_butterfly = save_stats_system.get_butterfly(inte.guild.id, inte.user.id)
                    if user_butterfly < shop_item.SHOP_ITEM_AMOUNT[int(select_menu.values[0])]:
                        return await inter.followup.send(embed=DefaultEmbed("***```У вас не достаточное количество валюты для покупки.```***"), delete_after=10, ephemeral=True)

                    save_stats_system.update_butterfly(inte.guild.id, inte.user.id, -shop_item.SHOP_ITEM_AMOUNT[int(select_menu.values[0])])
                    await menu_callback(inte)

                    def check(m):
                        if m.channel == inter.channel:
                            return m

                    if select_menu.values[0] in ["4", "8", "11", "12", "13", "14", "16", "20"]:
                        values_content = shop_item.SHOP_ITEM_RESPONSE[int(select_menu.values[0])]
                        await inter.followup.send(embed=DefaultEmbed(values_content), delete_after=120)
                        return await inte.client.get_channel(SHOP_CHANNEL_ID).send(embed=DefaultEmbed(f'{inte.user.mention}\n{values_content}'))

                    if select_menu.values[0] == '15':
                        item_num = shop_item.get_random_item()
                        get_random_item = shop_item.RAND_ITEM_RESPONSE[item_num]
                        await inter.followup.send(embed=DefaultEmbed(get_random_item), delete_after=120)
                        return await inte.client.get_channel(SHOP_CHANNEL_ID).send(embed=DefaultEmbed(f'{inte.user.mention} выпал предмет под номером {str(item_num)}\n{get_random_item}'))

                    else:
                        values_content = shop_item.SHOP_ITEM_RESPONSE[int(select_menu.values[0])]
                        await inter.followup.send(embed=DefaultEmbed(values_content), delete_after=120)
                        msg = await client.wait_for('message', check=check)
                        if msg.author.id == inte.user.id:
                            await inte.client.get_channel(SHOP_CHANNEL_ID).send(content=f'<@&{BLADEXSES_ID}>', embed=DefaultEmbed(f'{inte.user.mention}\n{values_content}\n{msg.content}'))
                            return await msg.delete()

                # обработка запроса кураторов на магазин | историю и т.д.
                shop_edit_view.button_back_menu.callback = menu_callback

                select_menu.callback = select_option

            # обработка обычных челов клан стаффа на магазин | историю и т.д.
            clan_staff_view.button_shop.callback = shop_menu
            clan_staff_view.button_quest.callback = quest_menu
            clan_staff_view.button_history.callback = history_menu
            clan_staff_view.button_fault.callback = fault_menu
            clan_staff_view.button_trash.callback = delete_callback

            # обработка кураторов клан стаффа
            clan_staff_view.button_edit_time.callback = edit_time_callback
            clan_staff_view.button_edit_event.callback = edit_event_callback
            clan_staff_view.button_edit_butterflies.callback = edit_butterfly_callback
            clan_staff_view.button_edit_xp.callback = edit_xp_callback
            clan_staff_view.button_shop.callback = shop_menu
            drop_down_menu.callback = menu_callback
            clan_staff_view.button_trash_two.callback = delete_callback

        drop_down_menu.callback = menu_callback
