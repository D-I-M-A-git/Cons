"""
    Файловий провідник

    Що він робить?

    1.Може показати всі файли в папці для цього треба написати боту таку команду @dir view або @dir <ім'я папки>

    2.
"""
import os
import json

from aiogram import types, Dispatcher

from handlers import file_explorer_function
from create_bot import bot
import config as cnf


async def file_explorer(message: types.Message):
    """
    Файловий провідник
    File Explorer

    parameter message: For the possibility of sending a message and for storing the path by user_id
    :param message: Для можливості надішлення повідомлення і для зберігання шляху по user_id
    """
    chat_id = message.chat.id
    user_id = message.from_user.id
    message_text = message.text.split()  # Розділення повідомлення в список
    if user_id in cnf.ADMIN_ID:  # Перевірка що юзер той
        match message_text:
            # Виконує команди після @dir
            case ['@dir', *new_way]:
                match new_way:
                    # Коли юзер пише @image txt то бот надсилає повідомлення файлів які знаходяться в media\image
                    case ["image", "txt"]:
                        images = '\n'.join(os.listdir(r"media\\images"))
                        await bot.send_message(chat_id=chat_id, text=images)

                    # Коли юзер пише @image img то бот надсилає файли які знаходяться в media\images
                    # (головне щоб файли були формата .png .jpg і так далі не відео формата або інших)
                    case ["image", "img"]:
                        images = os.listdir(r"media\\images")
                        for img_name in images:
                            with open(f"media\\images\\{img_name}", "rb") as image:
                                await bot.send_photo(chat_id=chat_id, photo=image, caption=img_name)

                    # Коли юзер пише @image й ім'я зображення з розширенням
                    # то бот надсилає це зображення
                    case ["image", file_name]:
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

            case _:
                print(message.text)

    else:
        match message_text:
            case ["@open"]:
                try:
                    with open("saves_texts.json", "r") as open_file:
                        open_file = json.load(open_file)
                        await message.reply(text=open_file[str(user_id)])
                except (FileNotFoundError, KeyError):
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
                except FileNotFoundError:
                    error = True
                finally:
                    if error:
                        with open("saves_texts.json", "w") as saves_texts:
                            json.dump(user_and_text, saves_texts)
                    else:
                        try:
                            saves_texts[user_id] = user_and_text[user_id]
                        except (NameError, KeyError):
                            saves_texts.update(user_and_text)
                        finally:
                            with open("saves_texts.json", "w") as file:
                                json.dump(saves_texts, file)
                            await message.reply(text="Текст збережено!")
        message_text = message.text.lower()
        for word in cnf.WORDS:
            if word in message_text:
                await message.delete()
        print(f"https://t.me/{message.from_user.username}, {message.from_user.language_code}, "
              f"{message.from_user.id}, "
              f"@{message.from_user.username}, "
              f"{message.from_user.full_name}, "
              f"chat id={chat_id}"
              f" => "
              f"{message_text}")


def register_handler_command_dir(dp: Dispatcher):
    """
    Функція регістрації file_explorer
    File_explorer registration function

    :param dp: Потрібно для регістрації file_explorer
    """
    dp.register_message_handler(file_explorer)
