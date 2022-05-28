from aiogram.types import CallbackQuery
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import Users, Tasks, Database
from settings import *
from keyboards import inline_kb_choose, params_keyboard, ikb_agree
import logging
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram_calendar import dialog_cal_callback, DialogCalendar

# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)


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


@dp.message_handler(commands=['start', 'help', 'h', 's'])
async def send_welcome(message: types.Message):
    Users().add(message.from_user.id, message.from_user.username)
    await message.answer(f"Hello 👋\n\nI'm a bot that will help you to plan your day 😊\n"
                         f"With me you can easily add, watch, delete, edit tasks that you have to do!"
                         f"\n\nJust type /t and you will figure out with me 🎯")


@dp.message_handler(commands=["t", "tasks"])
async def act_choosing(message: types.Message):
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer("Choose what you want to do:", reply_markup=inline_kb_choose)


# new task
@dp.callback_query_handler(lambda c: c.data == 'nt')
async def new_task(callback_query: types.CallbackQuery):
    Database().update(table_name="Users", columns={"selected_command": "nt"}, id=callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await simple_cal_handler(callback_query.from_user.id)


@dp.message_handler(state=TaskForm.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await TaskForm.stime.set()
    await message.answer("When starts?")


@dp.message_handler(state=TaskForm.stime)
async def get_start_time(message: types.Message, state: FSMContext):
    await state.update_data(stime=message.text)
    await TaskForm.etime.set()
    await message.answer("When ends?")


@dp.message_handler(state=TaskForm.etime)
async def get_end_time(message: types.Message, state: FSMContext):
    await state.update_data(etime=message.text)
    await TaskForm.desc.set()
    await message.answer("Description:")


@dp.message_handler(state=TaskForm.desc)
async def get_desc(message: types.Message, state: FSMContext):
    await state.update_data(desc=message.text)
    data = await state.get_data()
    await state.finish()
    date = Database().select(table_name="Users", fetchone=True, id=message.from_user.id, columns=["selected_date"])[0]
    Tasks().addt(name=data['name'], start_time=data['stime'], end_time=data['etime'], user_id=message.from_user.id,
                 desc=data['desc'], date=date)
    await message.answer("Successfully added ✅")


# show tasks
@dp.callback_query_handler(lambda c: c.data == "st")
async def find_tasks(callback_query: types.CallbackQuery):
    Database().update(table_name="Users", columns={"selected_command": "st"}, id=callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await simple_cal_handler(user_id=callback_query.from_user.id)


async def show_tasks(callback_query):
    date = \
        Database().select(table_name="Users", fetchone=True, id=callback_query.from_user.id,
                          columns=["selected_date"])[0]
    data = Tasks().showt(user_id=callback_query.from_user.id, date=date)
    result = []
    for each in data:
        result.append("name: " + each[0] + ",\nstarts at: " + each[1] + ",\nends at: " + each[2] + ",\n" + each[3])
    if len(result) == 0:
        await bot.send_message(chat_id=callback_query.from_user.id, text="You have no tasks for selected date.")
        return
    else:
        for i in result:
            await bot.send_message(chat_id=callback_query.from_user.id, text=i)


# delete task
@dp.callback_query_handler(lambda c: c.data == "dt")
async def del_task(callback_query: types.CallbackQuery):
    Database().update(table_name="Users", columns={"selected_command": "dt"}, id=callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await simple_cal_handler(callback_query.from_user.id)


async def delete_task(callback_query):
    date = \
        Database().select(table_name="Users", fetchone=True, id=callback_query.from_user.id,
                          columns=["selected_date"])[0]
    names = Database().select(table_name="Tasks", user_id=callback_query.from_user.id, columns=["name"], date=date)
    if len(names) == 0:
        await bot.send_message(chat_id=callback_query.from_user.id, text="You have no tasks for selected date.")
        return
    res = "\n\n".join([i[0] for i in names])
    await bot.send_message(chat_id=callback_query.from_user.id, text=f"Send task's name that you want to delete:\n\n{res}",)
    await DeleteForm.name.set()

    @dp.message_handler(state=DeleteForm.name)
    async def get_del_name(message: types.Message, state: FSMContext):
        global check
        await state.update_data(name=message.text)
        try:
            check = Database().select(table_name="Tasks", user_id=message.from_user.id, fetchone=True, name=message.text,
                                      columns=["name"])[0]
            Tasks().delt(date=date, name=message.text)
            await state.finish()
            await message.answer("Successfully deleted ✅")
        except TypeError:
            await message.answer("Wrong name ❌\ntry one more time")
            await delete_task(message)


# edit task

@dp.callback_query_handler(lambda c: c.data == "et")
async def ed_task(callback_query: types.CallbackQuery):
    Database().update(table_name="Users", columns={"selected_command": "et"}, id=callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await simple_cal_handler(callback_query.from_user.id)


async def edit_task(callback_query):
    date = \
        Database().select(table_name="Users", fetchone=True, id=callback_query.from_user.id,
                          columns=["selected_date"])[0]
    names = Database().select(table_name="Tasks", user_id=callback_query.from_user.id, columns=["name"], date=date)
    if len(names) == 0:
        await bot.send_message(chat_id=callback_query.from_user.id, text="You have no tasks for selected date.")
        return
    res = "\n\n".join([i[0] for i in names])
    await bot.send_message(chat_id=callback_query.from_user.id, text=f"Send task's name that you want to edit:\n\n{res}")
    await EditForm.name.set()


@dp.message_handler(state=EditForm.name)
async def get_name(message: types.Message, state: FSMContext):
    global check
    try:
        check = Database().select(table_name="Tasks", user_id=message.from_user.id, fetchone=True, name=message.text, columns=["name"])[0]
        await state.update_data(name=message.text)
        await message.answer("Choose what you want to edit:", reply_markup=params_keyboard)
    except TypeError:
        await message.answer("Wrong name ❌\ntry one more time")
        await state.finish()
        await edit_task(callback_query=message)


# params editing
# name editing
@dp.callback_query_handler(lambda c: c.data == 'name', state=[EditForm.name, EditForm.new_name])
async def new_name(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id, text="Enter new name:")
    await EditForm.new_name.set()


@dp.message_handler(state=EditForm.new_name)
async def edit_name(message: types.Message, state: FSMContext):
    await state.update_data(new_name=message.text)
    data = await state.get_data()
    Database().update(table_name="Tasks", columns={"name": data["new_name"]}, user_id=message.from_user.id,
                      name=data["name"])
    await state.finish()
    await message.answer("Name successfully edited ✅")


# start time editing
@dp.callback_query_handler(lambda c: c.data == 'stime', state=[EditForm.name, EditForm.new_stime])
async def new_stime(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id, text="Enter new start time:")
    await EditForm.new_stime.set()


@dp.message_handler(state=EditForm.new_stime)
async def edit_stime(message: types.Message, state: FSMContext):
    await state.update_data(new_stime=message.text)
    data = await state.get_data()
    Database().update(table_name="Tasks", columns={"start_time": data["new_stime"]}, user_id=message.from_user.id,
                      name=data["name"])
    await state.finish()
    await message.answer("Start time successfully edited ✅")


# end time editing
@dp.callback_query_handler(lambda c: c.data == 'etime', state=[EditForm.name, EditForm.new_etime])
async def new_etime(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id, text="Enter new end time:")
    await EditForm.new_etime.set()


@dp.message_handler(state=EditForm.new_etime)
async def edit_etime(message: types.Message, state: FSMContext):
    await state.update_data(new_etime=message.text)
    data = await state.get_data()
    Database().update(table_name="Tasks", columns={"end_time": data["new_etime"]}, user_id=message.from_user.id,
                      name=data["name"])
    await state.finish()
    await message.answer("End time successfully edited ✅")


# description editing
@dp.callback_query_handler(lambda c: c.data == 'desc', state=[EditForm.name, EditForm.new_desc])
async def new_description(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id, text="Enter new description:")
    await EditForm.new_desc.set()


@dp.message_handler(state=EditForm.new_desc)
async def edit_description(message: types.Message, state: FSMContext):
    await state.update_data(new_desc=message.text)
    data = await state.get_data()
    Database().update(table_name="Tasks", columns={"desc": data["new_desc"]}, user_id=message.from_user.id,
                      name=data["name"])
    await state.finish()
    await message.answer("Description successfully edited ✅")


# cancel any state
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("There is no state to cancel ❌")
        return
    logging.info('Cancelling state %r', current_state)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer("You cancelled operation ✅")
    await state.finish()


# calendar

async def simple_cal_handler(user_id):
    await bot.send_message(text="Please select a date: ", chat_id=user_id,
                           reply_markup=await DialogCalendar().start_calendar())


@dp.callback_query_handler(lambda c: c.data == 'y')
async def y_agree(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    selected_command = Database().select(table_name="Users", fetchone=True, id=callback_query.from_user.id,
                                         columns=["selected_command"])[0]
    if selected_command == "nt":
        await bot.send_message(callback_query.from_user.id, text="Enter name of a task:")
        await TaskForm.name.set()
    elif selected_command == "st":
        await show_tasks(callback_query=callback_query)
    elif selected_command == "dt":
        await delete_task(callback_query=callback_query)
    elif selected_command == "et":
        await edit_task(callback_query=callback_query)


@dp.callback_query_handler(lambda c: c.data == "n")
async def n_agree(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(text="You cancelled operation ✅", chat_id=callback_query.from_user.id)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)


@dp.callback_query_handler(dialog_cal_callback.filter())
async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        date = date.strftime("%d/%m/%Y")
        Database().update(table_name="Users", columns={"selected_date": date}, id=callback_query.from_user.id)
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await callback_query.message.answer(
            f'You selected {date},\nAre you sure?',
            reply_markup=ikb_agree,
        )


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    # bot start
    executor.start_polling(dp, skip_updates=True)
