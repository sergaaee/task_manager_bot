from aiogram.dispatcher.filters.state import State, StatesGroup


# forms for states
class TaskForm(StatesGroup):
    name = State()
    stime = State()
    etime = State()
    desc = State()
