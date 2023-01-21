"""
Фалй для надсилання диних про погоду
"""
import requests
import json

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
import translators.server as tss

import config
from create_bot import bot
from states.weather import Weather

def get_weather(city):
    r = requests.get(url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.WEATHER_TOKEN}&units=metric")

    weather_result = r.json()
    match int(weather_result["cod"]):
        case 200:
            city_name = weather_result["name"]
            humidity = weather_result["main"]["humidity"]
            weather = tss.google(weather_result["weather"][0]["description"], to_language="uk")
            temp = weather_result["main"]["temp"]
            wind_speed = weather_result["wind"]["speed"]
            text = f"Місто: {city_name}\n" \
                   f"Вологість: {humidity}%\n" \
                   f"Погода: {weather}\n" \
                   f"Температура: {temp}°C\n" \
                   f"Швидкість вітру: {wind_speed}"
                    
            return text
        case 404:
            return "Вибачте!\nНе вдалося получити дані про місто."
        case _:
            print(type(weather_result["cod"]))
            print(weather_result["cod"])
            return "Вибачте!\nСталася не відома помилка."

async def weather(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.text == "/weather !":
        await bot.send_message(chat_id=chat_id, text="Напишіть назву міста за замовчуванням")
        await Weather.city.set()
    else:
        try:
            with open("json/weather.json", 'r') as weather:
                weather_json = json.load(weather)
            error = False
        except:
            await bot.send_message(chat_id=chat_id, text="Напишіть назву міста за замовчуванням")
            error = True
            await Weather.city.set()
        finally:
            if error:
                pass
            else:
                await bot.send_message(chat_id=chat_id, text=get_weather(weather_json[str(user_id)]))

async def choose_city(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text="Секунду...")
    if message.text == "Гусятин":
        city = "Husiatyn"
    else:
        city = tss.google(message.text, to_language='en')
    with open("json/weather.json", 'w') as weather:
        json.dump({message.from_user.id: city}, weather)
    
    await bot.send_message(chat_id=chat_id, text=get_weather(city))
    
    await state.finish()

def register_handler_weather(dp: Dispatcher):
    dp.register_message_handler(weather, commands=["weather"])
    dp.register_message_handler(choose_city, state=Weather.city)
