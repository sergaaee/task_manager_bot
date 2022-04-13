from aiogram.types import Message, CallbackQuery
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import Users, Tasks
from settings import *
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram_calendar import dialog_cal_callback, DialogCalendar

# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)


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


# adding new task


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
    global date, nt
    desc = message.text
    await state.update_data(desc=desc)
    data = await state.get_data()
    await state.finish()
    Tasks().addt(name=data['name'], start_time=data['stime'], end_time=data['etime'], user_id=message.from_user.id,
                 desc=data['desc'], date=date)
    await message.answer("Success!")
    nt = False


# add task
@dp.message_handler(commands=['nt', 'new_task'])
async def start_date(message: types.Message):
    await simple_cal_handler(message)
    global nt
    nt = True


# show tasks
@dp.message_handler(commands=["st"])
async def show_tasks(message: types.Message):
    await simple_cal_handler(message)
    global st
    st = True


# delete task
@dp.message_handler(commands=['dt'])
async def delete_task(message: types.Message):
    await simple_cal_handler(message)
    global dt
    dt = True


@dp.message_handler(state=DeleteForm.name)
async def get_name_of_del(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name = name)
    data = await state.get_data()  # return dictionary {'name':'name'}
    Tasks().delt(date=date, name=data['name'])
    await message.answer("Success")
    await state.finish()


# calendar
async def simple_cal_handler(message: Message):
    await message.answer("Please select a date: ", reply_markup=await DialogCalendar().start_calendar())


# dialog calendar usage
@dp.callback_query_handler(dialog_cal_callback.filter())
async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: dict):
    global date, nt
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")},\nAre you sure? Send y/n',
        )

        @dp.message_handler()
        async def catcher(message: types.Message):
            if message.text == "y" or message.text == "Y":
                global date, st, nt, dt
                date = date.strftime("%d/%m/%Y")
                if nt:
                    await TaskForm.name.set()
                    await callback_query.message.answer("Name your task:")
                if st:
                    task = Tasks().showt(message.from_user.id, date=date)
                    result = []
                    for each in task:
                        result.append(
                            "Name: " + each[0] + ",\nstarts at: " + each[1] + ",\nends at: " + each[2] + ",\n" + each[
                                3])
                    for i in result:
                        await message.answer(i)
                    st = False
                if dt:
                    await DeleteForm.name.set()
                    await callback_query.message.answer("Enter name of a task")
                    dt = False
            if message.text == "n" or message.text == "N":
                await message.answer("You cancelled operation.")
                nt, st, dt = False, False, False


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    # bot start
    executor.start_polling(dp, skip_updates=True)
