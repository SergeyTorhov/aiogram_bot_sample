from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    NEW_USER = State()
    REGISTERED_USER = State()
