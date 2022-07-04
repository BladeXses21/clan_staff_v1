import discord
import os

from discord.ext import commands

from config import TOKEN, PREFIX
from extensions.logger import logger


client = commands.Bot(command_prefix=PREFIX,
                      help_command=None,
                      intents=discord.Intents.all())


@client.event
async def on_ready():
    logger.info('READY')


@client.event
async def on_command_error(ctx, error):
    if type(error) == commands.CommandNotFound:
        return
    logger.error(f'{str(ctx.author)} | {ctx.message.content}')
    logger.error(error)


for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN)