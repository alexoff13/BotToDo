from aiogram.dispatcher.filters.state import StatesGroup, State


class AddTask(StatesGroup):
    AddName = State()
    AddDate = State()
    AddDescription = State()
