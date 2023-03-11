from aiogram import Dispatcher, types
from keyboards.chat import keyboard
from aiogram.dispatcher import FSMContext
import openai
import translators.server as tss

from create_bot import bot
from states.chat import Chat
import config

answer = {"en": "Пусто", "uk": "."}


def answer_chat(text):
    text = tss.google(text, to_language="en")
    openai.api_key = config.OPENAI_TOKEN
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0.8,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0
    )
    answer["en"] = "Відповідь: " + response["choices"][0]["text"]
    answer["uk"] = "Ваше питання на англійській мові: " + text + "------------\n\n" + \
                   tss.google(response["choices"][0]["text"],
                              to_language="uk")
    return answer["uk"]


async def translate(callback_query: types.CallbackQuery):
    if "Ваше питання на англійській мові:" in callback_query.message.text:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=answer["en"], reply_markup=keyboard)
    elif "Відповідь: " in callback_query.message.text:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=answer["uk"], reply_markup=keyboard)
    else:
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)


async def delete(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)


async def continue_chat(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text="Добре задавайте своє питання")
    await Chat.warning_and_start_chat.set()


async def chat(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text.lower() == "вийти":
        await state.finish()
    else:
        await bot.send_message(chat_id=chat_id, text="Секунду...")
        await bot.send_message(chat_id=chat_id, text=answer_chat(message.text), reply_markup=keyboard)
        await state.finish()


async def warning_and_start_chat(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id,
                           text="ПОПЕРЕДЖЕННЯ!\n"
                                "Офіційний API який використовує автор є чуть-чуть глюканутий.\n"
                                "А саме GPT може відповідати не правильно, криво і так далі.\n"
                                "То вам рекомендується формулювати свої питання по різному.\n"
                                "Добре задавайте своє питання")
    await Chat.warning_and_start_chat.set()


def register_handler_chat(dp: Dispatcher):
    dp.register_callback_query_handler(translate, text="translate")
    dp.register_callback_query_handler(delete, text="delete")
    dp.register_callback_query_handler(continue_chat)
    dp.register_message_handler(warning_and_start_chat, commands=["chat"])
    dp.register_message_handler(chat, state=Chat.warning_and_start_chat)
