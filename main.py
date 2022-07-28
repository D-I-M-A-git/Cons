# Імпорт модулів
import logging

from aiogram.utils import executor

from create_bot import gp
from handlers import command_dir

logging.basicConfig(level=logging.INFO)
print('START BOT')

command_dir.register_handlers_command_dir(gp)

if __name__ == "__main__":
    executor.start_polling(gp)
