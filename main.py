"""
Файл для запуску бота
The file for starting the bot
"""
import logging

from aiogram.utils import executor

from create_bot import dp
from handlers import command_start_help
from handlers import command_dir
from handlers import command_report
from handlers import command_search

logging.basicConfig(level=logging.INFO)
print('START BOT')

command_search.register_handler_help(dp)
command_report.register_handler_report(dp)
command_start_help.register_handler_help(dp)
command_dir.register_handler_command_dir(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
