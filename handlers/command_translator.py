"""
Файл для перекладу
File for translation
"""
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import translators.server as tss

from create_bot import bot
from states.translator import Translator as ts


async def translation(message: types.Message):
    """
    Функція для запуску перекладача
    Function to start the translator
    """
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text="Ви хочете використати перекладач?\nБудь ласка напишіть який"
                                                 " перекладач ви хочете використати.")

    await ts.use.set()


async def used_translator(message: types.Message, state: FSMContext):
    """
    Статус для вибору перекладача
    Status for choosing a translator
    """
    chat_id = message.chat.id
    use_translator = message.text.lower()

    async with state.proxy() as data:
        data["used_translator"] = use_translator
    
    text = """
           Чудово!
        Тепер напишіть на яку мову перекласти
        (у скорочиній формі)
           Англійська - en
           Німеська - de
           Українська - uk
           Китайська? - zh
           """
    await bot.send_message(chat_id=chat_id, text=text)

    await ts.next()


async def language(message: types.Message, state: FSMContext):
    """
    Статус для вибору мови
    Status for language selection
    """
    chat_id = message.chat.id
    language = message.text.lower()

    async with state.proxy() as data:
        data["language"] = language
    
    await bot.send_message(chat_id=chat_id, text="Чудово тепер можете надсилати текст")

    await ts.next()


async def text(message: types.Message, state: FSMContext):
    """
    Статус для кінцевого перекладу
    Status for final translation
    """
    chat_id = message.chat.id
    text = message.text

    data = await state.get_data()

    try:
        await bot.send_message(chat_id=chat_id, text="Це може зайняти деякий час...")
        match data.get("used_translator"):
            case "google":
                await bot.send_message(chat_id=chat_id, text=tss.google(text, to_language=data.get("language")))
            case "bing":
                await bot.send_message(chat_id=chat_id, text=tss.bing(text, to_language=data.get("language")))
            case "yandex": # Does not work in Ukraine
                await bot.send_message(chat_id=chat_id, text=tss.yandex(text, to_language=data.get("language")))
            case "youdao":
                await bot.send_message(chat_id=chat_id, text=tss.youdao(text, to_language=data.get("language")))
            case "caiyun":
                await bot.send_message(chat_id=chat_id, text=tss.caiyun(text, to_language=data.get("language")))
            case _:
                await bot.send_message(chat_id=chat_id, text="Вибраний вами перекладач не знайдений\nнапишіть !report"
                                                             " або /report з рекомендацією щоб я добавив цей "
                                                             "перекладач")
    except Exception as ex:
        await bot.send_message(chat_id=chat_id, text=f"Вибачте!\nСталася критична помилка.\n\nНазва помилки:{ex}")
    finally:
        await state.finish()


def register_handler_translation(dp: Dispatcher):
    """
    Реєстрація translation
    Registration translation
    """
    dp.register_message_handler(translation, commands=["translate"])
    dp.register_message_handler(used_translator, state=ts.use)
    dp.register_message_handler(language, state=ts.language)
    dp.register_message_handler(text, state=ts.text)
