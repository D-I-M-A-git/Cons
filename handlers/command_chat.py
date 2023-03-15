from aiogram import Dispatcher, types
from keyboards.chat import keyboard
from aiogram.dispatcher import FSMContext
import openai
import translators.server as tss

from create_bot import bot
from states.chat import Chat
import config


def answer_chat(text):
    openai.api_key = config.OPENAI_TOKEN
    try:
        response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "system", "content": config.SYSTEM_MESSAGE},
                            {"role": "user", "content": text},
                        ],
                    top_p=1,
                    max_tokens=500
        )
        return response['choices'][0]['message']['content'].replace("```", "**")
    except Exception as ex:
        if "That model is currently overloaded with other requests." in ex:
            return f"Вибачте але зараз сервери перегруженні і вони не відповідають на запити."
        else:
            return f"Вибачте але зараз виникла невідома помилка.\nСпробуйте повторити питання пізніше.\nОпис помилки: {ex}"
    



async def delete(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)


async def continue_chat(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=callback_query.message.text + "\n\nДобре задавайте своє питання.")
    await Chat.warning_and_start_chat.set()


async def chat(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text.lower() == "вийти":
        await state.finish()
    else:
        await bot.send_message(chat_id=chat_id, text="Зачекайте будь ласка, це може зайнняти деякий час.")
        answer = answer_chat(message.text)
        try:
            await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=answer, reply_markup=keyboard, parse_mode=types.ParseMode.MARKDOWN)
            await state.finish()
        except:
            await bot.send_message(chat_id=chat_id, text=answer, reply_markup=keyboard)
            await state.finish()


async def warning_and_start_chat(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id,
                           text="ПОПЕРЕДЖЕННЯ!\n"
                                "Офіційний API який використовує автор є чуть-чуть глюканутий.\n"
                                "А саме GPT може відповідати не правильно, криво і так далі.\n"
                                "То вам рекомендується формулювати свої питання по різному.\n"
                                "Добре задавайте своє питання.")
    await Chat.warning_and_start_chat.set()


def register_handler_chat(dp: Dispatcher):
    dp.register_callback_query_handler(delete, text="delete")
    dp.register_callback_query_handler(continue_chat)
    dp.register_message_handler(warning_and_start_chat, commands=["chat"])
    dp.register_message_handler(chat, state=Chat.warning_and_start_chat)
