"""
Файл для перекладу
File for translation
"""
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import translators.server as tss

from create_bot import bot
from states.translator import Translator as ts
from keyboards.transtalor import *


async def translation(message: types.Message):
    """
    Функція для запуску перекладача
    Function to start the translator
    """
    await ts.trans.set()
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text="Ви який перекладач хочете використати?", reply_markup=choosing_translator)


async def used_translator(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Статус для вибору перекладача
    Status for choosing a translator
    """
    print(callback_query.data)
    if callback_query.data == "exit":
        await state.finish()
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                    text="Ви вийшли!")
    else:
        await ts.next()
        chat_id = callback_query.message.chat.id
        use_translator = callback_query.data.split(":")[1]
        message_id = callback_query.message.message_id

        async with state.proxy() as data:
            data["used_translator"] = use_translator
        text = "Чудово!\nТепер виберіть мову."
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                    reply_markup=choosing_language,
                                    text=text)


async def language(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Статус для вибору мови
    Status for language selection
    """
    if callback_query.data == "exit":
        await state.finish()
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                    text="Ви вийшли!")
    else:
        await ts.next()
        chat_id = callback_query.message.chat.id
        message_id = callback_query.message.message_id
        language = callback_query.data.split(":")[1]

        async with state.proxy() as data:
            data["language"] = language
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                    text="Пишіть повідомлення яке треба перекласти")
    

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
                await bot.send_message(chat_id=chat_id, text=str(
                    tss.google(text,
                            to_language=str(data.get("language")))))
            case "bing":
                await bot.send_message(chat_id=chat_id, text=str(
                    tss.bing(text,
                            to_language=str(data.get("language")))))
            case "yandex": # Does not work in Ukraine
                await bot.send_message(chat_id=chat_id, text=str(
                    tss.yandex(text,
                            to_language=str(data.get("language")))))
            case "youdao":
                await bot.send_message(chat_id=chat_id, text=str(
                    tss.youdao(text,
                            to_language=str(data.get("language")))))
            case "caiyun":
                await bot.send_message(chat_id=chat_id, text=str(
                    tss.caiyun(text,
                            to_language=str(data.get("language")))))
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
    dp.register_callback_query_handler(used_translator, state=ts.trans)
    dp.register_callback_query_handler(language, state=ts.lang)
    dp.register_message_handler(text, state=ts.text)
