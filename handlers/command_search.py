import requests
from bs4 import BeautifulSoup as BS
from aiogram import types, Dispatcher


async def search(message: types.Message):
    try:
        url = message.text.replace("/search ", "")
        r = requests.get("https://uk.wikipedia.org/wiki/" + url)
        html = BS(r.content, 'lxml')
        text = html.find("p").text.strip()
        if text == "Інші причини, чому Ви можете бачити це повідомлення:":
            await message.reply(text="Сталась помилка")
        else:
            await message.reply(text=text)
    except:
        await message.reply(text="Сталась помилка")

def register_handler_help(dp: Dispatcher):
    dp.register_message_handler(search, commands="search")
