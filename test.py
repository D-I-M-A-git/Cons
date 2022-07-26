# Імпорт модулів
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import UserProfilePhotos
from aiogram.utils import executor
from time import sleep

# Створення бота і глобального списку
bot = Bot(token="BOT TOKEN")
gp = Dispatcher(bot)
global users_way
users_way = {}
print('START BOT')


# Хендлер який приймає все якщо інші не приймуть
@gp.message_handler()
async def get_message(message: types.Message):
    chat_id = message.chat.id
    if chat_id == 1909237932 or chat_id == 1354921548:  # Перевірка що юзер той
        message_text = message.text.split()  # Розділення повідомлення в список
        match message_text:
            # Якщо повідомлення дорівнює gg або GG, то бот надсилає мемас
            case ["gg"] | ["GG"]:
                await bot.send_message(chat_id=chat_id, text="NO GG")
                await bot.send_video(chat_id=chat_id, video="https://c.tenor.com/2jZjeGLb0McAAAAM/gg-no-re-rematch.gif")
            # Якщо повідомлення дорівнює словам Хто я?, то бот надсилає інформацію про юзера
            case ["Хто", "я?"]:
                sent_message = await bot.send_message(chat_id=chat_id, text="Ви")
                await bot.send_message(chat_id=chat_id,
                                       text=f"{sent_message.chat.full_name}\nваш псевдонім {sent_message.chat.username}"
                                            f"ваш ID {sent_message.chat.id}")
            # Якщо повідомлення дорівнює BAN, то бот починає спамити (це експеримент)
            case ["BAN"]:
                num = 0
                for i in range(1, 1001):
                    try:
                        num += 1
                        await bot.send_message(chat_id=chat_id, text=f"num => {num}")
                    except:
                        print("ERROR")
                        sleep(11)
            # Якщо повідомлення дорівнює get_photo, то бот надсилає фото на аватарці
            case ["get_photo"]:
                user_photo = await bot.get_user_profile_photos(user_id=chat_id, offset=5)
                for i in user_photo.iter_values():
                    print(i, "num 0")
                print(type(user_photo))
                print(user_photo, "1")
                user_photo = user_photo['photos']
                print(type(user_photo))
                print(user_photo, "2")
                # for i in range(user_photo):
                #     print(i, "num 1")
                user_photo = user_photo[0]
                print(type(user_photo))
                print(user_photo, "3")
                # for i in user_photo.iter_values():
                #     print(i, "num 2")
                user_photo = user_photo[0]
                # user_photo = user_photo['PhotoSize']
                print(type(user_photo))
                print(user_photo, "4")
                for i in user_photo.items():
                    print(i, "num 3")
                user_photo = user_photo['file_id']
                await bot.send_photo(chat_id=chat_id, photo=user_photo)

            case ['photos', photo_name]:
                if photo_name == "all":
                    # try:
                    photos = os.listdir(r"media\\images")
                    print(photos, type(photos))
                    for photo in photos:
                        with open(f"media/images/{photo}", 'rb') as photo_file:
                            await bot.send_photo(chat_id=chat_id, photo=photo_file, caption=photo)
                    # except:
                    #     await bot.send_message(chat_id=chat_id, text="Файлів нема!")
            case ['dir', 'photos']:
                photos = '\n'.join(os.listdir(r"media\\images"))
                await bot.send_message(chat_id=chat_id, text=photos)
            case ['dir', 'videos']:
                try:
                    videos = '\n'.join(os.listdir(r"media\\videos"))
                    await bot.send_message(chat_id=chat_id, text=videos)
                except:
                    await bot.send_message(chat_id=chat_id, text="Файлів нема!")
            case ['@dir', '@back']:
                users_way[chat_id] = None
                await bot.send_message(chat_id=chat_id, text="Бекап зроблений")
            case ['@dir', way]:
                if way == "my":
                    await bot.send_message(chat_id=chat_id, text=f"Моє розположення\n{os.getcwd()}")
                else:
                    try:
                        print("TRY:")
                        file = users_way[chat_id]
                        print(file, "numer 0")
                        file += way
                        file += r"\\"
                        print(file, "numer 1")
                        users_way[chat_id] = file
                        way = file
                        try:
                            file = '\n'.join(os.listdir(file))
                            await bot.send_message(chat_id=chat_id, text=f"<{way}>\n{file}")
                        except:
                            users_way[chat_id] = None
                            await bot.send_message(chat_id=chat_id, text="Бекап зроблений")
                    except:
                        print("EXCEPT:")
                        users_way[chat_id] = way
                        file = users_way[chat_id] = way
                        print(file, "numer 2")
                        file += r"\\"
                        print(file, "numer 3")
                        users_way[chat_id] = file
                        way = file
                        try:
                            file = '\n'.join(os.listdir(file))
                            await bot.send_message(chat_id=chat_id, text=f"<{way}>\n{file}")
                        except:
                            users_way[chat_id] = None
                            await bot.send_message(chat_id=chat_id, text="Бекап зроблений")

            case _:
                sent_message = await bot.send_message(chat_id=chat_id, text=f'Я не розумію команду \"{message.text}\"')
                print(
                    f'Ім\'я людини= {sent_message.chat.first_name}\nПсевдонім людини= {sent_message.chat.username}\n'
                    f'ID людини= {sent_message.chat.id}\nНезрозуміла команда \"{message.text}\"\n')
    else:
        await bot.send_message(chat_id=chat_id, text="Йди геть!")


executor.start_polling(gp)
