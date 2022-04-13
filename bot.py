from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import Users, Tasks
from settings import token
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram_calendar import dialog_cal_callback, DialogCalendar

# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage = storage)

start_kb = ReplyKeyboardMarkup(resize_keyboard=True,)
start_kb.row('Navigation Calendar', 'Dialog Calendar')



class TaskForm(StatesGroup):
    name = State()
    stime = State()
    etime = State()
    desc = State()


@dp.message_handler(commands=['start', 'help', 'h', 's'])
async def send_welcome(message: types.Message):
    Users().add(message.from_user.id, message.from_user.username)
    await message.answer('hello message')


# adding new task


@dp.message_handler(commands=['nt', 'new_task'])
async def start_date(message: types.Message):
    await simple_cal_handler(message)


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
    await state.update_data(desc = desc)
    data = await state.get_data()
    await state.finish()
    Tasks().add(name=data['name'], user_id= message.from_user.id, start_time=data['stime'], end_time=data['etime'], desc=data['desc'],)
    await message.answer("Success!")


@dp.message_handler(commands=["st"])
async def show_tasks(message: types.Message):
    task = Tasks().show(message.from_user.id)
    result = []
    for each in task:
        result.append("Name: " + each[0] + ",\nstarts at: " + each[1] + ",\nends at: " + each[2] + ",\n" + each[3])
    for i in result:
        await message.answer(i)


#calendar



async def simple_cal_handler(message: Message):
    await message.answer("Please select a date: ", reply_markup=await DialogCalendar().start_calendar())


# dialog calendar usage
@dp.callback_query_handler(dialog_cal_callback.filter())
async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}',
        )
        await TaskForm.name.set()
        await callback_query.message.answer("Name your task:")



if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    # bot start
    executor.start_polling(dp, skip_updates=True)
