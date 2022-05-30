from aiogram.dispatcher.filters.state import State, StatesGroup


class TaskForm(StatesGroup):
    name = State()
    stime = State()
    etime = State()
    desc = State()
