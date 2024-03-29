"""
Файл для обробки репортів
File for processing reports
"""
from aiogram import types, Dispatcher

from create_bot import bot
from config import ADMIN_ID


async def report_command1(message: types.Message):
    """
    Коли у відповідь на негарне повідомлення пишуть /report то бот надсилає повідомлення адміну
    з посиланням на повідомлення з репортом і адмін розбирається з негарною людиною
    When /report is written in response to a nasty message, the bot sends a message to the admin
    with a link to the message with the report and the admin deals with the nasty person
    """
    if message.chat.id < 0:
        await message.reply(text="Репорт надішлений! (або рекомендація)")
        await bot.send_message(chat_id=ADMIN_ID[0], text=f"Користувач {message.from_user.full_name} робить репорт\n"
                                                        f"url={message.url}\n"
                                                        f"Текст повідомлення= {message.text}")
    else:
        await message.reply(text="Тут немає людей (хіба ви написали рекомендацію)")
        try:
            await bot.send_message(chat_id=ADMIN_ID[0], text=f"Користувач {message.from_user.full_name} робить репорт\n"
                                                            f"url={message.url}\n"
                                                            f"Текст повідомлення= {message.text}")
        except:
            await bot.send_message(chat_id=ADMIN_ID[0], text=f"Користувач {message.from_user.full_name} робить репорт\n"
                                                        f"Приватне повідомлення\n"
                                                        f"Текст повідомлення= {message.text}")


async def report_command2(message: types.Message):
    """
    Так само тільки коли пишуть !report
    Similarly, only when writing !report
    """
    if message.chat.id < 0:
        await message.reply(text="Репорт надішлений! (або рекомендація)")
        await bot.send_message(chat_id=ADMIN_ID[0], text=f"Користувач {message.from_user.full_name} робить репорт\n"
                                                        f"{message.url}"
                                                        f"Текст повідомлення= {message.text}")
    else:
        await message.reply(text="Тут немає людей (хіба ви написали рекомендацію)")
        await bot.send_message(chat_id=ADMIN_ID[0], text=f"Користувач {message.from_user.full_name} робить репорт\n"
                                                        f"{message.url}"
                                                        f"Текст повідомлення= {message.text}")


def register_handler_report(dp: Dispatcher):
    """
    Реєстрація report_command1 і report_command2
    Registration of report_command1 and report_command2
    """
    dp.register_message_handler(report_command1, commands=["report"])
    dp.register_message_handler(report_command2, commands=["report"], commands_prefix="!")
