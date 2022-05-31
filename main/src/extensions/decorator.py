from discord.ext import commands

from config import MAIN_OWNER, OWNER_IDS


def is_owner():
    def inner(ctx):
        if ctx.author.id == MAIN_OWNER:
            return True
        raise commands.CommandError(f'{ctx.author} not owner')

    return commands.check(inner)


def is_owner_rights():
    def inner(ctx):
        if ctx.author.id in OWNER_IDS:
            return True
        raise commands.CommandError(f'{ctx.author} not rights owner')

    return commands.check(inner)
