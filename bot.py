import time

from database import Users, Tasks
from settings import token
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher(bot)


class TaskForm(StatesGroup):
    name = State()
    stime = State()
    etime = State()
    desc = State()


@dp.message_handler(commands=['start', 'help', 'h', 's'])
async def send_welcome(message: types.Message):
    Users().add(message.from_user.id, message.from_user.first_name + ' ' + message.from_user.last_name)
    await TaskForm.name.set()
    await message.answer('Write name')


@dp.message_handler(state=TaskForm.name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.set_data(name=name)
    await TaskForm.stime.set()


@dp.message_handler(state=TaskForm.stime)
async def get_start_time(message: types.Message, state: FSMContext):
    stime = message.text
    await state.set_data(stime=stime)
    await TaskForm.etime.set()



@dp.message_handler(state=TaskForm.etime)
async def get_end_time(message: types.Message, state: FSMContext):
    etime = message.text
    await state.set_data(etime=etime)
    await TaskForm.desc.set()


@dp.message_handler(state=TaskForm.desc)
async def get_desc(message: types.Message, state: FSMContext):
    desc = message.text
    data = state.get_data()
    await state.finish()

    print(data)


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    # bot start
    executor.start_polling(dp, skip_updates=True)
