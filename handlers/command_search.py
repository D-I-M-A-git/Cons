import logging

import wikipedia
import translators.server as tss
from aiogram import types, Dispatcher


async def search(message: types.Message):
    await message.reply(text="Секунду...")
    logging.info(message.text)
    text = tss.google(message.text.replace("/search ", ""), to_language='en')
    logging.info(text)
    await message.reply(text="Зараз буде готово!")
    try:
        await message.reply(text=tss.google(wikipedia.summary(text), to_language='uk'))
    except:
        await message.reply(text="Вибачте сталась помилка!")


def register_handler_help(dp: Dispatcher):
    dp.register_message_handler(search, commands="search")
