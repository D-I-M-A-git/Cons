import requests
import json

from aiogram import Dispatcher, types

from create_bot import bot
import config


def get_rate(currency=None):
    if currency == None:
        rate = []
        for i in config.URLs:
            currency = i
            r = requests.get(url=f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={i}&json")
            r = r.content.decode('utf-8')
            rjson = json.loads(r)
            if currency == "USD":
                rate.append("Долар - " + str(round(float(rjson[0]["rate"]))) + "грн")
            if currency == "EUR":
                rate.append("Євро - " + str(round(float(rjson[0]["rate"]))) + "грн")
            if currency == "PLN":
                rate.append("Злотих - " + str(round(float(rjson[0]["rate"]))) + "грн")
        return rate


async def rate(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text="Секунду...")
    await bot.delete_message(chat_id=chat_id, message_id=message.message_id+1)
    await bot.send_message(chat_id=chat_id, text="Ця інформація взята з офіційного API НБУ\n" + "\n".join(get_rate()))


def register_handler_rate(dp: Dispatcher):
    dp.register_message_handler(rate, commands=["rate"])
