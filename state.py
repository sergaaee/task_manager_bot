from aiogram.dispatcher.filters.state import StatesGroup, State


class TaskForm(StatesGroup):
    name = State()
    stime = State()
    etime = State()
    desc = State()