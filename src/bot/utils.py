from aiogram.dispatcher.filters.state import State, StatesGroup


class STStates(StatesGroup):
    '''
    The bot has two states: style when it waits to receive a style image from a user,
    and content which means the bot already has a style image.
    '''
    style = State()
    content = State()
