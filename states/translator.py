from aiogram.dispatcher.filters.state import StatesGroup, State

class Translator(StatesGroup):
    trans = State()
    lang = State()
    text = State()
    select_manually = State()