from aiogram import types, Dispatcher

from create_bot import bot


async def help(message: types.Message):
    chat_id = message.chat.id
    help_message = "КОМАНДИ ДЛЯ АДМІНА:\n" \
                   "    @dir <шлях>: Показати всі файли за наведеним шляхом\n" \
                   "    @dir @back: Зробити бекап\n" \
                   "    @dir @view: Показати файли за збереженим шляхом\n" \
                   "    @dir @image txt: Показати всі імена доступних зображень\n" \
                   "    @dir @image img: Надіслати всі зображення (з іменами в описі зображення)\n" \
                   "    @dir @image <ім'я зображення>: Показати зображення\n" \
                   "    @dir my: Показати моє розташування у файловій системі\n" \
                   "КОМАНДИ ДЛЯ ЗВИЧАЙНИХ ЛЮДЕЙ:\n" \
                   "    /start, /help: Показати це повідомлення\n" \
                   "    @save <текст>: Зберегти повідомлення\n" \
                   "    @open: Показати збережене повідомлення"
    await bot.send_message(chat_id=chat_id, text=help_message)

# Функція регістрації help
def register_handler_help(gp : Dispatcher):
    gp.register_message_handler(help, commands=["start", "help"])