from aiogram.dispatcher.filters.state import StatesGroup, State


class Games(StatesGroup):
    choose_game = State()
    rock_paper_scissors = State()
    guess_number = State()
