from aiogram.dispatcher.filters.state import StatesGroup, State


class Chat(StatesGroup):
    warning_and_start_chat = State()
