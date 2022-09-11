"""Файл для надішлення допомоги"""
from aiogram import types, Dispatcher

from create_bot import bot


async def help(message: types.Message):
    """
    Функція для надішлення повідомлення з поясненням

    :param message: для можливості проглянути chat_id, щоб знати куда надіслати повідомлення
    """
    chat_id = message.chat.id
    help_message = "КОМАНДИ ДЛЯ АДМІНА:\n" \
                   "    @dir <шлях>: Показати всі файли за наведеним шляхом\n" \
                   "    @dir back: Зробити бекап\n" \
                   "    @dir view: Показати файли за збереженим шляхом\n" \
                   "    @dir image txt: Показати всі імена доступних зображень\n" \
                   "    @dir image img: Надіслати всі зображення (з іменами в описі зображення)\n" \
                   "    @dir image <ім'я зображення або шлях до нього>: Показати зображення\n" \
                   "    @dir my: Показати моє розташування у файловій системі\n" \
                   "КОМАНДИ ДЛЯ ЗВИЧАЙНИХ ЛЮДЕЙ:\n" \
                   "    /start, /help: Показати це повідомлення\n" \
                   "    /report або !report: Надіслати у відповідь на негарне повідомлення\n" \
                   "    /search <текст>: Пошук в Wikipedia\n" \
                   "    @save <текст>: Зберегти повідомлення\n" \
                   "    @open: Показати збережене повідомлення"
    await bot.send_message(chat_id=chat_id, text=help_message)


def register_handler_help(dp: Dispatcher):
    """
    Функція регістрації help

    :param dp: Потрібно для регістрації help
    """
    dp.register_message_handler(help, commands=["start", "help"])
