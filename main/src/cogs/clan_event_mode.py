import discord
from discord import ApplicationContext
from discord.commands import Option
from discord.ext import commands

from cogs.base import BaseCog
from config import TENDERLY_ID, META_ID, DARKNESS_ID, CLAN_STAFF, SWEETNESS_ID, OWNER_IDS
from database.clan_systems.event_history_system import event_history
from database.clan_systems.event_system import cross_event_system
from database.clan_systems.fault_system import fault_system
from database.clan_systems.quest_system import quest_system
from database.clan_systems.saved_stats_system import save_stats_system
from database.clan_systems.server_system import cross_server_system
from embeds.base import DefaultEmbed
from embeds.clan_embed.staff.fault.fault_embed import FaultEmbed
from embeds.clan_embed.staff.history.event_history import HistoryEmbed
from embeds.clan_embed.staff.quest.quest_embed import QuestEmbed
from embeds.clan_embed.staff.staff import StaffEmbed
from embeds.clan_embed.staff.staff_command import StaffCommandsEmbed
from embeds.clan_embed.view_builders.staff_view_builder import staff_view_builder
from embeds.view_builder import default_view_builder
from extensions.decorator import is_owner_rights
from extensions.funcs import get_guilds_list_async, get_staff_list_async, get_staff_event_list, \
    remove_clan_staff_response, add_clan_staff_response, \
    get_event_history, get_fault, get_quest_list, quest_info, quest_limit
from extensions.logger import staff_logger
from main import client
from service.event_service import EventService
from service.staff_service import ClanService


class CrossEventsMode(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        self.clan_service = ClanService(client)
        self.event_service = EventService(client)
        print("Cog 'clan event' connected!")

    event = discord.SlashCommandGroup('event', 'commands to request event')
    staffs = discord.SlashCommandGroup('staff', 'commands to request event')

    @commands.group(aliases=['стафф'])
    @commands.has_any_role(*CLAN_STAFF)
    async def staff(self, ctx):
        if not ctx.invoked_subcommand:
            if len(ctx.message.role_mentions) != 1:
                if ctx.author.id in OWNER_IDS:
                    return await ctx.send(embed=StaffCommandsEmbed().embed, delete_after=60)
                else:
                    pass

    @staff.command(description='Добавить человека в clan staff')
    @is_owner_rights()
    async def add(self, ctx, member: discord.Member):
        author_name = ctx.author.name
        guild = ctx.guild.id
        get_channel_id = cross_server_system.get_event_channel(guild_id=ctx.guild.id)
        event_channel = client.get_channel(get_channel_id)
        overwrite = discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)
        if member is None:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, вы не указали пользователя```***'),
                delete_after=60
            )

        if cross_server_system.find_guild_id(guild_id=guild) is False:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, клан стафф не существует на этом сервере```***'),
                delete_after=60
            )

        if cross_event_system.is_clan_staff(guild_id=guild, clan_staff_id=member.id) is True:
            return await ctx.send(
                embed=DefaultEmbed(
                    f'***```{author_name}, пользователь {member.name}, уже есть в списке clan staff```***'),
                delete_after=60
            )
        # <end>
        await event_channel.set_permissions(member, overwrite=overwrite)
        staff_logger.info(f'{ctx.author}, use !staff add to {member}')
        cross_event_system.add_clan_staff(guild_id=guild, clan_staff_id=member.id, curator=ctx.author.id)
        save_stats_system.create_stat(guild_id=guild, clan_staff_id=member.id)
        quest_system.formation_doc(guild_id=ctx.guild.id, clan_staff_id=member.id)
        event_history.create_history_list(guild_id=guild, clan_staff_id=member.id)
        fault_system.create_fault_list(guild_id=guild, clan_staff_id=member.id)
        await ctx.send(embed=DefaultEmbed(add_clan_staff_response(member)))
        return await ctx.message.delete()

    @staff.command(description='Убрать человека из clan staff')
    @is_owner_rights()
    async def kick(self, ctx, member: discord.Member):
        author_name = ctx.author.name
        guild = ctx.guild.id
        get_channel_id = cross_server_system.get_event_channel(guild_id=ctx.guild.id)
        event_channel = client.get_channel(get_channel_id)
        if member is None:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, вы не указали пользователя```***'),
                delete_after=60
            )

        if cross_server_system.find_guild_id(guild_id=guild) is False:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, клан стафф не существует на этом сервере```***'),
                delete_after=60
            )

        if cross_event_system.is_clan_staff(guild_id=guild, clan_staff_id=member.id) is False:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, пользователя {member.name}, нет в списке clan staff```***'),
                delete_after=60
            )

        await event_channel.set_permissions(member, overwrite=None)
        staff_logger.info(f'{ctx.author}, use !staff kick to {member}')
        cross_event_system.delete_clan_staff(guild_id=guild, clan_staff_id=member.id)
        quest_system.remove_quest_doc(guild_id=ctx.guild.id, clan_staff_id=member.id)
        event_history.remove_history_list(guild_id=guild, clan_staff_id=member.id)
        fault_system.remove_fault_list(guild_id=guild, clan_staff_id=member.id)
        await ctx.send(embed=DefaultEmbed(remove_clan_staff_response(member)))
        return await ctx.message.delete()

    @staff.command(description='Очистка статы clan staff')
    @is_owner_rights()
    async def clear(self, ctx):
        author_name = ctx.author.name
        guild = ctx.guild.id
        def_view = default_view_builder.create_choice_view()

        if cross_server_system.find_guild_id(guild_id=guild) is False:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, клан стафф не существует на этом сервере```***'),
                delete_after=60
            )

        msg = await ctx.send(
            embed=DefaultEmbed(f'{ctx.author.name}, подтвердите очистку статистики.'),
            view=def_view,
            delete_after=60
        )

        async def accept_callback(interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                return False

            cross_event_system.reset_staff_stats(guild)
            return await msg.edit(
                embed=DefaultEmbed(
                    f'***```{author_name}, вы успешно очистили статистику clan staff на {ctx.guild.name}```***'),
                view=default_view_builder.create_view()
            )

        async def decline_callback(interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                return False

            return await msg.edit(
                embed=DefaultEmbed(f'Команда была отклонена'),
                view=default_view_builder.create_view()
            )

        default_view_builder.button_accept.callback = accept_callback
        default_view_builder.button_decline.callback = decline_callback

    @staff.command(description='Просмотреть список всех челиксов из clan staff')
    @commands.has_any_role(*CLAN_STAFF)
    async def list(self, ctx):
        staff_button = staff_view_builder.create_staff_list_view()
        members = cross_event_system.get_event_organizers(guild_id=ctx.guild.id)
        description = get_staff_event_list(members, guild_id=ctx.guild.id)
        list_response = await ctx.send(
            embed=StaffEmbed(
                description=description,
                guild=ctx.guild.name,
                user=ctx.author.name,
                icon=ctx.guild.icon
            ).embed,
            view=staff_button,
            delete_after=160
        )
        await ctx.message.delete()

        async def tenderly_callback(interact: discord.Interaction):
            await get_staff_list_async(
                interaction=interact,
                ctx=ctx,
                server_id=TENDERLY_ID,
                list_response=list_response,
                button=staff_button
            )

        async def meta_callback(interact: discord.Interaction):
            await get_staff_list_async(
                interaction=interact,
                ctx=ctx,
                server_id=META_ID,
                list_response=list_response,
                button=staff_button
            )

        async def darkness_callback(interact: discord.Interaction):
            await get_staff_list_async(
                interaction=interact,
                ctx=ctx,
                server_id=DARKNESS_ID,
                list_response=list_response,
                button=staff_button
            )

        async def sweetness_callback(interact: discord.Interaction):
            await get_staff_list_async(
                interaction=interact,
                ctx=ctx,
                server_id=SWEETNESS_ID,
                list_response=list_response,
                button=staff_button
            )

        async def guild_callback(interact: discord.Interaction):
            guild_button = staff_view_builder.create_guild_list_view()
            await get_guilds_list_async(
                interaction=interact,
                ctx=ctx,
                clan_id=TENDERLY_ID,
                list_response=list_response,
                button=guild_button
            )

            async def guild_tenderly_callback(inter: discord.Interaction):
                await get_guilds_list_async(
                    interaction=inter,
                    ctx=ctx,
                    clan_id=TENDERLY_ID,
                    list_response=list_response,
                    button=guild_button
                )

            async def guild_meta_callback(inter: discord.Interaction):
                await get_guilds_list_async(
                    interaction=inter,
                    ctx=ctx,
                    clan_id=META_ID,
                    list_response=list_response,
                    button=guild_button
                )

            async def guild_darkness_callback(inter: discord.Interaction):
                await get_guilds_list_async(
                    interaction=inter,
                    ctx=ctx,
                    clan_id=DARKNESS_ID,
                    list_response=list_response,
                    button=guild_button
                )

            async def guild_sweetness_callback(inter: discord.Interaction):
                await get_guilds_list_async(
                    interaction=inter,
                    ctx=ctx,
                    clan_id=SWEETNESS_ID,
                    list_response=list_response,
                    button=guild_button
                )

            staff_view_builder.button_guild_tenderly.callback = guild_tenderly_callback
            staff_view_builder.button_guild_meta.callback = guild_meta_callback
            staff_view_builder.button_guild_darkness.callback = guild_darkness_callback
            staff_view_builder.button_guild_sweetness.callback = guild_sweetness_callback
            staff_view_builder.button_guild_back.callback = tenderly_callback

        staff_view_builder.button_tenderly.callback = tenderly_callback
        staff_view_builder.button_meta.callback = meta_callback
        staff_view_builder.button_darkness.callback = darkness_callback
        staff_view_builder.button_sweetness.callback = sweetness_callback
        staff_view_builder.button_guild.callback = guild_callback

    @event.command(name='request', description='Запрос ивента в клане', default_permission=True)
    async def request(self, interaction: discord.Interaction,
                      event_num: Option(int, 'укажите номер ивента из чата #клан-ивенты',
                                        min_value=1, max_value=61, required=True),
                      users_count: Option(int, 'Введите количество человек на ивенте.', required=True),
                      comment: Option(str, 'Введите коментарий к ивенту.', required=True)):
        await self.event_service.event_request(event_num=event_num, users_count=users_count, comment=comment,
                                               interaction=interaction)

    @staffs.command(name='profile', description='Профиль clan staff', default_permission=False)
    @commands.has_any_role(*CLAN_STAFF)
    async def profile(self, interaction: discord.Interaction):
        staff_logger.info(f'{interaction.user.name} use command /staff profile')
        await self.clan_service.drop_menu(interaction)

    @staff.command(description='see your event history')
    @commands.has_any_role(*CLAN_STAFF)
    async def quest(self, ctx: ApplicationContext, member: discord.Member = None):
        author = ctx.author
        if member is not None:
            get_description = get_quest_list(guild_id=ctx.guild.id, member_id=member.id)
            color, avatar = cross_event_system.get_color_and_avatar(guild_id=ctx.guild.id, clan_staff_id=member.id)
            await ctx.send(embed=QuestEmbed(member=member, description=get_description, msg_author=author, color=color,
                                            avatar=avatar).embed, delete_after=90)
            return await ctx.message.delete()
        else:
            get_description = get_quest_list(guild_id=ctx.guild.id, member_id=author.id)
            color, avatar = cross_event_system.get_color_and_avatar(guild_id=ctx.guild.id, clan_staff_id=author.id)
            await ctx.send(embed=QuestEmbed(member=author, description=get_description, msg_author=author, color=color,
                                            avatar=avatar).embed, delete_after=90)
            return await ctx.message.delete()

    @staff.command(description='see your event history')
    @commands.has_any_role(*CLAN_STAFF)
    async def his(self, ctx: ApplicationContext, member: discord.Member = None):
        try:
            if member is not None:
                staff_logger.info(f'{ctx.author.name} use command !staff his on {member.name}')
                get_description = get_event_history(guild_id=ctx.guild.id, member_id=member.id)
                color, avatar = cross_event_system.get_color_and_avatar(guild_id=ctx.guild.id, clan_staff_id=member.id)
                await ctx.send(
                    embed=HistoryEmbed(member=member, description=get_description, msg_author=ctx.author, color=color,
                                       avatar=avatar).embed, delete_after=90)
                return await ctx.message.delete()
        except TypeError:
            await ctx.send(embed=DefaultEmbed('***```История участника пуста или его нет в списке.```***'),
                           delete_after=30)
            return await ctx.message.delete()
        try:
            if member is None:
                staff_logger.info(f'{ctx.author.name} use command !staff his')
                get_description = get_event_history(guild_id=ctx.guild.id, member_id=ctx.author.id)
                color, avatar = cross_event_system.get_color_and_avatar(guild_id=ctx.guild.id,
                                                                        clan_staff_id=ctx.author.id)
                await ctx.send(embed=HistoryEmbed(member=ctx.author, description=get_description, msg_author=ctx.author,
                                                  color=color, avatar=avatar).embed, delete_after=90)
                return await ctx.message.delete()
        except TypeError:
            await ctx.send(embed=DefaultEmbed('***```История участника пуста или его нет в списке.```***'),
                           delete_after=30)
            return await ctx.message.delete()

    @staff.command(description='clear event history')
    @is_owner_rights()
    async def clear_his(self, ctx: ApplicationContext):
        event_history.clear_history(ctx.guild.id)
        await ctx.send(embed=DefaultEmbed(f'***```История участников на сервере {ctx.guild.name}, была сброшена.```***'), delete_after=30)
        return await ctx.message.delete()

    @staff.command(description='clear event history')
    @is_owner_rights()
    async def warn(self, ctx: ApplicationContext, member: discord.Member, reason: str, f_type: str):
        fault_system.add_fault(guild_id=ctx.guild.id, clan_staff_id=member.id, reason=reason, fault_type=f_type)
        await ctx.send(embed=DefaultEmbed(f'***```{member.name}, получил выговор по причине {reason} с типом {f_type}```***'))
        return await ctx.message.delete()

    @staff.command(description='see your fault')
    @commands.has_any_role(*CLAN_STAFF)
    async def fault(self, ctx: ApplicationContext, member: discord.Member = None):
        try:
            if member is None:
                staff_logger.info(f'{ctx.author.name} use command !staff fault')
                date, reason, f_type = get_fault(guild_id=ctx.guild.id, member_id=ctx.author.id)
                color, avatar = cross_event_system.get_color_and_avatar(guild_id=ctx.guild.id,
                                                                        clan_staff_id=ctx.author.id)
                await ctx.send(embed=FaultEmbed(member=ctx.author, command_use=ctx.author, date=date, reason=reason,
                                                fault_type=f_type, color=color, avatar=avatar).embed)
        except:
            await ctx.send(embed=DefaultEmbed('***```История участника пуста или его нет в списке.```***'),
                           delete_after=30)
        try:
            staff_logger.info(f'{ctx.author.name} use command !staff fault on {member.name}')
            date, reason, f_type = get_fault(guild_id=ctx.guild.id, member_id=member.id)
            color, avatar = cross_event_system.get_color_and_avatar(guild_id=ctx.guild.id, clan_staff_id=member.id)
            await ctx.send(
                embed=FaultEmbed(member=member, command_use=ctx.author, date=date, reason=reason, fault_type=f_type,
                                 color=color, avatar=avatar).embed)
        except:
            await ctx.send(embed=DefaultEmbed('***```История участника пуста или его нет в списке.```***'),
                           delete_after=30)
        return await ctx.message.delete()

    @staff.command(description='update birthday user')
    @is_owner_rights()
    async def dr(self, ctx: ApplicationContext, member: discord.Member, *args: str):
        birthday = ' '.join(args)
        if member is None:
            return await ctx.send(
                embed=DefaultEmbed('***```Ошибка | Форма команды: !staff dr [id/@link] [new_birthday]```***'),
                delete_after=10)
        # if len(args) <= 2:
        #     return await ctx.send(embed=DefaultEmbed('***```Укажите больше 2 символов```***'), delete_after=10)
        cross_event_system.update_birthday(ctx.guild.id, member.id, birthday)
        await ctx.send(embed=DefaultEmbed(f'***```{member.name}, успешно обновлен на {birthday}```***'),
                       delete_after=30)
        return await ctx.message.delete()

    @staff.command(description='update user avatar')
    @is_owner_rights()
    async def av(self, ctx: ApplicationContext, member: discord.Member, avatar_url: str):
        if member is None:
            return await ctx.send(embed=DefaultEmbed('***```Ошибка | участник не указан```***'), delete_after=10)
        if avatar_url is None:
            return await ctx.send(embed=DefaultEmbed('***```Ошибка | avatar_url не указан```***'), delete_after=10)
        cross_event_system.update_avatar(guild_id=ctx.guild.id, clan_staff_id=member.id, new_avatar=avatar_url)
        await ctx.send(embed=DefaultEmbed(f'***```{member.name}, аватар обновлен```***'), delete_after=10)
        return await ctx.message.delete()

    @staff.command(description='update user background')
    @is_owner_rights()
    async def back(self, ctx: ApplicationContext, member: discord.Member, background_url: str):
        if member is None:
            return await ctx.send(embed=DefaultEmbed('***```Ошибка | участник не указан```***'), delete_after=10)
        if background_url is None:
            return await ctx.send(embed=DefaultEmbed('***```Ошибка | background_url не указан```***'), delete_after=10)
        cross_event_system.update_background(guild_id=ctx.guild.id, clan_staff_id=member.id,
                                             new_background=background_url)
        await ctx.send(embed=DefaultEmbed(f'***```{member.name}, background обновлен```***'), delete_after=10)
        return await ctx.message.delete()

    @staff.command(description='remove user warn')
    @is_owner_rights()
    async def unwarn(self, ctx: ApplicationContext, member: discord.Member, warn_index: int):
        if member is None:
            return await ctx.send(embed=DefaultEmbed('***```Ошибка | участник не указан```***'), delete_after=10)
        if warn_index is None:
            return await ctx.send(embed=DefaultEmbed('***```Ошибка | номер выговора не указан```***'), delete_after=10)
        fault_system.remove_the_fault(guild_id=ctx.guild.id, clan_staff_id=member.id, warn_index=warn_index)
        return await ctx.send(embed=DefaultEmbed(f'***```Выговор: {warn_index} был снят.```***'), delete_after=10)

    @staff.command()
    @is_owner_rights()
    async def new_quest(self, ctx, timer: int, xp: int, *args: str):
        name = ' '.join(args)
        response = ''
        guild_id = ctx.guild.id
        _members = cross_event_system.get_event_organizers(guild_id=guild_id)
        try:
            for member in _members:
                if quest_limit(guild_id=guild_id, member_id=member['clan_staff_id']) is True:
                    quest_system.create_new_quest(guild_id=guild_id, member_id=member['clan_staff_id'], name=name,
                                                  timer=timer, xp=xp)
                    response += f'<@{member["clan_staff_id"]}> ***`квест {name} | {timer} m. | {xp} xp, заряжен;`***\n'
                else:
                    response += f'<@{member["clan_staff_id"]}> ***`пользователь достиг лимита, квест не заряжен;`***\n'
        except ValueError as e:
            await ctx.send(embed=DefaultEmbed(
                f"***```Error: {str(e)}\nCorrect command: !staff new_quest timer xp event_name```***"), delete_after=10)
        await ctx.send(embed=DefaultEmbed(response + "***```Зарядка окончена.```***"), delete_after=120)
        return await ctx.message.delete()

    @staff.command()
    @is_owner_rights()
    async def rem_quest(self, ctx, member: discord.Member = None, *args: str):
        name = ' '.join(args)
        if member is not None:
            xp, timer = quest_info(ctx.guild.id, member.id)
            quest_system.remove_quest(guild_id=ctx.guild.id, clan_staff_id=member.id, name=name)
            return await ctx.send(embed=DefaultEmbed(
                f'***```Квест {name} {xp[name]} xp. {timer[name]} timer. у {member.name} был удален ```***'))
        _members = cross_event_system.get_event_organizers(guild_id=ctx.guild.id)
        for member in _members:
            quest_system.remove_quest(guild_id=ctx.guild.id, clan_staff_id=member['clan_staff_id'], name=name)
        await ctx.send(embed=DefaultEmbed('***```Квест сброшен со всех ивентеров.```***'))
        return await ctx.message.delete()

    @staff.command()
    @is_owner_rights()
    async def refresh(self, ctx, member: discord.Member):
        cross_event_system.refresh(guild_id=ctx.guild.id, member_id=member.id)
        await ctx.send(embed=DefaultEmbed(f'***```{member.name}, теперь может проводить ивент без ошибок```***'))
        return await ctx.message.delete()


def setup(bot):
    bot.add_cog(CrossEventsMode(bot))
