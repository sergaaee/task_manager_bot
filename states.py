from aiogram.dispatcher.filters.state import State, StatesGroup


# forms for states
class TaskForm(StatesGroup):
    name = State()
    stime = State()
    etime = State()
    desc = State()


class DeleteForm(StatesGroup):
    name = State()


class EditForm(StatesGroup):
    name = State()
    new_name = State()
    new_stime = State()
    new_etime = State()
    new_desc = State()