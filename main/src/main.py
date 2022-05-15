import discord
import os
from discord.ext import commands

from config import TOKEN, PREFIX

client = commands.Bot(command_prefix=PREFIX,
                      help_command=None,
                      intents=discord.Intents.all())

for filename in os.listdir("src/cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN)
