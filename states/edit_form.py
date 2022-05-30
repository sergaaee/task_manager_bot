from aiogram.dispatcher.filters.state import State, StatesGroup


class EditForm(StatesGroup):
    name = State()
    new_name = State()
    new_stime = State()
    new_etime = State()
    new_desc = State()
