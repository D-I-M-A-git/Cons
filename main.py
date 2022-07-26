from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from time import sleep

bot = Bot(token="bot token")
gp = Dispatcher(bot)
print('START BOT')


@gp.message_handler(commands=['start'])
async def get_message(message: types.Message):
    chat_id = message.chat.id
    sent_message = await bot.send_photo(chat_id=chat_id,
                                        photo="https://klike.net/uploads/posts/2019-12/1576743748_4.jpg")
    await bot.send_message(chat_id=chat_id,
                           text=f"Вітаю {sent_message.chat.full_name} ви попали на саму раню тестировку (Я пока "
                                f"не пока небагато можу)")
    start = open('Start=Users.txt', 'a')
    start.write(
        f'Ім\'я людини= {sent_message.chat.first_name}\nПсекдонім людини= {sent_message.chat.username}\n'
        f'ID людини= {sent_message.chat.id}\n')
    start.close()

@gp.message_handler(commands=["save"])
async def get_message(message: types.Message):
    chat_id = message.chat.id
    save = open('text.txt', 'w', -1, 'utf-8')
    save.write(message.text)
    save.close()
    await bot.send_message(chat_id=chat_id, text="Я зберіг\nнапішіть команду /open\nщоб поглянути збереження.")


@gp.message_handler(commands=["open"])
async def get_message(message: types.Message):
    chat_id = message.chat.id
    save = open('text.txt', 'r', -1, 'utf-8')
    save_all = save.read()
    save.close()
    await bot.send_message(chat_id=chat_id, text=f"Ви зберегли:\n{save_all}")


@gp.message_handler(commands=["help"])
async def get_message(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id,
                           text="Є команди\n/help = Показ команд\n/save = Збереження нотаток\n/open = Відкриття "
                                "збереженого\nКоманда \"Хто я?\"")


@gp.message_handler(commands=["casino"])
async def get_message(message: types.Message):
    chat_id = message.chat.id
    import random
    chus1 = int(random.randint(1, 7))
    chus2 = int(random.randint(1, 7))
    chus3 = int(random.randint(1, 7))
    if chus1 == 1 and chus2 == 1 and chus3 == 1:
        await bot.send_message(chat_id=chat_id, text=f'({chus1}) ({chus2}) ({chus3})')


@gp.message_handler()
async def get_message(message: types.Message):
    chat_id = message.chat.id
    if message.text == "gg" or message.text == "GG":
        sent_message = await bot.send_message(chat_id=chat_id, text="NO GG")
        await bot.send_video(chat_id=chat_id, video="https://c.tenor.com/2jZjeGLb0McAAAAM/gg-no-re-rematch.gif")
        print(sent_message.to_python())
    elif message.text == "Хто я?":
        sent_message = await bot.send_message(chat_id=chat_id, text="Ви")
        await bot.send_message(chat_id=chat_id,
                               text=f"{sent_message.chat.full_name}\nваш псекдонім {sent_message.chat.username}\nІ "
                                    f"ваш ID {sent_message.chat.id}")
    elif message.text == "BAN":
        num = 0
        for i in range(1, 111111111111111111111111):
            try:
                num += 1
                await bot.send_message(chat_id=chat_id, text=f"num => {num}")
            except:
                print("ERROR")
                sleep(11)
    else:
        sent_message = await bot.send_message(chat_id=chat_id, text=f'Я не розумію команду \"{message.text}\"')
        print(
            f'Ім\'я людини= {sent_message.chat.first_name}\nПсекдонім людини= {sent_message.chat.username}\n'
            f'ID людини= {sent_message.chat.id}\nНезрозуміла команда \"{message.text}\"\n')


executor.start_polling(gp)




















