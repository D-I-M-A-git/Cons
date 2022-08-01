"""
Файл для створення бота
A file for creating a bot
"""
from aiogram import Bot, Dispatcher
import config as cfg

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)
