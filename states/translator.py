from aiogram.dispatcher.filters.state import StatesGroup, State

class Translator(StatesGroup):
    use = State()
    language = State()
    text = State()