import os

from aiogram import types, Dispatcher
from create_bot import bot
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
            case['@dir', *way]:
                match way:
                    # Коли юзер пише @back то бот видаляє інформацію про юзера
                    case ["@back"]:
                        del users_way[chat_id]
                        await bot.send_message(chat_id=chat_id, text="Бекап зроблений")
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
                        try:
                            file = users_way[user_id]
                            file += way
                            file += r"/"
                            users_way[user_id] = ''.join(file)
                            way = ''.join(file)
                            try:
                                files = '\n'.join(os.listdir(''.join(file)))
                                await bot.send_message(chat_id=chat_id, text=f"<{way}>\n{files}")
                            except:
                                del users_way[user_id]
                                await bot.send_message(chat_id=chat_id, text="Етап(1) Бекап зроблений через можливу помилку!")
                        except:
                            users_way[user_id] = way
                            file = users_way[user_id]
                            file += r"/"
                            users_way[user_id] = file
                            way = file
                            try:
                                files = '\n'.join(os.listdir(''.join(file)))
                                await bot.send_message(chat_id=chat_id, text=f"<{way[0]}>\n{files}")
                            except:
                                del users_way[user_id]
                                await bot.send_message(chat_id=chat_id, text='Етап(2) Бекап зроблений через можливу помилку!')

# Функція регістрації file_explorer
def register_handlers_command_dir(gp : Dispatcher):
    gp.register_message_handler(file_explorer)
