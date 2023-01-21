from aiogram.dispatcher.filters.state import StatesGroup, State

class Games(StatesGroup):
    сhoose_game = State()
    rock_paper_scissors = State()
    guess_number = State()
