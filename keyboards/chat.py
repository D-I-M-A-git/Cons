from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard = InlineKeyboardMarkup(row_width=2)
translate = InlineKeyboardButton(text="Перекласти", callback_data="translate")
keyboard.insert(translate)
delete = InlineKeyboardButton(text="Видалити", callback_data="delete")
keyboard.insert(delete)
continue_chat = InlineKeyboardButton(text="Продовжити чат", callback_data="continue_chat")
keyboard.insert(continue_chat)
