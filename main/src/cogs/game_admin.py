import discord
from discord.ext import commands
import urllib.request

from cogs.base import BaseCog
from discord import slash_command, Interaction, Bot, ApplicationContext

from config import PERMISSION_ROLE
from database.game_system.boss_system import boss_system
from embeds.base import DefaultEmbed
from embeds.game.admin_game.admin_help_embed import AdminHelpEmbed
from extensions.logger import staff_logger


class GameAdmin(BaseCog):
    def __init__(self, client: Bot):
        super().__init__(client)
        print('Cog "GameAdmin connected"')

    games = discord.SlashCommandGroup('game', 'commands to game')

    @commands.group(aliases=['админ'])
    @commands.has_any_role(*PERMISSION_ROLE)
    async def admin(self, ctx: ApplicationContext):
        # todo - invoked_subcommand
        if not ctx.invoked_subcommand:
            staff_logger.info(f'{ctx.author}')
            return await ctx.send(embed=AdminHelpEmbed().embed, delete_after=60)

    @admin.command(description='Создать боса для игры | Create enemy for game')
    @commands.has_any_role(*PERMISSION_ROLE)
    async def create_enemy(self, ctx: ApplicationContext, name: str, health: int, attack_dmg: int, image: str):
        if name or health or attack_dmg or image is None:
            return await ctx.send(embed=DefaultEmbed(f'***```{ctx.author.name}, check argument.```***'),
                                  delete_after=10)
        try:
            urllib.request.urlopen(image)
        except ValueError | TypeError as e:
            return await ctx.send(embed=DefaultEmbed(f'***```{ctx.author.name}, check link.\n{str(e)}.```***'),
                                  delete_after=20)
        boss_system.create_boss(name=name, health=health, attack_dmg=attack_dmg, image=image)
        await ctx.send(embed=DefaultEmbed(
            f'***```boss {name} has been created```***\nhis argument n:{name} h:{health} a:{attack_dmg} i:{image}'))


def setup(bot):
    bot.add_cog(GameAdmin(bot))
