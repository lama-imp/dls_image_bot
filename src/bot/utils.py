from aiogram.dispatcher.filters.state import State, StatesGroup


class STStates(StatesGroup):
    style = State()
    content = State()
