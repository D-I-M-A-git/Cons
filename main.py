# Імпорт модулів
import logging

from aiogram.utils import executor

from create_bot import dp
from handlers import command_start_help
from handlers import command_dir

logging.basicConfig(level=logging.INFO)
print('START BOT')

command_start_help.register_handler_help(dp)
command_dir.register_handler_command_dir(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates= True)
