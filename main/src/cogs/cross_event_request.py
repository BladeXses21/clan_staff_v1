import asyncio
import discord
from discord import Embed
from discord.commands import Option
from discord.ext import commands, tasks
from asyncio import TimeoutError

from embeds.clan_events_mode.event_mode_view.guild_list_view_builder import cross_staff_view_builder
from embeds.clan_events_mode.event_mode_view.event_request_view_builder import event_request_view_builder
from embeds.clan_events_mode.request_event_embed.embed_request_accept_event_mode import accept_event_embed
from embeds.clan_events_mode.request_event_embed.embed_request_decline_event_mode import decline_event_embed
from embeds.clan_events_mode.request_event_embed.embed_request_to_event_mode import full_request_respons
from embeds.clan_events_mode.request_event_embed.embed_request_pass_event_mode import pass_event_embed
from embeds.clan_events_mode.staff_embed.staff_list import StaffListEmbed, GuildListEmbed
from embeds.clan_events_mode.staff_embed.auction import AuctionStartEmbed
from embeds.clan_events_mode.staff_embed.staff_command import StaffCommandEmbed
from embeds.def_view_builder import default_view_builder
from embeds.def_embed import DefaultEmbed
from systems.clan_staff.cross_event_request_system import cross_event_system
from clan_staff_service.event_dict import all_events
from config import PREFIX, TENDERLY_ID, META_ID, DARKNESS_ID, HATORY_ID, CLAN_STAFF, OWNER_IDS
from base.funcs import *
from cogs.base import BaseCog
from main import client


class CrossEventsMode(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        print("Cog 'clan event' connected!")

    event = discord.SlashCommandGroup('event', 'commands to request event')

    @commands.group(aliases=['стафф'])
    @commands.has_any_role(*CLAN_STAFF)
    async def staff(self, ctx):
        if not ctx.invoked_subcommand:
            if len(ctx.message.role_mentions) != 1:
                return await ctx.send(embed=StaffCommandEmbed().embed, delete_after=60)

    @staff.command(description='Добавить человека в clan staff')
    async def add(self, ctx, member: discord.Member):
        author_name = ctx.author.name
        guild = ctx.guild.id

        # TODO: replace it into a method 'is_owner(id: int)'
        if ctx.author.id not in OWNER_IDS:
            return False

        # TODO: make method for it
        # <start>
        if member is None:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, вы не указали пользователя```***'),
                delete_after=60
            )

        if cross_event_system.find_guild_id(guild_id=guild) is False:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, клан стафф не существует на этом сервере```***'),
                delete_after=60
            )

        if cross_event_system.does_it_clan_staff(guild_id=guild, clan_staff_id=member.id) is True:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, пользователь {member.name}, уже есть в списке clan staff```***'),
                delete_after=60
            )
        # <end>

        cross_event_system.add_clan_staff(guild_id=guild, clan_staff_id=member.id)
        return await ctx.send(embed=DefaultEmbed(add_clan_staff_response(member)))

    @staff.command(description='Убрать человека из clan staff')
    async def kick(self, ctx, member: discord.Member):
        author_name = ctx.author.name
        guild = ctx.guild.id

        if ctx.author.id not in OWNER_IDS:
            return False

        if member is None:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, вы не указали пользователя```***'),
                delete_after=60
            )

        if cross_event_system.find_guild_id(guild_id=guild) is False:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, клан стафф не существует на этом сервере```***'),
                delete_after=60
            )

        if cross_event_system.does_it_clan_staff(guild_id=guild, clan_staff_id=member.id) is False:
            return await ctx.send(
                embed=DefaultEmbed(f'***```{author_name}, пользователя {member.name}, нет в списке clan staff```***'),
                delete_after=60
            )

        cross_event_system.remove_clan_staff(guild_id=guild, clan_staff_id=member.id)
        return await ctx.send(embed=DefaultEmbed(remove_clan_staff_response(member)))

    @staff.command(description='Очистка статы clan staff')
    async def clear(self, ctx):
        author_name = ctx.author.name
        guild = ctx.guild.id
        def_view = default_view_builder.chose_puth()

        if ctx.author.id not in OWNER_IDS:
            return False

        if cross_event_system.find_guild_id(guild_id=guild) is False:
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

            cross_event_system.clear_staff_stats(guild)
            return await msg.edit(
                embed=DefaultEmbed(f'***```{author_name}, вы успешно очистили статистику clan staff на {ctx.guild.name}```***'),
                delete_after=60,
                view=default_view_builder.remove_chose()
            )

        async def decline_callback(interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                return False

            return await msg.edit(
                embed=DefaultEmbed(f'Команда была отклонена'),
                delete_after=60,
                view=default_view_builder.remove_chose()
            )

        default_view_builder.button_accept.callback = accept_callback
        default_view_builder.button_decline.callback = decline_callback

    @staff.command(description='Просмотреть список всех челиксов из clan staff')
    @commands.has_any_role(*CLAN_STAFF)
    async def list(self, ctx):
        staff_button = cross_staff_view_builder.staff_list_view()
        members = cross_event_system.enumeration_events_mode(guild_id=ctx.guild.id)
        description = get_staff_event_list(members)
        list_response = await ctx.send(
            embed=StaffListEmbed(
                description=description,
                guild=ctx.guild.name,
                user=ctx.author.name,
                icon=ctx.guild.icon
            ).embed,
            view=staff_button,
            delete_after=160
        )

        async def tenderly_callback(interact: discord.Interaction):
            await get_staff_list_async(
                interaction=interact,
                ctx=ctx,
                clan_id=TENDERLY_ID,
                list_response=list_response,
                button=staff_button
            )

        async def meta_callback(interact: discord.Interaction):
            await get_staff_list_async(
                interaction=interact,
                ctx=ctx,
                clan_id=META_ID,
                list_response=list_response,
                button=staff_button
            )

        async def darkness_callback(interact: discord.Interaction):
            await get_staff_list_async(
                interaction=interact,
                ctx=ctx,
                clan_id=DARKNESS_ID,
                list_response=list_response,
                button=staff_button
            )

        async def hatory_callback(interact: discord.Interaction):
            await get_staff_list_async(
                interaction=interact,
                ctx=ctx,
                clan_id=HATORY_ID,
                list_response=list_response,
                button=staff_button
            )

        async def guild_callback(interact: discord.Interaction):
            guild_button = cross_staff_view_builder.guild_list_view()
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

            async def guild_hatory_callback(inter: discord.Interaction):
                await get_guilds_list_async(
                    interaction=inter,
                    ctx=ctx,
                    clan_id=HATORY_ID,
                    list_response=list_response,
                    button=guild_button
                )

            cross_staff_view_builder.button_guild_tenderly.callback = guild_tenderly_callback
            cross_staff_view_builder.button_guild_meta.callback = guild_meta_callback
            cross_staff_view_builder.button_guild_darkness.callback = guild_darkness_callback
            cross_staff_view_builder.button_guild_hatory.callback = guild_hatory_callback
            cross_staff_view_builder.button_guild_back.callback = tenderly_callback

        cross_staff_view_builder.button_tenderly.callback = tenderly_callback
        cross_staff_view_builder.button_meta.callback = meta_callback
        cross_staff_view_builder.button_darkness.callback = darkness_callback
        cross_staff_view_builder.button_hatory.callback = hatory_callback
        cross_staff_view_builder.button_guild.callback = guild_callback

    @event.command(name='request', description='Запрос ивента в клане', default_permission=True)
    async def request(self, interaction: discord.Interaction,
                      event_num: Option(int, 'укажите номер ивента из чата #клан-ивенты',
                                        min_value=1, max_value=61, required=True),
                      users_count: Option(int, 'Введите количество человек на ивенте.', required=True),
                      comment: Option(str, 'Введите коментарий к ивенту.', required=True)):
        guild = interaction.guild
        event_num = all_events[event_num]

        channel_id, role_id, text_category_id, voice_category_id = cross_event_system.get_all_by_guild_id(guild.id)
        event_request_view = event_request_view_builder.create_event_request_view()

        member_ids = is_member_in_voice(guild.categories, client.get_channel(voice_category_id).name)
        get_event_channel = client.get_channel(channel_id)

        if interaction.user.id not in member_ids:
            return await interaction.response.send_message(
                embed=DefaultEmbed(f'***```Вы должны быть в голосовом канале клана.```***'),
                ephemeral=True
            )

        clan_name = interaction.user.voice.channel.name

        request_msg = await full_request_respons(
            interaction=interaction, event_channel=get_event_channel,
            role_id=role_id, event_num=event_num, users_count=users_count,
            comment=comment, event_request_view=event_request_view
        )

        cross_event_system.create_request(
            guild_id=interaction.guild.id, message_id=request_msg.id,
            clan_name=clan_name, event_num=event_num,
            member_send_request=interaction.user.id, comment=comment
        )

        async def accept_callback(ctx):
            user = ctx.user
            server = ctx.guild
            get_msg = client.get_message(ctx.message.id)
            ev_num, com, clan_n, member_send_id = cross_event_system.get_field_request(guild_id=server.id,
                                                                                       message_id=get_msg.id)
            get_member_send = ctx.guild.get_member(member_send_id)

            if cross_event_system.does_it_clan_staff(server.id, user.id) is False:
                return await ctx.response.send_message(
                    embed=DefaultEmbed(f'***```{user.name}, тебя нет в clan staff```***'),
                    ephemeral=True
                )

            if cross_event_system.check_on_request_id(server.id, user.id) is False:
                return await ctx.response.send_message(
                    embed=DefaultEmbed(f'***```{user.name}, ты не закончил прошлый ивент.```***'),
                    ephemeral=True
                )

            cross_event_system.accept_event_request(
                guild_id=server.id,
                message_id=request_msg.id,
                clan_staff_id=user.id
            )

            event_request_view.remove_item(event_request_view_builder.button_accept)
            event_request_view.remove_item(event_request_view_builder.button_decline)

            pass_view = event_request_view_builder.pass_event_request_view()

            await accept_event_embed(
                user=get_member_send,
                request_msg=get_msg,
                clan_name=clan_n,
                event_num=ev_num,
                clan_staff=user,
                pass_view=pass_view
            )

        async def decline_callback(ctx):
            user = ctx.user
            server = ctx.guild
            get_msg = client.get_message(ctx.message.id)
            ev_num, com, clan_n, member_send_id = cross_event_system.get_field_request(guild_id=server.id,
                                                                                       message_id=get_msg.id)
            get_member_send = ctx.guild.get_member(member_send_id)

            if cross_event_system.does_it_clan_staff(server.id, user.id) is False:
                return await ctx.response.send_message(
                    embed=DefaultEmbed(f'***```{user.name}, тебя нет в clan staff```***'),
                    ephemeral=True
                )

            if cross_event_system.check_on_request_id(server.id, user.id) is False:
                return await ctx.response.send_message(
                    embed=DefaultEmbed(f'***```{user.name}, ты не закончил прошлый ивент.```***'),
                    ephemeral=True
                )

            cross_event_system.delete_request(guild_id=server.id, message_id=get_msg.id)

            event_request_view.remove_item(event_request_view_builder.button_accept)
            event_request_view.remove_item(event_request_view_builder.button_decline)

            await decline_event_embed(
                user=get_member_send,
                request_msg=get_msg,
                clan_name=clan_n,
                event_num=ev_num,
                clan_staff=user,
                decline_view=event_request_view
            )

        async def pass_callback(ctx):
            user = ctx.user
            server = ctx.guild
            message = ctx.message
            channel = client.get_channel(ctx.channel.id)
            get_msg = await channel.fetch_message(message.id)
            ev_num, com, clan_n, member_send_id = cross_event_system.get_field_request(guild_id=server.id,
                                                                                       message_id=message.id)

            time_accept = cross_event_system.get_time_accept_request(guild_id=server.id,
                                                                     message_id=message.id)

            request_member_id = cross_event_system.get_request_msg_id(guild_id=server.id,
                                                                      clan_staff_id=user.id)

            event_request_view.remove_item(event_request_view_builder.button_pass)

            if cross_event_system.does_it_clan_staff(server.id, user.id) is False:
                return await ctx.response.send_message(
                    embed=DefaultEmbed(f'***```{user.name}, тебя нет в clan staff```***'),
                    ephemeral=True
                )

            if request_member_id != message.id:
                return await ctx.response.send_message(
                    embed=DefaultEmbed(f'***```{user.name}, это не ваш ивент.```***'),
                    ephemeral=True
                )

            await ctx.response.send_message(embed=DefaultEmbed(
                f'***```{user.name}, введите конечный итог ивента по форме\n'
                f'@link [количество конфет] @link [количество конфет]...```***'),
                ephemeral=True
            )

            def check(m):
                if m.channel == channel:
                    if not m.author.bot:
                        return m

            msg = await client.wait_for('message', check=check)

            if msg.author.id == ctx.user.id:
                sum_time_event = sum_event_time(guild=server.id, message_id=message.id)

                await pass_event_embed(
                    request_msg=get_msg, event_num=ev_num, clan_name=clan_n,
                    clan_staff=user, sum_time_event=sum_time_event,
                    time_accept_request=time_accept, comment=com,
                    pass_view=event_request_view, end_result=msg.content
                )

                cross_event_system.pass_request(guild_id=server.id, clan_staff_id=user.id,
                                                waisting_time=int(time.time()) - int(time_accept))
                cross_event_system.delete_request(guild_id=server.id, message_id=message.id)
                await msg.delete()
                print(ev_num, com, clan_n, user.name, 'Ивент завершен!')

        event_request_view_builder.button_decline.callback = decline_callback
        event_request_view_builder.button_accept.callback = accept_callback
        event_request_view_builder.button_pass.callback = pass_callback

    # @tasks.loop(time=datetime.time(0, 0, 1, 0))
    # def clear(self):
    #     pass


# todo - Дневные задания ||| Балы и магазин - clan staff ||| Команда /close request |||
#  автоматически отклонять ивент если его не приняли на протяжении 15 минут |||
#  !staff add - возможность удаления сервера, указывая только его id |||
# todo - профиль для челиксов из clan staff - выбор рабочих дней(онли куратор) -
#  выбор выходных(онли куратор) - стата проведенных ивентов для каждого для и сумарно - поинты по времени - выговоры.


def setup(bot):
    bot.add_cog(CrossEventsMode(bot))
