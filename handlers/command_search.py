import wikipedia
import translators as ts
from aiogram import types, Dispatcher


async def search(message: types.Message):
    await message.reply(text="Секунду...")
    text = message.text.replace("/search ", "").lower()
    await message.reply(text=ts.google(wikipedia.summary(text), to_language='uk'))


def register_handler_help(dp: Dispatcher):
    dp.register_message_handler(search, commands="search")
