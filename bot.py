from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import Users, Tasks, Database
from settings import *
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


@dp.message_handler(commands=['start', 'help', 'h', 's'])
async def send_welcome(message: types.Message):
    Users().add(message.from_user.id, message.from_user.username)
    await message.answer('hello message')


# choose menu
ib_nt = InlineKeyboardButton("Add task", callback_data="nt")
ib_st = InlineKeyboardButton("Show tasks", callback_data="st")
ib_dt = InlineKeyboardButton("Delete task", callback_data="dt")
inline_kb_choose = InlineKeyboardMarkup().add(ib_nt, ib_st, ib_dt)


@dp.message_handler(commands=["t", "tasks"])
async def first_button(message: types.Message):
    await message.answer("Choose:", reply_markup=inline_kb_choose)


# new task
@dp.callback_query_handler(lambda c: c.data == 'nt')
async def new_task(callback_query: types.CallbackQuery):
    Database().update(table_name="Users", columns={"selected_command": "nt"}, id=callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await simple_cal_handler(callback_query.from_user.id)


@dp.message_handler(state=TaskForm.name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await TaskForm.stime.set()
    await message.answer("When starts?")


@dp.message_handler(state=TaskForm.stime)
async def get_start_time(message: types.Message, state: FSMContext):
    stime = message.text
    await state.update_data(stime=stime)
    await TaskForm.etime.set()
    await message.answer("When ends?")


@dp.message_handler(state=TaskForm.etime)
async def get_end_time(message: types.Message, state: FSMContext):
    etime = message.text
    await state.update_data(etime=etime)
    await TaskForm.desc.set()
    await message.answer("Description:")


@dp.message_handler(state=TaskForm.desc)
async def get_desc(message: types.Message, state: FSMContext):
    desc = message.text
    await state.update_data(desc=desc)
    data = await state.get_data()
    await state.finish()
    date = Database().select(table_name="Users", fetchone=True, id=message.from_user.id, columns=["selected_date"])[0]
    Tasks().addt(name=data['name'], start_time=data['stime'], end_time=data['etime'], user_id=message.from_user.id,
                 desc=data['desc'], date=date)
    await message.answer("Successfully added")


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
    print(date, data)
    result = []
    for each in data:
        result.append("name: " + each[0] + ",\nstarts at: " + each[1] + ",\nends at: " + each[2] + ",\n" + each[3])
    if len(result) == 0:
        await bot.send_message(chat_id=callback_query.from_user.id, text="You don't have any task for selected date.")
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
    inline_kb_delete = InlineKeyboardMarkup()
    if len(names) == 0:
        await bot.send_message(chat_id=callback_query.from_user.id, text="You don't have any tasks for this day.")
        return
    for i in names:
        inline_kb_delete.add(InlineKeyboardButton(text=i[0], callback_data=i[0]))  # gotta fix a problem w/ callback_data
    await bot.send_message(chat_id=callback_query.from_user.id, text="Choose task to delete:", reply_markup=inline_kb_delete)


# cancel any state
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("There is no state to cancel")
        return

    logging.info('Cancelling state %r', current_state)
    await message.answer("You cancelled operation.")
    await state.finish()


# calendar

async def simple_cal_handler(user_id):
    await bot.send_message(text="Please select a date: ", chat_id=user_id,
                           reply_markup=await DialogCalendar().start_calendar())


# dialog calendar usage
ib_y = InlineKeyboardButton(text="✅", callback_data="yes")
ib_n = InlineKeyboardButton(text="❌", callback_data="no")
ikb_agree = InlineKeyboardMarkup().add(ib_y, ib_n)


@dp.callback_query_handler(lambda c: c.data == 'yes')
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


@dp.callback_query_handler(lambda c: c.data == "no")
async def n_agree(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(text="You cancelled operation.", chat_id=callback_query.from_user.id)
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
