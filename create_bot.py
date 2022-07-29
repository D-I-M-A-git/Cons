from aiogram import Bot, Dispatcher
import config as cfg

# Створення бота і глобального списку
bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)
