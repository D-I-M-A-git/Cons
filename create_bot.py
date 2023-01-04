"""
Файл для створення бота
A file for creating a bot
"""
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config as cfg

bot = Bot(token=cfg.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
