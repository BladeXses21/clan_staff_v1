import logging
import traceback

from discord.ext import commands


def get_logger(name):
    logging.basicConfig(
        format='%(asctime)s [%(name)s] [%(levelname)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[logging.FileHandler(f'clan_staff.log', encoding='utf-8'), logging.StreamHandler()]
    )
    logger = logging.getLogger(name)
    logger.setLevel(level=logging.DEBUG)
    return logger


logger = get_logger('clan_staff')
