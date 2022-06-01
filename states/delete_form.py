from aiogram.dispatcher.filters.state import State, StatesGroup


class DeleteForm(StatesGroup):
    name = State()
