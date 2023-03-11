"""
Файл для запуску бота
The file for starting the bot
"""
import logging

from aiogram.utils import executor

from create_bot import dp
from handlers import *

logging.basicConfig(level=logging.INFO)

command_search.register_handler_help(dp)
command_report.register_handler_report(dp)
command_start_help.register_handler_help(dp)
command_translator.register_handler_translation(dp)
command_weather.register_handler_weather(dp)
command_games.register_handler_games(dp)
command_rate.register_handler_rate(dp)
command_chat.register_handler_chat(dp)
command_save_open.register_handler_command_save_open(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
