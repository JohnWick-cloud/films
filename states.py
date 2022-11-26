from aiogram.dispatcher.filters.state import StatesGroup, State


class Post(StatesGroup):
    photo = State()
    caption = State()
    url = State()