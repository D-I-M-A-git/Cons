import os
import json

from aiogram import types, Dispatcher

from handlers import file_explorer_function
from create_bot import bot
import config as cnf

global users_way
users_way = {}


# Файловий провідник
async def file_explorer(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id == 1909237932 or user_id == 1354921548:  # Перевірка що юзер той
        message_text = message.text.split()  # Розділення повідомлення в список
        match message_text:
            # Виконує команди після @dir
            case['@dir', *new_way]:
                match new_way:
                    # Коли юзер пише @image txt то бот надсилає повідомлення файлів які знаходяться в media\image
                    case ["@image", "txt"]:
                        images = '\n'.join(os.listdir(r"media\\images"))
                        await bot.send_message(chat_id=chat_id, text=images)
                    # Коли юзер пише @image img то бот надсилає файли які знаходяться в media\images
                    # (головне щоб файли були формата .png .jpg і так далі не відео формата або інших)

                    case ["@image", "img"]:
                        images = os.listdir(r"media\\images")
                        for img_name in images:
                            with open(f"media\\images\\{img_name}", "rb") as image:
                                await bot.send_photo(chat_id=chat_id, photo=image, caption=img_name)

                    # Коли юзер пише @image і ім'я зображення з розширенням
                    # то бот надсилає це зображення
                    case ["@image", file_name]:
                        with open(f"media\\images\\{file_name}", "rb") as image:
                            await bot.send_photo(chat_id=chat_id, photo=image)

                    # Коли юзер пише my то бот надсилає своє росположення у файловій системі
                    case ["my"]:
                        await bot.send_message(chat_id=chat_id, text=f"Моє розположення\n{os.getcwd()}")

                    # Показує файли, папки через відповідний шлях
                    case _:
                        way = " ".join(new_way)
                        user_id_str = str(user_id)
                        files = file_explorer_function.file_explorer_function(way, user_id_str)
                        await bot.send_message(chat_id=chat_id, text=files)

            case ["@open"]:
                try:
                    with open("saves_texts.json", "r") as open_file:
                        open_file = json.load(open_file)
                        await bot.send_message(chat_id=chat_id, text=open_file[str(user_id)])
                except:
                    await message.reply(text="Сталась помилка!")

            case ["@save", *text]:
                # збереження тексту у save_text
                save_text = " ".join(text)
                # Створення словника з user_id як ключ до save_text
                user_and_text = {str(user_id): save_text}
                global error
                # Спробувати прочитати файл saves_texts
                try:
                    with open("saves_texts.json", "r") as saves_texts:
                        saves_texts = json.load(saves_texts)
                    error = False
                except:
                    error = True
                finally:
                    if error == True:
                        with open("saves_texts.json", "w") as saves_texts:
                            json.dump(user_and_text, saves_texts)
                    else:
                        try:
                            saves_texts[user_id] = user_and_text[user_id]
                        except:
                            saves_texts.update(user_and_text)
                        finally:
                            with open("saves_texts.json", "w") as file:
                                json.dump(saves_texts, file)


            case _:
                message_text = message.text.lower()
                for word in cnf.WORDS:
                    if word in message_text:
                        await message.delete()
                print(f"https://t.me/{message.from_user.username}, {message.from_user.language_code} => {message_text}")

# Функція регістрації file_explorer
def register_handler_command_dir(dp : Dispatcher):
    dp.register_message_handler(file_explorer)

